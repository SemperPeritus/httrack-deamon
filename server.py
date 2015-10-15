# -*- coding: utf-8 -*-
# !/usr/bin/env python3

import socket
import threading
from os import listdir, path

import httrack
import config


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
        file_list = listdir(config.sites_directory)
        folder_list = []
        archive_list = []
        print(file_list)
        for file in file_list:
            if path.isdir(config.sites_directory + '/' + file) and file != "hts-cache":
                folder_list.append(file)
            if path.isfile(config.sites_directory + '/' + file) and \
                    (file[-7:] == ".tar.gz" or file[-8:] == ".tar.bz2" or file[-5:] == ".tar"):
                archive_list.append(file)
        print(folder_list)
        site_string = ""
        folder_found = False
        if folder_list:
            site_string += "List of folders:\n" + "\n".join(folder_list)
            folder_found = True
        if archive_list:
            if folder_found:
                site_string += "\n================================================================================\n"
            site_string += "List of archives:\n" + "\n".join(archive_list)
        if site_string == "":
            site_string = "Sites not found!"
        connection.sendall(bytes(site_string, encoding="utf-8"))


def args_analysis(connection, args):
    args = args.decode("utf-8").split()
    handle_commands(connection=connection, command=args[0], params=args[1:])


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((config.host, config.port))
sock.listen(True)
while True:
    conn, addr = sock.accept()
    print('Connected by ', addr)
    data = conn.recv(10240)
    args_analysis(connection=conn, args=data)
