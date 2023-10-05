import re
import requests
import os
import textwrap

from bs4 import BeautifulSoup


def get_description(problem_number: int) -> str:
    # Base URL for Project Euler problems
    base_url = "https://projecteuler.net/"

    # Construct the full URL for the specific problem
    problem_url = f"{base_url}problem={problem_number}"

    # Send a GET request to the problem page
    response = requests.get(problem_url)

    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.content, "html.parser")

        # Find the problem title element (usually in a h2 tag with class "problem_title")
        problem_title = soup.find("h2")

        # Find the problem description element (usually in a div with class "problem_content")
        problem_description = soup.find("div", class_="problem_content")

        if problem_title and  problem_description:
            # Extract the text content of the problem title
            title_text = problem_title.get_text()

            # Extract the text content of the problem description
            description_text = problem_description.get_text()

            # Find and download images within the problem description
            img_tags = problem_description.find_all("img")
            for img_tag in img_tags:
                img_url = img_tag.get("src")
                if img_url:
                    img_response = requests.get(base_url + img_url)
                    if img_response.status_code == 200:
                        # Save the image to the resources directory
                        img_filename = os.path.basename(img_url)
                        img_path = os.path.join(os.getcwd(), "resources", img_filename)
                        with open(img_path, 'wb') as img_file:
                            img_file.write(img_response.content)
                        # Replace the image URL in the description with the local path
                        img_tag['src'] = img_filename


            # Find and download links to files within the problem description
            file_links = problem_description.find_all("a")
            for file_link in file_links:
                file_url = file_link.get("href")
                if file_url:
                    file_response = requests.get(base_url + file_url)
                    if file_response.status_code == 200:
                        # Determine the filename from the URL
                        filename = os.path.basename(file_url)
                        # Save the file to the resources directory
                        file_path = os.path.join(os.getcwd(), "resources", filename)
                        with open(file_path, 'wb') as file:
                            file.write(file_response.content)
                        # Replace the file URL in the description with the local path
                        file_link['href'] = os.path.join("resources", filename)


            # Format the description to 79 characters per line
            formatted_description = textwrap.fill(description_text, width=79)

            # Combine the title and description
            problem_info = f"Problem {problem_number} - {title_text}\n\n{formatted_description}"

            # Print the formatted description as a raw string
            return f"{problem_info}"
        else:
            return f"Problem description not found for problem {problem_number}"
    else:
        return f"Failed to retrieve problem {problem_number}. Status code: {response.status_code}"



def get_files()
