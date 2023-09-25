#define _POSIX_C_SOURCE 200809L // Required for clock_gettime
#define N  100000000
#define NUM_THREAD 2
#define NUM_TASKS 2

#include <stdio.h>
#include <time.h>

int main(){
    struct timespec start,end;
    clock_gettime(CLOCK_MONOTONIC, &start);

    long long sum = 0;
    for(long long i = 0; i < N; i++){
        sum += i;
    }

    clock_gettime(CLOCK_MONOTONIC, &end);

    double cpu_seconds = (end.tv_sec - start.tv_sec) + (end.tv_nsec - start.tv_nsec) / 1e9;

    printf("Total sum from 0 to %lld is: %lld\n",N,sum);
    printf("Total CPU time taken in seconds: %.15f\n",cpu_seconds);

    return 0;
}