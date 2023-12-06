# Programming Assignment 4 - COMPE 571

This Python script is designed to simulate virtual memory management using various page replacement algorithms. Virtual memory management is a crucial part of operating systems, allowing multiple processes to run concurrently in a system with limited physical memory. The script reads a memory input data file, simulates the memory management process, and reports key metrics such as page faults, disk references, and dirty page writes.

This simulation is meant to support a virtual address space of 64KB, organized with 1-level page tables, while the physical memory consists of 32 pages. Five algorithms have been developed which includes: Random, FIFO, LRU, PER, and a custom algorithm built by the team in order to show how we can outperform the previous four algorithms.

## Table of Contents
- [Supported Page Replacement Algorithms](#supported-page-replacement-algorithms)
- [How to Use](#how-to-use)
- [Examples](#examples)
- [Results](#results)

## Supported Page Replacement Algorithms

This script supports the following page replacement algorithms:

1. **Random Replacement (`random`)**: The victim (i.e., the page to be replaced) is selected in random.

2. **FIFO Replacement (`fifo`)**: The oldest page in the memory gets replaced.

3. **LRU Replacement (`lru`)**: The least recently used page in the memory gets replaced. If there are two pages with the same value (the last used time unit), replace the one that is not dirty. If both pages are or neither page is dirty, replace the lower numbered paged.

4. **PER Replacement (`per`)**: Whenever a page is referenced, its reference bit is set to 1. After every 200 memory references, your program should set all of the reference bits to 0. When a page fault occurs choose a page to be replaced in the specified order:

        - Look for an unused page (this will only happen early in your simulation).
        - Look for an unreferenced page (reference bit is 0) where the dirty bit is 0.
        - Look for an unreferenced page (reference bit is 0) where the dirty bit is 1.
        - Look for a referenced page (reference bit is 1) where the dirty bit is 0.
        - Look for a page that is both referenced (reference bit is 1) and dirty (dirty bit is 1).
        - In order to make the results deterministic, always replace the lowest numbered page in a particular category.

5. **Extra Replacement (`extra`)**: The team's own replacement algorithm which is used to outperform the above four in terms of number of page faults, number of dirty page writes, and number of disk accesses.

## How to Use

To use this Python script, follow these steps:

1. Ensure you have Python 3.X installed on your system.

2. Open your terminal or command prompt.

3. Run the script with the following command:

   ```shell
   python <program_name> <data_file> <algorithm>
   ```

   - Replace '<program_name>' with the Python file name.
   - Replase '<data_file>' with the data file to be used for simulation.
   - Replace '<algorithm>' with the algorithm to process.

## Examples

- **Random Replacement Algorithm:**
    ```shell
    python pa4.py data1.txt random
    ```

## Results
- **Expected results for each algorithm simulation:**
    - Total page faults: The number of page faults that occurred during the simulation.
    - Total disk references: The total number of memory accesses that required disk I/O.
    - Total dirty page writes: The number of memory writes that resulted in disk writes.
