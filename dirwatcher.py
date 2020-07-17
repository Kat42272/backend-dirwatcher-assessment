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


def magic_text_func():
    """
    This function uses specific "magic" text to look through the
    specified directory for the "magic" text
    """
    pass


def spec_file_func():
    """
    This function will search the specific directory for files that
    match pre-assigned text.
    """
    pass


def match_file_func():
    """
    This function looks for files that have changed from the original
    directory and compares it to a temp directory to recognize changes.
    """
    pass


def run_time_func():
    """
    This function uses a predetermined amount of time to monitor
    the directory for changes.
    """
    pass


def sig_func():
    """
    Program responds to SIGINT and SIGTERM signals from the OS. Signal
    events are logged so that a human can determine what the signal was.
    Program will exit upon either signal.
    """
    pass


def main():
    """
    Runs the DirWatcher.py Program
    """
    pass


if __name__ == '__main__':
    main(sys.argv[1:])
