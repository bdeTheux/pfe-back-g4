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

| **Uri** | **Méthode** | **Auth?** | **Admin?** | **Action** |
| --- | --- | --- | --- | --- |
| **/users/login** | POST | Non | Non ||
| **/users/register** | POST | Non | Non | CREATE ONE : ajoute un nouvel utilisateur avec les données du corps de la requête |
| **/users/logout** || Oui | Non ||
| **/users** | GET | Oui (potentiellement admin) | Oui | READ ALL : récupère tous les utilisateurs de la db |
| **/users/{id}/ban** | POST | Oui | Oui | UPDATE ONE : Modifie le statut banned d&#39;un utilisateur ayant l&#39;id passé en paramètre |
| **/users/{id}** | GET | Oui | Non | READ ONE : récupère un utilisateur de la db |
| **/users/{id}** | PUT | Oui | Non\* | UPDATE ONE : modifie l&#39;utilisateur ayant l&#39;id passé en paramètre avec les données du corps de la requête |
| **/users/{id}** | DELETE | Oui -\&gt; admin | Oui | DELETE ONE : supprime l&#39;utilisateur avec l&#39;id passé en paramètre |

### Categories :

| **Uri** | **Méthode** | **Auth ?** | **Admin ?** | **Action** |
| --- | --- | --- | --- | --- |
| **/categories** | GET | Non | Non | READ ALL : récupère toutes les catégories de la db |
| **/categories/{id}** | GET | Non | Non | READ ONE : récupère une catégorie de la db |
| **/categories** | POST | Oui | Oui | CREATE ONE : ajoute une nouvelle catégorie à la db |
| **/categories/{id}** | PUT | Oui | Oui | UPDATE ONE : modifie la catégorie ayant l&#39;id passé en paramètre |
| **/categories/{id}** | DELETE | Oui | Oui | DELETE ONE : supprime une catégorie ayant l&#39;id passé en paramètre |

### Posts :

| **Uri** | **Méthode** | **Auth ?** | **Admin ?** | **Action** |
| --- | --- | --- | --- | --- |
| **/posts** | GET | Non | Non | READ ALL : récupère tous les posts de la db |
| **/posts/pending** | GET | Oui | Oui | READ ALL : récupère tous les posts en attente de confirmation |
| **/posts?category=value** | GET | Non | Non | READ ALL FILTERED : récupère tous les posts dont la catégorie est &#39;value&#39; |
| **/posts?campus=value** | GET | Non | Non | READ ALL FILTERED : récupère tous les posts dont le campus est &#39;value&#39; |
| **/posts/{id}** | GET | Non | Non | READ ONE : récupère un post de la db |
| **/posts** | POST | Oui | Non | CREATE ONE : rajoute un nouveau post dans la db |
| **/posts/{id}** | PUT | Oui | Oui si pas seller | UPDATE ONE : modifie le post ayant l&#39;id passé en paramètre |
| **/posts/{id}** | DELETE | Oui | Oui si pas seller | DELETE ONE : supprime un post ayant l&#39;id passé en paramètre |

### Addresses :

| **Uri** | **Méthode** | **Auth ?** | **Admin ?** | **Action** |
| --- | --- | --- | --- | --- |
| **/addresses** | GET | Non | Non | READ ALL : récupère toutes les adresses de la db |
| **/addresses/{id}** | GET | Oui | Non | READ ONE : récupère une adresse de la db |
| **/addresses** | POST | Oui | Oui | CREATE ONE : rajoute une nouvelle adresse dans la db |
| **/addresses/{id}** | PUT | Oui | Oui | UPDATE ONE : modifie une adresse ayant l&#39;id passé en paramètre |
| **/addresses/{id}** | DELETE | Oui | Oui | DELETE ONE : supprime une adresse ayant l&#39;id passé en paramètre |
