#define _POSIX_C_SOURCE 200809L // Required for clock_gettime
#define N 100000000
#define NUM_THREADS 2

#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <sys/wait.h>
#include <time.h>

// struct
struct ThreadData {
    int threadID;
    long long start;
    long long end;
    long long sum;
};

// function for calculating the sum of the numbers given
void* calculateSum(void* arg) {
    struct ThreadData* data = (struct ThreadData*)arg;
    long long sum = 0;
    for (long long i = data->start; i < data->end; i++) {
        sum += i;
    }
    data->sum = sum;

    // printf("Thread %d: Calculated sum from %d to %d: %lld\n",
    //        data->threadID, data->start, data->end, data->sum);

    pthread_exit(NULL);
}

int main() {
    struct timespec start,end;
    clock_gettime(CLOCK_MONOTONIC, &start);

    // Create the thread array
    pthread_t threads[NUM_THREADS];

    // We divide the work among the threads now
    struct ThreadData threadData[NUM_THREADS];
    long long chunkSize = N / NUM_THREADS;
    for (int i = 0; i < NUM_THREADS; i++) {
        threadData[i].threadID = i;
        threadData[i].start = i * chunkSize;
        threadData[i].end = (i + 1) * chunkSize;
    }

    // Create and start the threads
    for (int i = 0; i < NUM_THREADS; i++) {
        // printf("Creating Thread %d\n", i);
        pthread_create(&threads[i], NULL, calculateSum, &threadData[i]);
    }

    // Wait for the threads to finish
    for (int i = 0; i < NUM_THREADS; i++) {
        pthread_join(threads[i], NULL);
        // printf("Thread %d has finished\n", i);
    }

    // Now calculate the partition sums
    long long finalSum = 0;
    for (int i = 0; i < NUM_THREADS; i++) {
        finalSum += threadData[i].sum;
    }

    clock_gettime(CLOCK_MONOTONIC, &end);

    double cpu_seconds = (end.tv_sec - start.tv_sec) + (end.tv_nsec - start.tv_nsec) / 1e9;

    // Print the final result
    printf("Sum of numbers from 0 to %lld is %lld\n", N, finalSum);
    printf("Total CPU time taken in seconds: %.15f\n",cpu_seconds);

    return 0;
}
