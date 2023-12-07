import sys
import random
import matplotlib.pyplot as plt

def read_mem_ref(file_path):
    mem_ref = []

    with open(file_path, 'r') as file:
        for line in file:
            # print("Line: ", line) # To verify debug reading of input file
            parts = line.strip().split('\t')
            if len(parts) == 3:
                process_id, address, operation = parts
                mem_ref.append((int(process_id), int(address), operation))

    return mem_ref

def random_replacement(mem_ref, frame_count=32):
    frames = [None] * frame_count  # Physical frames
    pg_faults = 0
    dsk_ref = 0
    dirty_writes = 0

    # Page table: {virtual_page_number: (physical_frame_number, dirty_bit, reference_bit)}
    page_table = {}

    for process_id, address, operation in mem_ref:
        virtual_page_number = address >> 9  # 7 most significant bits
        is_dirty = operation == 'W'

        if virtual_page_number not in page_table or page_table[virtual_page_number][0] is None:
            # Page fault occurs
            pg_faults += 1
            dsk_ref += 1

            if None not in frames:
                # Choose a random frame to replace
                frame_to_replace = random.choice([frame for frame in frames if frame is not None])
                if page_table[frame_to_replace][1]:  # Check if the dirty bit is set
                    dirty_writes += 1
                    dsk_ref += 1

                # Update page table for the replaced frame
                page_table[frame_to_replace] = (None, False, False)

            # Find an empty frame or use the replaced frame
            empty_or_replaced_frame = frames.index(None) if None in frames else frames.index(frame_to_replace)
            frames[empty_or_replaced_frame] = virtual_page_number
            page_table[virtual_page_number] = (empty_or_replaced_frame, is_dirty, True)
        else:
            # Update page table entry
            frame_number, _, _ = page_table[virtual_page_number]
            page_table[virtual_page_number] = (frame_number, is_dirty, True)

    print(f"Total page faults: {pg_faults}")
    print(f"Total disk references: {dsk_ref}")
    print(f"Total dirty page writes: {dirty_writes}")

def fifo_replacement(mem_ref, frame_count=32):
    frames = [None] * frame_count  # Physical frames
    fifo_queue = []  # FIFO queue to track page order
    pg_faults = 0
    dsk_ref = 0
    dirty_writes = 0

    # Page table: {virtual_page_number: (physical_frame_number, dirty_bit)}
    page_table = {}

    for process_id, address, operation in mem_ref:
        virtual_page_number = address >> 9  # 7 most significant bits
        is_dirty = operation == 'W'

        if virtual_page_number not in page_table or page_table[virtual_page_number][0] is None:
            # Page fault occurs
            pg_faults += 1
            dsk_ref += 1

            if len(fifo_queue) >= frame_count:
                # using FIFO queue to track page order
                frame_to_replace = fifo_queue.pop(0)
                if page_table[frame_to_replace][1]:  # Check if  dirty bit is set
                    dirty_writes += 1
                    dsk_ref += 1

                # Update page table for the replaced frame
                page_table[frame_to_replace] = (None, False)

            # Find an empty frame or use the replaced frame
            empty_or_replaced_frame = frames.index(None) if None in frames else frames.index(frame_to_replace)
            frames[empty_or_replaced_frame] = virtual_page_number
            fifo_queue.append(virtual_page_number)  # Add page to FIFO queue
            page_table[virtual_page_number] = (empty_or_replaced_frame, is_dirty)
        else:
            # Update page table entry
            frame_number, _ = page_table[virtual_page_number]
            page_table[virtual_page_number] = (frame_number, is_dirty)

    print(f"Total page faults: {pg_faults}")
    print(f"Total disk references: {dsk_ref}")
    print(f"Total dirty page writes: {dirty_writes}")


def lru_replacement(mem_ref, frame_count=32):
    frames = [None] * frame_count  # Physical frames
    pg_faults = 0
    dsk_ref = 0
    dirty_writes = 0

    # Page table: {virtual_page_number: (physical_frame_number, dirty_bit, last_used_time)}
    page_table = {}
    
    last_used_time = 0

    for process_id, address, operation in mem_ref:
        virtual_page_number = address >> 9  # 7 most significant bits
        is_dirty = operation == 'W'
        
        if virtual_page_number not in page_table or page_table[virtual_page_number][0] is None:
            # Page fault occurs
            pg_faults += 1
            dsk_ref += 1

            # Determine the page to replace
            if None not in frames:  # No free frame
                # LRU order --> least recently used page --> dirty bit -- > page number
                lru_pg = min(page_table, key=lambda x: (page_table[x][2], not page_table[x][1], x))
                if page_table[lru_pg][1]:  # If dirty, increment dirty writes
                    dirty_writes += 1
                    dsk_ref += 1

                # remove LRU page from page table to make room fo rnext page loaded in memory
                lru_frame = page_table[lru_pg][0]
                frames[lru_frame] = None
                del page_table[lru_pg]

            # Find an empty frame or use the LRU frame
            empty_or_lru_frame = frames.index(None) if None in frames else lru_frame
            
            frames[empty_or_lru_frame] = virtual_page_number
            page_table[virtual_page_number] = (empty_or_lru_frame, is_dirty, last_used_time)
        else:
            frame_number, _, _ = page_table[virtual_page_number]
            page_table[virtual_page_number] = (frame_number, is_dirty, last_used_time)

        last_used_time += 1  # Increment the time unit

    print(f"Total page faults: {pg_faults}")
    print(f"Total disk references: {dsk_ref}")
    print(f"Total dirty page writes: {dirty_writes}")

# Example usage:
# lru_replacement(mem_ref, frame_count=32)



def pagefault_graph(page_faults):
    algorithms = ['Random', 'FIFO', 'LRU']
    plt.bar(algorithms, page_faults)
    plt.title('Page Faults Comparison')
    plt.xlabel('Algorithms')
    plt.ylabel('Number of Page Faults')
    plt.show()

def diskaccess_graph(disk_accesses):
    algorithms = ['Random', 'FIFO', 'LRU']
    plt.bar(algorithms, disk_accesses)
    plt.title('Disk Accesses Comparison')
    plt.xlabel('Algorithms')
    plt.ylabel('Number of Disk Accesses')
    plt.show()

def dirtypage_graph(dirty_pages):
    algorithms = ['Random', 'FIFO', 'LRU']
    plt.bar(algorithms, dirty_pages)
    plt.title('Dirty Page Writes Comparison')
    plt.xlabel('Algorithms')
    plt.ylabel('Number of Dirty Page Writes')
    plt.show()


def per_replacement(mem_ref):
    print("You are using the PER replacement algorithm.")
    pass

def extra_replacement(mem_ref):
    print("You are using the custom replacement algorithm.")
    pass

def simulate_virtual_memory(mem_ref, algorithm):
    if algorithm == 'random':
        random_replacement(mem_ref, frame_count=32)
    elif algorithm == 'fifo':
        fifo_replacement(mem_ref, frame_count=32) 
    elif algorithm == 'lru':
        lru_replacement(mem_ref, frame_count=32)
    elif algorithm == 'per':
        per_replacement(mem_ref)
    elif algorithm == 'extra':
        extra_replacement(mem_ref)
    else:
        print("Unknown algorithm specified.")

if __name__ == "__main__":
    if len(sys.argv) > 2:
        file_path = sys.argv[1]
        algorithm = sys.argv[2].lower()
        references = read_mem_ref(file_path)
        simulate_virtual_memory(references, algorithm)
    else:
        print("Please provide a file path and an algorithm name as command line arguments.")
