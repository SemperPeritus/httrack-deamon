# -*- coding: utf-8 -*-
# !/usr/bin/env python3

from subprocess import call
from os import makedirs
from shutil import rmtree

import config


def download(url, remove, archive_format):
    if url.find("//"):
        url = url[url.find("//")+2:]
    if url[-1:] == '/':
        url = url[:-1]
    site = config.sites_directory + '/' + url
    print("Downloading ", url, " started.")
    makedirs(config.sites_directory, mode=0o755, exist_ok=True)
    call(["httrack", url], cwd=config.sites_directory)
    print("Downloading is complete")
    if archive_format:
        if archive_format == "gz":
            call(["tar", "-czf", config.sites_directory + '/' + url + ".tar.gz",
                  "-C", config.sites_directory, url], cwd=config.sites_directory)
        elif archive_format == "bz2":
            call(["tar", "-cjf", config.sites_directory + '/' + url + ".tar.bz2",
                  "-C", config.sites_directory, url], cwd=config.sites_directory)
        elif archive_format == "tar":
            call(["tar", "-cf", config.sites_directory + '/' + url + ".tar",
                  "-C", config.sites_directory, url], cwd=config.sites_directory)
        else:
            print("Archive format is wrong")
    else:
        print("The site is not packed")
    if remove:
        rmtree(site)
        print("Removing is complete")
    else:
        print("Removing is canceled")
