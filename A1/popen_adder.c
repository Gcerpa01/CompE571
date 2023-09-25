#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[]) {
    if (argc != 3) { //not enough arguments or too many
         printf("Usage: %s <start_range> <end_range>\n", argv[0]);
        return 1; // Return an error code
    }

    long long start = atoll(argv[1]);
    long long end = atoll(argv[2]);

    long long sum = 0;

    for(long long i = start; i < end; i++){
        sum += i;
    }

    
    printf("%lld\n ",sum);

    return 0; // Return 0 to indicate success
}
