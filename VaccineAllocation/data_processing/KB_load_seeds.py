# -*- coding: utf-8 -*-
"""
Created on Tue Aug  2 12:17:00 2022

@author: kb44774
"""

import pickle
import random
from pathlib import Path

instances_path = Path(__file__).parent
#print(instances_path)

def load_seeds(seeds_file_name):
    open_path=str(instances_path) +"\\" +str(seeds_file_name)
    print(open_path)
    try:
        with open(open_path, 'rb') as infile:
            seeds_data = pickle.load(infile)
            print(seeds_data)
        return seeds_data[0], seeds_data[1]    
    except:
        return [],[]
    
    


a=load_seeds('new_seed17.p')
print(a)