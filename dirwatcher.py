#!/usr/bin/env python

# Assessment: Dirwatcher

"""
Dirwatcher monitors a specific directory. This directory will be
searched using pre-assigned text. When the directory changes (added files,
deleted files, and internally changed files) they will take place
without any action on the part of the user. 
"""

__author__ = "Kathryn Anderson"


import sys
import argparse
import re
import logging
import time
import os
import signal
import datetime
from os import walk

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s:\
        %(levelname)s:%(message)s')
logit = logging.getLogger(__name__)
logit.setLevel(logging.INFO)


dict_of_files = {}

def spec_file_func(ns):
    """
    This function will search the specific directory for files that
    match pre-assigned text.
    """
    
    temp_spec_file_func = {}

    try:
        if os.path.isdir(ns.dir):
            for f in walk(ns.dir):
                file_list = f[2]
            for file in file_list:
                if ns.ext is not None:
                    if file[-len(ns.ext):] == ns.ext:
                        temp_spec_file_func.setdefault(file, [])
                else:
                    temp_spec_file_func.setdefault(file, [])
        else:
            logit.info(f"The {ns.dir} directory does not exist ")
    except AttributeError:
        pass
    except Exception as inst:
        logit.exception(f"The {inst} error has taken place.")
    
    match_file_func(temp_spec_file_func, ns)


def match_file_func(temp_spec_file, ns):
    """
    This function looks for files that have changed from the original
    directory and compares it to a temp directory to recognize changes.
    """
    
    try:
        for k in temp_spec_file:
            if k not in dict_of_files:
                logit.info(f"The Directory has added file {k}")
                dict_of_files[k] = []
        for k in dict_of_files:
            if k not in temp_spec_file:
                logit.info(f"The Directory has removed file {k}")
                dict_of_files.pop(k, None)
    except RuntimeError:
        pass
    except Exception as inst:
        logit.exception(f"The {inst} error has occured.")
    magic_text_func(ns)



def magic_text_func(ns):
    """
    This function uses specific "magic" text to look through the
    specified directory for the "magic" text
    """
    
    try:
        for key in dict_of_files:
            with open(ns.dir + "/" + key, "r") as f:
                lines = f.readlines()
                for i, line in enumerate(lines):
                    result = re.search('(.+)' + ns.magic + '(.+)', line)
                    if result and i not in dict_of_files[key]:
                        dict_of_files[key].append(i)
                        logit.info(
                            f"Magic text found in file: {key} was found on line {str(i + 1)}")
    except Exception as inst:
        logit.exception(f"The {inst} error has occured.")




def run_time_func():
    """
    This function uses a predetermined amount of time to monitor
    the directory for changes.
    """

    return time.time() - time_to_start


def create_parser():
    """
    Command Line Parser
    """

    parser = argparse.ArgumentParser(
        description="Watch directory for files containing certain text"
    )
    parser.add_argument('dir', help='directory being watched')
    parser.add_argument('magic', help='magic text to search directory for')
    parser.add_argument('--ext', default=".txt", help='file extension to filter on')
    parser.add_argument('--interval', type=int, default=1, help='polling interval')
    return parser


exit_flag = False


def sig_func(sig_num, frame):
    """
    Program responds to SIGINT and SIGTERM signals from the OS. Signal
    events are logged so that a human can determine what the signal was.
    Program will exit upon either signal.
    """
    
    global exit_flag

    logit.warning(f'Received OS Process Signal, {signal.Signals(sig_num).name}')

    exit_flag = True


def main(args):
    """
    Runs the DirWatcher.py Program
    """
    time_to_start = datetime.datetime.now()
    
    parser = create_parser()
    ns = parser.parse_args(args)
    logit.info(f"\n{56 * '-'}\nDirWatcher.py Program Has Started\n{56 * '-'}\n")
    signal.signal(signal.SIGINT, sig_func)
    signal.signal(signal.SIGTERM, sig_func)
    logger_int = 1
    while not exit_flag:
        try:
            if ns.interval != 1:
                logger_int = int(ns.interval)
            spec_file_func(ns)
        except Exception as inst:
            logit.exception(f"The {inst} error has occured.")
            spec_file_func([])
        time.sleep(logger_int)

    logit.info(
        f"\nStopped: {sys.argv[0]}\nUptime was: {datetime.datetime.now() - time_to_start}")

if __name__ == '__main__':
    main(sys.argv[1:])
