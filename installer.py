# WARNING: This project requires pip to install all packages
from pip._internal import main as pipmain
import platform

def import_or_install(package):
    try:
        __import__(package)
    except ImportError:
        pipmain(['install', package])   

def getDependencies():
    assert (int(platform.python_version_tuple()[0]) >= 3 and int(platform.python_version_tuple()[1]) >= 6), """
        Python version is not greater than 3.6, some packages in this repository require python 3.6 >.
    """
    with open("requirements.txt") as requirements:
        for package in [line.rstrip() for line in requirements if line.rstrip() and not line.startswith('#')]:
            import_or_install(package)

def cleanDependencies():
    with open("requirements.txt") as requirements:
        for package in [line.rstrip() for line in requirements if line.rstrip() and not line.startswith('#')]:
            pipmain(['uninstall', package])

if __name__ == "__main__":
    getDependencies()