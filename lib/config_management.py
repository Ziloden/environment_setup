#!/usr/bin/env python3
import json
import os
import shutil
from functools import lru_cache

@lru_cache(maxsize=1)
def load_manifest(manifest_path):
    """Loads a json manifest file and returns the dictionary

    Args:
        manifest_path (string): the path to the manifest file

    Returns:
        dict: manifest containing information on what to process
    """
    manifest = {}
    with open(manifest_path, 'r') as f:
        try:
            manifest = json.load(f)
        except Exception as e:
            print(e)
    return manifest

@lru_cache(maxsize=1)
def load_backup_manifest(manifest_path):
    """Retriever for just the backup portion of the manifest

    Args:
        manifest_path (string): the path to the manifest file

    Returns:
        dict: manifest containing just the files for backup
    """
    return load_manifest(manifest_path)['backups']

@lru_cache(maxsize=1)
def load_setup_manifest(manifest_path):
    """Retriever for just the setup portion of the manifest

    Args:
        manifest_path (string): the path to the manifest file

    Returns:
        dict: manifest containing just the setup information
    """
    return load_manifest(manifest_path)['setup']

def get_source_path(file_name, path, is_home_dir, user):
    """Generates the source path of a file to backup. If the argument is_home_dir is true, the path argument is appended to it.

    Args:
        file_name (string): the name of the file to backup
        path (string): the path excluding the file name of the file to backup
        is_home_dir (bool): whether the path is in the home dir
        user (string): the user name for the home dir

    Returns:
        string: the full path to the source file for backup
    """
    source_path = path
    if is_home_dir:
        source_path = os.path.join(os.path.expanduser(f"~{user}"), source_path)
    
    full_source_path = os.path.join(source_path, file_name)
    
    return full_source_path

def get_backup_path(source_path, target):
    """Generates the backup path of a file to backup. This is where the file will be stored.

    Args:
        source_path (string): the full path of the file to backup
        target (string): the target environment. This is just to keep some configs for say laptop/desktop separate if needed.

    Returns:
        string: the full path to the backup file location
    """
    full_backup_path = os.path.join(os.getcwd(), f"settings_backups/{target}", source_path.lstrip('/'))

    return full_backup_path

def backup(manifest_path, target, user):
    manifest = load_backup_manifest(manifest_path)

    for file_entry in manifest:
        full_source_path = get_source_path(file_entry['name'], file_entry['path'], file_entry['home'], user)
        
        if not os.path.isfile(full_source_path):
            print(f"File {full_source_path} does not exist. Skipping...")
            continue
        
        full_backup_path = get_backup_path(full_source_path, target)

        if not os.path.exists(os.path.dirname(full_backup_path)):
            os.makedirs(os.path.dirname(full_backup_path))

        shutil.copy(full_source_path, full_backup_path)

def restore(manifest_path, target, user):
    manifest = load_manifest(manifest_path)

    for file_entry in manifest:
        full_source_path = get_source_path(file_entry['name'], file_entry['path'], file_entry['home'], user)
        full_backup_path = get_backup_path(full_source_path, target)

        if not os.path.isfile(full_backup_path):
            print(f"File {full_backup_path} does not exist. Skipping...")
            continue

        if not os.path.exists(os.path.dirname(full_source_path)):
            os.makedirs(os.path.dirname(full_source_path))

        shutil.copy(full_backup_path, full_source_path)

def setup():
    pass