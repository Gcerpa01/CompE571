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

    pid_t processes[] = {pid1, pid2, pid3, pid4};
	int runners[] = {running1, running2, running3, running4};
	double execution_times[] = {WORKLOAD1, WORKLOAD2, WORKLOAD3, WORKLOAD4};
	int NUM_PROCESSES = 4;
	double response_times[] = {0, 0, 0, 0};
	double total_response_time = 0;



	struct timespec 
		start_times,
		end_times[NUM_PROCESSES];
	
	// iniiate process readiness for scheduler
	running1 = 1;
	running2 = 1;
	running3 = 1;
	running4 = 1;


	int total_execution_time = 0;

	// initiate timer for all processes
	clock_gettime(CLOCK_MONOTONIC, &start_times);

	for (int i = 0; i < NUM_PROCESSES; i++) {

		kill(processes[i], SIGCONT);
		waitpid(processes[i], &runners[i],0);
	
		// clocking execution/response time for each process
		clock_gettime(CLOCK_MONOTONIC, &end_times[i]);
		if (i==0) {
			response_times[0] = (end_times[0].tv_nsec);
		} 
		else if (i >0) {
			response_times[i] = (end_times[i].tv_nsec - start_times.tv_nsec);
			total_response_time += response_times[i];
		}

	printf("Process ID: %d, Execution Workload: %f, Response Time: %f nanoseconds\n", processes[i], execution_times[i], response_times[i]);

    }

    double average_response_time = total_response_time / NUM_PROCESSES;
    printf("Average Response Time: %f nanoseconds\n", average_response_time);

	printf("total execution time: %f\n", total_response_time);
	return 0;   
}
	/************************************************************************************************
		- Scheduling code ends here
	************************************************************************************************/