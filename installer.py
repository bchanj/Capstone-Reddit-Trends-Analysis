import os
import sys
import platform

def getDependencies():
    # Check the current Python Version
    # PRAW requires Python > 3.6
    assert (int(platform.python_version_tuple()[0]) >= 3 and int(platform.python_version_tuple()[1]) >= 6), """
        Python version is not greater than 3.6, some packages in this repository require python 3.6 >.
    """

    # pip3 should be automatically installed with all python versions greater than 3.4
    # see: https://docs.python.org/3/installing/index.html

    try:
        import praw
    except ImportError(e):
        print("""
        Could not find the package praw. Attempting to install via pip3...
        """)
        os.system("pip3 install praw")

    try:
        import requests
    except ImportError(e):
        print("""
        Could not find the package requests. Attempting to install via pip3...
        """)
        os.system("pip3 install requests")

    try:
        import argparse
    except ImportError(e):
        print("""
        Could not find the package argparse. Attempting to install via pip3...
        """)
        os.system("pip3 install argparse")

    try:
        import typing
    except ImportError(e):
        print("""
        Could not find the package typing. Attempting to install via pip3...
        """)
        os.system("pip3 install typing")