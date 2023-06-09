import argparse
import fnmatch
import json
import logging
import os
from pathlib import Path

from pathspec import PathSpec

DEFAULT_EXCLUDED = [".git", ".idea"]

logger = logging.getLogger(__name__)


def _is_excluded(base: Path, path: Path, spec: PathSpec = None, only_patterns=None):
    path_relative_to_base = str(path.relative_to(base))

    if only_patterns:
        if any(path_relative_to_base == pattern for pattern in only_patterns):
            return False
        else:
            return True

    if not spec:
        return True

    return spec.match_file(path_relative_to_base)


def shlep(
    directory: Path | str,
    indent: int | None,
    additional_excludes: list[str],
    output_format: str,
    output_file: Path | str = None,
    quiet=False,
    only_patterns=None,
) -> str:
    """
    Generate a file of all files in a directory.

    Args:
        directory: The directory to analyze.
        indent: The number of spaces to use for indentation in the output JSON.
        additional_excludes: Additional files or directories to exclude.
        output_format: The output format. Can be 'json', 'csv', or 'plaintext'. Default is 'json'.
        output_file: The output file to generate. If not specified, output is printed to stdout.
        quiet: don't print output to stdout
        only_patterns: Only include files that match any of the specified patterns.

    Returns (str):
        output
    """
    files_list = []
    base = Path(directory).expanduser()

    if (gitignore := base / ".gitignore").exists():
        with gitignore.open() as f:
            additional_excludes.extend(
                line.strip() for line in f if line.strip() and not line.startswith("#")
            )
        spec = PathSpec.from_lines(
            "gitwildmatch",
            DEFAULT_EXCLUDED + additional_excludes,
        )
    else:
        spec = None

    for path in base.rglob("*"):
        if path.is_file() and not _is_excluded(base, path, spec, only_patterns):
            try:
                content = path.read_text()
            except UnicodeDecodeError:
                logger.error(f"Could not read {path}")
            else:
                files_list.append({"path": str(path), "content": content})

    if output_format == "json":
        output = json.dumps(files_list, indent=indent)
    else:  # plaintext
        output = ""
        len_files_list = len(files_list)
        for i, file in enumerate(files_list, start=1):
            filepath = file["path"]
            file_content = file["content"]
            output += f"`{filepath}`"
            output += os.linesep
            output += f"```{os.linesep + file_content}```"
            if not i == len_files_list:
                output += os.linesep * 2 + "---" + os.linesep * 2

    if output_file:
        with Path(output_file).expanduser().open("w") as f:
            f.write(output)
    elif not quiet:
        print(output)

    return output


def cli():
    parser = argparse.ArgumentParser(
        prog="shlep",
        usage="%(prog)s [OPTIONS] directory",
        description="Gather directory contents into a single output.",
    )
    parser.add_argument("directory", help="The directory to analyze.")
    parser.add_argument(
        "-o",
        "--output-file",
        help="The output file to generate. If not specified, output is printed to stdout.",
    )
    parser.add_argument(
        "-i",
        "--indent",
        type=int,
        default=2,
        help="The number of spaces to use for indentation in the output JSON.",
    )
    parser.add_argument(
        "-e",
        "--exclude",
        type=str,
        action="append",
        help="Additional files or directories to exclude.",
    )
    parser.add_argument(
        "-f",
        "--format",
        choices=["json", "plaintext"],
        default="json",
        help="The output format. Can be 'json' or 'plaintext'. Default is 'json'.",
    )
    parser.add_argument(
        "-y",
        "--only",
        type=str,
        action="append",
        help="Only include files that match this pattern. Can be used multiple times.",
    )
    args = parser.parse_args()
    excluded = args.exclude or []
    shlep(
        args.directory,
        args.indent,
        excluded,
        args.format,
        args.output_file,
        only_patterns=args.only,
    )


if __name__ == "__main__":
    cli()
