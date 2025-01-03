# https://www.webucator.com/article/python-clocks-explained/
from __future__ import annotations

import contextlib
import glob
import json
import re
import time
from collections.abc import Generator
from datetime import timedelta
from pathlib import Path

import click
import requests
from humanize import precisedelta

# from io import TextIOWrapper

# import sys


# Filenames follow the format (prefix, number, suffix, extension)
BASE_NAME = "{}{:04d}{}{}"
FILE_RE = re.compile(r"(.*)(\d{4})(.*)(\.\w+)")


class Problem:
    def __init__(self, problem_number: int, extension: str = ".py"):
        self.num: int = problem_number
        self.ext: str = extension

    def filename(self, prefix="pe_", suffix="", extension=".py") -> str:
        """Generate a formatted filename for the problem"""
        return BASE_NAME.format(prefix, self.num, suffix, extension)

    @property
    def glob(self) -> list[Path]:
        """Retrieve a sorted list of files belonging to a given problem"""
        file_glob: list[Path] = list(
            Path(".").glob(
                BASE_NAME.format("*", self.num, "*", self.ext),
            ),
        )

        # Sort globbed files by tuple (filename, extension)
        return sorted(file_glob, key=lambda x: (x.stem, x.suffix))

    @property
    def file(self) -> ProblemFile | None:
        """Retrieve the first matching file as a ProblemFile instance"""
        return ProblemFile(self.glob[0]) if self.glob else None


class ProblemFile:
    def __init__(self, filename: Path):
        self.path: Path = filename
        self.name: str = filename.name
        self.stem: str = filename.stem

    @property
    def _filename_parts(self):
        """Parse the filename into parts (prefix, number, suffix, extension)"""
        match = FILE_RE.search(self.name)
        if match:
            return match.groups()
        else:
            raise ValueError("Invalid filename format")

    prefix = property(lambda self: self._filename_parts[0])
    str_num = property(lambda self: self._filename_parts[1])
    suffix = property(lambda self: self._filename_parts[2])
    extension = property(lambda self: self._filename_parts[3])
    num = property(lambda self: int(self.str_num))


def problem_glob(extension: str = ".py") -> list[ProblemFile]:
    """Retrieve a list of ProblemFile objects for all valid problem files"""
    filenames = glob.glob(f"*[0-9][0-9][0-9][0-9]*{extension}")
    return list(map(lambda file: ProblemFile(Path(file)), filenames))


@contextlib.contextmanager
def timing(name: str = "") -> Generator[None]:
    """Get the time elapsed and format as a human-readable string"""
    start: float = time.perf_counter()

    yield

    end: float = time.perf_counter()

    elapsed_time = timedelta(seconds=(end - start))
    human_time = precisedelta(elapsed_time, minimum_unit="microseconds")

    if name:
        name = f" ({name})"

    # print(f"Time elapsed: {human_time}", file=sys.stderr, flush=True)
    click.secho(f"Time elapsed: {human_time}", fg="cyan")


@contextlib.contextmanager
def fetch_data():
    url = "https://raw.githubusercontent.com/lucky-bai/projecteuler-solutions/refs/heads/master/Solutions.md"  # noqa: E501
    cache_file = "solutions.json"
    cache_age_days = 7
    cache_dir = Path.home() / ".cache" / "euler"
    cache_dir.mkdir(parents=True, exist_ok=True)
    cache_file_path = cache_dir / cache_file

    def is_cache_valid():
        if cache_file_path.exists():
            then = cache_file_path.stat().st_mtime
            now = time.time()
            return now - then < cache_age_days * 86400

    if not is_cache_valid():
        response = requests.get(url)
        response.raise_for_status()

        # Clean and parse the data into a dictionary
        solutions = {}
        for line in response.text.splitlines()[4:]:
            try:
                q, a = line.split(". ", maxsplit=1)
                solutions[q] = a
            except ValueError:
                continue

        # Save the parsed data as a JSON file
        with open(cache_file_path, "w") as file:
            json.dump(solutions, file)

    # Open and load the JSON data, then yield it
    with open(cache_file_path) as file:
        # data = json.load(file)
        # yield data
        yield file
