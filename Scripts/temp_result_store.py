import sys
import json
import random

for line in sys.stdin:
    #temp_dict = json.loads(line)
    with open("scripts/results/phase1_rating_result","a") as output:
        output.write(line)
    output.close()