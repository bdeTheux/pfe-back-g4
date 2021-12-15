# Préparation

## Installations nécessaires sur la machine

* Python 3.9+ installé sur la machine
    * https://www.python.org/
* PyCharm (ou utiliser l'environnement virtuel)
    * https://www.jetbrains.com/pycharm/download/
* Récupérer le projet
    * ```git clone [url du projet]```

## Mise en place de l'environnement

### Environnement virtuel (optionnel)

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

### Sélection de l'environnement

* Sous PyCharm, sélectionner l'environnement virtuel du projet, ou celui de votre choix

### Lancement
* Utiliser PyCharm directement
* OU
* lancer, dans l'environnement virtuel (suite à la seconde commande de son installation), ```flask run```

### Information supplémentaires
https://flask.palletsprojects.com/en/2.0.x/installation/

# Routes

### Users :

| **Uri**             | **Méthode** | **Auth?** | **Admin?** | **Action**                                                                                                 |
| ------------------- | ----------- | --------- | ---------- | ---------------------------------------------------------------------------------------------------------- |
| **/users/login**    | POST        | Non | Non        | LOG IN : renvoie un token dans les headers sous la clef 'Authorization' en cas de succès                         |
| **/users/signup**   | POST        | Non | Non        | CREATE ONE : ajoute un nouvel utilisateur avec les données du corps de la requête                                |
| **/users**          | GET         | Oui | Oui        | READ ALL : récupère tous les utilisateurs de la db                                                               |
| **/users/whoami**   | GET         | Oui | Oui        | READ ONE : récupère l'utilisateur courant ssi le token est présent et valide, sinon renvoie null                 |
| **/users/{id}/ban** | POST        | Oui | Oui        | UPDATE ONE : modifie le statut banned d&#39;un utilisateur ayant l&#39;id passé en paramètre                     |
| **/users/{id}**     | GET         | Oui | Non        | READ ONE : récupère un utilisateur de la db                                                                      |
| **/users/edit**     | PUT         | Oui | Non        | UPDATE ONE : modifie l&#39;utilisateur ayant l&#39;id passé en paramètre avec les données du corps de la requête |
| **/users/{id}**     | DELETE      | Oui | Non        | DELETE ONE : supprime l&#39;utilisateur avec l&#39;id passé en paramètre                                         |
| **/users/changepassword**  | POST | Oui | Non        | UPDATE ONE: modifie le mot de passe de l&#39;utilisateur connecté                                                |
| **/users/changefavorite/{id}**  | POST | Oui | Non   | UPDATE ONE: modifie la liste des favoris de l'utilisateur connecté                                               |

### Categories :

| **Uri**                            | **Méthode** | **Auth?** | **Admin ?** | **Action**                                                                                                              |
| ---------------------------------- | --- | --- | --- | ------------------------------------------------------------------------------------------------------------------------|
| **/categories**                    | GET | Non | Non | READ ALL : récupère toutes les catégories de la db                                                                      |
| **/categories/tree**               | GET | Non | Non | READ ALL : récupère toutes les catégories de la db et les affiches en arborescence, les parents contenant les sous-catégories |
| **/categories/{id}**               | GET | Non | Non | READ ONE : récupère une catégorie de la db                                                                              |
| **/categories/{id}/subcategories** | GET | Non | Non | READ ONE : récupère toutes les sous-catégories de la catégorie et les renvoie dans une liste simple                     |
| **/categories/{id}/parents**       | GET | Non | Non | READ ONE : récupère tous les parents de la catégorie et les renvoie dans une liste simple                              |
| **/categories**                    | POST | Oui | Oui | CREATE ONE : ajoute une nouvelle catégorie à la db                                                                      |
| **/categories/{id}**               | PUT | Oui | Oui | UPDATE ONE : modifie la catégorie ayant l&#39;id passé en paramètre                                                     |
| **/categories/{id}**               | DELETE | Oui | Oui | DELETE ONE : supprime une catégorie ayant l&#39;id passé en paramètre                                                   |

### Posts :

| **Uri**                          | **Méthode** | **Auth?** | **Admin ?** | **Action**                                                                                    |
| -------------------------------- | ------ | --- | ----------------- | -------------------------------------------------------------------------------------------------- |
| **/posts**                       | GET    | Non | Non               | READ ALL : récupère toutes les annonces de la db                                                   |
| **/posts?category=value\***      | GET    | Non | Non               | READ ALL FILTERED : récupère toutes les annonces dont la catégorie est &#39;value&#39;             |
| **/posts?campus=value\***        | GET    | Non | Non               | READ ALL FILTERED : récupère toutes les annonces dont le campus est &#39;value&#39;                |
| **/posts?order=value\***         | GET    | Non | Non               | READ ALL ORDERED : ordonne selon le prix, où value est 'asc' ou 'desc                              |
| **/posts/closed**                | GET    | Oui | Non               | READ ALL : récupère toutes les annonces de la db étant en état "Clôturé"                           |
| **/posts/pending**               | GET    | Oui | Oui               | READ ALL : récupère toutes les annonces de la db étant en état "En attente d'approbation"          |
| **/posts/myposts**               | GET    | Oui | Non               | READ ALL : récupère toutes les annonces de l'utilisateur courant'                                  |
| **/posts/{id}**                  | GET    | Non | Non               | READ ONE : récupère une annonce de la db                                                           |
| **/posts/favourites**            | GET    | Oui | Non               | READ ALL SELECTED : récupère toutes les annonces de la liste des favoris et supprime les invalides |
| **/posts**                       | POST   | Oui | Non               | CREATE ONE : rajoute une nouvelle annonce dans la db                                               |
| **/posts/{id}**                  | PUT    | Oui | Oui si pas seller | UPDATE ONE : modifie l'annoce ayant l&#39;id passé en paramètre                                    |
| **/posts/{id}**                  | DELETE | Oui | Oui si pas seller | DELETE ONE : supprime une annonce ayant l&#39;id passé en paramètre                                |
| **/posts/{id}/file/{file_id}**   | DELETE | Oui | Oui si pas seller | DELETE ONE : supprime un fichier ayant l&#39;id comme id d'annonce et file_id comme id propre      |

&#42; les paramètres sont cumulables
### Addresses :

| **Uri** | **Méthode** | **Auth?** | **Admin?** | **Action** |
| ------------------------ | ------ | --- | --- | ------------------------------------------------------------------- |
| **/addresses**           | GET    | Non | Non | READ ALL : récupère toutes les adresses de la db                    |
| **/addresses/{id}**      | GET    | Oui | Non | READ ONE : récupère une adresse de la db                            |
| **/addresses**           | POST   | Oui | Oui | CREATE ONE : rajoute une nouvelle adresse dans la db                |
| **/addresses/{id}**      | PUT    | Oui | Oui | UPDATE ONE : modifie une adresse ayant l&#39;id passé en paramètre  |
| **/addresses/{id}**      | DELETE | Oui | Oui | DELETE ONE : supprime une adresse ayant l&#39;id passé en paramètre |
