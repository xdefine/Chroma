ChromaX
Suite d’Outils Réseau en Python

Une application légère et complète pour le diagnostic et la surveillance réseau, avec interface graphique sombre.

Fonctionnalités
🔍 Diagnostic réseau complet

📡 Analyse IP locale et publique

⚡ Test de vitesse Internet (Speedtest)

🛠️ Ping vers Google ou adresse personnalisée

🔓 Scan multi-thread des ports locaux (20-1024)

📄 Génération et consultation de rapports réseau temporaires

Contenu du projet
Fichier	Description
main.py	Point d’entrée et interface graphique (GUI)
net_utils.py*	Fonctions utilitaires pour l’analyse réseau
README.md	Documentation du projet

* (Dans ce dépôt, tout est dans main.py mais peut être séparé pour modularité)

Installation
Cloner le dépôt :

bash
Copier
Modifier
git clone https://github.com/votre-utilisateur/chromax.git
cd chromax
Installer les dépendances :

bash
Copier
Modifier
pip install requests speedtest-cli
Lancer l’application :

bash
Copier
Modifier
python main.py
Utilisation
Lancez l’application GUI.

Cliquez sur les boutons pour effectuer des tests réseau.

Le rapport réseau s’ouvre automatiquement après génération et est supprimé après consultation pour garantir votre confidentialité.

Compatibilité
Fonctionne sous Windows, macOS, et Linux avec détection automatique du système.

