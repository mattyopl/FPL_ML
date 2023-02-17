import numpy as np
import tensorflow as tf
import pandas as pd
import wandb
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, BatchNormalization
from tensorflow.keras import optimizers
from wandb.keras import WandbCallback

##parameters - tuning still in process
nEpochs = 50
batch = 32

#initializing
np.set_printoptions(precision=4, suppress=True)
wandb.init(project="SecondTryDeep", entity="matthewlchen",sync_tensorboard=True, name="Test2", config = {
  "learning_rate": 0.002,
  "epochs": nEpochs,
  "batch_size": batch
})

#pulling data

trainInput = pd.read_excel("FPL_Season_Data_Only_Inputs_Shuffled2.xlsx")
trainInput = trainInput.drop(trainInput.columns[0], axis=1)
trainOutput = pd.read_excel("FPL_Season_Data_Only_Outputs_Shuffled2.xlsx")
trainOutput = trainOutput.pop("Points")

#transforming categorical position data into one hot encoding

position = pd.get_dummies(trainInput["Position"],prefix="Position")
trainInput = pd.concat([position,trainInput], axis =1)
trainInput.drop(["Position"], axis=1, inplace=True)
trainInput.drop(["YC"], axis=1, inplace=True)
trainInput.drop(["RC"], axis=1, inplace=True)
trainInput.drop(["Bonus Points"], axis=1, inplace=True)

# for column in trainInput.columns:
#     trainInput[column] = trainInput[column]  / trainInput[column].abs().max()

#converting dataframes to numpy arrays

inputNP = np.asarray(trainInput)
outputNP = np.asarray(trainOutput)

#train/test split

#inpTrain, inpTest, outTrain, outTest = train_test_split(inputNP, outputNP, test_size=0.20)

#define model



model = Sequential([
    Dense(256, input_shape=(15,), activation="relu"),
    BatchNormalization(),
    Dense(256,activation="relu"),
    BatchNormalization(),
    Dense(128,activation="relu"),
    BatchNormalization(),
    Dense(128,activation="relu"),
    BatchNormalization(),
    Dense(64,activation="relu"),
    BatchNormalization(),
    Dense(64,activation="relu"),
    BatchNormalization(),
    Dense(32,activation="relu"),
    BatchNormalization(),
    Dense(16,activation="relu"),
    BatchNormalization(),
    Dense(1,activation="relu")
])

model.compile(
    optimizer=optimizers.Adam(learning_rate=0.002),
    loss = "mean_squared_error",
    metrics = ["accuracy"]
)

#run

model.fit(inputNP,outputNP,batch_size=batch, validation_split=0.3,verbose=2,epochs=nEpochs, callbacks=[WandbCallback()])

# df = pd.read_excel("PredictionsData.xlsx")
# position = pd.get_dummies(df["Position"],prefix="Position")
# df = pd.concat([position,df], axis =1)
# df.drop(["Position"], axis=1, inplace=True)
# names = df.pop("Name")

# inputNP = np.asarray(df)
# df.drop(["YC"], axis=1, inplace=True)
# df.drop(["RC"], axis=1, inplace=True)
# df.drop(["Bonus Points"], axis=1, inplace=True)
# predictions = model.predict(df)
# predictions = pd.DataFrame(predictions, columns=["Points"])
# predictions = pd.concat([names, predictions], axis =1)
# predictions.to_excel("Predictions2.xlsx")


#model.save_weights("weights")
#print(model.evaluate(inpTest, outTest, verbose=2))