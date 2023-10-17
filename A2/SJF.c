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
	************************************************************************************************/

    int execution_times[] = {WORKLOAD1, WORKLOAD2, WORKLOAD3, WORKLOAD4};
    pid_t processes[] = {pid1, pid2, pid3, pid4};
    int response_times[] = {0, 0, 0, 0};
    int num_processes = 4;

    struct timeval start_times[num_processes];

    // Sort processes based on execution times (SJF)
    for (int i = 0; i < num_processes - 1; i++) {
        for (int j = 0; j < num_processes - i - 1; j++) {
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
    for (int i = 0; i < num_processes; i++) {
        gettimeofday(&start_times[i], NULL); // Record the start time
        kill(processes[i], SIGCONT);
        wait(NULL); // Wait for the child process to finish
        struct timeval end_time;
        gettimeofday(&end_time, NULL);
        response_times[i] = (end_time.tv_sec - start_times[i].tv_sec) * 1000000 + (end_time.tv_usec - start_times[i].tv_usec);
        printf("Process ID: %d, Execution Workload: %d, Response Time: %ld microseconds\n", processes[i], execution_times[i], response_times[i]);
    }

    // Now take the response times and average them
    int total_response_time = 0;
    for (int i = 0; i < num_processes; i++) {
        total_response_time += response_times[i];
    }
    int average_response_time = total_response_time / num_processes;
    printf("Average Response Time: %d microseconds\n", average_response_time);
	
	/************************************************************************************************
		- Scheduling code ends here
	************************************************************************************************/

	return 0;
}