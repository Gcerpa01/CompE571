import sys
from dataclasses import dataclass

CLK_TIMES = ["1188", "918", "648", "384", "IDLE"]

@dataclass
class Task:
    name: str
    period: int
    wcet_clk: list[int]

    time_left: int = 0
    deadline: int = 0


@dataclass
class Scheduler:
    tasks: int
    exec_time: int
    power_clk: list[int]
    wTasks:list[Task]



def parse_file(fileName:str) -> Scheduler:
    try:
        with open(fileName,'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print("Error: The file {} was not found".format(fileName))
        sys.exit(1)
    except Exception as e:
        print("Unable to open the file {} due to exception: {}".format(fileName,e))
        sys.exit(1)

    system_info = lines[0].split()
    
    tasks, exec_time, *power_clk = map(int, system_info)

    wTasks = []

    for line in lines[1:]:
        task_desc = line.split()
        taskName, taskPeriod, *wcet_clk = task_desc
        wTasks.append(Task(taskName,int(taskPeriod),list(map(int,wcet_clk)),int(wcet_clk[0]),int(taskPeriod)))
    
    return Scheduler(tasks,exec_time,power_clk,wTasks)

    

