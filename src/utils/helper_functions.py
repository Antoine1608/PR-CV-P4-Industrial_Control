import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
from tqdm import tqdm
from time import time
import math

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import label_binarize, LabelEncoder
from sklearn.utils import class_weight, shuffle
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score

from tensorflow.keras.models import Model, Sequential
from keras.preprocessing.image import ImageDataGenerator
from keras.applications.vgg16 import VGG16
from keras.models import Sequential
from keras.layers import Dense, Dropout, GlobalAveragePooling2D
from keras.optimizers import Adam
from keras.callbacks import ModelCheckpoint, EarlyStopping
from keras.utils import to_categorical

import tensorflow as tf
from tensorflow.keras.preprocessing import image
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.applications.vgg16 import preprocess_input
from tensorflow.keras.optimizers import SGD

# For normalization
import cv2
from skimage.exposure import match_histograms

# Data augmentation function for train-val
def data_flow_fct(data, datagen, data_type=None, batch_size=None) :

    data_flow = datagen.flow_from_dataframe(data,
                                            #directory=dir_, # Pas besoin
                                            x_col='Image_Path',  # Utilisez 'image_path' comme colonne des chemins d'images
                                            y_col='Label',#_name',
                                            weight_col=None,
                                            target_size=(224, 224),
                                            classes=None,
                                            class_mode='categorical',
                                            batch_size=batch_size,
                                            shuffle=False,
                                            seed=42,
                                            subset=data_type)
    return data_flow

# Data augmentation function
def datagen_trainer(preprocessing_input):
    datagen_train = ImageDataGenerator(
    #    featurewise_center=True,
    #    featurewise_std_normalization=True,
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        horizontal_flip=True,
        validation_split=0.25,# détermine le ration training/validation
        preprocessing_function=preprocessing_input)
    return datagen_train

def datagen_tester(preprocessing_input):
    datagen_test = ImageDataGenerator(
        validation_split=0,
        preprocessing_function=preprocess_input)
    return datagen_test

# Model creation function
def create_model_fct(nb_lab) :
    #weights_path = "/kaggle/input/vgg16-weights/vgg16_weights_tf_dim_ordering_tf_kernels_notop.h5" # ATTENTION : activer hors connexion
    weights_path = 'imagenet'
    # Charger le modèle VGG16 pré-entraîné
    model0 = VGG16(include_top=False, weights=weights_path, input_shape=(224, 224, 3)) 
    
    # Layer non entraînables = on garde les poids du modèle pré-entraîné
    for layer in model0.layers:
        layer.trainable = False

    # Récupérer la sortie de ce réseau
    x = model0.output
    # Compléter le modèle
    x = GlobalAveragePooling2D()(x)
    x = Dense(224, activation='relu')(x)
    x = Dropout(0.5)(x)
    predictions = Dense(nb_lab, activation='softmax')(x)

    # Définir le nouveau modèle
    model = Model(inputs=model0.input, outputs=predictions)
       
    # compilation du modèle 
    model.compile(loss="categorical_crossentropy", optimizer=optimizer_dic[1], metrics=["accuracy"])

    print(model.summary())
    
    return model

# Step flow definition
def define_flow(data, preprocessing_flow):
    # Data augmentation for train-val
    test_flow = data_flow_fct(data, datagen_tester(preprocessing_flow), data_type=None, batch_size=1)
    return test_flow

# Step model creation and training
def model_creation_training(train_flow, val_flow,epochs_entry):
    # 4min35 for epochs = 1 and batch_size = 32
    # Model creation and training
    with tf.device('/gpu:0'):

        # Model creation
        print('1/3-Model creation')
        model = create_model_fct(nb_lab)

        # Call back creation
        print('2/3-Callbacks')
        model_save_path = r"C:\Users\John\Desktop\camcontrol\models\model_best_weights.h5"
        checkpoint = ModelCheckpoint(model_save_path, monitor='val_accuracy', verbose=1, mode='max', save_best_only=True)
        es = EarlyStopping(monitor='val_accuracy', mode='max', verbose=1, patience=10)
        callbacks_list = [checkpoint, es]

        # Training
        print('3/3-Training')
        history = model.fit(train_flow, epochs=epochs_entry, 
                            steps_per_epoch=len(train_flow),
                            callbacks=callbacks_list, 
                            validation_data=val_flow,
                            validation_steps=len(val_flow),
                            verbose=1)
    return model, history

# Step performance train_val
def performance_train_val(history, model, val_flow, batch_size_entry):
    # Performances
    print('1/6-val accuracy/epochs')
    show_history(history)
    plot_history(history, path=r"C:\Users\John\Desktop\camcontrol\reports\history_train_val.png")
    plt.close()

    print('2/6-predicting y_pred')
    #1min 28 for batch_size = 32
    y_pred = model.predict(val_flow, steps=len(val_flow), batch_size=batch_size_entry)

    print('3/6-getting y_val')
    nombre_total_val = len(val_flow) * batch_size_entry

    # Initialisation d'un tableau pour stocker les étiquettes réelles
    y_val = np.zeros((nombre_total_val, nb_lab))  

    # Itérer sur le générateur pour extraire les étiquettes réelles
    for i in range(len(val_flow)):
        _, batch_y_val = val_flow[i]  # Supposons que le générateur génère des paires (X_val, y_val)
        start_index = i * batch_size_dic[1]
        end_index = start_index + len(batch_y_val)
        y_val[start_index:end_index] = batch_y_val

    print('4/6-building the basic confusion matrix')
    # Obtenez les indices des classes prédites et réelles pour les échantillons disponibles
    y_val_indices = y_val.argmax(axis=1)[0:len(y_pred)]
    y_pred_indices = y_pred.argmax(axis=1)

    # Générer la matrice de confusion
    cm = confusion_matrix(y_val_indices, y_pred_indices)

    # Afficher la matrice de confusion
    print(cm)

    # Afficher le rapport de classification
    print("\n5/6-building the classification report")
    print(classification_report(y_val.argmax(axis=1)[0:len(y_pred)], y_pred.argmax(axis=1)))

    print('6/6-building the sns confusion matrix')
    # Finding the matching categorical labels for the numerical labels
    list_num_labels = sorted([x for x in set(y_val_indices)|set(y_pred_indices)])
    list_cat_labels = le.inverse_transform(list_num_labels)

    # Proceeding with sns
    df_cm = pd.DataFrame(cm, index=list_cat_labels, columns=list_cat_labels)

    plt.figure(figsize=(6, 4))
    ax = sns.heatmap(df_cm, annot=True, cmap="Blues")

    # Ajouter des étiquettes aux axes
    ax.set_xlabel("Prediction")
    ax.set_ylabel("True")
    ax.set_title("confusion matrix train_val")
    # Sauvegardez l'image dans un fichier
    plt.savefig(r'C:\Users\John\Desktop\camcontrol\reports\confusion_matrix_train_val.png')

    plt.show()

# Step performance test
# Performance
def performance_test(data, model, test_flow):

    # Class list
    le = LabelEncoder()
    le.fit_transform(['c','nc','t','unknown'])
    
    print('getting y_pred')
    # Testing on whole dataset
    #y_pred = model.predict(images_np)
    y_pred = model.predict(test_flow, steps=len(test_flow), batch_size=1)

    print('4/6-building the basic confusion matrix')
    # get y_val and y_pred
    y_pred_indices = y_pred.argmax(axis=1)
    y_pred_cat = le.inverse_transform(y_pred_indices)

    return y_pred_cat, y_pred
