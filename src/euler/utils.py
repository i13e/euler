# https://www.webucator.com/article/python-clocks-explained/
from __future__ import annotations

import contextlib
import glob
import re
import time
from collections.abc import Generator
from datetime import datetime
from datetime import timedelta
from pathlib import Path

import click
import requests
from humanize import precisedelta

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
def fetch_data(url, cache_file="solutions.txt", cache_age_days=30):
    """
    Fetch and clean data from a URL, caching the result.

    :param url: URL to fetch the data from
    :param cache_file: Path to the cached file
    :param cache_age_days: Number of days before cache is considered stale
    :yield: A file object with cleaned data
    """
    cache_dir = Path.home() / ".cache" / "euler"
    cache_dir.mkdir(parents=True, exist_ok=True)
    cache_file_path = cache_dir / cache_file

    def is_cache_valid(file_path):
        if file_path.exists():
            last_modified = datetime.fromtimestamp(
                file_path.stat().st_mtime,
            )
            now = datetime.now()
            return now - last_modified < timedelta(days=cache_age_days)
        return False

    url = "https://raw.githubusercontent.com/lucky-bai/projecteuler-solutions/refs/heads/master/Solutions.md"  # noqa: E501

    try:
        if not is_cache_valid(cache_file_path):
            # Fetch data from the URL
            # print("Fetching data from URL...")
            response = requests.get(url)
            response.raise_for_status()  # Raise an error for bad status codes

            # Clean the data and save to the cache file
            cleaned_lines = []
            for line in response.text.splitlines():
                line = line.strip()
                if not (line and any(char.isdigit() for char in line)):
                    continue
                if "." in line:
                    line = line.replace(".", "", 1)
                cleaned_lines.append(line)

            with open(cache_file, "w") as file:
                file.write("\n".join(cleaned_lines))

        # Open the cache file for reading
        with open(cache_file) as file:
            yield file
