from datetime import datetime
import os, subprocess, time, AN_perf

#dir_from='C:/Users/yannw/OneDrive/Bureau/analyse_defaut_orange' et csv_result='C:/Users/yannw/OneDrive/Bureau/analyse_defaut_orange/data OUT/_data_out.csv'

@AN_perf.AN_pf
def AN_lance(dir_orange, csv_result):
    print('traitement des images...')
    _deb_Orange = datetime.now().timestamp()
    os.chdir(dir_orange)
    p = subprocess.Popen(["start", "cmd", "/k", "Analyse_images.ows"], shell = True)
    _fin_Orange = os.path.getmtime(csv_result)
    processtime = _fin_Orange-_deb_Orange

    try:
        while processtime<0:
            _fin_Orange = os.path.getmtime(csv_result)
            processtime = _fin_Orange-_deb_Orange
        os.popen('taskkill /fi "windowtitle eq Analyse_images.ows*"')
        time.sleep(2)
        os.popen('taskkill /fi "windowtitle eq C:\WINDOWS\system32\cmd.exe"')
    except:
        print('erreur lors du traitement des images (csv_result ouvert ?)')
        exit()
  
 
