# -*- coding: utf-8 -*-
# !/usr/bin/env python3

import struct


def send(connection, data):
    data = bytes(data, "utf8")
    connection.sendall(struct.pack('>I', len(data)) + data)


def recv_packets(connection, n):
    piece = b''
    while len(piece) < n:
        packet = connection.recv(n - len(piece))
        if not packet:
            return None
        piece += packet
    return piece


def recv(connection):
    length_data = recv_packets(connection, 4)
    if not length_data:
        return None
    data_len = struct.unpack('>I', length_data)[0]
    return recv_packets(connection, data_len).decode("utf8")
