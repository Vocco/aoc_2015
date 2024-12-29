<!-- SPDX-License-Identifier: MIT -->
<!-- Copyright (c) Vojtech Krajnansky -->
# User Guide for Santa's Floor Direction Helper
This guide explains how to use the program to determine the final floor based on a sequence of floor directions, leveraging the provided utilities.

## 1 Program Overview
### 1.1 Purpose
The program calculates the final floor from a sequence of directions using the following rules:
- `"("` indicates moving **up** one floor.
- `")"` indicates moving **down** one floor.

### 1.2 Requirements
- Python version: **3.10 or higher**
- Input file containing only `"("` and `")"` characters in a single line.

## 2 Components
The program consists of the following modules:
- `floorfinder.py`:
  - Main entry point for the program. Handles argument parsing, calls supporting modules, and outputs results.
- `floordirections.py`:
  - Contains the logic to validate and analyze the direction sequence.
- `fileinputhandler.py`:
  - Manages file reading with robust error handling.
- `outputhandler.py`:
  - Handles success and error notifications for user feedback.

## 3 How to Use
### Step 1: Prepare Your Input File
Create and save a file containing the direction sequence. For example:
```text
((())())(()))
```

### Step 2: Run the Program
Use the following command to run the program:
```bash
python floorfinder.py <FILE>
```

Replace `<FILE>` with the path to your input file. For example:
```bash
python floorfinder.py directions.txt
```
## 4 Example Usage
### Input File: `directions.txt`
```
((())(
```

### Command:
```bash
python floorfinder.py directions.txt
```

### Output:
```text
Execution successful
Final Floor: 2
```

## 5 Error Handling
The program handles common errors gracefully and provides detailed error messages.

| **Error Type**                     | **Cause**                                                      | **Message**                                                          |
|------------------------------------|----------------------------------------------------------------|----------------------------------------------------------------------|
| **File Not Found**                 | The specified file path does not exist.                        | `The resource "<FILE_PATH>" does not exist`                          |
| **Path Is Not a File**             | The specified path is a directory or non-file resource.        | `The resource "<FILE_PATH>" is not a file`                           |
| **File Not Accessible**            | The file lacks read permissions.                               | `The file "<FILE_PATH>" is not accessible`                           |
| **Invalid Characters in Sequence** | The input file contains characters other than `"("` and `")"`. | `Sequence contains invalid characters; only "(" and ")" are allowed` |
| **Unexpected Encoding**            | The file is not encoded in UTF-8.                              | `The file "<FILE_PATH>" is not UTF-8 encoded`                        |
| **Keyboard Interruption**          | The user interrupts the process (typically with `CTRL + C`).   | `Execution interrupted by user`                                      |
| **Critical Failure**               | An unexpected error occurs.                                    | `Cause: <ERROR_MESSAGE>`                                             |


---

**License**: This program and related documentation is licensed under the **MIT License**. See the `LICENSE` file in the project root for full license details.
