# Raspberry Pi 使用 BlueALSA 将音频推送到小米音箱

本项目演示了如何在 Raspberry Pi 上使用 BlueALSA，通过 A2DP 协议将音频流推送到小米蓝牙音箱。示例包含：

- 使用 `aplay` 的命令行播放示例
- 使用 `python3-alsaaudio` 的 Python 脚本播放示例

## 功能

- 将 WAV/MP3 文件通过 BlueALSA 推送到小米蓝牙音箱
- 简单的命令行播放示例
- Python 脚本示例，方便程序化播放

## 环境要求

- 运行 Raspberry Pi OS（或其他 Debian 系 Linux）的 Raspberry Pi
- 内置或 USB 蓝牙适配器
- 小米蓝牙音箱（或任何支持 A2DP 的蓝牙接收设备）
- 网络连接，用于安装软件包

## 安装步骤

1. 更新软件包列表：
   ```bash
   sudo apt update
   ```
2. 安装 BlueALSA 和 ALSA 工具：
   ```bash
   sudo apt install -y bluealsa alsa-utils
   ```
3. （可选）安装 Python ALSA 绑定，用于 Python 脚本播放：
   ```bash
   sudo apt install -y python3-alsaaudio python3-pip
   ```

## 蓝牙配对与连接

1. 启动蓝牙交互式工具：
   ```bash
   bluetoothctl
   ```
2. 在提示符下执行以下命令：
   ```text
   [bluetooth]# power on             # 打开蓝牙适配器
   [bluetooth]# agent on             # 启用代理
   [bluetooth]# default-agent        # 设为默认代理
   [bluetooth]# scan on              # 开始扫描
   # 等待出现音箱 MAC 地址，如 XX:XX:XX:XX:XX:XX
   [bluetooth]# pair XX:XX:XX:XX:XX:XX  # 配对
   [bluetooth]# trust XX:XX:XX:XX:XX:XX # 信任设备
   [bluetooth]# connect XX:XX:XX:XX:XX:XX # 连接设备
   [bluetooth]# scan off             # 停止扫描
   [bluetooth]# exit                 # 退出工具
   ```
3. 如果连接成功，你会看到类似 `Connection successful` 的提示。

## 使用示例

### 1. 命令行播放（aplay）

使用 `aplay` 将 WAV 文件推送到小米音箱：
```bash
aplay -D bluealsa:HCI=hci0,DEV=XX:XX:XX:XX:XX:XX,PROFILE=a2dp ~/Music/song.wav
```
- 将 `XX:XX:XX:XX:XX:XX` 替换为音箱的实际 MAC 地址。  
- `PROFILE=a2dp` 确保使用高质量音频通道。

播放 MP3 文件（需先安装 `mpg123`）：
```bash
sudo apt install -y mpg123
mpg123 -a bluealsa:HCI=hci0,DEV=XX:XX:XX:XX:XX:XX,PROFILE=a2dp ~/Music/song.mp3
```

### 2. Python 脚本播放

仓库已经内置 `main.py` 可直接播放 WAV 文件：

```bash
python3 main.py /home/pi/Music/song.wav bluealsa:HCI=hci0,DEV=XX:XX:XX:XX:XX:XX,PROFILE=a2dp
```

如需在其他脚本中复用，导入 `bluealsa_player.py` 的 `play_wav_via_bluealsa`：

```python
from bluealsa_player import play_wav_via_bluealsa
play_wav_via_bluealsa('/home/pi/Music/song.wav', 'bluealsa:HCI=hci0,DEV=XX:XX:XX:XX:XX:XX,PROFILE=a2dp')
```

## 故障排除

- **无声音**：确认设备已连接（`bluetoothctl info XX:...`）。
- **权限错误**：将当前用户加入 `audio` 组（`sudo usermod -aG audio $USER`），然后重新登录。
- **延迟高或掉帧**：可尝试减小 `period size`，或切换到 PulseAudio/​PipeWire 获取更好缓冲管理。

## 配置技巧

可在 `~/.asoundrc` 中设置 BlueALSA 为默认 PCM 设备，配置后在命令或脚本中无需再显式指定 MAC 和 A2DP 协议：

```text
pcm.!default {
  type plug
  slave.pcm {
    type bluealsa
    device "XX:XX:XX:XX:XX:XX"
    profile "a2dp"
    interface "hci0"
  }
}
ctl.!default {
  type bluealsa
}
```

## 许可证

MIT © Your Name

