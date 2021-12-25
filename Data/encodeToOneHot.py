import numpy as np
import wandb
import tensorflow as tf
import pandas as pd
import random
from tensorflow.keras import layers
from tensorflow.keras import Sequential
from tensorflow.keras import optimizers
import math
from sklearn.preprocessing import OneHotEncoder

data = [[0],[1],[2],[3]]
encoder = OneHotEncoder(sparse=False)
onehot = encoder.fit_transform(data)
print(onehot[1])
inputData = pd.read_excel("FPL_Season_Data_Only_Inputs_Shuffled.xlsx")
inputData = inputData.drop(inputData.columns[0], axis=1)
for i in range(len(inputData["Position 1"])):
    if inputData.at[i, "Position 1"] == 0:
        inputData.at[i,"Position 1"] = 1
        inputData.at[i,"Position 2"] = 0
        inputData.at[i,"Position 3"] = 0
        inputData.at[i,"Position 4"] = 0
    elif inputData.at[i, "Position 1"] == 1:
        inputData.at[i,"Position 1"] = 0
        inputData.at[i,"Position 2"] = 1
        inputData.at[i,"Position 3"] = 0
        inputData.at[i,"Position 4"] = 0
    elif inputData.at[i, "Position 1"] == 2:
        inputData.at[i,"Position 1"] = 0
        inputData.at[i,"Position 2"] = 0
        inputData.at[i,"Position 3"] = 1
        inputData.at[i,"Position 4"] = 0
    elif inputData.at[i, "Position 1"] == 3:
        inputData.at[i,"Position 1"] = 0
        inputData.at[i,"Position 2"] = 0
        inputData.at[i,"Position 3"] = 0
        inputData.at[i,"Position 4"] = 1
inputData.to_excel("FPL_Season_Data_Only_Inputs_Shuffled.xlsx")
