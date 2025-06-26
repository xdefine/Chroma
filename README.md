# ChromaX - Outil Réseau


ChromaX est une application Python avec interface graphique pour réaliser diverses opérations réseau : affichage des IP locale et publique, test de vitesse internet, ping, scan des ports locaux, et génération d’un rapport réseau complet. Le rapport est généré dans un fichier texte, ouvert automatiquement, puis supprimé après consultation.

Fonctionnalités
Afficher IP locale et IP publique

Lancer un speedtest internet (avec timeout)

Ping Google (8.8.8.8) ou une adresse personnalisée

Scanner les ports locaux ouverts (20-1024)

Générer un rapport réseau complet dans un fichier texte
Le fichier s’ouvre automatiquement dans l’éditeur par défaut et est supprimé après fermeture.

Prérequis
Python 3.x

Modules Python à installer :

bash
Copier
Modifier
pip install requests speedtest-cli
Utilisation
Clonez ce dépôt ou téléchargez le fichier main.py.

Installez les dépendances avec pip.

Lancez l’application :

bash
Copier
Modifier
python main.py
Utilisez l’interface graphique pour lancer les actions réseau souhaitées.

Pour le rapport réseau, un fichier texte s’ouvrira automatiquement, il sera supprimé une fois fermé.

Plateformes supportées
Windows (Notepad est utilisé pour afficher le rapport)

macOS (TextEdit est utilisé)

Linux (xdg-open est utilisé, suppression automatique après un délai)

Notes
Le scan de ports couvre les ports de 20 à 1024.

Le speedtest peut prendre jusqu’à 30 secondes.

Le ping personnalisé ouvre une petite fenêtre pour saisir une adresse IP ou un domaine.
