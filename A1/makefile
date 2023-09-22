CC = gcc
CFLAGS = -std=c99

.PHONY: all clean

all: multitasking baseline multithreading

multitasking: multitasking.c
	$(CC) $(CFLAGS) -w -o multitasking multitasking.c

baseline: baseline.c
	$(CC) $(CFLAGS) -w -o baseline baseline.c

multithreading: multithreading.c
	$(CC) $(CFLAGS) -w -o multithreading multithreading.c

clean:
	rm -f *.txt multitasking baseline multithreading

clean_txt:
	rm -f *.txt