from __future__ import annotations

from typing import Callable

import click
from euler.problem import fetch
from euler.utils import Problem
from euler.utils import problem_glob
from euler.verify import cheat
from euler.verify import verify
from euler.verify import verify_all


def euler_commands(fn: Callable[..., int]) -> Callable[[int], int]:
    """Decorator to link CLI options with their appropriate functions"""
    euler_functions = cheat, fetch, verify, verify_all

    # Reverse functions to print help page options in alphabetical order
    for option in reversed(euler_functions):
        name, docstring = option.__name__, option.__doc__
        kwargs = {"flag_value": option, "help": docstring}

        # Apply flag(s) depending on whether or not name is a single word
        flag = f"--{name.replace('_', '-')}"
        flags = [flag] if "_" in name else [flag, f"-{name[0]}"]

        fn = click.option(
            "command",
            *flags,
            **kwargs,
            type=click.UNPROCESSED,
        )(fn)

    return fn


@click.command(name="euler", options_metavar="[OPTION]")
@click.argument("problem", default=0, type=click.IntRange(min=0))
@euler_commands
def main(command: Callable[[int], int], problem: int) -> int:
    """Python-based Project Euler command line tool."""

    # No problem number provided
    if not problem:
        # Determine the max problem number in the current directory
        problem = max((file.num for file in problem_glob()), default=0)

        # No Project Euler files in current directory
        if not problem:
            if command != cheat:
                msg = "No Project Euler files found in the current directory."
                click.echo(msg)
                if command == verify_all:
                    raise SystemExit(1)
                command = fetch
            problem = 1

        # found problem, no option; generate next file if answer is correct
        if command is None:
            verify(problem)
            problem += 1
            command = fetch

    # Problem given but no option; decide between generate and verify
    elif command is None:
        command = verify if Problem(problem).glob else fetch

    # Execute function based on option
    raise SystemExit(command(problem))


if __name__ == "__main__":
    raise SystemExit(main())
