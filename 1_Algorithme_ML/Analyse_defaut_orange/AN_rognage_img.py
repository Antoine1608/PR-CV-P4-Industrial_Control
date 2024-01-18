import os, time, AN_perf
from PIL import Image
import math

@AN_perf.AN_pf
def crop_img(from_dir, list_bornes):
    
    for im in os.listdir(from_dir) :
        try:
            name=str(from_dir)+'/'+str(im)
            os.chdir(from_dir)
            ima = Image.open(im,"r")             
            width, height = ima.size                
            left_ = float(list_bornes[0])*width 
            top_ = float(list_bornes[1])*width 
            right_ = float(list_bornes[2])*height 
            bottom_ = float(list_bornes[3])*height 
            im1 = ima.crop((left_, top_, right_, bottom_))
            im1.save(name)
            
        except:
            print(f'exception lors du rognage des images avec le fichier {im}')
            continue

#lst_rognage=['0.1','0.1','0.9','0.9']
#crop_img('C:/Users/yannw/OneDrive/Bureau/analyse_defaut_orange/data IN', lst_rognage)



    
    
