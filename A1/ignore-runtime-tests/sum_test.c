#include <stdio.h>

int main() {
    int start, end;

    printf("Enter the starting value: ");
    scanf("%d", &start);
    printf("Enter the ending value: ");
    scanf("%d", &end);

    long long sum = 0;
    for (int i = start; i <= end; i++) {
        sum += i;
    }

    printf("Sum of numbers from %d to %d is %lld\n", start, end, sum);

    return 0;
}