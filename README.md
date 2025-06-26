# 🚀 ChromaX - Outil Réseau
ChromaX est une application réseau intuitive en Python avec interface graphique sombre, conçue pour vous offrir un ensemble complet d’outils réseau dans une seule application légère.

✨ Fonctionnalités principales
🔹 Afficher l’adresse IP locale et publique

🔹 Test de vitesse Internet (Speedtest) avec gestion de timeout

🔹 Ping Google (8.8.8.8) ou toute adresse personnalisée via popup

🔹 Scan des ports locaux (20-1024) en multi-threading pour rapidité

🔹 Génération d’un rapport réseau complet dans un fichier texte

Le rapport s’ouvre automatiquement dans votre éditeur par défaut et est supprimé dès sa fermeture pour plus de confidentialité.

⚙️ Prérequis
Python 3.x

Modules Python nécessaires :

bash
Copier
Modifier
pip install requests speedtest-cli
🚀 Installation et lancement
Clonez ce dépôt ou téléchargez le fichier main.py.

Installez les dépendances via pip (voir ci-dessus).

Lancez l’application avec :

bash
Copier
Modifier
python main.py
Utilisez l’interface graphique pour accéder aux fonctionnalités réseau.

🖥️ Compatibilité multi-plateforme
Windows : utilise Notepad pour afficher le rapport.

macOS : utilise TextEdit.

Linux : utilise xdg-open (le fichier est supprimé après un délai).

🔧 Détails techniques
Le scan de ports exploite le multi-threading pour un scan efficace.

Le speedtest est exécuté dans un thread avec timeout pour éviter de bloquer l’interface.

La fenêtre de ping personnalisé propose un champ pour saisir l’adresse cible.

La couleur de l’interface est sombre, pour un confort visuel prolongé.

