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
    printf("Scheduling code starts\n");

    int level1 = 1, level2 = 1, level3 = 1, level4 = 1; // Flags to indicate which level a process is in

    running1 = 1;
    running2 = 1;
    running3 = 1;
    running4 = 1;

    while (running1 > 0 || running2 > 0 || running3 > 0 || running4 > 0)
    {
        printf("Checking queues\n");

        // Round-Robin queue (First Level)
        if (level1 && running1 > 0){
            printf("Round-Robin, First Level: Process 1\n");
            kill(pid1, SIGCONT);
            usleep(QUANTUM1);
            kill(pid1, SIGSTOP);
            level1 = 0; // Move to FCFS queue (Second Level)
        }
        if (level2 && running2 > 0){
            printf("Round-Robin, First Level: Process 2\n");
            kill(pid2, SIGCONT);
            usleep(QUANTUM2);
            kill(pid2, SIGSTOP);
            level2 = 0; // Move to FCFS queue (Second Level)
        }
        if (level3 && running3 > 0){
            printf("Round-Robin, First Level: Process 3\n");
            kill(pid3, SIGCONT);
            usleep(QUANTUM3);
            kill(pid3, SIGSTOP);
            level3 = 0; // Move to FCFS queue (Second Level)
        }
        if (level4 && running4 > 0){
            printf("Round-Robin, First Level: Process 4\n");
            kill(pid4, SIGCONT);
            usleep(QUANTUM4);
            kill(pid4, SIGSTOP);
            level4 = 0; // Move to FCFS queue (Second Level)
        }

        // FCFS queue (Second Level)
        if (!level1 && running1 > 0){
            printf("FCFS, Second Level: Process 1\n");
            kill(pid1, SIGCONT);
            usleep(QUANTUM1);
            kill(pid1, SIGSTOP);
        }
        if (!level2 && running2 > 0){
            printf("FCFS, Second Level: Process 2\n");
            kill(pid2, SIGCONT);
            usleep(QUANTUM2);
            kill(pid2, SIGSTOP);
        }
        if (!level3 && running3 > 0){
            printf("FCFS, Second Level: Process 3\n");
            kill(pid3, SIGCONT);
            usleep(QUANTUM3);
            kill(pid3, SIGSTOP);
        }
        if (!level4 && running4 > 0){
            printf("FCFS, Second Level: Process 4\n");
            kill(pid4, SIGCONT);
            usleep(QUANTUM4);
            kill(pid4, SIGSTOP);
        }

        printf("Checking if processes are still running\n");
        waitpid(pid1, &running1, WNOHANG);
        waitpid(pid2, &running2, WNOHANG);
        waitpid(pid3, &running3, WNOHANG);
        waitpid(pid4, &running4, WNOHANG);
    }

    printf("Scheduling code ends\n");
    /************************************************************************************************
        - Scheduling code ends here
    ************************************************************************************************/


    return 0;
}