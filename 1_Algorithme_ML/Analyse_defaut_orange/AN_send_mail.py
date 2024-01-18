import os, smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication

def send_mail(from_, smtp_, number_, code_, to_, subject, mail, image):
    print('tentative d\'envoi d\'email')
    # bien penser à baisser la sécurité sur "Accès moins sécurisé des applications" sur gmail
    # on rentre les renseignements pris sur le site du fournisseur

    os.chdir('C:/Users/yannw/OneDrive/Bureau/dataorange')    

    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = from_
    msg['To'] = to_
    msgText = MIMEText(mail[0]+mail[1])
    msg.attach(msgText)

    try:
        with open(image, 'rb') as fp:
            img = MIMEImage(fp.read())
            img.add_header('Content-Disposition', 'attachment', filename=image)
            msg.attach(img)                
        try:
            with smtplib.SMTP(smtp_, number_) as smtpObj:
                smtpObj.ehlo()
                smtpObj.starttls()
                smtpObj.login(from_, code_)
                smtpObj.sendmail(from_, to_.split(","), msg.as_string())
        except Exception as e:
            print('erreur dans l\'envoi du message (connexion internet ?) - pas de mise à jour de l\'archive')        
    except :
        print('pas d\'image, pas d\'envoi d email')


#image='C:/Users/yannw/OneDrive/Bureau/analyse_defaut_orange/20220121_154126.jpg'
#mail=['bonjour','un defaut a ete detecte', 'un gros defaut']
#send_email('anaudy@eurocast.fr','smtp.office365.com', 587, "LpCdt@dcX!aVY3F8", 'antoine.naudy@gmail.com','[Defaut detecte]', mail, image)
