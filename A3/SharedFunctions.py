from DataParsing import Scheduler,Task,SchedOrg
from math import lcm

##update deadline if it has been reached
def update_deadline(data: Scheduler, curr_time: int):
    for wTask in data.wTasks:
        if curr_time == wTask.deadline:
            wTask.deadline += wTask.period
            wTask.time_left = wTask.wcet_clk[wTask.state]
    return

##find the next task based on the mode(EDF / RM)
def get_next_task(data:Scheduler,mode:str) -> Task:
    next_task: Task = None
    for wTask in data.wTasks:
        if (wTask.time_left > 0) and next_task is None:
            next_task = wTask
        elif wTask.time_left > 0:
            if mode == "EDF" and (wTask.deadline < next_task.deadline): ## Earlier Deadline
                next_task = wTask
            elif mode == "RM" and (wTask.period < next_task.period): ## Lower Period
                next_task = wTask

    return next_task

##Create the vector/query that holds the order of our processes
def create_query(data:Scheduler,mode:str)->list[SchedOrg]:
    sched_query: list[SchedOrg] = []

    for i in range(1,data.exec_time+1):
        update_deadline(data,i)
        next_task = get_next_task(data,mode)
        ##Check if in idle state
        if next_task is None:
            sched_query.append(SchedOrg("IDLE",4,data.power_clk[4]))
        else:
            ##update time to symbolize time has passed
            next_task.time_left -= 1
            sched_query.append(SchedOrg(next_task.name,next_task.state,data.power_clk[next_task.state]))
    return sched_query

def get_hyperperiod(data:Scheduler):
    periods = []
    for wTask in data.wTasks:
        periods.append(wTask.period)
    return lcm(*periods)