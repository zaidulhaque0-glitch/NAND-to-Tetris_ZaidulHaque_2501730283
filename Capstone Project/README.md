# Nand2Tetris Capstone

**Student:** Zaidul Haque · **Roll number:** 2501730283 · **K:** 83

This folder contains the project 5 hardware chips, a two-pass Python Hack assembler with the K=83 duplicate-label warning, the personalized `Box.asm` program, its assembled `Box.hack`, and the capstone report.

## Personalized requirements

- Rectangle starts at screen row 83.
- Rectangle is 20 rows high and 64 pixels wide (four screen words).
- Since `83 mod 3 = 2`, duplicate labels produce a warning and the first definition is kept.

## Assemble Box.asm

Run `python assembler.py Box.asm` from this folder. The output is `Box.hack`.

Load `Box.hack` in the Nand2Tetris CPU Emulator. Enable its keyboard, focus the screen, and hold a key to display the black box; release it to clear the box.

## Contents

- `CPU.hdl`, `Memory.hdl`, `Computer.hdl`: project 5 chips.
- `assembler.py`: two-pass Hack assembler.
- `Box.asm`, `Box.hack`: personalized keyboard-controlled rectangle.
- `REPORT.md`: capstone report, test results, and evidence status.
- `ASSEMBLER_COMPARISONS.md`: course sample machine-code comparison record.
- `evidence/`: pass screenshots for all five hardware tests and the Box demo.

The box demo and pass screenshots for CPU.tst, Memory.tst, ComputerAdd.tst, ComputerMax.tst, and ComputerRect.tst are included.
