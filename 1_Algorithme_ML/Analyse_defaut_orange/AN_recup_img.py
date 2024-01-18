import os, time, AN_perf, pandas as pd, datetime, shutil

def recup(from_dir, nb_sample):
    try :
        lst_from_dir = os.listdir(from_dir)
        lst_tps_modif=[]
        lst_recup_cloud =[]

        os.chdir(from_dir)

        for i in range(len(lst_from_dir)):
            tps_modif=datetime.datetime.fromtimestamp(os.path.getmtime(lst_from_dir[i]))
            lst_tps_modif.append(tps_modif)
            lst_recup_cloud.append(lst_from_dir[i])

        df_nom_date=pd.DataFrame(list(zip(lst_recup_cloud, lst_tps_modif)),columns = ['nom','date_import'])
        df_nom_date_jpg=df_nom_date[df_nom_date['nom'].astype(str).str.contains('jpg')]
        df_nom_date_jpg_tri=df_nom_date_jpg.sort_values(by=['date_import'], ascending=False)
        lst_recup_cloud_jpg_tri=df_nom_date_jpg_tri.nom[0:nb_sample].tolist()
        return(lst_recup_cloud_jpg_tri)

    except:
        print('impossible de récupérer les images de from_dir')
        lst_recup_cloud_jpg_tri=[]
        print('i: ', i)
        return (lst_recup_cloud_jpg_tri)
        
@AN_perf.AN_pf
def recup_img(from_dir, to_dir, nb_sample, ens_memory):
    print('préparation de la récupération des images...')
    _deb_recup = time.time()
    try :
        #ens_to_dir=set(os.listdir(to_dir))
        list_recup_cloud_jpg_sorted_sample=recup(from_dir,nb_sample)

        os.chdir(to_dir)

        ens_from_dir_jpg=set(list_recup_cloud_jpg_sorted_sample)
        ens_from_dir_jpg_nv=ens_memory.union(ens_from_dir_jpg)-ens_memory
        #tant que l'ens orange ne contient que des images qui sont déjà dans l'ens_memory =>tourne en boucle
        while len(ens_from_dir_jpg_nv)==0:
            print('pas d\'images à récupérer pour le moment...')
            time.sleep(1)
            #mise àjour de l'ens orange avant de reprendre la boucle while
            #ens_to_dir=set(os.listdir(to_dir))            
            list_recup_cloud_jpg_sorted_sample=recup(from_dir,nb_sample)

            os.chdir(to_dir)

            ens_from_dir_jpg=set(list_recup_cloud_jpg_sorted_sample)            
            ens_from_dir_jpg_nv=ens_memory.union(ens_from_dir_jpg)-ens_memory

        #sinon l'ens_to_dir devient l'ensemble des nouvelles images
        #ens_to_dir = ens_from_dir_jpg_nv
        print('des images ont été répertoriées...')        

        #ensuite on vide le dossier to_dir
        list_to_dir = os.listdir(to_dir)
        for i in range(len(list_to_dir)):
            if list_to_dir[i].endswith ('.jpg'):
                try:
                    os.remove(list_to_dir[i])
                except:
                    continue
        print('dossier d\'enregistrement des images "to_dir" vidé avant récupération : \n', os.listdir(to_dir))
        #et on le remplit des nouvelles images
        list_from_dir_jpg_nv = list(ens_from_dir_jpg_nv)
        print(f'récupération de {len(list_from_dir_jpg_nv)} fichiers de "from_dir" dans "to_dir"...')

        os.chdir(from_dir)

        for _name_file in list_from_dir_jpg_nv:
            if _name_file.endswith('.jpg'):
                shutil.copy2(_name_file, to_dir)                                
        print(f'{len(os.listdir(to_dir))} images récupérées dans "to_dir" : \n', os.listdir(to_dir))
    except :
        print ('erreur lors de la récupération des images - impossible de copier un fichier de from_dir')

