from DataParsing import Task,Scheduler,SchedOrg,CLK_TIMES
from SharedFunctions import get_earliest_task,update_deadline


def rm(data:Scheduler):
    sched_query: list[SchedOrg] = []

    for i in range(1,data.exec_time+1):
        update_deadline(data,i)
        earliest_task = get_earliest_task(data,"RM")
        ##Check if in idle state
        if earliest_task is None:
            sched_query.append(SchedOrg("IDLE",4,data.power_clk[4]))
        else:
            ##update time to symbolize time has passed
            earliest_task.time_left -= 1
            sched_query.append(SchedOrg(earliest_task.name,0,data.power_clk[earliest_task.state]))

    prev_task = sched_query[0]
    time_start = 1 
    counter = 1 

    print("-------------------------------------------")
    print("\tPrinting Schedule Process")
    print("-------------------------------------------")

    for i in range(1, len(sched_query)):
        ##check if task has changed
        if(sched_query[i].task == prev_task.task) and (i != len(sched_query) - 1):
            counter+= 1
        else:
            ##calculate cosumption based on time task was scheduled
            power_consumption = (prev_task.power*counter)/1000.0
            print("{}\t{}\t{}\t{}\t{} J".format(time_start,prev_task.task,CLK_TIMES[prev_task.freq],counter,power_consumption))
            counter = 1
            time_start = i + 1
        if sched_query[i].freq == 4: ##IDLE State
            data.exec_time_passed += 1

        prev_task = sched_query[i]
    
    ##Calculatations
    data.idle_rate = (data.exec_time_passed / data.exec_time)*100
    data.exec_time_passed = data.exec_time - data.exec_time_passed

    data.tot_energy = 0.0

    for i in range(min(data.exec_time,len(sched_query))):
        data.tot_energy += sched_query[i].power
    data.tot_energy /= 1000.0

    print("\n")
    print("-------------------------------------------")
    print("\tAdditional Information")
    print("-------------------------------------------")
    print("Total Energy Consumption: {}J\tIdle Rate: {}% \tTotal Execution Time: {}s".format(data.tot_energy,data.idle_rate,data.exec_time_passed))

