from DataParsing import Scheduler,Task

##update deadline if it has been reached
def update_deadline(data: Scheduler, curr_time: int):
    for wTask in data.wTasks:
        if curr_time == wTask.deadline:
            wTask.deadline += wTask.period
            wTask.time_left = wTask.wcet_clk[wTask.state]
    return

##find the earliest task
def get_earliest_task(data:Scheduler,mode:str) -> Task:
    earliest_task: Task = None
    for wTask in data.wTasks:
        if (wTask.time_left > 0) and earliest_task is None:
            earliest_task = wTask
        elif wTask.time_left > 0:
            if mode == "EDF" and (wTask.deadline < earliest_task.deadline):
                earliest_task = wTask
            elif mode == "RM" and (wTask.period < earliest_task.period):
                earliest_task = wTask

    return earliest_task