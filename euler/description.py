import os
import textwrap
import requests
from bs4 import BeautifulSoup

# Project Euler Base URL 
BASE_URL = "https://projecteuler.net/"
RESOURCES_DIR = os.path.join(os.getcwd(), "resources")

def get_description(problem_number: int) -> str:
    """Get the description for a Project Euler problem."""
    problem_url = f"{BASE_URL}problem={problem_number}"

    response = requests.get(problem_url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        problem_title = soup.find("h2")
        problem_description = soup.find("div", class_="problem_content")

        if problem_title and problem_description:
            title_text = problem_title.get_text()
            description_text = problem_description.get_text()

            os.makedirs(RESOURCES_DIR, exist_ok=True)
            get_images(problem_description)
            get_files(problem_description)

            formatted_description = textwrap.fill(description_text, width=79)


            problem_info = f"Problem {problem_number} - {title_text}\n\n{formatted_description}"
            return problem_info
        else:
            return f"Problem description not found for problem {problem_number}"
    else:
        return f"Failed to retrieve problem {problem_number}. Status code: {response.status_code}"


def get_images(problem_description):
    """Find and download images within the problem description."""
    img_tags = problem_description.find_all("img")
    for img_tag in img_tags:
        img_url = img_tag.get("src")
        if img_url:
            img_response = requests.get(BASE_URL + img_url)
            if img_response.status_code == 200:
                img_filename = img_tag["alt"]
                img_path = os.path.join(RESOURCES_DIR, img_filename)
                with open(img_path, "wb") as img_file:
                    img_file.write(img_response.content)
                img_tag["src"] = img_filename


def get_files(problem_description):
    """Find and download links to files within the problem description."""
    file_links = problem_description.find_all("a")
    for file_link in file_links:
        file_url = file_link.get("href")
        if file_url:
            file_response = requests.get(BASE_URL + file_url)
            if file_response.status_code == 200:
                filename = os.path.basename(file_url)
                file_path = os.path.join(RESOURCES_DIR, filename)
                with open(file_path, "wb") as file:
                    file.write(file_response.content)
                file_link["href"] = os.path.join("resources", filename)
