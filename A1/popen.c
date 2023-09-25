#define N 100000000
#define NUM_TASKS 2

#include <stdio.h>
#include <sys/wait.h>
#include <unistd.h>
#include <stdlib.h>
#include <time.h>

int main(){
    clock_t start,end;
    clock_t cpu_time_used;
    
    start = clock();

    FILE *fp;
    long long sum = 0;
    for(int i = 0; i < NUM_TASKS; i++){
        
        long long current_sum = 0;
        long long start = (N/NUM_TASKS)*i;

        long long end = start + N/NUM_TASKS;

        char command[100];

        snprintf(command,sizeof(command), "./popen_adder %lld %lld",start,end);

        fp = popen(command,"r");
        if (fp == NULL){
            perror("popen");
            return 1;
        }


        if(fscanf(fp,"%lld",&current_sum) != 1){
            perror("fscanf");
            return 1;
        }

        sum += current_sum;

        pclose(fp);
        
        // printf("Task %d finished sums from %lld to %lld and got: %lld\n",i,start,end,current_sum);

    }

    end = clock();
    cpu_time_used = end - start;
    double cpu_seconds = (double)cpu_time_used/CLOCKS_PER_SEC;


    printf("Total sum from 0 to %lld is: %lld\n",N,sum);
    printf("Total CPU time taken in seconds: %.15f\n",cpu_seconds);

}