# COMPE571 – Embedded Operating Systems – Fall 2023
## Programming Assignment 3 - Real-Time Task Scheduling with DVFS

## Assignment Description

This programming assignment involves creating real-time task schedules along with DVFS (Dynamic Voltage and Frequency Scaling) settings for each task. This assignment is designated to be completed using the Python scripting language.

The script(s) will process an input text file containing a list of tasks to be executed, their deadlines, and generate an output listing a sequence of scheduling decisions based on four different scheduling policies: EDF (Earliest Deadline First), RM (Rate-Monotonic), Energy-Efficient (EE) EDF, and EE RM.

## Command Line Usage

To use the program, follow these command line arguments:

- `<input_file_name>`: Replace this with the path to your input text file.
- `<EDF or RM>`: Choose either "EDF" (Earliest Deadline First) or "RM" (Rate-Monotonic) as the scheduling strategy.
- `[EE]`: This argument is optional. If included, it stands for energy efficiency (EE).

Here are two example calls:

$ ./python main.py input1.txt EDF EE
$ ./python main.py input2.txt RM

## Input Format

The input file format is as follows:

<# of tasks> <system execution time in seconds>
<active CPU power @ 1188 Mhz> <active CPU power @ 918 Mhz> <active CPU power @ 648 Mhz> <active CPU power @ 384 Mhz> <idle CPU power @ lowest frequency>
<name of task> <deadline/period> <WCET @ 1188 Mhz> <WCET @ 918 Mhz> <WCET @ 648 Mhz> <WCET @ 384 Mhz>

- `<# of tasks>`: Number of tasks.
- `<system execution time in seconds>`: The time the system will execute up to in seconds.
- `<active CPU power>`: Power settings for the active CPU at different frequencies (in mW).
- `<idle CPU power>`: Power consumed by CPU at the lowest frequency (in mW).

## Scheduling Algorithms

The program will generate scheduling sequences based on the following four algorithms:

1. EDF: Earliest deadline first when all tasks run at maximum CPU frequency.
2. RM: Rate-Monotonic when all tasks run at maximum CPU frequency.
3. EE EDF: The scheduler adjusts CPU frequency to be as low as possible while still meeting deadlines and ensuring tasks are scheduled in order as defined by EDF policy.
4. EE RM: The scheduler adjusts CPU frequency to be as low as possible while still meeting deadlines and ensuring tasks are scheduled in order as defined by RM policy.

## Output Format

When a task is scheduled, it will output the following information:

<time started> <task name> <CPU frequency task runs at> <how long it ran for> <energy consumed in Joules>