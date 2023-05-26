# horde

`horde` is a Python package that helps you package your directory's content in a format that can be easily passed to ChatGPT. 
`horde` automatically excludes files and directories that match patterns from your `.gitignore` file, as well as any additional exclude patterns you provide.

## Installation

You can install `horde` from PyPI using pip:

```bash
pip install horde
```

## Features

- Supports various output formats: JSON, CSV, and plain text
- Excludes files and directories matching patterns in your `.gitignore` file
- Allows you to provide additional exclude patterns
- Can write output to a file or print it to stdout

## Usage

`horde` can be used as a command-line tool or programmatically in your Python code.

### Command-line usage

```
usage: horde [-h] [-o OUTPUT_FILE] [-i INDENT] [-e EXCLUDE] [-f {json,csv,plaintext}] directory

Gather directory contents into a single output.

positional arguments:
  directory             The directory to analyze.

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        The output file to generate. If not specified, output is printed to stdout.
  -i INDENT, --indent INDENT
                        The number of spaces to use for indentation in the output JSON.
  -e EXCLUDE, --exclude EXCLUDE
                        Additional files or directories to exclude.
  -f {json,csv,plaintext}, --format {json,csv,plaintext}
                        The output format. Can be 'json', 'csv', or 'plaintext'. Default is 'json'.
```

### Programmatically in Python

```python
from horde import create_output

directory = "path/to/your/directory"
indent = 2
additional_excludes = [".env", "node_modules/"]
output_format = "json"
output_file = "output.json"

create_output(directory, indent, additional_excludes, output_format, output_file)
```

## License

This project is licensed under the Apache License 2.0. You can find the full license text in the [LICENSE](LICENSE) file.
