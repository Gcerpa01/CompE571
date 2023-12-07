def lru_replacement(mem_ref,frame_count=32):
    frames = [None] * frame_count
    pg_faults = 0
    dsk_ref = 0
    dirty_writes = 0

    # Page table: {virtual_page_number: (physical_frame_number, dirty_bit,last_used_time)}
    page_table = {}
    
    last_used_time = 0

    for process_id, address, operation in mem_ref:
        virtual_page_number = address >> 9  # 7 most significant bits
        is_dirty = operation == 'W'
        if virtual_page_number not in page_table or page_table[virtual_page_number][0] is None:
            pg_faults += 1
            dsk_ref += 1
            
            if None not in frames:
                ##prioritize last used time -> dirty bit -> page num
                lru_pg = min(page_table, key=lambda x: (page_table[x][2], not page_table[x][1], x))
                if page_table[lru_pg][1]:
                    dirty_writes += 1
                    dsk_ref += 1
                page_table[lru_pg] = (None,False,last_used_time)
            
            # Find an empty frame or use the replaced frame
            empty_or_replaced_frame = frames.index(None) if None in frames else page_table[lru_pg][0]

            if empty_or_replaced_frame is not None:
                frames[empty_or_replaced_frame] = virtual_page_number
                page_table[virtual_page_number] = (empty_or_replaced_frame, is_dirty, last_used_time)
        else:
            # Update page table entry and last used time
            frame_number, _, _ = page_table[virtual_page_number]
            page_table[virtual_page_number] = (frame_number, is_dirty, last_used_time)

        last_used_time += 1 ##time has passed

    print(f"Total page faults: {pg_faults}")
    print(f"Total disk references: {dsk_ref}")
    print(f"Total dirty page writes: {dirty_writes}")