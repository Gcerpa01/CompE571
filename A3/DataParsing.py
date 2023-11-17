import sys

CLK_TIMES = ["1188", "918", "648", "384", "IDLE"]

class Task:
    def __init__(self, name: str, period: int, wcet_clk: list[int], time_left: int = 0, deadline: int = 0, state: int = 0):
        self.name = name
        self.period = period
        self.wcet_clk = wcet_clk
        self.time_left = time_left
        self.deadline = deadline
        self.state = state

class Scheduler:
    def __init__(self, tasks: int, exec_time: int, power_clk: list[int], wTasks: list[Task], tot_energy: float = 0.0, idle_rate: float = 0.0, exec_time_passed: int = 0):
        self.task = tasks
        self.exec_time = exec_time
        self.power_clk = power_clk
        self.wTasks = wTasks
        self.tot_energy = tot_energy
        self.idle_rate = idle_rate
        self.exec_time_passed = exec_time_passed

class SchedOrg:
    def __init__(self, task: str, freq: int, power: int):
        self.task = task
        self.freq = freq
        self.power = power

def parse_file(fileName:str) -> Scheduler:
    try:
        with open(fileName,'r') as file: ##check if file can be opened
            lines = file.readlines()
    except FileNotFoundError: ##return error if not found
        print("Error: The file {} was not found".format(fileName))
        sys.exit(1)
    except Exception as e: ##demonstrate error opening files
        print("Unable to open the file {} due to exception: {}".format(fileName,e))
        sys.exit(1)

    system_info = lines[0].split()
    
    tasks, exec_time, *power_clk = map(int, system_info) ##note as system info

    wTasks = []

    ##append all tasks to vector
    for line in lines[1:]:
        task_desc = line.split()
        taskName, taskPeriod, *wcet_clk = task_desc
        wTasks.append(Task(taskName,int(taskPeriod),list(map(int,wcet_clk)),int(wcet_clk[0]),int(taskPeriod)))
    
    return Scheduler(tasks,exec_time,power_clk,wTasks)
