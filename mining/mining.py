import os
import pandas as pd
import numpy as np
import csv
import time
from datetime import datetime
import subprocess
import shutil
import logging
from git import Repo
from git import exc

# Set up logging to a file named 'mining.log' with a specific format
logging.basicConfig(
    filename='mining.log',  # Log to a file named 'mining.log'
    level=logging.DEBUG,  # Log all levels from DEBUG and above
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Function to get timestamp (for logging purposes)
def giveTimeStamp():
    tsObj = time.time()
    strToret = datetime.fromtimestamp(tsObj).strftime('%Y-%m-%d %H:%M:%S')
    logging.debug(f"Timestamp generated: {strToret}")  # Log the timestamp creation
    return strToret

# Function to delete a repository folder
def deleteRepo(dirName, type_):
    logging.debug(f"Attempting to delete directory {dirName} of type {type_}")  # Log method call with parameters
    try:
        if os.path.exists(dirName):
            shutil.rmtree(dirName)
            logging.info(f"Successfully deleted {dirName}")  # Log successful deletion
    except OSError as e:
        logging.error(f"Failed to delete {dirName}. Error: {e}")  # Log error details

# Function to dump content into a file
def dumpContentIntoFile(strP, fileP):
    logging.debug(f"Attempting to write to file {fileP}")  # Log method call with parameters
    try:
        with open(fileP, 'w') as fileToWrite:
            fileToWrite.write(strP)
        logging.info(f"Content successfully written to {fileP}. File size: {os.stat(fileP).st_size} bytes")  # Log success
    except Exception as e:
        logging.error(f"Failed to write to file {fileP}. Error: {e}")  # Log error details
    return str(os.stat(fileP).st_size)

# Function to check Python files in a directory
def checkPythonFile(path2dir):
    logging.debug(f"Checking Python files in directory {path2dir}")  # Log method call with directory
    usageCount = 0
    patternDict = ['sklearn', 'h5py', 'gym', 'rl', 'tensorflow', 'keras', 'tf', 'stable_baselines', 'tensorforce', 'rl_coach', 'pyqlearning', 'MAMEToolkit', 'chainer', 'torch', 'chainerrl']
    try:
        for root_, dirnames, filenames in os.walk(path2dir):
            for file_ in filenames:
                full_path_file = os.path.join(root_, file_) 
                if file_.endswith('py') or file_.endswith('ipynb'):
                    with open(full_path_file, 'r', encoding='latin-1') as f:
                        pythonFileContent = f.read().split('\n')
                        pythonFileContent = [z_.lower() for z_ in pythonFileContent if z_ != '\n']
                        for content_ in pythonFileContent:
                            for item_ in patternDict:
                                if item_ in content_:
                                    usageCount += 1
                                    logging.info(f"Pattern match found in file {full_path_file}: {content_}")
    except Exception as e:
        logging.error(f"Error processing files in {path2dir}: {e}")  # Log error details
    return usageCount

# Function to get the email addresses of developers for a specific commit
def getDevEmailForCommit(repo_path_param, hash_):
    logging.debug(f"Getting emails for commit {hash_} in repo {repo_path_param}")  # Log method call with parameters
    author_emails = []
    try:
        cdCommand = f"cd {repo_path_param} ; "
        commitCountCmd = f" git log --format='%ae' {hash_}^!"
        command2Run = cdCommand + commitCountCmd
        author_emails = str(subprocess.check_output(['bash', '-c', command2Run]))
        author_emails = author_emails.split('\n')
        author_emails = [x_.replace(hash_, '') for x_ in author_emails if '@' in x_]
        logging.info(f"Found {len(author_emails)} unique author emails: {author_emails}")  # Log success
    except Exception as e:
        logging.error(f"Error retrieving emails for commit {hash_}: {e}")  # Log error details
    return author_emails

# Function to get the development email count and days of activity for a repository
def getDevDayCount(full_path_to_repo, branchName='master', explore=1000):
    logging.debug(f"Getting dev and commit count for repo {full_path_to_repo} on branch {branchName}")  # Log method call with parameters
    try:
        repo_ = Repo(full_path_to_repo)
        all_commits = list(repo_.iter_commits(branchName))
        dev_count = len(set([commit.author.email for commit in all_commits]))  # Count unique authors
        commit_count = len(all_commits)
        age_days = (datetime.now() - min([commit.committed_datetime for commit in all_commits])).days  # Calculate repo age in days
        logging.info(f"Repository has {dev_count} developers, {commit_count} commits, and an age of {age_days} days")
    except exc.GitCommandError as e:
        logging.error(f"Error processing repo {full_path_to_repo}: {e}")
        dev_count = commit_count = age_days = 0
    return dev_count, commit_count, age_days
