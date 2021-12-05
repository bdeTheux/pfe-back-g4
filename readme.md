# Mise en place de l'environnement
## Installations nécessaires sur la machine
* Python 3.9+ installé sur la machine
  * https://www.python.org/
* PyCharm
  * https://www.jetbrains.com/pycharm/download/
##
* Récupérer le projet
  * ```git clone [url du projet]```
* Créer l'environnement virtuel
  * Aller dans le dossier du projet
    * Windows:
      ```
        py -3 -m venv venv
        venv\Scripts\activate
        pip install -r requirements.txt 
        ```
    * Linux:
      ```
        python3 -m venv venv
        . venv/bin/activate
        pip install -r requirements.txt 
        ```
* Sous PyCharm, sélectionner l'environnement virtuel du projet