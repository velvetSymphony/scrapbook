#!/usr/bin/env python3
import os
from datetime import datetime
import yaml
import logging
from pathlib import Path
import argparse


debug_log_filename = "scrapbook-debug.log"
debug_log_filedirname = "scrapbooking-cli-debug-logs"
debug_log_filedirpath = Path.home() / debug_log_filedirname
debug_log_filepath = debug_log_filedirpath / debug_log_filename


# See function generate_markdown to know why you need this.
backslash_character = chr(10)

config_file_name = "scrapbook_config.yaml"
default_config_file = Path.home() / ".config" / config_file_name
scraps_dir = "scraps"
newline = "\n"


class NoteTakingError(Exception):
    pass


def check_debug_log_path(debug_log_filedirpath):
    if not os.path.exists(debug_log_filedirpath):
        try:
            os.makedirs(debug_log_filedirpath)
            print(f"Directory '{debug_log_filedirpath}' created successfully.")
        except OSError as e:
            raise OSError(f"Error creating directory: {e}")
    else:
        print(
            f"Directory '{debug_log_filedirpath}' exists. Check {debug_log_filepath} for debug/trace logs."
        )


def create_scrapbook_config_file():
    # Default headings used.
    config = {
        "headings": {
            "tasks": "Tasks",
            "challenges": "Challenges",
            "solutions": "Solutions",
            "learnings": "Learnings",
            "addtional_notes": "Additional Notes",
        }
    }
    with open(file=default_config_file, mode="w") as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False)
    return default_config_file


def find_config_file(project_dir, config_file_name):
    logging.info(f"Locating project config file for project directory: {project_dir}")
    scrapbook_config_file = os.path.join(project_dir, config_file_name)
    if not os.path.exists(scrapbook_config_file):
        logging.info(
            f"Scrapbook config file not found. Using default config file: {default_config_file} if it exists..."
        )
        scrapbook_config_file = default_config_file
        if not os.path.exists(scrapbook_config_file):
            logging.info("Default config file not found. Creating one...")
            scrapbook_config_file = create_scrapbook_config_file()
    return scrapbook_config_file


def read_config_file(config_file):
    with open(config_file, "r") as file:
        config = yaml.safe_load(file)

    if not isinstance(config, dict) or "headings" not in config:
        logging.error("Invalid config format: missing 'headings'")
        raise ValueError("Invalid config format: missing 'headings'")

    logging.info(f"Reading config file: {config_file}")

    headings = list(config["headings"])
    if not isinstance(headings, list):
        logging.error("Headings must be a list")
        raise ValueError("Headings must be a list")

    logging.info(f"Loaded {len(headings)} headings from config")
    return headings


def add_content(content_type):
    contents = []
    print(f"\n{content_type} summary:")
    while True:
        content = input(f"\nEnter {content_type} (or press Enter to finish):").strip()
        if not content:
            break
        contents.append(content)
    return contents


def generate_markdown(heading, contents):
    clean_heading = heading.replace("_", " ")
    # Cannot have \n or backslashes in general for brace substitutions in f-strings: see https://stackoverflow.com/questions/67680296/syntaxerror-f-string-expression-part-cannot-include-a-backslash
    markdown_content = f"""
## {clean_heading}
{backslash_character.join([f"- {content}" for content in contents])}
"""
    logging.info("Markdown content generated")
    return markdown_content


def write_to_log_file(file_path, markdown_content):
    try:
        os.makedirs(file_path.parent, exist_ok=True)
        with open(file_path, "a") as file:
            file.write(markdown_content)
        logging.info(f"Scrapbook entry written to file: {file_path}")
    except Exception as e:
        logging.error(f"Failed to write scrapbook entry: {str(e)}")
        raise NoteTakingError(f"Failed to write scrapbook entry`: {str(e)}")


def command_line_options():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-h",
        "--help",
        action="help",
        default=argparse.SUPPRESS,
        help="Display this help message",
    )
    return parser.parse_args()


def main():
    check_debug_log_path(debug_log_filedirpath)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        filename=debug_log_filepath,
        filemode="a",
    )
    try:
        project_name = input("Enter the project name: ")
        author_name = input("Enter your name: ")
        project_overview = input("Enter project overview: ")
        logging.info(
            f"Generating logs for project: {project_name}, author: {author_name}"
        )

        config_file = find_config_file("./config", config_file_name)
        headings = read_config_file(config_file)

        current_datetime = datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
        current_date = datetime.now().strftime("%Y-%m-%d")
        current_month= datetime.now().strftime("%B")
        current_year = datetime.now().year
        file_path = Path(scraps_dir) / f"{current_year}" / f"{current_month}" / f"{current_date}" / f"{current_datetime}_log_entry.md"

        markdown_content = \
f"""# Log Entry : {project_name}

## MetaData:
- Author: {author_name}
- Date written: {current_datetime}

## Project Overview:
{project_overview}

"""
        # Collect and add content for each heading
        for heading in headings:
            points = add_content(heading)
            if points:
                markdown_content += generate_markdown(heading, points)

        write_to_log_file(file_path, markdown_content)
        print(f"\nScrapbook journal entry created successfully: {file_path}")

    except NoteTakingError as e:
        logging.error(f"Fatal error: {e}")


if __name__ == "__main__":
    main()
