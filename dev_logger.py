#!/usr/bin/env python3
import os
from datetime import datetime
import yaml

# Content keywords below:
# Tasks, Progress, Challenges, Solutions, Decisions, Learnings, Next Steps, Additional Notes, Conclusion

backslash_character = chr(10)


def find_config_file(project_dir, config_file_name):
    try:
        project_config_file = os.path.join(project_dir, config_file_name)
        print(project_config_file)
        if not os.path.exists(project_config_file):
            default_config_file = os.path.expanduser(os.path.join('~', '.config', 'project_config.yaml'))
            project_config_file = default_config_file
        return project_config_file
    except FileNotFoundError as e:
        print(f'Error: {e} - File not found')


def read_config_file(config_file):
    with open(config_file, "r") as file:
        config = yaml.safe_load(file)
        headings = list(config['headings'])
        if isinstance(headings, list):
            return headings
        else:
            raise ValueError("Config file does not contain top level list")

def add_content(content_type):
    contents = []
    print(f"\n{content_type} summary:")
    while True:
        content = input(f"\nEnter {content_type} (or press Enter to finish):")
        if not content:
            break
        contents.append(content)
    return contents


def generate_dev_log(heading, contents):
    clean_heading = heading.replace("_", " ")
    # Cannot have \n or backslashes in general for brace substitutions in f-strings: see https://stackoverflow.com/questions/67680296/syntaxerror-f-string-expression-part-cannot-include-a-backslash
    markdown_content = f"""
## {clean_heading}
{backslash_character.join([f'- {content}' for content in contents])}
"""
    return markdown_content


def write_to_log_file(file_path, markdown_content):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "a") as file:
        file.write(markdown_content)


if __name__ == "__main__":
    today = datetime.today().strftime("%Y-%m-%d-%s")
    file_path = f"dev-logs/{today}_dev_log.md"
    
    project_dir = './config'
    config_file_name = 'project_config.yaml'

    config_file = find_config_file(project_dir, config_file_name)
    headings = read_config_file(config_file=config_file)

    project_name = input("Enter the project name: ")
    author_name = input("Enter your name: ")
    project_overview = input("Enter project overview: ")

    markdown_content = f"""
# Development Log - {project_name}

## Date: {today}

## Author: {author_name}

## Project Overview:
{project_overview}

"""
    write_to_log_file(file_path, markdown_content)

    for heading_to_complete in headings:
        points = add_content(heading_to_complete)
        markdown_content = generate_dev_log(heading_to_complete, points)
        write_to_log_file(file_path, markdown_content)

    print(f"\nDev log created: {file_path}")
