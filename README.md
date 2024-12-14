# KHRAL - Outils de tests de vulnérabilités web

### Description du projet

**KHRAL** est un logiciel destiné à tester et exploiter certaines vulnérabilités web courantes telles que l'**injection SQL**, les **attaques XSS** (Cross-Site Scripting), et d'autres vulnérabilités mentionnées dans le **Top 10 de l'OWASP**. Ce projet a pour but de créer des outils permettant de tester ces vulnérabilités de manière personnalisée, tout en comprenant le fonctionnement des tests de pénétration. Les outils créés seront utilisés dans des tests d'intrusion (pentesting) pour identifier des failles de sécurité dans les applications web.

Le projet regroupe plusieurs outils permettant d'identifier et d'exploiter des vulnérabilités communes dans les applications web, tout en permettant aux utilisateurs de mieux comprendre comment ces outils fonctionnent en coulisses.

### Objectifs

- Développer des outils de test pour les vulnérabilités OWASP telles que l'injection SQL, XSS, etc.
- Créer une interface utilisateur moderne pour naviguer entre les outils de test.
- Fournir une documentation pour permettre l'extension et la compréhension du fonctionnement des outils de pentesting.

### Fonctionnalités principales

- **Test d'injection SQL** : Teste la vulnérabilité d'un site aux injections SQL via des paramètres d'URL.
- **Test d'attaque XSS** : Vérifie la présence de vulnérabilités XSS dans une application web.
- **Interface graphique moderne** : Une interface graphique simple et moderne permettant de naviguer entre les outils de tests.

### Prérequis

Avant de commencer, assurez-vous d'avoir installé les outils suivants sur votre machine :

- **Python 3.x** : Ce projet utilise Python pour implémenter les outils de tests.
- **Bibliothèques Python** :
  - `requests` : pour effectuer des requêtes HTTP et tester les vulnérabilités.
  - `tkinter` : pour l'interface graphique.
  - `Pillow` : pour afficher des images dans l'interface.


## Installation

1. **Clone ce repository sur ta machine** :

```bash
git clone https://github.com/votre-utilisateur/KHRAL.git
cd KHRAL
```

2. **Crée un environnement virtuel et activez-le (optionnel mais recommandé)** :
bash

```bash
python3 -m venv env
source env/bin/activate  # Sur macOS/Linux
env\Scripts\activate     # Sur Windows
```

3. Installez les dépendances :
Copier le code
```bash
pip install -r requirements.txt
```

4. Utilisation
Pour lancer l'application et accéder aux outils de tests, exécutez le fichier principal appli.py :

Copier le code
```bash
python appli.py
```
Cela ouvrira une fenêtre graphique avec les différents outils de tests de vulnérabilités.

## Contribuer

Si vous souhaitez contribuer à ce projet, voici les étapes à suivre :

1. **Fork le repository**.
2. **Crée une branche pour tes nouvelles fonctionnalités** :
```bash
git checkout -b feature/nom_de_fonctionnalité
```
3. **Commite tes changements :**
Copier le code
```bash
git commit -am 'Ajout d'une nouvelle fonctionnalité'
```
4. **Pousse sur la branche :**
Copier le code
```bash
git push origin feature/nom_de_fonctionnalité
```
5. **Ouvre une Pull Request sur le repository principal.**
## Auteurs
- Karim ABDALLAH - @abdhkarim
- LAZHARI Haroun-Rachid @CambouiMan
## Liens utiles
- [OWASP Top 10](https://owasp.org/Top10/fr/)
- [MITRE ATT&CK](https://attack.mitre.org/)
- [NIST CVE](https://nvd.nist.gov/vuln)
