import csv,os, AN_perf

#@AN_perf.AN_pf
def evaluation(csv_result, set_defaut, from_dir):
    _nom_defaut=[]
    _nom_image=[]
    lst_evaluation=[]
    try :        
        with open(csv_result, newline='') as f:
            print('vérification de la présence de défauts dans les images traitées...')            
            reader = csv.reader(f, delimiter=',')            
            for col in reader:
                _nom_image.append(col[1002]) 
                _nom_defaut.append(col[1006]) 
        intersection=set(_nom_defaut)&set_defaut
        if len(intersection)==0:
            print('pas de défauts répertoriés')
        else:
            print('les types de défauts répertoriés sont :\n', intersection)
    except :
        print('erreur pendant l\'étape d\'évaluation')                         
                       
    #ETAPE 4 : crée un texte de message avec le nom de l'image et le type de défaut et envoi le message avec l'image attachée par email           
    os.chdir(from_dir)
    for i in range(len(_nom_defaut)):       
        if _nom_defaut[i] in set_defaut and not _nom_image[i]=='':
            lst_evaluation.append([str('Un defaut type '+ _nom_defaut[i] + ' a été détecté sur l\'image ' + _nom_image[i]),_nom_image[i]])

    return lst_evaluation

#evaluation('C:/Users/yannw/OneDrive/Bureau/analyse_defaut_orange/data OUT/_data_out.csv',{'Test','8HP65 1-71'}, 'C:/Users/yannw/OneDrive/Bureau/analyse_defaut_orange/data IN')
