import os
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup, Tag

class ProblemFetchError(Exception):
    pass

# Constants 
BASE_URL = "https://projecteuler.net/"
RESOURCES_DIR = os.path.join(os.getcwd(), "resources")

def fetch_problem(number: int) -> str:
    """
    Get the description for a Project Euler problem.

    Args:
        number (int): The problem number to retrieve.

    Returns:
        str: A message indicating the result of the operation.
    """
    problem_url = f"{BASE_URL}problem={number}"

    try:
        response = requests.get(problem_url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "html.parser")
        title = soup.find("h2")
        content = soup.find("div", class_="problem_content")

        if not (isinstance(title, Tag) and isinstance(content, Tag)):
            raise ProblemFetchError(f"Problem description not found for problem {number}")

        os.makedirs(RESOURCES_DIR, exist_ok=True)
        fetch_images(content)
        fetch_files(content)

        filename = f"{number:04d}.md"
        md_path = os.path.join(RESOURCES_DIR, filename)
        with open(md_path, "w") as md_file:
            md_file.write(f"{title}{content}")
        return f"Successfully created \"{filename}\"."

    except requests.exceptions.HTTPError as e:
        raise ProblemFetchError(f"HTTP error occurred while retrieving problem {number}: {e}")
    except requests.exceptions.RequestException as e:
        raise ProblemFetchError(f"Request error occurred while retrieving problem {number}: {e}")
    except Exception as e:
        raise ProblemFetchError(f"An unexpected error occurred: {e}")


def download_resource(url: str) -> str:
    """
    Download a resource from a URL and save it to the destination directory.

    Args:
        url (str): The URL of the resource.

    Returns:
        str: The filename of the downloaded resource.
    """
    try:
        response = requests.get(BASE_URL + url)
        response.raise_for_status()

        filename = os.path.basename(urlparse(url).path)
        file_path = os.path.join(RESOURCES_DIR, filename)
        with open(file_path, "wb") as file:
            file.write(response.content)
        return filename
    except requests.exceptions.HTTPError as e:
        raise ProblemFetchError(f"HTTP error occurred while retrieving {url}: {e}")
    except requests.exceptions.RequestException as e:
        raise ProblemFetchError(f"Request error occurred while retrieving {url}: {e}")
    except Exception as e:
        raise ProblemFetchError(f"An unexpected error occurred while downloading {url}: {e}")


def fetch_images(content: Tag):
    """
    Find and download images within the problem description.

    Args:
        content (Tag): The BeautifulSoup Tag containing the problem content.
    """
    for img_tag in content.find_all("img"):
        if img_url := img_tag.get("src"):
            img_filename = download_resource(img_url)
            img_tag["src"] = img_filename


def fetch_files(content: Tag):
    """
    Find and download links to files within the problem description.

    Args:
        content (Tag): The BeautifulSoup Tag containing the problem content.
    """
    for file_link in content.find_all("a"):
        if file_url := file_link.get("href"):
            # Check if the file ends with an extension
            if os.path.splitext(file_url)[1]:
                file_filename = download_resource(file_url)
                file_link["href"] = file_filename
