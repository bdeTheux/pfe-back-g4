# Préparation

## Installations nécessaires sur la machine

* Python 3.9+ installé sur la machine
    * https://www.python.org/
* PyCharm
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

* Sous PyCharm, sélectionner l'environnement virtuel du projet

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
### Categories :

| **Uri**                            | **Méthode** | **Auth ?** | **Admin ?** | **Action**                                                                                                              |
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

| **Uri**                                | **Méthode** | **Auth ?** | **Admin ?** | **Action**                                                                     |
| -------------------------------------- | ------ | --- | ----------------- | ------------------------------------------------------------------------------------ |
| **/posts**                             | GET    | Non | Non               | READ ALL : récupère tous les posts de la db                                          |
| **/posts/pending**                     | GET    | Oui | Oui               | READ ALL : récupère tous les posts en attente de confirmation                        |
| **/posts?category=value\***              | GET    | Non | Non               | READ ALL FILTERED : récupère tous les posts dont la catégorie est &#39;value&#39;    |
| **/posts?campus=value\***                | GET    | Non | Non               | READ ALL FILTERED : récupère tous les posts dont le campus est &#39;value&#39;       |
| **/posts?order=value\***                 | GET    | Non | Non               | READ ALL ORDERED : ordonne selon le prix, où value est 'asc' ou 'desc                |
| **/posts/closed**                      | GET    | Non | Non               | READ ALL : récupère tous les posts de la db étant en état "Clôturé"                  |
| **/posts/pending**                     | GET    | Non | Non               | READ ALL : récupère tous les posts de la db étant en état "En attende d'approbation" |
| **/posts/myposts**                     | GET    | Non | Non               | READ ALL : récupère tous les posts de l'utilisateur courant'                         |
| **/posts/{id}**                        | GET    | Non | Non               | READ ONE : récupère un post de la db                                                 |
| **/posts**                             | POST   | Oui | Non               | CREATE ONE : rajoute un nouveau post dans la db                                      |
| **/posts/{id}**                        | PUT    | Oui | Oui si pas seller | UPDATE ONE : modifie le post ayant l&#39;id passé en paramètre                       |
| **/posts/{id}**                        | DELETE | Oui | Oui si pas seller | DELETE ONE : supprime un post ayant l&#39;id passé en paramètre                      |

&#42; les paramètres sont cumulables
### Addresses :

| **Uri** | **Méthode** | **Auth ?** | **Admin ?** | **Action** |
| ------------------------ | ------ | --- | --- | ------------------------------------------------------------------- |
| **/addresses**           | GET    | Non | Non | READ ALL : récupère toutes les adresses de la db                    |
| **/addresses/{id}**      | GET    | Oui | Non | READ ONE : récupère une adresse de la db                            |
| **/addresses**           | POST   | Oui | Oui | CREATE ONE : rajoute une nouvelle adresse dans la db                |
| **/addresses/{id}**      | PUT    | Oui | Oui | UPDATE ONE : modifie une adresse ayant l&#39;id passé en paramètre  |
| **/addresses/{id}**      | DELETE | Oui | Oui | DELETE ONE : supprime une adresse ayant l&#39;id passé en paramètre |
