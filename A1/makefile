CC = gcc
CFLAGS = -std=c99

.PHONY: all clean

all: multitasking baseline multithreading

multitasking: multitasking.c
	$(CC) $(CFLAGS) -o multitasking multitasking.c

baseline: baseline.c
	$(CC) $(CFLAGS) -o baseline baseline.c

multithreading: multithreading.c
	$(CC) $(CFLAGS) -o multithreading multithreading.c

clean:
	rm -f *.txt multitasking baseline multithreading

clean_txt:
	rm -f *.txt