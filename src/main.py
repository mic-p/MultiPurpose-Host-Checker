#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from libs.config import GlobalConfig

from libs import startup


class Work():
    def __init__(self):

        st = startup.Startup()
        st.startup()

        self._gc = GlobalConfig()


if __name__ == '__main__':
    Work()
