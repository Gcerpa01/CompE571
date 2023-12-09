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

    print(f"---------------------RANDOM----------------------")
    print(f"Total page faults: {pg_faults}")
    print(f"Total disk references: {dsk_ref}")
    print(f"Total dirty page writes: {dirty_writes}\n")

    return pg_faults, dsk_ref, dirty_writes



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

    print(f"---------------------FIFO----------------------")
    print(f"Total page faults: {pg_faults}")
    print(f"Total disk references: {dsk_ref}")
    print(f"Total dirty page writes: {dirty_writes}\n")

    return pg_faults, dsk_ref, dirty_writes




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
    
    print(f"---------------------LRU----------------------")

    print(f"Total page faults: {pg_faults}")
    print(f"Total disk references: {dsk_ref}")
    print(f"Total dirty page writes: {dirty_writes}\n")

    return pg_faults, dsk_ref, dirty_writes

def per_replacement(mem_ref, frame_count=32, max_ref=200):
    frames = [None] * frame_count  # Physical frames
    pg_faults = 0
    dsk_ref = 0
    dirty_writes = 0

    # Page table: {virtual_page_number: (physical_frame_number, dirty_bit, reference_bit)}
    page_table = {}

    curr_ref = 0

    for process_id, address, operation in mem_ref:
        virtual_page_number = address >> 9  # 7 most significant bits
        is_dirty = operation == 'W'

        curr_ref += 1

        # reset criteria met
        if curr_ref == max_ref:
            for page_number in page_table:
                if page_table[page_number][2] == 1:  # Reset reference bit for all referenced pages
                    page_table[page_number] = (page_table[page_number][0], page_table[page_number][1], 0)
            curr_ref = 0

        if virtual_page_number not in page_table or page_table[virtual_page_number][0] is None:
            # Page fault occurs
            pg_faults += 1
            dsk_ref += 1

            if None not in frames:
                # select only those not in the page table
                unused_pages = [page for page in frames if page not in page_table]
                # select unreferenced page with low dirty bit
                unreferenced_clean_pages = [page for page in frames if page_table[page][2] == 0 and page_table[page][1] == 0]
                # select unreferenced page with high dirty bit
                unreferenced_dirty_pages = [page for page in frames if page_table[page][2] == 0 and page_table[page][1] == 1]
                # select referenced page with low dirty bit
                referenced_clean_pages = [page for page in frames if page_table[page][2] == 1 and page_table[page][1] == 0]
                # select referenced page with high dirty bit
                referenced_dirty_pages = [page for page in frames if page_table[page][2] == 1 and page_table[page][1] == 1]
                
                if unused_pages:
                    per_pg = min(unused_pages)
                elif unreferenced_dirty_pages:
                    per_pg = min(unreferenced_dirty_pages)
                elif unreferenced_clean_pages:
                    per_pg = min(unreferenced_clean_pages)
                elif referenced_dirty_pages:
                    per_pg = min(referenced_dirty_pages)
                elif referenced_clean_pages:
                    per_pg = min(referenced_clean_pages)
                
                if page_table[per_pg][1]:
                    dirty_writes += 1
                    dsk_ref += 1
                
                # remove per page from page table to make room for next page loaded in memory
                per_frame = page_table[per_pg][0]
                frames[per_frame] = None
                del page_table[per_pg]


            # Find an empty frame or use the replaced frame
            empty_or_replaced_frame = frames.index(None) if None in frames else frames.index(per_frame)
            frames[empty_or_replaced_frame] = virtual_page_number
            page_table[virtual_page_number] = (empty_or_replaced_frame, is_dirty, True)

        else:
            # Update page table entry
            frame_number, _, _ = page_table[virtual_page_number]
            page_table[virtual_page_number] = (frame_number, is_dirty, True)

    print(f"---------------------PER----------------------")
    print(f"Total page faults: {pg_faults}")
    print(f"Total disk references: {dsk_ref}")
    print(f"Total dirty page writes: {dirty_writes}\n")

    return pg_faults, dsk_ref, dirty_writes



def lfu_rr_replacement(mem_ref, frame_count=32):
    frames = [None] * frame_count
    pg_faults = 0
    dsk_ref = 0
    dirty_writes = 0
    access_frequency = {}
    last_used_time = {}
    dirty_bit = {}

    current_time = 0

    for process_id, address, operation in mem_ref:
        current_time += 1
        virtual_page_number = address >> 9
        is_dirty = operation == 'W'

        # Update access frequency, last used time, and dirty bit
        access_frequency[virtual_page_number] = access_frequency.get(virtual_page_number, 0) + 1
        last_used_time[virtual_page_number] = current_time
        dirty_bit[virtual_page_number] = is_dirty

        if virtual_page_number not in frames:
            # Page fault occurs
            pg_faults += 1
            dsk_ref += 1

            if None not in frames:
                # Find the page with the lowest frequency and least recent use, prioritize clean pages
                replacement_candidate = min(frames, key=lambda page: (dirty_bit[page], access_frequency[page], last_used_time[page]))

                # Only increment dirty_writes if the page to be replaced is dirty
                if dirty_bit[replacement_candidate]:
                    dirty_writes += 1
                    dsk_ref += 1

                # Replace the page
                frame_index = frames.index(replacement_candidate)
                frames[frame_index] = virtual_page_number
            else:
                # Find the first empty frame and use it
                empty_frame_index = frames.index(None)
                frames[empty_frame_index] = virtual_page_number
        else:
            # Update dirty bit if necessary
            dirty_bit[virtual_page_number] = is_dirty

    print(f"---------------------LFU-RR (Modified)----------------------")
    print(f"Total page faults: {pg_faults}")
    print(f"Total disk references: {dsk_ref}")
    print(f"Total dirty page writes: {dirty_writes}\n")

    return pg_faults, dsk_ref, dirty_writes



def addlabels(x,y):
    for i in range(len(x)):
        plt.text(i, y[i], y[i], ha = 'center')

def matplot_magic(pagefault_stats, diskaccess_stats, dirtypage_stats):
    pagefault_graph(pagefault_stats)
    diskaccess_graph(diskaccess_stats)
    dirtypage_graph(dirtypage_stats)

def pagefault_graph(page_faults):
    algorithms = ['Random', 'FIFO', 'LRU', 'PER', 'LfuRR']
    plt.bar(algorithms, page_faults)
    plt.title('Page Faults ')
    plt.ylabel('# of Page Faults')
    plt.ylim(ymin=2000)  
    addlabels(algorithms, page_faults)
    plt.show()

def diskaccess_graph(disk_accesses):
    algorithms = ['Random', 'FIFO', 'LRU', 'PER', 'LfuRR']
    plt.bar(algorithms, disk_accesses)
    plt.title('Disk Accesses ')
    plt.ylabel('# of Disk Accesses')
    plt.ylim(ymin=2000)  
    addlabels(algorithms, disk_accesses)
    plt.show()

def dirtypage_graph(dirty_pages):
    algorithms = ['Random', 'FIFO', 'LRU', 'PER', 'LfuRR']
    plt.bar(algorithms, dirty_pages, )
    plt.title('Dirty Page Writes ')
    plt.xlabel('Algorithms')
    plt.ylabel('# of Dirty Page Writes')
    plt.ylim(ymin=0)  
    addlabels(algorithms, dirty_pages)
    plt.show()


def simulate_virtual_memory(mem_ref, algorithm):

    if algorithm == 'random':
        random_replacement(mem_ref, frame_count=32)
    elif algorithm == 'fifo':
        fifo_replacement(mem_ref, frame_count=32)
    elif algorithm == 'lru':
        lru_replacement(mem_ref, frame_count=32)
    elif algorithm == 'per':
        per_replacement(mem_ref, frame_count=32)
    elif algorithm == 'lfurr':
        lfu_rr_replacement(mem_ref, frame_count=32)
    else:
        print("Unknown algorithm specified.")

if __name__ == "__main__":
    if len(sys.argv) > 2:
        file_path = sys.argv[1]
        algorithm = sys.argv[2].lower()
        references = read_mem_ref(file_path)
        simulate_virtual_memory(references, algorithm)

    elif len(sys.argv) == 2: 
        file_path = sys.argv[1]
        references = read_mem_ref(file_path)

        random_stats = random_replacement(references, frame_count=32)
        fifo_stats = fifo_replacement(references, frame_count=32)
        lru_stats = lru_replacement(references, frame_count=32)
        per_stats = per_replacement(references, frame_count=32)
        lfu_rr_stats = lfu_rr_replacement(references, frame_count=32)

        #  data for all algorithms and graph
        pagefault_stats = [random_stats[0], fifo_stats[0], lru_stats[0], per_stats[0], lfu_rr_stats[0]]
        diskaccess_stats = [random_stats[1], fifo_stats[1], lru_stats[1], per_stats[1], lfu_rr_stats[1]]
        dirtypage_stats = [random_stats[2], fifo_stats[2], lru_stats[2], per_stats[2], lfu_rr_stats[2]]

        matplot_magic(pagefault_stats, diskaccess_stats, dirtypage_stats)

    else:
        print("Please provide a file path and an algorithm name as command line arguments.")

