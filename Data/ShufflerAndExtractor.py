import numpy as np
import wandb
import tensorflow as tf
import pandas as pd
import random
from tensorflow.keras import layers
import math

#initializing

inputs = []
outputs = []

raw_data = pd.read_excel("FPL_Player_Data_Season.xlsx")
raw_data = raw_data.drop(columns=raw_data.columns[0], axis=1)

#matching one player's season's data to same player's next season's data

for i in range(len(raw_data["Position"])):
    for j in range(14):
        tempIn = []
        tempOut = []
        if raw_data.at[i,raw_data.columns[19*j + 1]] == float(raw_data.at[i, raw_data.columns[19*j + 1]]) and raw_data.at[i,raw_data.columns[19*(j+1) + 1]] == float(raw_data.at[i, raw_data.columns[19*(j+1) + 1]]):
            tempIn.append(raw_data.at[i, "Position"])
            for k in range(19):
                if k != 7 and k !=8:
                    tempIn.append(raw_data.at[i,raw_data.columns[19*j + 1 + k]])
                    tempOut.append(raw_data.at[i,raw_data.columns[19*(j+1) + 1 + k]])
            inputs.append(tempIn)
            outputs.append(tempOut)


#shuffling the inputs so that order doesn't matter

transpose = {}
used = []
#unique random number for every index of the inputs/outputs list, i.e. setting the shuffle parameters
for h in range(len(inputs)):
    newPos = random.randint(1,len(inputs)-1)
    while newPos in used:
        newPos = random.randint(1,len(inputs)-1)
    #print(newPos)
    transpose[h] = newPos

#more variable initialization
newColumns = ["Position", "Points", "Minutes","I","C","T","Bonus","Bonus Points","Goals","Assists","YC","RC","Saves","Penalty Saves","OG","Penalty Misses","CS","GC"]
newColumnsOut = ["Points", "Minutes","I","C","T","Bonus","Bonus Points","Goals","Assists","YC","RC","Saves","Penalty Saves","OG","Penalty Misses","CS","GC"]
inDF = pd.DataFrame(columns=newColumns)
outDF = pd.DataFrame(columns = newColumnsOut)


#invert the list
#invert = {v:k for k, v in transpose.items()}


#set up the shuffled lists and training/testing division
for g in range(len(transpose)):
    inDF = pd.concat([inDF, pd.DataFrame([inputs[transpose[g]]], columns=newColumns)], sort=False)
    outDF = pd.concat([outDF, pd.DataFrame([outputs[transpose[g]]], columns=newColumnsOut)], sort=False)
print(inputs[transpose[0]])
inDF.to_excel("FPL_Season_Data_Only_Inputs_Shuffled2.xlsx")
outDF.to_excel("FPL_Season_Data_Only_Outputs_Shuffled2.xlsx")

#fun stuff - define the model!

