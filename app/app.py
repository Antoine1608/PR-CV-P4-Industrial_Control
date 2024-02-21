# Import des librairies
import pandas as pd
import numpy as np
import sys
import os
import pickle
from keras.models import load_model
import streamlit as st
st.set_page_config(layout="wide")

sys.path.append(os.path.abspath(r"C:\Users\John\Desktop\camcontrol\data\utils"))
sys.path.append(os.path.abspath(r"C:\Users\John\Desktop\camcontrol\src\utils"))

from img_to_excel_func import imgtoexcel
from helper_functions import *

# Titre de la page
st.title("Détection de défauts")

# Le dossier source des images

image_dir = st.sidebar.text_input(r"répertoire des images (exemple : C:\Users\John\Desktop\camcontrol\data\train)")
# Exemple : C:\Users\John\Desktop\camcontrol\data\train

# Le document excel de sortie

result_doc = st.sidebar.text_input(r"document de sortie (exemple : C:\Users\John\Desktop\camcontrol\data\train_excel.xlsx)")

# Le bouton de prédiction

if st.button("Analyse des images"):
    model = load_model(r"C:\Users\John\Desktop\camcontrol\models\model_best_weights.h5")
    data = imgtoexcel(image_dir, result_doc)   
    
    preprocessing_entry = preprocess_input
    test_flow = define_flow(data, preprocessing_entry)
    y_pred_cat, y_pred = performance_test(data, model, test_flow)

    df = data.copy()
    df['pred'] = y_pred_cat
    df.to_excel(result_doc, index=False)
    for img_path in df.loc[df['pred']=='nc','Image_Path'].tolist():
        img = cv2.imread(img_path)
        img = cv2.resize(img, (256,256))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        st.text(img_path)
        st.image(img)
