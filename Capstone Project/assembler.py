#!/usr/bin/env python3
"""Two-pass assembler for the Hack computer (Nand2Tetris Part I)."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


PREDEFINED = {"SP": 0, "LCL": 1, "ARG": 2, "THIS": 3, "THAT": 4,
              "SCREEN": 16384, "KBD": 24576}
PREDEFINED.update({f"R{i}": i for i in range(16)})
DEST = {"": "000", "M": "001", "D": "010", "MD": "011", "A": "100",
        "AM": "101", "AD": "110", "AMD": "111"}
JUMP = {"": "000", "JGT": "001", "JEQ": "010", "JGE": "011",
        "JLT": "100", "JNE": "101", "JLE": "110", "JMP": "111"}
COMP = {
    "0": "0101010", "1": "0111111", "-1": "0111010", "D": "0001100",
    "A": "0110000", "M": "1110000", "!D": "0001101", "!A": "0110001",
    "!M": "1110001", "-D": "0001111", "-A": "0110011", "-M": "1110011",
    "D+1": "0011111", "A+1": "0110111", "M+1": "1110111",
    "D-1": "0001110", "A-1": "0110010", "M-1": "1110010",
    "D+A": "0000010", "D+M": "1000010", "D-A": "0010011",
    "D-M": "1010011", "A-D": "0000111", "M-D": "1000111",
    "D&A": "0000000", "D&M": "1000000", "D|A": "0010101", "D|M": "1010101",
}
SYMBOL_RE = re.compile(r"^[A-Za-z_.$:][A-Za-z0-9_.$:]*$")


class AssemblyError(Exception):
    def __init__(self, line_number: int, message: str):
        super().__init__(f"Line {line_number}: {message}")
        self.line_number = line_number


def clean_lines(source: str):
    for number, raw in enumerate(source.splitlines(), 1):
        code = raw.split("//", 1)[0].strip().replace(" ", "").replace("\t", "")
        if code:
            yield number, code


def assemble(source: str, warn=print):
    lines = list(clean_lines(source))
    symbols = dict(PREDEFINED)
    instructions = []
    rom = 0
    for number, code in lines:
        if code.startswith("(") and code.endswith(")"):
            label = code[1:-1]
            if not SYMBOL_RE.fullmatch(label):
                raise AssemblyError(number, "invalid label")
            if label in symbols:
                warn(f"Line {number}: warning: label '{label}' is already defined")
            else:
                symbols[label] = rom
        else:
            instructions.append((number, code))
            rom += 1

    next_variable = 16
    machine = []
    for number, code in instructions:
        if code.startswith("@"):
            token = code[1:]
            if not token:
                raise AssemblyError(number, "invalid A-instruction")
            if token.isdecimal():
                value = int(token)
            elif token in symbols:
                value = symbols[token]
            elif SYMBOL_RE.fullmatch(token):
                value = next_variable
                symbols[token] = value
                next_variable += 1
            else:
                raise AssemblyError(number, "invalid symbol")
            if not 0 <= value <= 32767:
                raise AssemblyError(number, "A-instruction value must be between 0 and 32767")
            machine.append(f"{value:016b}")
            continue

        if code.count(";") > 1 or code.count("=") > 1:
            raise AssemblyError(number, "invalid C-instruction")
        left, sep, jump = code.partition(";")
        dest, eq, comp = left.partition("=")
        if not eq:
            comp, dest = dest, ""
        if dest not in DEST or comp not in COMP or (sep and jump not in JUMP):
            raise AssemblyError(number, "invalid instruction")
        machine.append("111" + COMP[comp] + DEST[dest] + JUMP[jump if sep else ""])
    return machine, symbols


def main():
    parser = argparse.ArgumentParser(description="Assemble Hack .asm into .hack machine code")
    parser.add_argument("input", help="input .asm file")
    parser.add_argument("-o", "--output", help="output .hack file (defaults to same basename)")
    args = parser.parse_args()
    source_path = Path(args.input)
    output_path = Path(args.output) if args.output else source_path.with_suffix(".hack")
    try:
        machine, _ = assemble(source_path.read_text(encoding="utf-8"),
                              warn=lambda message: print(message, file=sys.stderr))
        output_path.write_text("\n".join(machine) + "\n", encoding="ascii")
    except (OSError, AssemblyError) as exc:
        print(exc, file=sys.stderr)
        return 1
    print(f"Wrote {len(machine)} instructions to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
