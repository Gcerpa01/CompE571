--------------------------------------------------
SDSU COMPE-571 - Fall Session 
Assignment #1: Sequential vs Multithreading vs Multitasking Programming

Group members:
Richard Marmito (822132643)
Jarrod Rowson (826453843)
Gerardo Cerpa (819144749)

Filename (of this file): README.txt
--------------------------------------------------
===== README =====
File manifest:
- baseline.c
- multithreading.c
- multitasking.c
- popen.c
- popen_adder.c
- makefile
- run_times.sh


Compile instructions:
- Manually Compiling:
    - use "gcc -std -w -o baseline baseline.c" to compile to baseline executable file
    - use "gcc -std -w -o multithreading multithreading.c" to compile to multithreading object file
    - use "gcc -std -w -o multitasking multitasking.c" to compile to multitasking executable file
    - use "gcc -std -w -o popen popen.c" to compile to popen executable file
    - use "gcc -std -w -o popen_adder popen_adder.c" to compile to popen_adder executable file

- Compile using Makefile:
    - use "make" for the makefile to create the executable files for all scenarios

- Manually Cleaning:
    - use "rm -f *.txt multitasking baseline multithreading popen popen_adder" to remove object files and executable files
    
- Clean using Makefile
    - use "make clean" to remove object files, executable files and text files created from the script
    - use "make clean_txt" to remove text files created from the script


Operating instructions:
- Operating instructions for individual executable files:
    - Compile files 
    - Using the command line, run the desired executable file by running "./{file_name}"
    - The program will then output the sum to N macro within the source code using the associated necessary macros
    - Important Note: 
        - To run popen_adder on its own, run the executable file by running "./popen_adder {int} {int} " for it to return the sum of all values between the two points

Operating instructions via script:
    - Compile files
    - To execute all files N number of times, modify the count variable in run_times.sh to the desired quantity for each executable file to be ran
    - Using the command line, run "./run_times.sh"
    - The program will then output the average time it takes for the executable file to complete as well as over the standard deviation of completion over N number of times
    - Important Note: 
        - All executable file outputs will be saved to "{executable_file_name}_times.txt" if you desire to review the output
        - If you wish to modify the threads,tasks, and number the executable files are counting up to, you will have to modify the associated macros in each respective source file

Novel/significant design decisions:
- For this assignment, given that we had 3 people in our group, we opted to implement both methods of multitasking, via fork() in "multitasking.c" and popen() in "popen.c"

Extras:
- Originally we were modifiying the code to run N times in order to calculate the average time it took for each case to run,
after consideration and research we decided to create a shell script, "run_times.sh" in order to save the outputs to txt files and output
the average times and standard deviation as well 

Deficiencies/bugs:
- At the time of writing this, no deficiencies nor bugs in our program are apparent.