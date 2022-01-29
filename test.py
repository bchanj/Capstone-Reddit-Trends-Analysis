if __name__ == '__main__':

    import installer
    installer.getDependencies()

    import os
    import subprocess
    import doctest
    from typing import List
    from colorama import Fore, Back, Style

    target_extensions: List[str] = [
        ".py"
    ]

    packages: List[str] = [
        os.path.join('.', 'reddit'),
        os.path.join('.', 'sheets')
    ]

    successful = 0
    failures = 0
    for package in packages:
        for root, dirs, files in os.walk(package):
            path = root.split(os.sep)
            for file in files:
                if any([file.endswith(ext) for ext in target_extensions]):
                    print(Fore.WHITE + f"""
=========================================                
RUN: Running tests for: {os.path.join(root, file)}""")
                    file_path = os.path.join(root, file)
                    try:
                        result = subprocess.run(['python3', file_path], check = True, shell=True, capture_output=True)
                        if result.stderr:
                            raise subprocess.CalledProcessError(returncode = result.returncode, cmd = result.args, stderr = result.stderr)
                    except subprocess.CalledProcessError as e:
                        failures += 1
                        print(Fore.RED + f"""FAILURE: {file}, Path: {file_path}.
Here was the error {e.stderr.decode('utf-8')}""")
                    else:
                        successful += 1
                        print(Fore.GREEN + f"""SUCCESS: Tests for {file} succeeded.""")
    print()
    print()
    print(Fore.WHITE + "Test Summary")
    print(Fore.GREEN + f"""Successful Tests: {successful}""")
    print(Fore.RED + f"""Failed Tests: {failures}""")
    print(Fore.WHITE)

    if (failures > 0):
        raise Exception(Fore.RED + f"{failures} tests failed" + Fore.WHITE)