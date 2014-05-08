#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
up_to_date is a program that checks if the translations files are up to date with the English ones. It then builds a database and a textile file with this data.

Usage:
    up_to_date.py [--verbose]  <repository>
    up_to_date.py (-h | --help)
    up_to_date.py --version

Arguments:
    <repository>      The path to the repository containing the files

Options:
    -h  --help       Shows the help screen
    --version        Outputs version information
    --verbose        Runs the program as verbose mode
"""
import sys

try:
    from docopt import docopt  # Creating command-line interface
except ImportError:
    sys.stderr.write("""
        %s is not installed: this program won't run correctly.
        To install %s, run: aptitude install %s
        """ % ("python-docopt", "python-docopt", "python-docopt"))

import os
import subprocess

from collections import defaultdict

# Defining the function that builds the database
def create_database(filename, dirname, database):
    filepath = os.path.join(dirname, filename)
    pipe = subprocess.Popen(["git", "log", "-1", "--format=%ad",
                              "--date=local", "--", filepath],
                              stdout=subprocess.PIPE)
    output, error = pipe.communicate()
    output = output[4:]
    if output != "":
        time = output.split(" ")[2]
        day = output.split(" ")[1]
        month = output.split(" ")[0]
        year = (output.split(" ")[3]).strip("\n")
        database[dirname].append(
            [os.path.splitext(filename)[0],
            time, day, month, year])
    return database

# Defining the function that generates the textile file
def textile(database):
    f = open("up_to_date.text", "w")
    f.write("{:<10} {:<10} {:<10} {:<10} {:<10} {:<10}".format(
        "Directory","Language","Time", "Day", "Month", "Year"))
    for directory in database.iterkeys():
        for values in database.itervalues():
            for value in values:
                lang, time, day, month, year = value
                f.write("{:<10} {:<10} {:<10} {:<10} {:<10} {:<10}".format(
                    directory, lang, time, day, month, year))
    f.close()


# Defining main function
def main():
    args = docopt(__doc__, version="up_to_date XX")
    database = defaultdict(list)
    for dirname, _, filenames in os.walk(
                                   args["<repository>"],
                                   topdown=False):
        for filename in filenames:
            if os.path.splitext(filename)[1] == ".text":
                try:
                   database = create_database(filename, dirname, database)
                except KeyboardInterrupt:
                    raise
    textile(database)
#    print(database["./pages"])

# Calling main function
if __name__ == "__main__":
    main()