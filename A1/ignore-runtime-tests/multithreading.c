#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <time.h>

#define N 1000000000
#define NUM_THREADS 4
#define NUM_RUNS 500

// struct
struct ThreadData {
    int threadID;
    int start;
    int end;
    long long sum;
};

// function for calculating the sum of the numbers given
void* calculateSum(void* arg) {
    struct ThreadData* data = (struct ThreadData*)arg;
    long long sum = 0;
    for (int i = data->start; i < data->end; i++) {
        sum += i;
    }
    data->sum = sum;

    //printf("Thread %d: Calculated sum from %d to %d: %lld\n",
    //       data->threadID, data->start, data->end, data->sum);

    pthread_exit(NULL);
}

int main() {
    // Create the thread array
    pthread_t threads[NUM_THREADS];

    clock_t start, end;
    double timeTotal = 0.0;

    // We divide the work among the threads now
    struct ThreadData threadData[NUM_THREADS];
    int chunkSize = N / NUM_THREADS;
    for (int i = 0; i < NUM_THREADS; i++) {
        threadData[i].threadID = i;
        threadData[i].start = i * chunkSize;
        threadData[i].end = (i + 1) * chunkSize;
    }

    for (int run = 1; run <= NUM_RUNS; run++){
        start = clock();
        
        // Create and start the threads
        for (int i = 0; i < NUM_THREADS; i++) {
            //printf("Creating Thread %d\n", i);
            pthread_create(&threads[i], NULL, calculateSum, &threadData[i]);
        }

        // Wait for the threads to finish
        for (int i = 0; i < NUM_THREADS; i++) {
            pthread_join(threads[i], NULL);
            //printf("Thread %d has finished\n", i);
        }

        // Now calculate the partition sums
        long long finalSum = 0;
        for (int i = 0; i < NUM_THREADS; i++) {
            finalSum += threadData[i].sum;
        }
        end = clock();


        double timeTook = ((double)(end - start)) / CLOCKS_PER_SEC;
        timeTotal += timeTook;
        printf("Sum of numbers from 0 to %d is %lld\n", N, finalSum);

    }
    // Print the final result
    double averageTotalTime = timeTotal / NUM_RUNS;

    printf("Total average time taken for the program across 500 iterations is: %f\n seconds", averageTotalTime);

    return 0;
}
