import pandas as pd
import os
import shutil
import openpyxl
from openpyxl.drawing.image import Image
import PIL
import cv2
from datetime import datetime, timedelta
from tqdm import tqdm

# Définissons l'emplacement des différents dossiers et fichiers
# Le dossier où sont stockées les images d'entraînement
#dir_img = r"C:\Users\John\Desktop\camcontrol\data\train"
# Le tableau des données d'entraînement
#dataset_img = r"C:\Users\John\Desktop\camcontrol\data\train.xlsx"
def imgtoexcel(dir_img, dataset_img) :
    ''' sauvegarde dans un document xlsx dataset_img un tableau avec des thumbnails des images de dir_img 
    et retourne le dtaframe correspondant '''
    # Initions un df d'entraînement
    df = pd.DataFrame( {
        'Image_Path': [], #image_path,
        'Image_Size': [], #os.path.getsize(image_path),  # Taille de l'image en octets.
        'Image_Width': [], #image.width,  # Largeur de l'image en pixels.
        'Image_Height': [], #image.height,  # Hauteur de l'image en pixels.
        'Image_Mode': [], #image.mode,  # Mode de couleur de l'image (par exemple : "RGB", "L", etc.).
        'Image_Format': [], #image.format,  # Format de l'image (par exemple : "JPEG", "PNG", etc.).
        'Date_Modified': [], #os.path.getmtime(image_path),  # Date de modification du fichier de l'image.
        'Thumbnail' : [],
        'Label': []
    } )
    df
    
    # Remplissons le df avec les données des images d'entraînement
    for img in tqdm([img for img in os.listdir(dir_img) if not img.startswith('.ipynb')]):
        image_path = os.path.join(dir_img,img)
        image = PIL.Image.open(image_path)
        list_row = [image_path, os.path.getsize(image_path), image.width, image.height, image.mode, image.format, os.path.getmtime(image_path), 'img','unknown']
        df.loc[len(df)] = list_row
    df.head()

    df['Label'] = 'none'
    
    # On exporte le df vers data_set_train.xls
    df.to_excel(dataset_img, index=False)
    
    # On va rajouter un thumbnail à chaque ligne
    # 1-Instanciation un objet Openpyxl de data_set_train.xls
    try:
        # On essaie d'ouvrir le fichier Excel s'il existe déjà.
        file_path = dataset_img
        workbook = openpyxl.load_workbook(file_path)
        #print(f"Fichier Excel existant ouvert : {file_path}")
        
    except FileNotFoundError:
        print("fichier non trouvé")
    
    worksheet = workbook.active
    
    # 2-On ajoute les thumbnails dans le document Openpyxl
    for idc, image_path in tqdm(enumerate(df['Image_Path'])):
        # Resize cells ligne idx+2
        worksheet.row_dimensions[idc+2].height = 50
    
        # Collage du thumbnail sur la cellule colonne Hde la ligne idx+2
        # la première ligne qui contient les en-têtes des colonnes provoquent une exception
        try : 
            img = cv2.imread(df.iloc[idc,0])
        except :
            continue
        img = cv2.resize(img, (50, 50))
        # On sauvegarde l'image.son nom est img suivi de l'indice de la ligne où elle est collée
        img = cv2.imwrite(f'img{idc+2}.png', img)
         
        worksheet.add_image(Image(f'img{idc+2}.png'), anchor=f'H{idc+2}')#il faut que Image soit un objet Openpyxl et non pas PIL       
    
    # 3-Sauvegarde du document data_set_train.xls avec ses thumbnails prêt à une labellisation manuelle
    workbook.save(dataset_img)
    workbook.close()

    # 4-On nettoie le dossier des images temporaires créées
    for img in [img for img in os.listdir(os.getcwd()) if img.startswith('img')]:
        os.remove(img)


    return pd.read_excel(dataset_img)

