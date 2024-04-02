# API pour réaliser du contrôle caméra industriel à partir d'un smartphone

## Comment ça marche ?

Le smartphone installé sur la ligne de production prend une image à intervalle régulier (en timelapse) et enregistre ces images dans un dossier interne. 
Ce dossier est disponible sur le réseau wifi local via un serveur ouvert sur le téléphone avec une appli android (HTTP File Server par exemple). 
Une API streamlit distante et sur le même réseau local permet de récupérer les images et les trie grâce à un algorithme entraîné. 
En sortie les images de défaut s'affichent à l'écran avec leur traçabilité :
![Texte alternatif](https://github.com/Antoine1608/PR-CV-P4-Industrial_control/blob/main/Streamlit_screen.png?raw=true)

Un document excel est également généré avec la classification complète et les images associées sous forme de miniatures :
![Texte alternatif](https://github.com/Antoine1608/PR-CV-P4-Industrial_control/blob/main/Result_xlsx_screen.png?raw=true)
