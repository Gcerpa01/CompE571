
#define N  100000000
#define NUM_THREAD 2
#define NUM_TASKS 2
#define NUM_RUNS 500

#include <stdio.h>
#include <time.h>

int main() {
    double timeTotal;

    for (int run = 1; run <= NUM_RUNS; run++) {
        clock_t start, end;
        clock_t cpu_time_used;

        start = clock();
        long long sum = 0;

        for (int i = 0; i < N; i++) {
            sum += i;
        }

        end = clock();

        
    double timeTook = ((double)(end - start)) / ((double)(CLOCKS_PER_SEC));
    timeTotal += timeTook;
    
    printf("Total sum from 0 to %d is: %lld\n",N,sum);
    printf("Total time taken by the program is : %f seconds\n", timeTook);
    }
    double averageTotalTime = timeTotal / NUM_RUNS;
    printf("Total average time taken by the program across 500 iterations is : %f seconds\n", averageTotalTime);
    return 0;
};