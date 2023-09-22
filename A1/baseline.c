
#define N  100000000
#define NUM_THREAD 2
#define NUM_TASKS 2

#include <stdio.h>
#include <time.h>

int main(){
    clock_t start,end;
    clock_t cpu_time_used;
    start = clock();
    long long sum = 0;
    for(long long i = 0; i < N; i++){
        sum += i;
    }

    end = clock();
    cpu_time_used = end - start;
    double cpu_seconds = (double)cpu_time_used/CLOCKS_PER_SEC;

    printf("Total sum from 0 to %lld is: %lld\n",N,sum);
    printf("Total CPU time taken in seconds: %.15f\n",cpu_seconds);

    return 0;
}