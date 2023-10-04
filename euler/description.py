import textwrap

import requests
from bs4 import BeautifulSoup


def get_description(problem_number: int) -> str:
    # Base URL for Project Euler problems
    base_url: str = "https://projecteuler.net/problem="

    # Construct the full URL for the specific problem
    problem_url = f"{base_url}{problem_number}"

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
