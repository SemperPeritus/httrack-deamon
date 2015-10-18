# -*- coding: utf-8 -*-
# !/usr/bin/env python3

import socket

import config
import protocol


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((config.host, config.port))
protocol.send(sock, input())
data = protocol.recv(sock)
sock.close()
print(data)
