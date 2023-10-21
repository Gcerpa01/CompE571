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

#define WORKLOAD1 10000
#define WORKLOAD2 10000
#define WORKLOAD3 10000
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
    printf("Scheduling code starts\n");

    int level1 = 1, level2 = 1, level3 = 1, level4 = 1; // Flags to indicate which level a process is in

    pid_t processes[] = {pid1, pid2, pid3, pid4};
	int runners[] = {running1, running2, running3, running4};
    int NUM_PROCESSES = 4;
    unsigned long long int execution_times[] = {WORKLOAD1, WORKLOAD2, WORKLOAD3, WORKLOAD4};
	unsigned long long int response_times[] = {0, 0, 0, 0};
	unsigned long long int total_response_time = 0;

    while (running1 > 0 || running2 > 0 || running3 > 0 || running4 > 0)
    {
        printf("Checking queues\n");

	struct timespec 
		start_times,
		end_times[NUM_PROCESSES];

	// iniitalize runners
	running1 = 1;
	running2 = 1;
	running3 = 1;
	running4 = 1;

	// start initial timer for all processes
	clock_gettime(CLOCK_MONOTONIC, &start_times);

    for (int i = 0; i < NUM_PROCESSES; i++) {

		// initiate RR with QUANTUM constraints
        while (running1 > 0 || running2 > 0 || running3 > 0 || running4 > 0) {

            if (running1 > 0){
                kill(pid1, SIGCONT);
                usleep(QUANTUM1);
                kill(pid1, SIGSTOP);

            }
            if (running2 > 0){
                kill(pid2, SIGCONT);
                usleep(QUANTUM2);
                kill(pid2, SIGSTOP);

            }
            if (running3 > 0){
                kill(pid3, SIGCONT);
                usleep(QUANTUM3);
                kill(pid3, SIGSTOP);
            }
            if (running4 > 0){
                kill(pid4, SIGCONT);
                usleep(QUANTUM4);
                kill(pid4, SIGSTOP);
            }
			break;
	}


	// fcfs for each process
	kill(processes[i], SIGCONT);
	waitpid(processes[i], &runners[i],0);

	
	// clocking execution/response time for each process
	clock_gettime(CLOCK_MONOTONIC, &end_times[i]);
	response_times[i] = (end_times[i].tv_nsec - start_times.tv_nsec) * 1000000 + (end_times[i].tv_nsec - start_times.tv_nsec) / 1000;
	total_response_time += response_times[i];


	printf("Process ID: %d, Execution Workload: %llu, Response Time: %llu microseconds\n", processes[i], execution_times[i], response_times[i]);


	}
	// total average turn around time calculation
	unsigned long int average_response_time = total_response_time / NUM_PROCESSES;
    printf("Average Response Time: %lu microseconds\n", average_response_time);

	/************************************************************************************************
		- Scheduling code ends here
	************************************************************************************************/

	return 0;
	}
}
