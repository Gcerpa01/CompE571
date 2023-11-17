import sys
import DataParsing
from EDF import edf
from RM import rm

# import os

if len(sys.argv) != 3 and len(sys.argv) != 4:
    print("\n-------------------------------------------")
    print("Incorrect arguments. Please use the format:")
    print("your_program <input_file_name> <EDF or RM> [EE]")
    print("-------------------------------------------\n")
    sys.exit(1)

if sys.argv[2] not in ["EDF", "RM"]:
    print("-------------------------------------------")
    print("Invalid argument for schedule policy")
    print("The available arguments for schedule policies are EDF and RM")
    print("-------------------------------------------\n")
    sys.exit(1)

if len(sys.argv) == 4 and sys.argv[3] not in ["" , "EE"]:
    print("\n-------------------------------------------")
    print("For energy efficiency please use the format:")
    print("your_program <input_file_name> <EDF or RM> [EE]")
    print("Otherwise please omit EE")
    print("-------------------------------------------\n")
    sys.exit(1)
elif len(sys.argv) == 4 and sys.argv[3] == "EE":
    EE = True
else:
    EE = False

file_name = sys.argv[1]
if len(file_name) < 4 or file_name[-4:] != ".txt":
    print("-------------------------------------------")
    print("Error: only '.txt' files are supported")
    print("-------------------------------------------\n")
    sys.exit(1)


scheduler_data = DataParsing.parse_file(sys.argv[1])

if sys.argv[2] == "EDF" and not EE:
    print("-------------------------------------------")
    print("\tNow running EDF")
    print("-------------------------------------------\n")
    edf(scheduler_data)
elif sys.argv[2] == "RM" and not EE:
    print("-------------------------------------------")
    print("\tNow running RM")
    print("-------------------------------------------\n")
    rm(scheduler_data)

sys.exit(0)
