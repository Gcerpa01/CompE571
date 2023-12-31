#define _POSIX_C_SOURCE 200809L // Required for clock_gettime
#define N 100000000
#define NUM_TASKS 2

#include <stdio.h>
#include <sys/wait.h>
#include <unistd.h>
#include <stdlib.h>
#include <time.h>

int main(){
    struct timespec start,end;
    clock_gettime(CLOCK_MONOTONIC, &start);

    FILE *fp[NUM_TASKS];
    long long sum = 0;
    long long current_sum = 0;

    for(int i = 0; i < NUM_TASKS; i++){
        
        long long start = (N/NUM_TASKS)*i;

        long long end = start + N/NUM_TASKS;

        char command[100];

        snprintf(command,sizeof(command), "./popen_adder %lld %lld",start,end);

        fp[i] = popen(command,"r");
        if (fp == NULL){
            perror("popen");
            return 1;
        }

    }

    for(int i = 0; i < NUM_TASKS; i++){
        if(fscanf(fp[i],"%lld",&current_sum) != 1){
            perror("fscanf");
            return 1;
        }

        sum += current_sum;

        pclose(fp[i]);
        
        // printf("Task %d finished sums from %lld to %lld and got: %lld\n",i,start,end,current_sum);

    }

    clock_gettime(CLOCK_MONOTONIC, &end);

    double cpu_seconds = (end.tv_sec - start.tv_sec) + (end.tv_nsec - start.tv_nsec) / 1e9;

    printf("Total sum from 0 to %lld is: %lld\n",N,sum);
    printf("Total CPU time taken in seconds: %.15f\n",cpu_seconds);

}