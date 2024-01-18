#0-LES MODULES :

import shutil, os, subprocess, time, csv
import datetime

#pour l'étape 5 :
import smtplib
import pandas as pd
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
from tqdm import tqdm
from PIL import Image

#1-LES CHEMINS :
#chemin vers le cloud-serveur :
dataorange = 'C:/Users/yannw/OneDrive/Bureau/dataorange'
#chemin vers le dossier des images en entrée d'Orange :
data_IN = 'C:/Users/yannw/OneDrive/Bureau/analyse_defaut_orange/data IN'
#cheminversledossier d'analyse des défauts
data_defaut="C:\\Users\\yannw\\OneDrive\\Bureau\\analyse_defaut_orange"
#chemin vers le dossier en sortie d'Orange :
data_exit = 'C:/Users/yannw/OneDrive/Bureau/analyse_defaut_orange/data OUT'
#chemin vers le dossier du tableau en sortie d'Orange :
data_out = 'C:/Users/yannw/OneDrive/Bureau/analyse_defaut_orange/data OUT/_data_out.csv'

#2-LES VARIABLES :
#le nombre de boucle du progamme
nb_loop = 1
#le nombre d'images traitées :
nb_fich = 3300

#l'ensemble des défauts (voir L142) :
#ens_df = {'test','8HP65 1-30','8HP65 1-71','8HP65 2-68','8HP65 2-70','8HP65 3-47','8HP65 4-82','8HP65 5-52','8HP65 5-54','8HP65 6-91','8HP95 1-49-50-60-61','8HP95 3-36','8HP95 3-47-58','Datamatrix','Traça grille'}
#ens_df = {'_1-53','test'}

#les coordonnées d'envoi et de réception
sender_email = "anaudy@eurocast.fr"
#receiver_email = "anaudy@eurocast.fr"
sender_code = "LpCdt@dcX!aVY3F8"

#pour l'étape 4 (création d'un message):
message =['Bonjour,\n\n']
#la liste des images suspectes pour l'écriture du message :
img_s=[]
#l'ensemble data_IN archive initial
ens_data_IN_jpg_archive=set(os.listdir(data_IN))

#-LES FONCTIONS :

#fonction de traitement des images :

def datetime_to_float(d):
    return d.timestamp()

def recup():
    try :
        lst_modif=[]
        lst_fic = list(os.listdir(dataorange))
        lst_nm =[]
        os.chdir(dataorange)
        for i in range(len(lst_fic)):
            tps = time.ctime(os.path.getmtime(lst_fic[i]))
            tps = datetime.datetime.strptime(tps, "%a %b %d %H:%M:%S %Y")            
            lst_modif.append(tps)
            nm=str(lst_fic[i])
            lst_nm.append(nm)
        df=pd.DataFrame(list(zip(lst_nm, lst_modif)),columns = ['nom','date_import'])
        df2=df[df['nom'].astype(str).str.contains('jpg')]
        df3=df2.sort_values(by=['date_import'], ascending=False)
        lst_nm2=df3.nom[0:nb_fich].tolist()
        return(lst_nm2)
    except:
        print('impossible de récupérer les images de dataorange')
        lst_nm2=[]
        return (lst_nm2)          

def etape_2():
    print('traitement des images...')
    from datetime import datetime
    _deb_Orange = datetime_to_float(datetime.now())
    os.chdir(data_defaut)
    p = subprocess.Popen(["start", "cmd", "/k", "Analyse_images.ows"], shell = True)
    _fin_Orange = os.path.getmtime(data_out)
    processtime = _fin_Orange-_deb_Orange
    try:
    #boucle pour fermer Orange à la fin du traitement :
        while processtime<0:
            _fin_Orange = os.path.getmtime(data_out) #comment l'empêcher de bloque là
            processtime = _fin_Orange-_deb_Orange
        print('temps de traitement orange: ',_fin_Orange-_deb_Orange)
        os.popen('taskkill /fi "windowtitle eq Analyse_images.ows*"')           
        #temps de latence nécessaire sinon on passe à l'étape 3 sans que le tableau soit complètement enregistré (2s n'est peut-être pas suffisant)
        time.sleep(2)
    except:
        print('erreur lors du traitement des images (dat_out.csv ouvert ?)')
        exit()
  
 
#fonction d'envoi de l'email :
def send_email(mail, image):
    # bien penser à baisser la sécurité sur "Accès moins sécurisé des applications"
    #sur gmail
    # on rentre les renseignements pris sur le site du fournisseur

    os.chdir(dataorange)    
    msg = MIMEMultipart()
    msg['Subject'] = '[Defaut detecte]'
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msgText = MIMEText(mail[0]+mail[1])
    msg.attach(msgText)
    try:
        with open(image, 'rb') as fp:
            img = MIMEImage(fp.read())
            img.add_header('Content-Disposition', 'attachment', filename=image)
            msg.attach(img)                
        try:
            with smtplib.SMTP('smtp.office365.com', 587) as smtpObj:
                smtpObj.ehlo()
                smtpObj.starttls()
                smtpObj.login(sender_email, sender_code)
                smtpObj.sendmail(sender_email, receiver_email.split(","), msg.as_string())
                #ens_data_IN_jpg_archive=ens_data_IN_jpg_archive.union(ens_dataorange_jpg_nv) #problème ici
                print('mise à jour de l\'archive')                
        except Exception as e:
            print('erreur dans l\'envoi du message (connexion internet ?) - pas de mise à jour de l\'archive')        
    except :
        print('pas d\'image, pas d\'envoi d email')

#CORPS PRINCIPAL
j=1
while j<=nb_loop:    
    print('la boucle n°',j,'commence...')

#ETAPE 0 : initialisation des adresses email et de l'ensemble des intitulés défauts
    fichier = open('C:/Users/yannw/OneDrive/Bureau/analyse_defaut_orange/parametres.txt', 'r')
    fichier_texte = fichier.readlines()
    receiver_email = fichier_texte[1]
    #ens_df = fichier_texte[3]
    ens_df ={'Test','Defaut_1'}
    
#ETAPE 1 : récupération des images
    print('préparation de la récupération des images...')
    _deb_recup = time.time()
    try :
        os.chdir(data_IN)
        ens_data_IN_jpg=set(os.listdir(data_IN))
        liste_recup=recup()
        os.chdir(data_IN)
        ens_dataorange_jpg=set(liste_recup)
        ens_dataorange_jpg_nv=ens_data_IN_jpg_archive.union(ens_dataorange_jpg)-ens_data_IN_jpg_archive
        #tant que l'ens orange ne contient que des images qui sont déjà dans ens IN archives =>tourne en boucle
        while len(ens_dataorange_jpg_nv)==0:
            print('pas d\'images à récupérer pour le moment...')
            time.sleep(1)
            #mise àjour de l'ens orange avant de reprendre la boucle while
            ens_data_IN_jpg=set(os.listdir(data_IN))            
            liste_recup=recup()
            os.chdir(data_IN)
            ens_dataorange_jpg=set(liste_recup)            
            ens_dataorange_jpg_nv=ens_data_IN_jpg_archive.union(ens_dataorange_jpg)-ens_data_IN_jpg_archive
        #sinon l'ens_data_IN devient l'ensemble des nouvelles images
        ens_data_IN_jpg = ens_dataorange_jpg_nv
        print('des images ont été répertoriées...')        
        #ensuite on vide le dossier data_IN
        c_liste_1 = os.listdir(data_IN)
        for i in tqdm(range(len(c_liste_1))):
            if c_liste_1[i].endswith ('.jpg'):
                try:
                    os.remove(c_liste_1[i])
                except:
                    continue
        print('dossier d\'enregistrement des images "data_IN" vidé avant récupération : \n', os.listdir(data_IN))
        #et on le remplit des nouvelles images
        c_liste_2 = list(ens_dataorange_jpg_nv)
        print(f'récupération de {len(c_liste_2)} fichiers de "dataorange" dans "data_IN"...')
        os.chdir(dataorange)
        for _name_file in c_liste_2:
            if _name_file.endswith('.jpg'):
                shutil.copy2(_name_file, data_IN)                                
        print(f'{len(os.listdir(data_IN))} images récupérées dans "data_IN" : \n', os.listdir(data_IN))
    except :
        print ('erreur lors de la récupération des images - impossible de copier un fichier de dataorange')
        continue
    #on rogne les images        
    liste_img = os.listdir(data_IN)    
    for im in liste_img :
        try:
            #name = str(f'C:/Users/yannw/OneDrive/Bureau/Data_IN/{im}')
            name=str(data_IN)+'/'+str(im)
            os.chdir(data_IN)
            # Opens a image in RGB mode
            ima = Image.open(im,"r")             
            # Size of the image in pixels (size of original image)
            # (This is not mandatory)
            width, height = ima.size                
            # Setting the points for cropped image - swap width and height sometimes !!!
            left_ = fichier_texte[5].rstrip()
            top_ = fichier_texte[6].rstrip()
            right_ = fichier_texte[7].rstrip()
            bottom_ = fichier_texte[8].rstrip()
            corres ={'xA':0,'xB':(width/3),'xC':(2*width/3),'xD':width,'y1':0,'y2':(height/3),'y3':(2*height/3),'y4':height}
            left=corres[left_]
            top=corres[top_]
            right=corres[right_]
            bottom=corres[bottom_] 
            # Cropped image of above dimension
            # (It will not change original image)
            im1 = ima.crop((left, top, right, bottom))
            # Shows the image in image viewer
            #im1.show()
            #os.chdir('C:/Users/yannw/OneDrive/Bureau')
            im1.save(name)            
        except:
            print('exception lors du rognage des images')
            pass
            

#ETAPE 2 : vérifie s'il y a des images dans data_in et lance orange et donne le temps passé pour modifier _data_out.xls
    _fin_recup =time.time()
    print('durée de récupération : ',_fin_recup-_deb_recup)

    if any(file.endswith('.jpg') for file in os.listdir(data_IN)):
        etape_2()
    else:
        try:
            with open(data_out,'w') as f:
                pass
        except OSError as e:
            print('étape 2', e)


#ETAPE 3 : fait deux listes de deux colonnes de data_out avec le nom de l'image en valeur et son statut en clé
    _nom_defaut=[]
    _nom_image=[]    
    try :        
        with open(data_out, newline='') as f:
            print('vérification de la présence de défauts dans les images traitées...')            
            reader = csv.reader(f, delimiter=',')            
            for col in reader:
            #faire un except quand il n'y a plus rien dans la col 1006               
                _nom_image.append(col[1002]) #n°0 = 1ére colonne
                _nom_defaut.append(col[1006]) #n°1 = 2eme colonne
        intersection=set(_nom_defaut)&ens_df
        if len(intersection)==0:
            print('pas de défauts répertoriés')
            print('les types de défauts répertoriés sont', intersection)                        
        else:
            print('des défauts ont été répertoriés, préparation des emails à envoyer...')
            print('les types de défauts répertoriés sont', intersection)
    except OSError as e:
        print('étape 3', e)                           
                       
#ETAPE 4 : crée un texte de message avec le nom de l'image et le type de défaut et envoi lemassage avec l'image attachée par email           
    os.chdir(data_IN)
    for i in tqdm(range(len(_nom_defaut))):       
        if _nom_defaut[i] in ens_df and not _nom_image[i]=='':            
            message.append('Un defaut type '+ _nom_defaut[i] + ' a été détecté sur l\'image ' + _nom_image[i])
            img_s.append(_nom_image[i])        
            send_email(message, _nom_image[i])
            print('tentative d\'envoi message:\n',message[1])
            message = ['Bonjour,\n\n']

#ETAPE 5 : ferme la fenêtre de commande résiduelle et vide img_s                           
    os.popen('taskkill /fi "windowtitle eq C:\WINDOWS\system32\cmd.exe"')
    time.sleep(5)
    img_s =[]
    c_liste_1=[]
    ens_data_IN_jpg_archive=ens_data_IN_jpg_archive | set(os.listdir(data_IN))
    print(f'fin de la boucle {j} - archive :\n', ens_data_IN_jpg_archive,'\nnombre de fichiers dans l\'archive :\n',len(ens_data_IN_jpg_archive))
    j=j+1
os.popen('taskkill /fi "windowtitle eq C:\WINDOWS\system32\cmd.exe"')

