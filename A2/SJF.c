#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>
#include <stdlib.h>
#include <sys/wait.h>
#include <string.h>
#include <time.h>
#include <signal.h>
#include <sys/time.h>

/************************************************************************************************ 
	These DEFINE statements represent the workload size of each task and 
	the time quantum values for Round Robin scheduling for each task.
*************************************************************************************************/

#define WORKLOAD1 100000
#define WORKLOAD2 50000
#define WORKLOAD3 25000
#define WORKLOAD4 10000

#define QUANTUM1 1000
#define QUANTUM2 1000
#define QUANTUM3 1000
#define QUANTUM4 1000

/************************************************************************************************ 
	DO NOT CHANGE THE FUNCTION IMPLEMENTATION
*************************************************************************************************/
void myfunction(int param) {
    int i = 2;
    int j, k;

    while (i < param) {
        k = i;
        for (j = 2; j <= k; j++) {
            if (k % j == 0) {
                k = k / j;
                j--;
                if (k == 1) {
                    break;
                }
            }
        }
        i++;
    }
}
/************************************************************************************************/

int main(int argc, char const *argv[]) {
    pid_t pid1, pid2, pid3, pid4;
    int running1, running2, running3, running4;

    pid1 = fork();

    if (pid1 == 0) {
        myfunction(WORKLOAD1);
        exit(0);
    }
    kill(pid1, SIGSTOP);

    pid2 = fork();

    if (pid2 == 0) {
        myfunction(WORKLOAD2);
        exit(0);
    }
    kill(pid2, SIGSTOP);

    pid3 = fork();

    if (pid3 == 0) {
        myfunction(WORKLOAD3);
        exit(0);
    }
    kill(pid3, SIGSTOP);

    pid4 = fork();

    if (pid4 == 0) {
        myfunction(WORKLOAD4);
        exit(0);
    }
    kill(pid4, SIGSTOP);

    /************************************************************************************************ 
        At this point, all newly-created child processes are stopped and ready for scheduling.
    *************************************************************************************************/

    /************************************************************************************************
        - Scheduling code starts here
    ************************************************************************************************/

    int execution_times[] = {WORKLOAD1, WORKLOAD2, WORKLOAD3, WORKLOAD4};
    pid_t processes[] = {pid1, pid2, pid3, pid4};
    int response_times[] = {0, 0, 0, 0};
    int NUM_PROCESSES = 4;

    struct timespec start_times[NUM_PROCESSES], end_time;

    // Create a variable to keep track of the total context switching time
    struct timespec context_switch_time = {0, 0};

    // Sort processes based on execution times (SJF)
    for (int i = 0; i < NUM_PROCESSES - 1; i++) {
        for (int j = 0; j < NUM_PROCESSES - i - 1; j++) {
            if (execution_times[j] > execution_times[j + 1]) {
                // Swap execution times
                int temp = execution_times[j];
                execution_times[j] = execution_times[j + 1];
                execution_times[j + 1] = temp;
                // Swap corresponding processes
                pid_t temp_pid = processes[j];
                processes[j] = processes[j + 1];
                processes[j + 1] = temp_pid;
            }
        }
    }

    // Start and resume processes in SJF order and calculate response time
    for (int i = 0; i < NUM_PROCESSES; i++) {
        // Record the start time for context switching measurement
        clock_gettime(CLOCK_MONOTONIC, &start_times[i]);

        // Send SIGCONT signal to start the process
        kill(processes[i], SIGCONT);
        // Wait for the child process to finish
        wait(NULL);

        // Record the end time for context switching measurement
        clock_gettime(CLOCK_MONOTONIC, &end_time);

        // Calculate the context switching time and add it to the total
        long context_switch_ns = (end_time.tv_sec - start_times[i].tv_sec) * 1000000000 + (end_time.tv_nsec - start_times[i].tv_nsec);
        context_switch_time.tv_sec += context_switch_ns / 1000000000;
        context_switch_time.tv_nsec += context_switch_ns % 1000000000;

        // Calculate and store the response time
        response_times[i] = (end_time.tv_sec - start_times[i].tv_sec) * 1000000 + (end_time.tv_nsec - start_times[i].tv_nsec) / 1000;
        printf("Process ID: %d, Execution Workload: %d, Response Time: %ld microseconds\n", processes[i], execution_times[i], response_times[i]);
    }

    // Calculate and print average response time
    int total_response_time = 0;
    for (int i = 0; i < NUM_PROCESSES; i++) {
        total_response_time += response_times[i];
    }
    int average_response_time = total_response_time / NUM_PROCESSES;
    printf("Average Response Time: %d microseconds\n", average_response_time);

    // Print total context switching time
    printf("Total Context Switching Time: %ld seconds %ld nanoseconds\n", context_switch_time.tv_sec, context_switch_time.tv_nsec);

    /************************************************************************************************
        - Scheduling code ends here
    ************************************************************************************************/

    return 0;
}
