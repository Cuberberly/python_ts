# python_ts

基于 **Python 3.11.9** 的虚拟环境（Windows），由 `py -3.11 -m venv` 创建。

## 目录

- 解释器：`D:\python_ts\Scripts\python.exe`
- 依赖清单：`requirements.txt`（版本与本机原 3.11 环境 `D:\python` 一致）

## 已安装的库

matplotlib、numpy、opencv-python、pillow（PIL）、pyzbar、contourpy、fonttools、kiwisolver、cycler、python-dateutil、pyparsing、packaging、six。

## 用法

直接调用解释器：

```bat
D:\python_ts\Scripts\python.exe main.py
```

或在 cmd 中激活：

```bat
D:\python_ts\Scripts\activate.bat
```

## 重建依赖

virturalenv 本体（`Lib/`、`Scripts/` 等）不纳入版本控制，换机器后按下面命令重建：

```bat
py -3.11 -m venv D:\python_ts
D:\python_ts\Scripts\python.exe -m pip install -r requirements.txt
```
