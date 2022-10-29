#! /usr/bin/env python
# coding=utf-8

"""
Utilities for fetching and unpacking packages from pypi
"""
import os
import shutil
import tarfile
import tempfile
import requests


def create_sandbox(name='healthybox'):
    """
    Create a temporary sandbox directory
    :param name: name of the directory to create
    :return: The directory created
    """
    sandbox = tempfile.mkdtemp(prefix=name)
    if not os.path.isdir(sandbox):
        os.mkdir(sandbox)

    return sandbox

def download_package_to_sandbox(sandbox, package_url):
    """
    Downloads an unzips a package to the sandbox
    :param sandbox: temporary directory name
    :param package_url: link to package download
    :returns: name of unzipped package directory
    """

    response = requests.get(package_url)

    package_tar = os.path.join(sandbox, 'package.tar.gz')

    with open(package_tar, 'w') as f:
        f.write(response.content)

    os.chdir(sandbox)

    with tarfile.open('package.tar.gz', 'r:gz') as tf:
        def is_within_directory(directory, target):
            
            abs_directory = os.path.abspath(directory)
            abs_target = os.path.abspath(target)
        
            prefix = os.path.commonprefix([abs_directory, abs_target])
            
            return prefix == abs_directory
        
        def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
        
            for member in tar.getmembers():
                member_path = os.path.join(path, member.name)
                if not is_within_directory(path, member_path):
                    raise Exception("Attempted Path Traversal in Tar File")
        
            tar.extractall(path, members, numeric_owner=numeric_owner) 
            
        
        safe_extract(tf)

    directory = [d for d in os.listdir(sandbox) if os.path.isdir(d)][0]

    return os.path.join(sandbox, directory)


def destroy_sandbox(sandbox):
    """
    Destroys a temporary sandbox directory
    :param sandbox: name of the directory acting as sandbox
    """
    if os.path.isdir(sandbox):
        shutil.rmtree(sandbox)


def main():
    """
    Main function for this module
    """
    sandbox = create_sandbox()
    directory = download_package_to_sandbox(
        sandbox,
        'https://pypi.python.org/packages/source/c/checkmyreqs/checkmyreqs-0.1.6.tar.gz'
    )
    print(directory)
    destroy_sandbox(sandbox)


if __name__ == '__main__':
    main()
