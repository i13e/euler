import argparse
import os

from euler.description import get_description


def create_problem_file(problem_number: int, description_text: str) -> int:
    """
    Create a markdown problem description file.

    Args:
        problem_number (int): The problem number.
        description_text (str): The description text to write to the file.

    Returns:
        int: 0 if the file creation is successful, 1 if there's an error.
    """

    # Create a filename based on the problem_number
    filename = f"{problem_number:03d}.md"

    # Write the description to the markdown file
    try:
        with open(filename, "w") as markdown_file:
            markdown_file.write(description_text)
        print(f"Successfully created '{filename}'.")
        return 0
    except IOError as e:
        print(f"Error creating '{filename}': {e}")
        return 1


def create_python_file(problem_number: int) -> int:
    """
    Create a Python solution file with a template.

    Args:
        problem_number (int): The problem number.

    Returns:
        int: 0 if the file creation is successful, 1 if there's an error.
    """

    # Create a filename based on the problem_number
    filename = f'{problem_number:03d}.py'

    # Create the Python file content
    python_code = f'''\
def main():
    pass


if __name__ == "__main__":
    main()
'''

    # Write the Python code to the file
    try:
        with open(filename, 'w') as file:
            file.write(python_code)
        print(f"Successfully created '{filename}'.")
        return 0
    except IOError as e:
        print(f"Error creating '{filename}': {e}")
        return 1


def find_missing_problem() -> int:
    """
    Find the first missing problem number by checking existing filenames.

    Returns:
        int: The first missing problem number.
    """
    problem_number = 1
    while os.path.exists(f"{problem_number:03d}.md"):
        problem_number += 1
    return problem_number


def main() -> None:
    parser = argparse.ArgumentParser(description="Scrape and display a Project Euler problem description.")
    parser.add_argument("problem_number", type=int, nargs="?", help="The number of the Project Euler problem to scrape")
    args = parser.parse_args()

    # If no problem number is provided, find the first missing problem
    problem_number = args.problem_number or find_missing_problem()

    if not args.problem_number and problem_number == 1:
        print("No Project Euler files found in the current directory.")
    generate_file = input(f"Generate file for problem {problem_number}? [Y/n]: ").strip().lower()
    if generate_file != 'n':
        description_text = get_description(problem_number)
        create_problem_file(problem_number, description_text)
        create_python_file(problem_number)
    else:
        print("Aborted!")


if __name__ == "__main__":
    main()
