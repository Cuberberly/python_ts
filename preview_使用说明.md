# preview.py 使用说明

- 代码位置（板子）：`/home/lckfb/py_work/preview.py`
- 说明位置（本机）：`E:\lsuse3\preview_使用说明.md`
- `preview.py` 内部**没有任何注释**，所有说明以本文件为准。

---

## 一、它做什么

把一帧 OpenCV 图像（BGR）编码成 JPEG，维护「最新一帧」，通过 HTTP 的 MJPEG 协议推给浏览器。

你的程序只需要在「想让人看到这一帧」时调用一次 `push(frame)`，其余（编码、限流、并发、断线）都由它处理。

**它不打开摄像头**，也不独占设备；采集仍然由你的代码负责。

---

## 二、依赖

| 依赖 | 板子现状 |
|---|---|
| Python 3 | 3.10 |
| opencv-python | 4.5.4（已装） |
| numpy | 1.21.5（已装） |

不需要 Flask / websockets / 任何第三方库。

---

## 三、最小示例

```python
import cv2
from preview import Preview

p = Preview(port=8080).start()

cap = cv2.VideoCapture('/dev/video10', cv2.CAP_V4L2)
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

while True:
    ok, frame = cap.read()
    if not ok:
        continue
    p.push(frame)
```

浏览器打开：`http://192.168.43.5:8080/`

---

## 四、和你的算法结合

```python
from preview import Preview
from scan import qr

p = Preview(port=8080, size=(320, 180), fps=10, quality=60).start()

drawn, result = qr.process(frame)
p.push(drawn)
if result['ok']:
    handle(result)
```

要点：

- `push()` 放在算法**之后**，主循环里每帧都可以调，它自己会限流
- 算法不需要知道预览的存在，测试时可以不 `start()`

---

## 五、参数

| 参数 | 默认值 | 说明 |
|---|---|---|
| `host` | `'0.0.0.0'` | 监听地址；改成 `'127.0.0.1'` 则只能本机访问 |
| `port` | `8080` | HTTP 端口 |
| `size` | `(320, 180)` | 推送尺寸，自动缩放；`None` 表示不缩放、原样推送 |
| `fps` | `10` | 推送帧率上限；`0` 表示不限 |
| `quality` | `60` | JPEG 质量 1–100 |

---

## 六、方法与属性

| 名称 | 作用 |
|---|---|
| `push(frame)` | 更新「最新一帧」；按 `fps` 限流，非阻塞 |
| `latest()` | 返回最新 JPEG 字节；还没有帧时返回 `None` |
| `start()` | 启动 HTTP 服务（后台线程），返回自身，可链式调用 |
| `stop()` | 停止 HTTP 服务并释放端口 |
| `url` | 形如 `http://127.0.0.1:8080/` |

---

## 七、HTTP 端点

| 路径 | 内容 |
|---|---|
| `/` | 简易 HTML 页面，内部引用 `/stream` |
| `/stream` | MJPEG 长连接（`multipart/x-mixed-replace`），浏览器 `<img>`、VLC 均可 |
| `/snap` | 单帧 JPEG；还没有帧时返回 503 |

调试技巧：

```bash
curl -N http://127.0.0.1:8080/stream -o /dev/null
curl -o /tmp/a.jpg http://127.0.0.1:8080/snap
```

---

## 八、性能与用法建议

- 调试用 `size=(320,180), fps=10`，带宽约 0.4 Mbps，CPU 开销很小
- 想看清晰些用 `size=(640,480), quality=70`
- 多人同时看不会增加解码次数，大家共享同一份 JPEG
- 生产环境不需要预览时，直接去掉 `Preview(...).start()`，算法照样跑
- 服务线程是 daemon，主程序退出即自动结束

---

## 九、常见问题

| 现象 | 原因 / 处理 |
|---|---|
| 页面打不开 | 没调 `start()`；或端口被占用（换 `port`） |
| 页面一直转圈 | 还没 `push` 过帧；用 `/snap` 确认是否 503 |
| 画面卡顿 | 算法太慢阻塞了主循环；把算法放独立线程，预览从共享帧取 |
| 画面花屏 | 同一数组边改边推；`push()` 内部会立即编码，通常不会，若出现请先 `frame.copy()` |
| 外网打不开 | `host` 是 `127.0.0.1`，或防火墙未放行 |
| 端口冲突 | 8080 被 motion 等占用时换 8081、8090 |

---

## 十、边界

- 不做认证：谁在同一局域网谁就能看，需要时用 SSH 隧道或只绑 `127.0.0.1`
- 不做录像：只保留最新一帧，历史帧不留
- 不做摄像头管理：设备号、分辨率、重连都由你的采集代码负责
