import numpy as np
import wandb
import tensorflow as tf
import pandas as pd
from tensorflow.keras import layers, Sequential, optimizers, Input, Model, losses
import math

#initializing

np.set_printoptions(precision=4, suppress=True)
#wandb.init(project="FPL_Season_Data_Only_First_Try", entity="matthewlchen")

#pulling data

trainInput = pd.read_excel("FPL_Season_Data_Only_Inputs_Shuffled2.xlsx")
trainInput = trainInput.drop(trainInput.columns[0], axis=1)
trainOutput = pd.read_excel("FPL_Season_Data_Only_Outputs_Shuffled2.xlsx")
trainOutput = trainOutput.drop(trainOutput.columns[0], axis=1)
trainOutput = trainOutput.rename(columns={name: name + "Out" for name in trainOutput.columns})
outputColumns = [name for name in trainOutput.columns]
##creating big dataframe with everything
dataset = pd.concat([trainInput,trainOutput], axis=1)

#train/test split

trainData, evalData, testData = np.split(dataset.sample(frac=1),[int(0.8*len(dataset)), int(0.9*len(dataset))])

##utility function to convert pandas dataframe to tf.data.Dataset then shuffles, function adapted from https://www.tensorflow.org/tutorials/structured_data/preprocessing_layers
def df_to_dataset(dataframe, colOut, shuffle=True, batch_size=100):
  df = dataframe.copy()
  labels = pd.DataFrame()
  for i in range(len(colOut)):
      labels = pd.concat([labels,df.pop(colOut[i])], axis=1)
  df = {key: value[:,tf.newaxis] for key, value in dataframe.items()}
  ds = tf.data.Dataset.from_tensor_slices((dict(df), labels))
  if shuffle:
    ds = ds.shuffle(buffer_size=len(dataframe))
  ds = ds.batch(batch_size)
  ds = ds.prefetch(batch_size)
  return ds

##creating datasets to be fed into model
batch = 100
train_ds = df_to_dataset(trainData, outputColumns, batch_size=batch)
eval_ds = df_to_dataset(evalData, outputColumns,shuffle=False, batch_size=batch)
test_ds = df_to_dataset(testData, outputColumns, shuffle=False, batch_size=batch)

#preprocessing

inputs, encoded_features = [],[]

##encoding categorical position data

###what the name says
def get_category_encoding_layer(name, dataset, max_tokens=None):
    index = layers.IntegerLookup(max_tokens=max_tokens)
    feature_ds = dataset.map(lambda x, y: x[name])
    index.adapt(feature_ds)
    encoder = layers.CategoryEncoding(num_tokens=index.vocabulary_size())
    return lambda feature: encoder(index(feature))

###getting position encoding
position_col = Input(shape=(1,), name="Position")
encoding_layer = get_category_encoding_layer(name="Position",dataset=train_ds,max_tokens=4)
inputs.append(position_col)
encoded_features.append(encoding_layer)

##normalizing numerical features

###what the name says
def get_normalization_layer(name, dataset):
  normalizer = layers.BatchNormalization()
  #Normalization(axis=None)
  feature_ds = dataset.map(lambda x, y: x[name])
  normalizer.adapt(feature_ds)
  return normalizer
###doing the normalization
for col in trainInput.columns[1:]:
    numeric_col = Input(shape=(1,), name=col)
    normalization_layer = get_normalization_layer(col, train_ds)
    encoded_numeric_col = normalization_layer(numeric_col)
    inputs.append(numeric_col)
    encoded_features.append(encoded_numeric_col)

#yay the model!

#all_features = layers.concatenate(encoded_features)
#x = layers.Dense(32, activation="relu")(all_features)
#x = layers.Dense(16, activation="relu")(x)
#output = layers.Dense(14)(x)

#model = Model(inputs,output)

model = Sequential([
  Dense()
])

model.compile(optimizer="adam",loss=losses.binary_crossentropy(from_logits=True),metrics=["accuracy"])

tf.keras.utils.plot_model(model,show_shapes=True, rankdir="LR")

#unused stuff

#define training/testing data split

#dataSplit = 0.80
#numData = len(trainInput)
#numTest = math.floor(dataSplit*numData)
#testInput = trainInput.drop(range(0,numTest),axis=0)
#testOutput = trainOutput.drop(range(0,numTest), axis=0)
#trainInput = trainInput.drop(range(numTest, numData), axis=0)
#trainOutput = trainOutput.drop(range(numTest, numData), axis=0)

#turn input data into a tensor

#trainTensor = tf.convert_to_tensor(trainInput)
#testTensor = tf.convert_to_tensor(testInput)

#initializing feature columns

#colNames = ["Position", "Points","Minutes","I","C","T","Bonus","Bonus Points","Goals","Assists","YC","RC","Saves","CS","GC"]
#feature_columns = []
#Categorical Position Column
#position = tf.feature_column.categorical_column_with_vocabulary_list("Position", [0,1,2,3])
#feature_columns.append(tf.feature_column.embedding_column(position,4))
#Numeric Columns
#for i in range(1, len(colNames)):
    #feature_columns.append(tf.feature_column.numeric_column(colNames[i]))

#feature_columns = dict(zip(colNames, feature_columns))

#position = tf.feature_column.categorical_column_with_identity("Position", num_buckets=4)
#position_embedding= tf.feature_column.embedding_column(position, dimension=4)
#numeric_features = ["Points","Minutes","I","C","T","Bonus","Bonus Points","Goals","Assists","YC","RC","Saves","CS","GC"] 
#numeric_featureColumns = [tf.feature_column.numeric_column(feat) for feat in numeric_features]
#featureColumns = [position_embedding] + numeric_featureColumns
#feature_layer = layers.DenseFeatures(featureColumns)

#model = Sequential([
#    layers.DenseFeatures(featureColumns),
#    layers.Dense(256),
#    layers.Dense(64),
#    layers.Dense(16),
#    layers.Dense(14,activation=tf.nn.softmax)
#])

#model.compile(
#    optimizer = optimizers.Adam(),
#    loss="sparse_categorical_crossentropy",
#    metrics=["accuracy"]
#)

#model.fit(inputTensor,steps_per_epoch=1561/64)


#define training/testing data split
#dataSplit = 0.80
#numTest = math.floor(dataSplit)

#data = [[0],[1],[2],[3]]
#encoder = OneHotEncoder(sparse=False)
#onehot = encoder.fit_transform(data)
#inputData["Position"] = inputData["Position"].map(lambda Position: onehot[Position])