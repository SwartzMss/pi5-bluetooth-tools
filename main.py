"""BlueALSA 播放示例入口脚本."""

import argparse

from bluealsa_player import play_wav_via_bluealsa


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="通过 BlueALSA 播放 WAV 文件")
    parser.add_argument("wav_file", help="要播放的 WAV 文件路径")
    parser.add_argument(
        "device",
        help=(
            "蓝牙设备字符串，如 bluealsa:HCI=hci0,DEV=XX:XX:XX:XX:XX:XX,PROFILE=a2dp"
        ),
    )
    parser.add_argument(
        "--period",
        type=int,
        default=1024,
        help="ALSA 写入的 period 大小，默认为 1024",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    play_wav_via_bluealsa(args.wav_file, args.device, period_size=args.period)


if __name__ == "__main__":
    main()
