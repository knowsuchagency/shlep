import argparse
import json
import logging
import os
from pathlib import Path

DEFAULT_EXCLUDED = [
    ".git/",
    ".idea/",
    ".pytest_cache/",
]

logger = logging.getLogger(__name__)


def get_excluded_patterns(directory, additional_excludes):
    excluded_patterns = DEFAULT_EXCLUDED + additional_excludes
    gitignore_path = os.path.join(directory, ".gitignore")
    if os.path.exists(gitignore_path):
        with open(gitignore_path) as f:
            for line in f:
                if line.strip() and not line.startswith("#"):
                    excluded_patterns.append(line.strip())
    return excluded_patterns


def is_excluded(path, excluded_patterns):
    return any(p in str(path) for p in excluded_patterns)


def create_output(
    directory: str,
    indent: int,
    additional_excludes: list[str],
    output_format: str,
    output_file: str = None,
) -> None:
    """
    Generate a file of all files in a directory.

    Args:
        directory: The directory to analyze.
        indent: The number of spaces to use for indentation in the output JSON.
        additional_excludes: Additional files or directories to exclude.
        output_format: The output format. Can be 'json', 'csv', or 'plaintext'. Default is 'json'.
        output_file: The output file to generate. If not specified, output is printed to stdout.

    Returns:
        None
    """
    excluded_patterns = get_excluded_patterns(directory, additional_excludes)

    files_list = []

    for path in Path(directory).rglob("*"):
        if path.is_file() and not is_excluded(path, excluded_patterns):
            try:
                content = path.read_text()
            except UnicodeDecodeError:
                logger.error(f"Could not read {path}")
            else:
                files_list.append({"path": str(path), "content": content})

    if output_format == "json":
        output = json.dumps({"files": files_list}, indent=indent)
    elif output_format == "csv":
        output = f"path,content{os.linesep}"
        for file in files_list:
            file_path = file["path"]
            file_content = file["content"]
            output += f"{file_path},{file_content}{os.linesep}"
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
        with open(output_file, "w") as f:
            f.write(output)
    else:
        print(output)


def cli():
    parser = argparse.ArgumentParser(
        prog="horde",
        description="Gather directory contents into a single output."
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
        choices=["json", "csv", "plaintext"],
        default="json",
        help="The output format. Can be 'json', 'csv', or 'plaintext'. Default is 'json'.",
    )
    args = parser.parse_args()
    excluded = args.exclude or []
    create_output(args.directory, args.indent, excluded, args.format, args.output_file)


if __name__ == "__main__":
    cli()
