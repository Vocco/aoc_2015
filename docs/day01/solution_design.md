<!-- SPDX-License-Identifier: MIT -->
<!-- Copyright (c) Vojtech Krajnansky -->
# Solution Design: Advent of Code 2015: Day 01
## Part 1
### 1.1 Requirements Analysis
#### 1.1.1 Problem Statement
Given a sequence of `(` and `)` characters (`directions`), where:
- `(` means "go up 1 floor".
- `)` means "go down 1 floor".

The task is to determine the final floor based on the provided sequence.

#### 1.1.2 Inputs
- **Input format**: A file containing a single line of `directions`.
  - **Constraints**:
    - File must exist and be readable.
    - The sequence may only contain `(` and `)` characters.

#### 1.1.3 Outputs
- **Output format**: A single integer representing the **final floor**.

#### 1.1.4 Edge Cases
1. **Empty input**: Return `0`.
2. **Single direction** in the file:
   - Return `1` for `(`.
   - Return `-1` for `)`.
3. **Balanced directions** (equal numbers of `(` and `)`): Return `0`.
4. **Only `(` or `)` in the file**:
   - Return `count('(')` or `-count(')')` respectively.

### 1.2 Design
#### 1.2.1 Solution Steps
1. **File Reading**:
   - Read the file containing `directions`.
   - Handle errors such as missing file or unreadable content.
2. **Input Validation**:
   - Ensure the sequence contains only `(` and `)` characters.
   - Handle invalid input gracefully.
3. **Final Floor Calculation**:
   - Compute the difference between the counts of `(` and `)`:
     - `final_floor = count('(') - count(')')`.
4. **Output Handling**:
   - Print the calculated `final_floor` or an error message.

#### 1.2.2 Responsibility Domains
1. **File Input Reading**:
   - Handles reading from the input file.
2. **Sequence Analysis**:
   - Validates the sequence and computes the final floor.
3. **Output Handling**:
   - Prints the result or an appropriate error message.
4. **Orchestration**:
   - Manages argument parsing and the flow of computation.

#### 1.2.3 Module Breakdown
1. `fileinputhandler`:
   - **Responsibility**: Reads input from the file.
   - **Approach**: Functional.
   - **Justification**: File reading is straightforward and stateless.
2. `floordirections`:
   - **Responsibility**: Analyzes the `directions` sequence.
   - **Approach**: Object-oriented.
   - **Justification**: Encapsulation of sequence properties and methods (e.g., validation, floor computation) improves modularity and reusability.
3. `outputhandler`:
   - **Responsibility**: Manages result or error output.
   - **Approach**: Functional.
   - **Justification**: Simple, stateless operation suited for functional design.
4. `floorfinder`:
   - **Responsibility**: Orchestrates the solution flow.
   - **Approach**: Functional with support from `ArgumentParser`.
   - **Justification**: Argument parsing integrates seamlessly with a functional flow for orchestrating other modules.

### 1.3 Implementation Considerations
1. **Error Handling**:
   - File reading errors (e.g., missing file) should result in a clear, user-friendly message.
   - Invalid input sequences should return an error specifying the issue.
2. **Performance**:
   - Input size is assumed to be small (single line). Performance concerns are minimal.
3. **Maintainability**:
   - Clearly defined module responsibilities improve code clarity and ease of updates.

### 1.4 Summary
This solution design ensures modularity, clarity, and maintainability. The division of responsibilities into functional and object-oriented modules helps encapsulate logic while keeping the codebase organized and extensible.

## Part 2
### 2.1 Requirements Analysis
#### 2.1.1 Problem Statement
Given the same sequence of `directions` as before, the task is to find the **position** of the first instruction that causes the total floor to reach `-1` (the first basement floor). If no such position exists, the result should explicitly indicate this.

#### 2.1.2 Inputs (Unchanged)
- **Input format**: A file containing a single line of `directions`.
  - **Constraints**:
    - File must exist and be readable.
    - The sequence may only contain `(` and `)` characters.

#### 2.1.3 Outputs
- **Output format**: A single positive integer representing the **position** of the first instruction that leads to floor `-1`.
  - **Constraints**:
    - Position is indexed from `1` (the first character in a sequence has position `1`). Therefore, if such a position exists, it is a **positive integer**.
    - If no such position exists, indicate this with a `0`, which should be translated to an appropriate message.

#### 2.1.4 Edge Cases
1. **Empty Input**: Return `0` as no directions exist.
2. **Only `(` in the sequence**: Return `0`, as the basement is never reached.
3. **Only `)` in the sequence**: Return `1`, as the basement is reached on the first instruction.
4. **Basement not reached at all**: Return `0`.
5. **Basement reached at the last instruction**: Return the length of the sequence.

### 2.2 Design
#### 2.2.1 Solution Steps
1. **File Reading**: As before.
2. **Input Validation**: As before.
3. **First Basement Instruction Calculation**:
   - Traverse the sequence while maintaining a running total of the `current_floor` as well as the `position` of each character, starting from `1`.
   - When `current_floor` reaches `-1`, immediately return the current `position`.
   - If no such position exists, return `0`.

4. **Output Handling**:
   - Add `first_basement_instruction` to the result output, everything else is as before.

#### 2.2.2 Responsibility Domains
1. **File Input Reading**: As before.
2. **Sequence Analysis**:
   - Incorporates basement detection into the validation and floor computation process.
3. **Output Handling**: As before.
4. **Orchestration**:
   - Additionally ensures printing of the newly computed measure.

### 2.3 Implementation Considerations
1. **Multiple Passes Over Data**:
   - The current solution processes the `directions` sequence twice:
     - Once for validation.
     - Again to compute the `final_floor`.
   - These operations could be combined into a single pass, even with the `first_basement_instruction` calculation included.
     - While this optimization doesn't change the overall asymptotic complexity, it reduces the constant factor in the linear complexity: from `c*n` (when the passes are separate) to `(c-2)*n`.
     - Considering the size of the inputs, as well as readability concerns, this seems like more of an over-engineered solution than a practical improvement. It is likely not justified, and will not be included in the addition.

### 2.4 Summary
The design integrates basement detection into the solution with minimal changes to the existing flow. It prioritizes readability and maintainability over maximal optimization, while keeping the asymptotic complexity linear.

---

**License**: This document is licensed under the **MIT License**. See the `LICENSE` file in the project root for full license details.
