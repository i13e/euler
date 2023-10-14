[![main](https://github.com/i13e/euler/actions/workflows/main.yml/badge.svg)](https://github.com/i13e/euler/actions/workflows/main.yml)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/i13e/euler/master.svg)](https://results.pre-commit.ci/latest/github/i13e/euler/master)

# Euler

Euler is a command-line utility thoughtfully designed to simplify the process of solving Project Euler challenges using Python.
This versatile tool is centered around four primary functions:

1. **Problem Retrieval**: Conveniently fetch problems, associated files, and images from Project Euler for local reference.
2. **Code Generation**: Generate basic Python template files (with potential support for additional languages in the future).
3. **Solution Validation**: Verify the correctness of your solutions to Project Euler problems, ensuring that you're on the right track.
4. **Utility Functions**: Access a range of utility functions that can aid you in tackling complex problems more effectively.

## Getting Started

To begin, clone the Git repository by entering the following command in your
terminal/command prompt:

```sh
git clone https://github.com/i13e/euler.git
```

Once you have cloned the repository, navigate to its directory and create a new
Python virtual environment by running:

```sh
cd euler
python -m venv env
```

Activate the environment by running either of the following commands based on
your operating system:

```sh
source env/bin/activate # Mac or Linux
env\Scripts\activate # Windows
```

Next, install the packages listed in the `requirements.txt` file using the
following command:

```sh
pip install -r requirements.txt
```

You're now ready to go! Once you've finished, you can exit the
environment by running the following command (or simply close the terminal):

```sh
deactivate
```
