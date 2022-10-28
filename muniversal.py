#!/usr/bin/env python3

"""plot arbitrary json dict stream with munin"""

import json
import sys
import os
import re
import unicodedata



def print_config(config):
    """print config for munin"""
    for attr, val in config['config'].items():
        print(f"{attr} {val}")

def print_values(config):
    """print values for munin"""

    # ensure list
    logfiles = config["logfile"]
    if not isinstance(logfiles, (list, tuple)):
        logfiles = [ logfiles ]

    # process all logfiles
    for logfile in logfiles:
        with open(logfile, "rb") as fd:
            # last line of file
            datagram = json.loads(tail(fd))
            # map dict to munin values according to valuemap
            for k,v in config["valuemap"].items():
                print(f"{v}.value {datagram[k]}")

def tail(fd):
    """return last line of file"""
    # seek to end of file
    fd.seek(-2, os.SEEK_END)
    # Until EOL is found...
    while fd.read(1) != b"\n":
        # ...jump back the read byte plus one more.
        fd.seek(-2, os.SEEK_CUR)
    return fd.readline()


def sanitized(s):
    """sanitize string so it can be used as variable name"""
    s = unicodedata \
        .normalize('NFKD', s) \
        .encode('ASCII', 'ignore') \
        .decode('UTF-8')
    s = re.sub(r"[^A-Za-z]+", "", s)
    return re.sub(r"\s", r"_", s)

# ---------------------------------------------------------------------

if __name__ == "__main__":
    # parse our filename
    splitted = os.path.basename(sys.argv[0]).split("_")
    try:
        name = sanitized(splitted[0])
    except IndexError:
        name = "muniversal"
    try:
        plot = sanitized(splitted[1])
    except IndexError:
        plot = sanitized(sys.argv[0])

    # get configfile from munin config or use default
    configfile = os.getenv('configfile', '/etc/muniversal.json')
    # parse config
    config_fd = open(configfile)
    config = json.load(config_fd)

    # parse arguments
    if len(sys.argv) > 1:

        match sys.argv[1]:
            case "config":
                print_config(config[name][plot])
                sys.exit(0)

            case "autoconf":
                print("yes")
                sys.exit(0)

            case _:
                print(
                    f"unknown argument: \"{sys.argv[1]}\"", file=sys.stderr
                )
                sys.exit(1)

    else:
        print_values(config[name][plot])
