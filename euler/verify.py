from __future__ import annotations

import sys
import time
from importlib import import_module
from pathlib import Path

import click

from euler.utils import format_time
from euler.utils import Problem
from euler.utils import problem_glob


# Store problem answers
ANSWERS: dict[int, str] = {}

# Load answers from the solutions file
solutions = Path(__file__).parent / "solutions.txt"
with solutions.open() as file:
    for line in file:
        parts = line.strip().split()
        if len(parts) == 2:
            num, answer = map(str, parts)
            ANSWERS[int(num)] = answer

sys.path.append(".")


def verify(num: int) -> int:
    """Verify the solution for a given problem number."""
    p = Problem(num)
    file = p.file

    if not file:
        click.secho(f"No file found for problem {p.num}.", fg="red")
        return 2

    print(file.stem)
    module = import_module(file.stem)

    solution = ANSWERS.get(num)
    # if solution is None:
    #     click.secho(f"No solution found for problem {num}.", fg="red")
    #     msg = f'Answer for problem {num} not found in solutions.txt.'
    #     click.secho(msg, fg="red")
    #     click.echo('If you have an answer, please submit a PR on GitHub.')
    #     return 3

    click.echo(f"Checking \"{file.name}\" against solution: ", nl=False)

    start = time.perf_counter()
    try:
        actual = str(module.main())
    except Exception as e:
        click.secho(f"Error calling \"{file.name}\".", fg="red")
        click.secho(str(e), fg="red")
        return 2
    end = time.perf_counter()

    incorrect = actual != solution
    fg_color = ["green", "red"][incorrect]
    click.secho(actual, bold=True, fg=fg_color)
    click.secho(format_time(start, end), fg="cyan")
    return incorrect


def verify_all(max_num: int) -> int:
    """Verify solutions for all available problems."""

    # Define status icons for different outcomes
    keys = ("correct", "incorrect", "error", "skipped", "missing")
    colors = ("green", "red", "yellow", "cyan", "white")
    symbols = ("C", "I", "E", "S", ".")
    status_icons: dict[str, str] = {}
    for key, color, symbol in zip(keys, colors, symbols):
        status_icons[key] = click.style(symbol, fg=color, bold=True)

    overview: dict[int, str] = {}

    # Search through problem files using glob module
    for file in problem_glob():
        try:
            # Verify the problem file and determine its status.
            is_correct = verify(file.num)
        except KeyboardInterrupt:
            # Allow user to skip verification if it takes too long.
            overview[file.num] = status_icons["skipped"]
        else:
            # Determine the status based on the result
            if is_correct == 2:
                overview[file.num] = status_icons["error"]
            elif is_correct == 0:
                overview[file.num] = status_icons["correct"]
            elif is_correct == 1:
                overview[file.num] = status_icons["incorrect"]

        click.echo()

    # Create a legend for status icons
    legend = ", ".join(f"{v} = {k}" for k, v in status_icons.items())

    click.echo("-" * 63)
    click.echo(legend + "\n")

    num_rows = (max_num + 19) // 20

    for row in range(1, num_rows + 1):
        lo, hi = (row * 20) - 19, row * 20
        click.echo(f"Problems {lo:04d}-{hi:04d}: ", nl=False)

        for problem in range(lo, hi + 1):
            status = overview.get(problem, ".")
            spacer = " " if problem % 5 else "   "
            click.secho(status + spacer, nl=(not problem % 20))

    click.echo()
    return 0


def cheat(num: int) -> int:
    """View the answer to a problem."""
    solution = click.style(ANSWERS.get(num), bold=True)
    click.confirm(f"View answer to problem {num}?", abort=True)
    click.echo(f"The answer to problem {num} is {solution}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(verify_all(0))
