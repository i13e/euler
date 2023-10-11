from __future__ import annotations

import os
from urllib.parse import urlparse

import click
import requests
from bs4 import BeautifulSoup
from bs4 import Tag

from euler.utils import Problem


# Constants
BASE_URL = "https://projecteuler.net/"
RESOURCES_DIR = os.path.join(os.getcwd(), "resources")


def fetch(number: int) -> int:
    """Fetch the description and all related files for a problem."""

    click.confirm(f"Generate file for problem {number}", abort=True)
    problem_url = f"{BASE_URL}problem={number}"

    try:
        response = requests.get(problem_url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "html.parser")
        title = soup.find("h2")
        content = soup.find("div", class_="problem_content")

        if not (isinstance(title, Tag) and isinstance(content, Tag)):
            print(f"Problem description not found for problem {number}")
            return 1

        os.makedirs(RESOURCES_DIR, exist_ok=True)
        fetch_images(content)
        fetch_files(content)
        create_solution(number)

        filename = f"{number:04d}.md"
        md_path = os.path.join(RESOURCES_DIR, filename)
        with open(md_path, "w") as md_file:
            md_file.write(f"{title}{content}")

        click.secho(f"Successfully created \"{filename}\".", fg="green")
        return 0

    except requests.exceptions.HTTPError as e:
        print(f"HTTP error occured while retrieving problem {number}: {e}")
        raise
    except requests.exceptions.RequestException as e:
        print(f"Request error while retrieving problem {number}: {e}")
        raise
    except Exception as e:
        print(f"An unexpected error occured: {e}")
        raise


def download_resource(url: str) -> str:
    """Download a resource from and save it to the destination directory."""

    try:
        response = requests.get(BASE_URL + url)
        response.raise_for_status()

        filename = os.path.basename(urlparse(url).path)
        file_path = os.path.join(RESOURCES_DIR, filename)
        with open(file_path, "wb") as file:
            file.write(response.content)

        msg = f"Copied {filename} to {file_path}."
        click.secho(msg, fg="green")
        return filename
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error occured while retrieving {url}: {e}")
        raise
    except requests.exceptions.RequestException as e:
        print(f"Request error while retrieving {url}: {e}")
        raise
    except Exception as e:
        print(f"An unexpected error occured while retrieving {url}: {e}")
        raise


def fetch_images(content: Tag) -> None:
    """Find and download images within the problem description."""

    for img_tag in content.find_all("img"):
        if img_url := img_tag.get("src"):
            img_filename = download_resource(img_url)
            img_tag["src"] = img_filename


def fetch_files(content: Tag) -> None:
    """Find and download files within the problem description."""

    for file_link in content.find_all("a"):
        if file_url := file_link.get("href"):
            # Check if the file ends with an extension
            if os.path.splitext(file_url)[1]:
                file_filename = download_resource(file_url)
                file_link["href"] = file_filename


def create_solution(number: int, extension: str = ".py") -> int:
    """Create a Python solution file with a template."""

    p = Problem(number)

    # Allow skipped problem files to be recreated
    if p.glob:
        filename = str(p.file)
        msg = f"\"{filename}\" already exists. Overwrite?"
        click.confirm(click.style(msg, fg="red"), abort=True)
    else:
        # Try to keep prefix consistent with existing files
        previous_file = Problem(p.num - 1).file
        prefix = previous_file.prefix if previous_file else "pe_"
        filename = p.filename(prefix=prefix, extension=extension)

    # Create the Python file content
    python_code = '''\
def main():
    pass


if __name__ == "__main__":
    print(main())
'''

    # Write the Python code to the file
    try:
        with open(filename, "w") as file:
            file.write(python_code)
        click.secho(f"Successfully created \"{filename}\".", fg='green')
        return 0
    except OSError as e:
        print(f"Error creating \"{filename}\": {e}")
        raise
