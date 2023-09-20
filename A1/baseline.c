
#define N  100000000
#define NUM_THREAD 2
#define NUM_TASKS 2

#include <stdio.h>

int main(){
    long long sum = 0;
    for(int i = 0; i < N; i++){
        sum += i;
    }

    printf("Total sum from 0 to %d is: %lld\n",N,sum);
    return 0;
}