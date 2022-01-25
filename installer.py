# WARNING: This project requires pip to install all packages
from pip._internal import main as pipmain
import platform

pkg_list = [
    "praw",
    "google-auth-httplib2",
    "google-api-python-client",
    "google-auth-oauthlib",
    "gspread",
    "requests",
    "argparse",
    "typing",
    "pathlib",
    "python-dotenv"
]

def import_or_install(package):
    try:
        __import__(package)
    except ImportError:
        pipmain(['install', package])   

def getDependencies():
    cleanDependencies()
    # Check the current Python Version
    # PRAW requires Python > 3.6
    assert (int(platform.python_version_tuple()[0]) >= 3 and int(platform.python_version_tuple()[1]) >= 6), """
        Python version is not greater than 3.6, some packages in this repository require python 3.6 >.
    """

    # pip3 should be automatically installed with all python versions greater than 3.4
    # see: https://docs.python.org/3/installing/index.html
    for package in pkg_list:
        import_or_install(package)

def cleanDependencies():
    for package in pkg_list:
        pipmain(['uninstall', package])

if __name__ == "__main__":
    getDependencies()