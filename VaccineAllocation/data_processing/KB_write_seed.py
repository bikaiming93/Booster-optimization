# -*- coding: utf-8 -*-
"""
Created on Mon Aug  1 14:59:26 2022

@author: kb44774
"""

import pickle
import random
from pathlib import Path
import os

instances_path = Path(__file__).parent
print(instances_path)

if __name__ == "__main__":
    path = instances_path / 'seeds_saved'

isExist = os.path.exists(path)
if not isExist:
    os.makedirs(path)
#print(isExist)

#number_of_data=100
#number_of_seeds=100



def write_multi_seeds(number_of_seeds,number_of_data):
    for j in range(number_of_seeds):
        data=[]
        for i in range(number_of_data):
            raw = int(random.uniform(0,100))
            data.append(raw)
            
        csp = str(Path(path))
        file_path = csp+"/new_seed"+str(j)+".p"
        
        with open(str(file_path), 'wb') as outfile:
            pickle.dump(data, outfile)
            
            
write_multi_seeds(100,100)