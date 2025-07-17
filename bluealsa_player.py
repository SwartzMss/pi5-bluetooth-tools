"""BlueALSA 播放工具.

该模块提供通过 BlueALSA 播放 WAV 音频的函数接口, 便于其他脚本调用.
"""

from __future__ import annotations

import wave


import alsaaudio


def play_wav_via_bluealsa(wav_file: str, bt_device: str, period_size: int = 1024) -> None:
    """播放指定的 WAV 文件到蓝牙设备.

    参数:
        wav_file: WAV 文件路径
        bt_device: 形如 ``bluealsa:HCI=hci0,DEV=XX:XX:XX:XX:XX:XX,PROFILE=a2dp`` 的设备字符串
        period_size: ALSA 写入的 period 大小, 默认为 1024
    """
    with wave.open(wav_file, "rb") as wf:
        pcm = alsaaudio.PCM(type=alsaaudio.PCM_PLAYBACK, card=bt_device)
        try:
            pcm.setchannels(wf.getnchannels())
            pcm.setrate(wf.getframerate())
            fmt = (
                alsaaudio.PCM_FORMAT_S16_LE
                if wf.getsampwidth() == 2
                else alsaaudio.PCM_FORMAT_S8
            )
            pcm.setformat(fmt)
            pcm.setperiodsize(period_size)

            data = wf.readframes(period_size)
            while data:
                pcm.write(data)
                data = wf.readframes(period_size)
        finally:
            pcm.close()
