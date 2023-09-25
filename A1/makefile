CC = gcc
CFLAGS = -std=c99

.PHONY: all clean

all: multitasking baseline multithreading popen popen_adder

multitasking: multitasking.c
	$(CC) $(CFLAGS) -w -o multitasking multitasking.c

baseline: baseline.c
	$(CC) $(CFLAGS) -w -o baseline baseline.c

multithreading: multithreading.c
	$(CC) $(CFLAGS) -w -o multithreading multithreading.c

popen: 
	$(CC) $(CFLAGS) -w -o popen popen.c

popen_adder:
	$(CC) $(CFLAGS) -w -o popen_adder popen_adder.c

clean:
	rm -f *times.txt multitasking baseline multithreading popen popen_adder

clean_txt:
	rm -f *times.txt