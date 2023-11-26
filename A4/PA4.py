import sys
import random

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


def fifo_replacement(mem_ref):
    print("You are using the FIFO replacement algorithm.")
    pass

def lru_replacement(mem_ref):
    print("You are using the LRU replacement algorithm.")
    pass

def per_replacement(mem_ref):
    print("You are using the PER replacement algorithm.")
    pass

def extra_replacement(mem_ref):
    print("You are using the custom replacement algorithm.")
    pass

def simulate_virtual_memory(mem_ref, algorithm):
    if algorithm == 'random':
        random_replacement(mem_ref)
    elif algorithm == 'fifo':
        fifo_replacement(mem_ref)
    elif algorithm == 'lru':
        lru_replacement(mem_ref)
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