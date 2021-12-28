import numpy as np
import tensorflow as tf
import pandas as pd
import wandb
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, BatchNormalization
from wandb.keras import WandbCallback

#initializing
np.set_printoptions(precision=4, suppress=True)
wandb.init(project="FPL_Season_Data_Only_First_Try", entity="matthewlchen",sync_tensorboard=True)

#pulling data

trainInput = pd.read_excel("FPL_Season_Data_Only_Inputs_Shuffled2.xlsx")
trainInput = trainInput.drop(trainInput.columns[0], axis=1)
trainOutput = pd.read_excel("FPL_Season_Data_Only_Outputs_Shuffled2.xlsx")
trainOutput = trainOutput.drop(trainOutput.columns[0], axis=1)

#transforming categorical position data into one hot encoding

position = pd.get_dummies(trainInput["Position"],prefix="Position")
trainInput = pd.concat([position,trainInput], axis =1)
trainInput.drop(["Position"], axis=1, inplace=True)

#converting dataframes to numpy arrays

inputNP = np.asarray(trainInput)
outputNP = np.asarray(trainOutput)

#train/test split

inpTrain, inpTest, outTrain, outTest = train_test_split(inputNP, outputNP, test_size=0.20)

#define model

##parameters - tuning still in process
nEpochs = 200
batch = 32

model = Sequential([
    Dense(64, input_shape=(18,), activation="relu"),
    BatchNormalization(),
    Dense(64,activation="relu"),
    BatchNormalization(),
    Dense(16, activation="relu"),
    BatchNormalization(),
    Dense(16, activation="relu"),
    BatchNormalization(),
    Dense(14,activation="softmax")
])

model.compile(
    optimizer="adam",
    loss = "categorical_crossentropy",
    metrics = ["accuracy"]
)

wandb.config = {
  "learning_rate": 0.001,
  "epochs": nEpochs,
  "batch_size": batch
}

#run

model.fit(inpTrain,outTrain,batch_size=batch, validation_split=0.25,verbose=2,epochs=nEpochs, callbacks=[WandbCallback()])
print(model.evaluate(inpTest, outTest, verbose=2))