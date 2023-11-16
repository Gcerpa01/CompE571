from process import Task,Scheduler,SchedOrg,CLK_TIMES

##find the earliest task
def get_earliest_task(data:Scheduler) -> Task:
    earliest_task: Task = None
    for wTask in data.wTasks:
        if wTask.time_left > 0 and earliest_task is None:
            earliest_task = wTask
        elif wTask.time_left > 0:
            if wTask.deadline < earliest_task.deadline:
                earliest_task = wTask
    return earliest_task

##update deadline if it has been reached
def update_deadline(data: Scheduler, curr_time: int):
    for wTask in data.wTasks:
        if curr_time == wTask.deadline:
            wTask.deadline += wTask.period
            wTask.time_left = wTask.wcet_clk[wTask.state]
    return
    

def edf(data: Scheduler):
    sched_query: list[SchedOrg] = []

    ##iterate through tasks
    for i in range(1,data.exec_time+1):
        update_deadline(data,i)
        earliest_task = get_earliest_task(data)
        ##Check if in idle state
        if earliest_task is None:
            sched_query.append(SchedOrg("IDLE",4,data.power_clk[4]))
        else:
            ##update time to symbolize time has passed
            earliest_task.time_left -= 1
            sched_query.append(SchedOrg(earliest_task.name,earliest_task.state,data.power_clk[earliest_task.state]))

    
    first_task = sched_query[0]
    time_start = 1 
    counter = 1 

    print("-------------------------------------------")
    print("\tPrinting Schedule Process")
    print("-------------------------------------------")

    for i in range(1, len(sched_query)):
        ##check if task has changed
        if(sched_query[i].task == first_task.task) and (i != len(sched_query) - 1):
            counter+= 1
        else:
            ##calculate cosumption based on time task was scheduled
            power_consumption = (first_task.power*counter)/1000.0
            print("{}\t{}\t{}\t{}\t{} J".format(time_start,first_task.task,CLK_TIMES[first_task.freq],counter,power_consumption))
            counter = 1
            time_start = i + 1
        if sched_query[i].freq == 4: ##IDLE State
            data.exec_time_passed += 1

        first_task = sched_query[i]
    
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




