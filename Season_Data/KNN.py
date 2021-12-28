import pandas as pd
from sklearn.neighbors import KNeighborsRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error 
from math import sqrt
from sklearn.preprocessing import MinMaxScaler

trainInput = pd.read_excel("FPL_Season_Data_Only_Inputs_Shuffled2.xlsx")
trainInput = trainInput.drop(trainInput.columns[0], axis=1)
trainOutput = pd.read_excel("FPL_Season_Data_Only_Outputs_Shuffled2.xlsx")
trainOutput = trainOutput.pop("Points")

#position = pd.get_dummies(trainInput["Position"],prefix="Position")
#trainInput = pd.concat([position,trainInput], axis =1)
trainInput.drop(["Position"], axis=1, inplace=True)
trainInput.drop(["YC"], axis=1, inplace=True)
trainInput.drop(["RC"], axis=1, inplace=True)
trainInput.drop(["Bonus Points"], axis=1, inplace=True)

df = pd.read_excel("PredictionsData.xlsx")
#position = pd.get_dummies(df["Position"],prefix="Position")
#df = pd.concat([position,df], axis =1)
df.drop(["Position"], axis=1, inplace=True)
df.drop(["YC"], axis=1, inplace=True)
df.drop(["RC"], axis=1, inplace=True)
df.drop(["Bonus Points"], axis=1, inplace=True)
names = df.pop("Name")

trainIn, testIn,trainOut, testOut = train_test_split(trainInput, trainOutput, test_size = 0.2)
scaler = MinMaxScaler(feature_range=(0, 1))

trainIn = scaler.fit_transform(trainIn)
trainIn = pd.DataFrame(trainIn)

testIn = scaler.fit_transform(testIn)
testIn = pd.DataFrame(testIn)

# rmse_val=[]
# for K in range(30):
#     K = K+1
#     model = KNeighborsRegressor(n_neighbors = K)

#     model.fit(trainIn, trainOut)  #fit the model
#     pred=model.predict(testIn) #make prediction on test set
#     error = sqrt(mean_squared_error(testOut,pred)) #calculate rmse
#     rmse_val.append(error) #store rmse values
#     print('RMSE value for k= ' , K , 'is:', error)
#k=26
model = KNeighborsRegressor(n_neighbors = 13)
model.fit(trainInput, trainOutput)
predictions = model.predict(df)
predictionsDF = pd.DataFrame(predictions, columns=["Points"])
predictionsDF = pd.concat([names, predictionsDF],axis=1)
predictionsDF.sort_values("Points",ascending=False, inplace=True)
predictionsDF.to_excel("PredictionsKNNwithoutPosition.xlsx")

# import numpy as np
# import tensorflow as tf
# import pandas as pd
# import wandb

# from wandb.keras import WandbCallback

# #initializing
# np.set_printoptions(precision=4, suppress=True)
# wandb.init(project="RandomForest", entity="matthewlchen",sync_tensorboard=True)
# #pulling data

# trainInput = pd.read_excel("FPL_Season_Data_Only_Inputs_Shuffled2.xlsx")
# trainInput = trainInput.drop(trainInput.columns[0], axis=1)
# trainOutput = pd.read_excel("FPL_Season_Data_Only_Outputs_Shuffled2.xlsx")
# trainOutput = trainOutput.pop("Points")

# #transforming categorical position data into one hot encoding

# position = pd.get_dummies(trainInput["Position"],prefix="Position")
# trainInput = pd.concat([position,trainInput], axis =1)
# trainInput.drop(["Position"], axis=1, inplace=True)

# #converting dataframes to numpy arrays

# inputNP = np.asarray(trainInput)
# outputNP = np.asarray(trainOutput)

# #train/test split

# #inpTrain, inpTest, outTrain, outTest = train_test_split(inputNP, outputNP, test_size=0.20)

# #define model

# ##parameters - tuning still in process
# nEpochs = 100
# batch = 32

# model = 

# model.compile(
#     optimizer="adam",
#     loss = "mean_squared_error",
#     metrics = ["accuracy"]
# )

# wandb.config = {
#   "learning_rate": 0.001,
#   "epochs": nEpochs,
#   "batch_size": batch
# }

# #run

# model.fit(inputNP,outputNP,batch_size=batch, validation_split=0.20,verbose=2,epochs=nEpochs, callbacks=[WandbCallback()])

# #model.save_weights("weights")
# #print(model.evaluate(inpTest, outTest, verbose=2))