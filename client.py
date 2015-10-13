# -*- coding: utf-8 -*-
# !/usr/bin/env python3

import socket

import config


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((config.host, config.port))
sock.sendall(bytes(input(), encoding="utf-8"))
data = sock.recv(1024)
sock.close()
print('Response:', data.decode("utf-8"))
