# https://www.webucator.com/article/python-clocks-explained/
from __future__ import annotations

import datetime
import glob
import re
from pathlib import Path

import humanize


# Filenames follow the format (prefix, number, suffix, extension)
BASE_NAME = '{}{:04d}{}{}'
FILE_RE = re.compile(r'(.*)(\d{4})(.*)(\.\w+)')


class Problem:
    """Represents a Project Euler problem of a given problem number"""

    def __init__(self, problem_number: int, extension: str = ".py"):
        self.num: int = problem_number
        self.ext: str = extension

    def filename(self, prefix="pe_", suffix="", extension=".py") -> str:
        """Returns filename padded with leading zeros"""
        return BASE_NAME.format(prefix, self.num, suffix, extension)

    @property
    def glob(self) -> list[Path]:
        """Returns a sorted glob of files belonging to a given problem"""
        file_glob: list[Path] = list(
            Path(".").glob(
                BASE_NAME.format("*", self.num, "*", self.ext),
            ),
        )

        # Sort globbed files by tuple (filename, extension)
        return sorted(file_glob, key=lambda x: (x.stem, x.suffix))

    @property
    def file(self) -> ProblemFile | None:
        """Returns a ProblemFile instance of the first matching file"""
        return ProblemFile(self.glob[0]) if self.glob else None


class ProblemFile:
    """Represents a file that belongs to a given Project Euler problem"""

    def __init__(self, filename: Path):
        self.path: Path = filename
        self.name: str = filename.name
        self.stem: str = filename.stem

    @property
    def _filename_parts(self):
        """Returns (prefix, number, suffix, extension)"""
        match = FILE_RE.search(self.name)
        if match:
            return match.groups()
        else:
            raise ValueError("Invalid filename format")

    @property
    def prefix(self):
        return self._filename_parts[0]

    @property
    def str_num(self):
        return self._filename_parts[1]

    @property
    def suffix(self):
        return self._filename_parts[2]

    @property
    def extension(self):
        return self._filename_parts[3]

    @property
    def num(self):
        return int(self.str_num)


def problem_glob(extension: str = ".py") -> list[ProblemFile]:
    """Returns ProblemFile objects for all valid problem files"""
    # Only match with 3 numbers for now
    filenames = glob.glob(f"*[0-9][0-9][0-9]*{extension}")
    return [ProblemFile(Path(file)) for file in filenames]


def format_time(start: float, end: float) -> str:
    """Returns string with relevant time information formatted properly"""
    elapsed_time_seconds = end - start
    elapsed_time = datetime.timedelta(seconds=elapsed_time_seconds)
    human_time = humanize.precisedelta(
        elapsed_time, minimum_unit="microseconds",
    )

    return f"Time elapsed: {human_time}"
