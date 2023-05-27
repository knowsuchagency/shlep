# shlep


![ai](https://github.com/knowsuchagency/shlep/assets/11974795/ec862cfe-c1e3-45d8-9a75-92a240d2fb8d)


`shlep` lets you package your directory's content in a format that can be easily passed to ChatGPT. This is especially
useful when using the code interpreter plugin!

It automatically excludes files that match what's in your `.gitignore` file, as well as any additional exclude patterns you provide.

## Installation
You can install `shlep` from PyPI, but the recommended installation for the CLI is through [pipx][pipx].

```bash
pipx install shlep
```

## Features

- Supports various output formats: JSON, CSV, and plain text
- Excludes files and directories matching patterns in your `.gitignore` file
- Allows you to provide additional exclude patterns
- Can write output to a file or print it to stdout

## Demo

https://github.com/knowsuchagency/shlep/assets/11974795/ebfdae55-35f2-4edc-b0cb-089d2f99a7ca

## Usage

`shlep` can be used as a command-line tool or programmatically in your Python code.

### Command-line usage

```
usage: shlep [-h] [-o OUTPUT_FILE] [-i INDENT] [-e EXCLUDE] [-f {json,csv,plaintext}] directory

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
from shlep import shlep

directory = "path/to/your/directory"
indent = 2
additional_excludes = [".env", "node_modules/"]
output_format = "json"
output_file = "output.json"

shlep(directory, indent, additional_excludes, output_format, output_file)
```

## License

This project is licensed under the Apache License 2.0. You can find the full license text in the [LICENSE](LICENSE) file.

[pipx]: https://pypa.github.io/pipx/
