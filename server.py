# -*- coding: utf-8 -*-
# !/usr/bin/env python3

import socket
import threading

import httrack
import config


downloading = []


def dl_status_checker(thread, connection):
    if thread.isAlive:
        connection.sendall(b'Downloading has started')
    else:
        connection.sendall(b'Downloading has FAILED')


def handle_commands(connection, command, params):
    if command == "dl":
        if params[1] == '0':
            params[1] = False
        else:
            params[1] = True
        if not params[1]:
            params.append(None)
        htt_thread = threading.Thread(target=httrack.download, args=(params[0], params[1], params[2]))
        htt_thread.start()
        dl_status = threading.Timer(2.0, dl_status_checker, args=(htt_thread, connection))
        dl_status.start()
    elif command == "list":
        connection.sendall(b'Existing...')


def args_analysis(connection, args):
    args = args.decode("utf-8").split()
    handle_commands(connection=connection, command=args[0], params=args[1:])


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((config.host, config.port))
sock.listen(True)
while True:
    conn, addr = sock.accept()
    print('Connected by ', addr)
    data = conn.recv(1024)
    args_analysis(connection=conn, args=data)
