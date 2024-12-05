import random
import string
import subprocess
import os
import time
from mining.py import *

# Method 1: deleteRepo
def fuzz_deleteRepo():
    dirs = ["invalid_path", "/root", "/non_existent_dir"]
    for dir_name in dirs:
        try:
            deleteRepo(dir_name, "FuzzTest")
        except Exception as e:
            print(f"Error in deleteRepo with dir {dir_name}: {e}")

# Method 2: dumpContentIntoFile
def fuzz_dumpContentIntoFile():
    test_strings = [
        ''.join(random.choices(string.ascii_letters + string.digits, k=1024)),
        "Test String\nNew Line\nAnother Line",
        ''.join(random.choices(string.ascii_letters + string.digits, k=10000))
    ]
    file_paths = ["test_output.txt", "/invalid_path/test_output.txt"]
    
    for test_string in test_strings:
        for file_path in file_paths:
            try:
                print(f"Testing dumpContentIntoFile with file {file_path}")
                dumpContentIntoFile(test_string, file_path)
                file_size = os.stat(file_path).st_size
                print(f"File {file_path} written with size: {file_size}")
            except Exception as e:
                print(f"Error in dumpContentIntoFile with file {file_path}: {e}")

# Method 3: getDevEmailForCommit
def fuzz_getDevEmailForCommit():
    # Use some random commit hash and repo path for fuzz testing
    repo_path = "/some/nonexistent/repo"
    commit_hash = "123456abcdef"  # Random hash for fuzzing
    try:
        emails = getDevEmailForCommit(repo_path, commit_hash)
        print(f"Emails retrieved: {emails}")
    except Exception as e:
        print(f"Error in getDevEmailForCommit with repo {repo_path} and hash {commit_hash}: {e}")

# Method 4: getDevDayCount
def fuzz_getDevDayCount():
    # Use non-existent repo or incorrect paths
    repo_paths = ["/some/nonexistent/repo", ".", "../some_other_repo"]
    for repo_path in repo_paths:
        try:
            print(f"Fuzzing getDevDayCount with repo {repo_path}")
            dev_count, commit_count, age_days, age_months = getDevDayCount(repo_path)
            print(f"Dev count: {dev_count}, Commit count: {commit_count}, Age days: {age_days}, Age months: {age_months}")
        except Exception as e:
            print(f"Error in getDevDayCount with repo {repo_path}: {e}")

# Method 5: checkPythonFile
def fuzz_checkPythonFile():
    dirs = ["invalid_path", "/some/existing/path"]
    for dir_ in dirs:
        try:
            print(f"Fuzzing checkPythonFile with dir {dir_}")
            usage_count = checkPythonFile(dir_)
            print(f"Usage count: {usage_count}")
        except Exception as e:
            print(f"Error in checkPythonFile with dir {dir_}: {e}")

# Main function to run all fuzz tests
def main():
    fuzz_deleteRepo()
    fuzz_dumpContentIntoFile()
    fuzz_getDevEmailForCommit()
    fuzz_getDevDayCount()
    fuzz_checkPythonFile()

if __name__ == "__main__":
    main()
