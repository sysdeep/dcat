#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import sys
from app.rc import VERSION


def main():
    # парсер командной строки
    parser = argparse.ArgumentParser()
    parser.add_argument("-ui", "--ui", help="тип ui", choices=["tk", "qt"], default="tk")
    parser.add_argument("-v", "--version", help="версия", action="store_true", default=False)

    args = parser.parse_args()

    if args.version:
        print(VERSION)
        sys.exit(0)

    if args.ui == "tk":
        sys.exit(start_tk())

    if args.ui == "qt":
        start_qt()
        sys.exit(0)

    sys.exit(0)


def start_tk():
    from app.AppTK import AppTK

    my_app = AppTK()
    my_app.start()


def start_qt():
    from app.AppQT import AppQT

    my_app = AppQT()
    my_app.start()


if __name__ == '__main__':
    main()
