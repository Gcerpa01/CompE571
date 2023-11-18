from DataParsing import Scheduler, CLK_TIMES

def calculate_energy(power, duration):
    return (power * duration) / 1000.0  # Convert mW to J

def rm(data: Scheduler):
    # Sort tasks by period (shortest period = highest priority)
    data.wTasks.sort(key=lambda task: task.period)

    print("-------------------------------------------")
    print("\tPrinting Schedule Process")
    print("-------------------------------------------")
    print("<Time Started>\t<Task Name>\t<CPU Freq>\t<Runtime>\t<NRG Consumed>")

    current_time = 0
    total_idle_time = 0

    while current_time < data.exec_time:
        task_scheduled = False

        for task in data.wTasks:
            # Check if task is ready to run
            if current_time % task.period == 0 and task.time_left > 0:
                runtime = min(task.wcet_clk[0], data.exec_time - current_time)
                energy_consumed = calculate_energy(data.power_clk[0], runtime)
                print(f"{current_time}\t\t{task.name}\t\t1188\t\t{runtime}\t\t{energy_consumed} J")
                task.time_left -= runtime
                current_time += runtime
                data.tot_energy += energy_consumed
                task_scheduled = True
                break

        if not task_scheduled:
            # No task scheduled, CPU is idle
            print(f"{current_time}\t\tIDLE\t\tIDLE\t\t1\t\t{calculate_energy(data.power_clk[-1], 1)} J")
            data.tot_energy += calculate_energy(data.power_clk[-1], 1)
            total_idle_time += 1
            current_time += 1

    # Calculations for additional information
    data.idle_rate = (total_idle_time / data.exec_time) * 100
    data.exec_time_passed = data.exec_time - total_idle_time

    print("\n")
    print("-------------------------------------------")
    print("\tAdditional Information")
    print("-------------------------------------------")
    print(f"Total Energy Consumption: {data.tot_energy}J\tIdle Rate: {data.idle_rate}% \tTotal Execution Time: {data.exec_time_passed}s")


