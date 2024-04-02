# API pour réaliser du contrôle caméra industriel à partir d'un smartphone

## Comment ça marche ?

Le smartphone installé sur la ligne de production prend une image à intervalle régulier (en timelapse) et enregistre ces images dans un dossier interne. 
Ce dossier est disponible sur le réseau wifi local via un serveur ouvert sur le téléphone avec une appli android (HTTP File Server par exemple). 
Une API streamlit distante et sur le même réseau local permet de récupérer les images et les trie grâce à un algorithme entraîné. 
En sortie les images de défaut s'affichent à l'écran avec leurs traçabilité.
![Texte alternatif](lien_de_l_image)
