import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import cv2


class Preview:
    def __init__(self, host='0.0.0.0', port=8080, size=(320, 180), fps=10, quality=60):
        self.host = host
        self.port = port
        self.size = size
        self.fps = fps
        self.quality = quality
        self._lock = threading.Lock()
        self._buf = None
        self._seq = 0
        self._last = 0.0
        self._server = None
        self._thread = None

    def push(self, frame):
        now = time.time()
        if self.fps and now - self._last < 1.0 / self.fps:
            return
        self._last = now
        img = frame
        if self.size is not None:
            h, w = frame.shape[:2]
            if (w, h) != tuple(self.size):
                img = cv2.resize(frame, tuple(self.size))
        ok, j = cv2.imencode('.jpg', img, [int(cv2.IMWRITE_JPEG_QUALITY), int(self.quality)])
        if not ok:
            return
        data = j.tobytes()
        with self._lock:
            self._buf = data
            self._seq += 1

    def latest(self):
        with self._lock:
            return self._buf

    def start(self):
        if self._server is not None:
            return self
        preview = self

        class Handler(BaseHTTPRequestHandler):
            protocol_version = 'HTTP/1.0'

            def log_message(self, *args):
                pass

            def do_GET(self):
                if self.path in ('/', '/index.html'):
                    body = ('<html><head><meta charset="utf-8"></head>'
                            '<body style="margin:0;background:#000">'
                            '<img src="/stream" style="width:100%;display:block">'
                            '</body></html>').encode()
                    self.send_response(200)
                    self.send_header('Content-Type', 'text/html; charset=utf-8')
                    self.send_header('Content-Length', str(len(body)))
                    self.end_headers()
                    self.wfile.write(body)
                    return
                if self.path == '/snap':
                    data = preview.latest()
                    if data is None:
                        self.send_error(503)
                        return
                    self.send_response(200)
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', str(len(data)))
                    self.end_headers()
                    self.wfile.write(data)
                    return
                if self.path == '/stream':
                    self.send_response(200)
                    self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=frame')
                    self.send_header('Cache-Control', 'no-cache')
                    self.end_headers()
                    seen = -1
                    while True:
                        with preview._lock:
                            data = preview._buf
                            seq = preview._seq
                        if data is not None and seq != seen:
                            seen = seq
                            try:
                                self.wfile.write(b'--frame\r\nContent-Type: image/jpeg\r\nContent-Length: '
                                                 + str(len(data)).encode()
                                                 + b'\r\n\r\n'
                                                 + data
                                                 + b'\r\n')
                                self.wfile.flush()
                            except OSError:
                                return
                        time.sleep(0.02)
                self.send_error(404)

        self._server = ThreadingHTTPServer((self.host, self.port), Handler)
        self._server.daemon_threads = True
        self._thread = threading.Thread(target=self._server.serve_forever, daemon=True)
        self._thread.start()
        return self

    def stop(self):
        if self._server is None:
            return
        self._server.shutdown()
        self._server.server_close()
        self._server = None
        self._thread = None

    @property
    def url(self):
        host = '127.0.0.1' if self.host in ('0.0.0.0', '') else self.host
        return 'http://%s:%d/' % (host, self.port)
