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


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s:\
        %(levelname)s:%(message)s:%(threadName)s:')
logit = logging.getLogger(__name__)


dict_of_files = {}


def magic_text_func(n):
    """
    This function uses specific "magic" text to look through the
    specified directory for the "magic" text
    """
    
    try:
        for key in dict_of_files:
            with open(n.dir[0] + "/" + key, "r") as f:
                lines = f.readlines()
                for i, line in enumerate(lines):
                    result = re.search('(.+)' + n.magic[0] + '(.+)', line)
                    if result and i not in dict_of_files[key]:
                        dict_of_files[key].append(i)
                        logit.info(f"Magic text found in file {key} on line\{str(i + 1)}")
    except Exception as inst:
        logit.exception(f"The following error has occured {inst}")



def spec_file_func(n):
    """
    This function will search the specific directory for files that
    match pre-assigned text.
    """
    
    temp_spec_file_func = {}

    try:
        if os.path.isdir(n.dir[0]):
            logging.info(f"Directory {n.dir[0]} is being searched")
            for f in n.dir[0]:
                file_list = f[2]
            for file in file_list:
                if n.ext is not None:
                    if file[-len(n.ext[0]):] == n.ext[0]:
                        temp_spec_file_func.setdefault(file, [])
                else:
                    temp_spec_file_func.setdefault(file, [])
        else:
            logit.info(f"{n.dir[0]} directory does not exist ")
    except AttributeError:
        pass
    except Exception as inst:
        logit.exception(f"The {inst} error has taken place.")
    
    match_file_func(temp_spec_file_func, n)


def match_file_func(temp_spec_file, n):
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
                logit.info(f"The Direcotry has removed file {k}")
                dict_of_files.pop(k, None)
    except RuntimeError:
        pass
    except Exception as inst:
        logit.exception(f"The following error has occured {inst}")
    magic_text_func(n)


time_to_start = time.time()


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
    parser.add_argument('--dir', help='directory being watched', nargs='+')
    parser.add_argument('--ext', help='file extension to filter on', nargs='+')
    parser.add_argument('--magic', help='magic text to search directory for', nargs='+')
    parser.add_argument('-i', default=2, help='polling interval', nargs='+')
    return parser


exit_flag = False

def sig_func():
    """
    Program responds to SIGINT and SIGTERM signals from the OS. Signal
    events are logged so that a human can determine what the signal was.
    Program will exit upon either signal.
    """
    
    global exit_flag
    run_time = run_time_func()
    logit.info(f"\n{56 * '-'}\nDirWatcher.py Program Has Stopped\n\
                Uptime was {run_time}\n{56 * '-'}\n")
    exit_flag = True


def main(args):
    """
    Runs the DirWatcher.py Program
    """
    
    logit.info(f"\n{56 * '-'}\nDirWatcher.py Program Has Started\n\
                 {56 * '-'}\n")
    signal.signal(signal.SIGINT, sig_func)
    signal.signal(signal.SIGTERM, sig_func)
    logger = 1
    while not exit_flag:
        try:
            parser = create_parser()
            n = parser.parse_args(args)
            print(n)
            if n.int != 1:
                logger = int(n.int[0])
            spec_file_func(n)
        except Exception as inst:
            logit.exception(f"The following error has occured {inst}")
            spec_file_func([])
        time.sleep(logger)


if __name__ == '__main__':
    main(sys.argv[1:])
