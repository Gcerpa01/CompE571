CC = gcc
CFLAGS = -std=c99

.PHONY: all clean

all: sample_program FCFS SJF

sample_program: sample_program.c
	$(CC) $(CFLAGS) -w -o sample_program sample_program.c

FCFS: FCFS.c
	$(CC) $(CFLAGS) -w -o FCFS FCFS.c

SJF: SJF.c
	$(CC) $(CFLAGS) -w -o SJF SJF.c

clean:
	rm -f sample_program FCFS SJF
