# https://www.webucator.com/article/python-clocks-explained/
from __future__ import annotations

import glob
import re
from datetime import timedelta
from pathlib import Path

from humanize import precisedelta


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
    # TODO: Match with 4 numbers
    filenames = glob.glob(f"*[0-9][0-9][0-9]*{extension}")
    return list(map(lambda file: ProblemFile(Path(file)), filenames))


def format_time(start: float, end: float) -> str:
    """Format the time elapsed as a human-readable string"""
    elapsed_time_seconds = end - start
    elapsed_time = timedelta(seconds=elapsed_time_seconds)
    human_time = precisedelta(elapsed_time, minimum_unit="microseconds")

    return f"Time elapsed: {human_time}"
