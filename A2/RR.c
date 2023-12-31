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
void myfunction(int param){

	int i = 2;
	int j, k;

	while(i < param){
		k = i; 
		for (j = 2; j <= k; j++)
		{
			if (k % j == 0){
				k = k/j;
				j--;
				if (k == 1){
					break;
				}
			}
		}
		i++;
	}
}
/************************************************************************************************/

int main(int argc, char const *argv[])
{
	pid_t pid1, pid2, pid3, pid4;
	int running1, running2, running3, running4;

	pid1 = fork();

	if (pid1 == 0){

		myfunction(WORKLOAD1);

		exit(0);
	}
	kill(pid1, SIGSTOP);

	pid2 = fork();

	if (pid2 == 0){

		myfunction(WORKLOAD2);

		exit(0);
	}
	kill(pid2, SIGSTOP);

	pid3 = fork();

	if (pid3 == 0){

		myfunction(WORKLOAD3);

		exit(0);
	}
	kill(pid3, SIGSTOP);

	pid4 = fork();

	if (pid4 == 0){

		myfunction(WORKLOAD4);

		exit(0);
	}
	kill(pid4, SIGSTOP);

	/************************************************************************************************ 
		At this point, all  newly-created child processes are stopped, and ready for scheduling.
	*************************************************************************************************/



	/************************************************************************************************
		- Scheduling code starts here
		- Below is a sample schedule. (which scheduling algorithm is this?)
		- For the assignment purposes, you have to replace this part with the other scheduling methods 
		to be implemented.
	************************************************************************************************/
	
    struct timespec context_switch_time = {0, 0};

    int execution_times[] = {WORKLOAD1, WORKLOAD2, WORKLOAD3, WORKLOAD4};
    int response_times[] = {0, 0, 0, 0};
    int NUM_PROCESSES = 4;
    struct timespec start_times[NUM_PROCESSES], end_time;

    printf("Executing test with QUANTUM1: %d, QUANTUM2: %d, QUANTUM3: %d, QUANTUM4: %d.\n", QUANTUM1, QUANTUM2, QUANTUM3, QUANTUM4);

    // Round-Robin scheduling
    running1 = 1;
    running2 = 1;
    running3 = 1;
    running4 = 1;

    while (running1 > 0 || running2 > 0 || running3 > 0 || running4 > 0) {
        if (running1 > 0) {
            struct timespec start_context_switch, end_context_switch;
            clock_gettime(CLOCK_MONOTONIC, &start_context_switch);
            kill(pid1, SIGCONT);
            usleep(QUANTUM1);
            kill(pid1, SIGSTOP);
            clock_gettime(CLOCK_MONOTONIC, &end_context_switch);
            long context_switch_ns = (end_context_switch.tv_sec - start_context_switch.tv_sec) * 1000000000 + (end_context_switch.tv_nsec - start_context_switch.tv_nsec);
            context_switch_time.tv_sec += context_switch_ns / 1000000000;
            context_switch_time.tv_nsec += context_switch_ns % 1000000000;

            clock_gettime(CLOCK_MONOTONIC, &start_times[0]);
            kill(pid1, SIGCONT);
            usleep(QUANTUM1);
            kill(pid1, SIGSTOP);
            clock_gettime(CLOCK_MONOTONIC, &end_time);
            response_times[0] += (end_time.tv_sec - start_times[0].tv_sec) * 1000000 + (end_time.tv_nsec - start_times[0].tv_nsec) / 1000;
        }

        if (running2 > 0) {
            struct timespec start_context_switch, end_context_switch;
            clock_gettime(CLOCK_MONOTONIC, &start_context_switch);
            kill(pid2, SIGCONT);
            usleep(QUANTUM2);
            kill(pid2, SIGSTOP);
            clock_gettime(CLOCK_MONOTONIC, &end_context_switch);
            long context_switch_ns = (end_context_switch.tv_sec - start_context_switch.tv_sec) * 1000000000 + (end_context_switch.tv_nsec - start_context_switch.tv_nsec);
            context_switch_time.tv_sec += context_switch_ns / 1000000000;
            context_switch_time.tv_nsec += context_switch_ns % 1000000000;

            clock_gettime(CLOCK_MONOTONIC, &start_times[1]);
            kill(pid2, SIGCONT);
            usleep(QUANTUM2);
            kill(pid2, SIGSTOP);
            clock_gettime(CLOCK_MONOTONIC, &end_time);
            response_times[1] += (end_time.tv_sec - start_times[1].tv_sec) * 1000000 + (end_time.tv_nsec - start_times[1].tv_nsec) / 1000;
        }

        if (running3 > 0) {
            struct timespec start_context_switch, end_context_switch;
            clock_gettime(CLOCK_MONOTONIC, &start_context_switch);
            kill(pid3, SIGCONT);
            usleep(QUANTUM3);
            kill(pid3, SIGSTOP);
            clock_gettime(CLOCK_MONOTONIC, &end_context_switch);
            long context_switch_ns = (end_context_switch.tv_sec - start_context_switch.tv_sec) * 1000000000 + (end_context_switch.tv_nsec - start_context_switch.tv_nsec);
            context_switch_time.tv_sec += context_switch_ns / 1000000000;
            context_switch_time.tv_nsec += context_switch_ns % 1000000000;

            clock_gettime(CLOCK_MONOTONIC, &start_times[2]);
            kill(pid3, SIGCONT);
            usleep(QUANTUM3);
            kill(pid3, SIGSTOP);
            clock_gettime(CLOCK_MONOTONIC, &end_time);
            response_times[2] += (end_time.tv_sec - start_times[2].tv_sec) * 1000000 + (end_time.tv_nsec - start_times[2].tv_nsec) / 1000;
        }

        if (running4 > 0) {
            struct timespec start_context_switch, end_context_switch;
            clock_gettime(CLOCK_MONOTONIC, &start_context_switch);
            kill(pid4, SIGCONT);
            usleep(QUANTUM4);
            kill(pid4, SIGSTOP);
            clock_gettime(CLOCK_MONOTONIC, &end_context_switch);
            long context_switch_ns = (end_context_switch.tv_sec - start_context_switch.tv_sec) * 1000000000 + (end_context_switch.tv_nsec - start_context_switch.tv_nsec);
            context_switch_time.tv_sec += context_switch_ns / 1000000000;
            context_switch_time.tv_nsec += context_switch_ns % 1000000000;

            clock_gettime(CLOCK_MONOTONIC, &start_times[3]);
            kill(pid4, SIGCONT);
            usleep(QUANTUM4);
            kill(pid4, SIGSTOP);
            clock_gettime(CLOCK_MONOTONIC, &end_time);
            response_times[3] += (end_time.tv_sec - start_times[3].tv_sec) * 1000000 + (end_time.tv_nsec - start_times[3].tv_nsec) / 1000;
        }

        // Check if processes are finished
        waitpid(pid1, &running1, WNOHANG);
        waitpid(pid2, &running2, WNOHANG);
        waitpid(pid3, &running3, WNOHANG);
        waitpid(pid4, &running4, WNOHANG);
    }

    // Calculate and print response times
    for (int i = 0; i < NUM_PROCESSES; i++) {
        printf("Process ID: %d, Execution Workload: %d, Response Time: %d microseconds\n", getpid(), execution_times[i], response_times[i]);
    }

    int total_response_time = 0;
    for (int i = 0; i < NUM_PROCESSES; i++) {
        total_response_time += response_times[i];
    }

    int average_response_time = total_response_time / NUM_PROCESSES;

    printf("Average Response Time: %d microseconds.\n", average_response_time);

    // Print total context switching time
    printf("Total Context Switching Time: %ld seconds %ld nanoseconds\n", context_switch_time.tv_sec, context_switch_time.tv_nsec);

    return 0;
}