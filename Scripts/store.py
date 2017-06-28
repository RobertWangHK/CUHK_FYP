import sys
import json
import random

for line in sys.stdin:
    #temp_dict = json.loads(line)
    with open("scripts/results/uid","a") as output:
        output.write(line)
    output.close()