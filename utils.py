"""
Utility Functions Module

Description:
Provides supporting functions for logging errors and warnings,
ensuring necessary directories exist, saving files, and loading configuration.
"""

import os
import logging
import yaml
import re
import json
import csv

# Removed unused import 'sys'

# Configure logging
logging.basicConfig(level=logging.INFO)


def log_error(message):
    """
    Logs an error message and raises a RuntimeError to stop the program.

    Parameters:
    - message (str): Error message.
    """
    logging.error(message)
    raise RuntimeError(message)


def log_warning(message):
    """
    Logs a warning message for debugging.

    Parameters:
    - message (str): Warning message.
    """
    logging.warning(message)


def create_directory_if_missing(path):
    """
    Ensures that the specified directory exists. If not, raises an error.

    Parameters:
    - path (str): Directory path.
    """
    if not os.path.exists(path):
        log_error(f"Directory does not exist: {path}")
    else:
        logging.info(f"Directory already exists: {path}")


def save_file(data, path, file_format='json'):
    """
    Saves data to a file in the specified format.

    Parameters:
    - data: Data to save.
    - path (str): File path.
    - file_format (str): 'json' or 'csv'. Defaults to 'json'.
    """
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        if file_format.lower() == 'json':
            with open(path, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4)
        elif file_format.lower() == 'csv':
            with open(path, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                if isinstance(data, dict):
                    for key, value in data.items():
                        writer.writerow([key, value])
                else:
                    writer.writerows(data)
        else:
            log_warning("Unsupported file format. Saving as JSON by default.")
            with open(path, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4)
    except Exception as e:
        log_error(f"Failed to save data to file: {e}")


def load_config(config_file="config.yaml"):
    """
    Loads configuration settings from a YAML file.

    Parameters:
    - config_file (str): Path to the YAML configuration file.

    Returns:
    - dict: Configuration dictionary.
    """
    try:
        with open(config_file, 'r', encoding='utf-8') as file:
            return yaml.safe_load(file)
    except Exception as e:
        log_error(f"Failed to load configuration file: {e}")


def parse_page_ranges(page_ranges):
    """
    Parses page ranges from the configuration (e.g., '1-5') into a list of page numbers.

    Parameters:
    - page_ranges (list): List of strings in 'start-end' format.

    Returns:
    - list: List of individual page numbers.
    """
    pages = []
    for page_range in page_ranges:
        try:
            start, end = map(int, page_range.split('-'))
            pages.extend(range(start, end + 1))
        except ValueError:
            log_warning(f"Invalid page range format: {page_range}")
    return pages


def get_page_number_from_filename(filename):
    """
    Extracts the page number from an image filename assumed to be in the format 'page_<number>.tiff'.

    Parameters:
    - filename (str): Image filename.

    Returns:
    - int or None: The extracted page number, or None if not found.
    """
    match = re.match(r'page_(\d+)\.tiff$', filename)
    if match:
        return int(match.group(1))
    return None
