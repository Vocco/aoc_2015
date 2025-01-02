<!-- SPDX-License-Identifier: MIT -->
<!-- Copyright (c) Vojtech Krajnansky -->
# Solution Design: Advent of Code 2015: Day 02
## Part 1
### 1.1 Requirements Analysis
#### 1.1.1 Problem Statement
Given a list of `dimensions` of presents (perfect right rectangular prisms) in the format `LxWxH`, where `L` is the length, `W` the width, and `H` the height of the present, calculate the amount of wrapping paper needed for wrap all presents, given by the formula: `2*L*W + 2*W*H + 2*H*L + min(L*W, W*H, H*L)`, where:
- `2*L*W + 2*W*H + 2*H*L` is the surface area of the present
- `min(L*W, W*H, H*L)` (the area of the smallest side) is slack for the wrapping

#### 1.1.2 Inputs
- **Input format**: A file containing 1 line per present describing the present's dimensions in feet.
  - **Constraints**:
    - File must exist and be readable.
    - Each line has the format: `LxWxH`, where `L`, `W`, and `H` are all string representations of a **positive integer**.

#### 1.1.3 Outputs
- **Output format**: A single integer representing the **total square feet of wrapping paper needed**.

#### 1.1.4 Edge Cases
1. **Empty input**: Return `0`.
2. **Single line** in the file: Return `2*(L*W + W*H + H*L) + min(L*W, W*H, H*L)`.
3. **Minimal Present**: For a present of dimensions `1x1x1`, return a `wrapping_paper` area of: `7`.
4. **Skewed Present**: For a present of dimensions `1x8000x1`, return a `wrapping_paper` area of: `32003`.

### 1.2 Design
#### 1.2.1 Solution Steps
1. **File Reading**:
   - Read the file containing `dimensions`.
   - Handle errors such as missing file or unreadable content.
2. **Input Validation**:
   - Ensure each line is in the format `LxWxH`, where:
     - `L`, `W`, and `H` can all be parsed into integers.
     - `L`, `W`, and `H` are all larger than `0`.
   - Handle invalid input gracefully.
3. **Tracking of Present Dimensions**:
   - For each present, track its:
     - `side_areas` = `[L*W, W*H, H*L]`, sorted by size
     - `surface_area` = `2*(side_areas)`
3. **Total Wrapping Paper Amount Calculation**:
   - Compute the sum of all `wrapping_paper` integers, defined as:
     - `wrapping_paper` = `present.side_areas[0] + present.surface_area`
4. **Output Handling**:
   - Print the calculated `total_paper_area` or an error message.

#### 1.2.2 Responsibility Domains
1. **File Input Reading**:
   - Handles reading from the input file.
2. **Present Dimensions Representation**:
   - Represents a Christmas present's dimensions.
   - Provides a method to instantiate from a string description, including validation.
   - Provides methods to compute the surface area and side areas of the present.
3. **Wrapping Analysis**:
   - Handles analysis of the wrapping paper requirements.
   - Provides a method to compute an amount of wrapping paper necessary for a single present.
   - Provides a method to compute the summary amount of paper necessary for a collection of presents.
3. **Output Handling**:
   - Prints the result or an appropriate error message.
4. **Orchestration**:
   - Manages argument parsing and the flow of computation.

#### 1.2.3 Module Breakdown
1. `fileinputhandler`:
   - **Responsibility**: Reads input from the file.
   - **Notes**: Reused from `floorfinder` solution.
2. `presentdimensions`:
   - **Responsibility**: Represents and handles `dimensions` data.
   - **Approach**: Object-oriented.
   - **Justification**: Encapsulation of present properties and methods (e.g., validation, area computation) improves modularity and reusability.
3. `wrappinganalysis`:
   - **Responsibility**: Computes the amount of wrapping paper necessary to wrap the presents.
   - **Approach**: Object-oriented.
   - **Justification**: Enables easy extensibility if additional metrics need to be computed for a collection of presents.
3. `outputhandler`:
   - **Responsibility**: Manages result or error output.
   - **Notes**: Reused from `floorfinder` solution.
4. `wrappingordercalc`:
   - **Responsibility**: Orchestrates the solution flow.
   - **Approach**: Functional with support from `ArgumentParser`.
   - **Justification**: Argument parsing integrates seamlessly with a functional flow for orchestrating other modules.

### 1.3 Implementation Considerations
1. **Error Handling**:
   - File reading errors (e.g., missing file) should result in a clear, user-friendly message.
   - Invalid input sequences should return an error specifying the issue.
2. **Performance**:
   - Input size is assumed to be small (thousands of presents). Performance concerns are minimal.
3. **Maintainability**:
   - Clearly defined module responsibilities improve code clarity and ease of updates.

### 1.4 Summary
This solution design ensures modularity, clarity, and maintainability. The division of responsibilities into functional and object-oriented modules helps encapsulate logic while keeping the codebase organized and extensible.

---

**License**: This document is licensed under the **MIT License**. See the `LICENSE` file in the project root for full license details.
