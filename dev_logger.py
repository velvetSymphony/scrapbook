#!/usr/bin/env python3
import os
from datetime import datetime

# Content keywords below:
# Tasks, Progress, Challenges, Solutions, Decisions, Learnings, Next Steps, Additional Notes, Conclusion

backslash_character = chr(10)

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
    today = datetime.today().strftime("%Y-%m-%d")
    file_path = f"dev-logs/{today}_dev_log.md"
    headings_to_complete = (
        "tasks",
        "challenges",
        "solutions",
        "decisions_made",
        "learnings",
        "next_steps",
        "additional_notes",
        "conclusion",
    )

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

    for heading_to_complete in headings_to_complete:
        points = add_content(heading_to_complete)
        markdown_content = generate_dev_log(heading_to_complete, points)
        write_to_log_file(file_path, markdown_content)

    print(f"\nDev log created: {file_path}")
