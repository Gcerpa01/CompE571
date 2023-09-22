CC = gcc
CFLAGS = -std=c99

.PHONY: all clean

all: multitasking baseline

multitasking: multitasking.c
	$(CC) $(CFLAGS) -o multitasking multitasking.c

baseline: baseline.c
	$(CC) $(CFLAGS) -o baseline baseline.c



clean:
	rm -f *.txt multitasking baseline

clean_times:
	rm -f *.txt