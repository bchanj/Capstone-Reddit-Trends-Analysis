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

    successful = 0
    failures = 0
    for root, dirs, files in os.walk('.'):
        path = root.split(os.sep)
        # skip files in root directory, we only want to test packages
        if len(path) <= 1:
            continue
        for file in files:
            if any([file.endswith(ext) for ext in target_extensions]):
                print(Fore.WHITE + f"""
=========================================                
RUN: Running tests for: {os.path.join(root, file)}""")
                file_path = os.path.join(root, file)
                try:
                    subprocess.run(['python3', file_path], check = True)
                except subprocess.CalledProcessError as e:
                    failures += 1
                    print("Tests Failed")
                    print(Fore.RED + f"""FAILURE: {file}, Path: {file_path}.
Here was the error {e}""")
                else:
                    successful += 1
                    print(Fore.GREEN + f"""SUCCESS: Tests for {file} succeeded.""")
    print()
    print()
    print(Fore.WHITE + "Test Summary")
    print(Fore.GREEN + f"""Successful Tests: {successful}""")
    print(Fore.RED + f"""Failed Tests: {failures}""")
    print(Fore.WHITE)