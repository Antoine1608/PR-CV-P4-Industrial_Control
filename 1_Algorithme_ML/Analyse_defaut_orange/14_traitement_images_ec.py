import AN_recup_img,AN_lance_orange, AN_evaluation, AN_send_mail, AN_perf, os

import AN_rognage_img

from_dir='C:/Users/yannw/OneDrive/Bureau/analyse_defaut_orange/data IN'
from_orange='C:/Users/yannw/OneDrive/Bureau/dataorange'
to_dir=from_dir
nb_sample= 10
ens_memory=set()
dir_analyse_images_ows='C:/Users/yannw/OneDrive/Bureau/analyse_defaut_orange'
csv_result='C:/Users/yannw/OneDrive/Bureau/analyse_defaut_orange/data OUT/_data_out.csv'
set_defaut={'Test', 'Defaut1'}
from_="anaudy@eurocast.fr"
smtp_='smtp.office365.com'
number_= 587
code_="LpCdt@dcX!aVY3F8"
to_="antoine.naudy@gmail.com"
subject='[Defaut detecte]'



rognage=input('rogner les images ? Y/N :\n')

if rognage=='Y':
    while True:
        try:
            lst_rognage=input('donner les bornes du rognage sous forme de liste(ex:0.1,0.2,0.2,0.4)\n')
            lst_rognage=lst_rognage.split(',')

            AN_rognage_img.crop_img(from_dir, lst_rognage)
            break
        except:
            print('êtes-vous sûr d\'avoir rentré le bon format de liste ?')
            continue
else:
    pass

while True :
    
    AN_recup_img.recup_img(from_orange, to_dir, nb_sample, ens_memory)

    
    AN_lance_orange.AN_lance(dir_analyse_images_ows, csv_result)

    lst_evaluation=AN_evaluation.evaluation(csv_result, set_defaut, from_dir)

    for i in range(len(lst_evaluation)):

        mail=["Bonjour,\n\n",lst_evaluation[i][0]]
        os.chdir(from_dir)
        image = lst_evaluation[i][1]

        
        AN_send_mail.send_mail(from_, smtp_, number_, code_, to_, subject, mail, image)

    ens_memory=ens_memory | set(os.listdir(from_dir))

    


    
