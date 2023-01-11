"""
Main Lox entrypoint.
"""

import sys

import scanner as s

HAD_ERROR = False


def run(source):
    """Executes the Lox code."""

    scanner = s.Scanner(source)
    tokens = scanner.scan_tokens()

    for token in tokens:
        print(token)


def run_file(path):
    """Executes a Lox file."""

    with open(path, "r", encoding="UTF-8") as file_in:
        bytes_in = file_in.readlines()
    run(bytes_in)
    if HAD_ERROR is True:
        sys.exit(65)


def run_prompt():
    """Executes a Lox REPL session."""

    while True:
        print("> ", end="")
        line = input()
        if line == "exit":
            break
        run(line)
        global HAD_ERROR
        HAD_ERROR = False


def error(line, message):
    """Raises an error."""

    report(line, "", message)


def report(line, where, message):
    """Reports an error."""

    print(f"[line {line}] Error{where}: {message}")
    global HAD_ERROR
    HAD_ERROR = True


if __name__ == "__main__":
    # Load in arguments
    args = sys.argv[1:]

    if len(args) > 1:
        print("Usage: plox [script]")
        sys.exit(64)
    elif len(args) == 1:
        run_file(args[0])
    else:
        run_prompt()
