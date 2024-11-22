![Bannière du Projet](images_readme\oppenheimer.jpg)



# Projet de Fullstack data : Les 200 films les plus rentables de l'histoire
Dans ce README vous trouverez toutes les informations relatives au lancement de notre projet (il s'agit de notre [User Guide](#user-guide) ) ainsi qu'une analyse de notre projet et des problématiques que nous avons eues (il s'agit de notre [Developper Guide](#developper-guide)).

## Préambule
Ce projet est une API de gestion de films construite avec FastAPI, 
offrant une plateforme robuste pour la gestion et 
l'exploration des données cinématographiques. 
L'API fournit des informations détaillées sur les
 200 films ayant eu le plus de succès au box office mondial 
 (à la date du 1er Octobre 2024), 
 leurs casting et des métadonnées associées 
 telles que le budget, la date de sortie etc. 
 Cette application possède des fonctionnalités destinées à la fois aux utilisateurs occasionnels
 et aux passionnés de cinéma.

Nous avons récupérées ces données sur les sites [Rotten Tomatoes](https://www.rottentomatoes.com/) (pour chaque film) ainsi que sur le site [box office mojo](https://www.boxofficemojo.com/chart/ww_top_lifetime_gross/?ref_=bo_lnav_hm_shrt)

# User Guide

## Exécution du projet


Pour exécuter le projet vous devrez tout d'abord récupérer le projet, pour cela vous pouvez récupérer le fichier zip de notre projet
ou faire un git pull 

## Aperçu du Projet



# Developper Guide

### Principales Fonctionnalités

- Opérations CRUD (Create, Read, Update, Delete) complètes pour les films et les membres du casting
- Système avancé de filtrage des films basé sur plusieurs critères :
  - Performance au box-office (recettes brutes)
  - Plages de budgets
  - Années de sortie
  - Durée
  - Classifications MPAA
  - Genres
  - Casting + Réalisateur
- Système d'authentification et d'autorisation des utilisateurs
- Gestion détaillée des informations du casting
- Interface web moderne pour une interaction facile avec les données

### Pile Technologique

- **Framework Backend** : FastAPI (Python)
- **Base de données** : PostgreSQL
- **Authentification** : Système d'authentification basé sur JWT
- **Documentation** : Documentation automatique OpenAPI/Swagger
- **Frontend** : Modèles rendus côté serveur avec Jinja2
- **Style** : CSS moderne avec design réactif

### Gestion des Données

Notre base de données contient des informations complètes sur les films, y compris :

- Titre et classement
- Données financières (recettes brutes, budget)
- Informations sur la sortie (année, date)
- Détails du contenu (résumé, classification MPAA, genres)
- Spécifications techniques (durée)
- Informations sur le casting (acteurs, réalisateurs, scénaristes)
- Assets médiatiques (images des films et du casting)

# Structure des Données

## Organisation de la Base de Données

Notre base de données PostgreSQL est structurée autour de trois entités principales :

### Table des Films

L'entité centrale stockant les informations sur les films avec :

- Identifiants uniques et classement
- Détails principaux du film (titre, résumé)
- Métriques financières (recettes brutes, budget)
- Informations techniques (durée, classification MPAA)
- Catégorisation (genres stockés sous forme de tableaux)
- Données temporelles (date de sortie, année de production)
- Assets marketing (images promotionnelles)

### Table du Casting

Une entité liée gérant tous les membres du casting avec :

- UUID unique pour chaque entrée de casting
- Informations personnelles (nom, image)
- Classification des rôles (acteur, réalisateur, scénariste)
- Informations sur les personnages pour les acteurs
- Relation avec les films via des clés étrangères

### Table des Utilisateurs

Gère les utilisateurs de l'application et l'authentification avec :

- Identifiants uniques pour chaque utilisateur
- Détails d'authentification (email, mot de passe haché)
- Informations de profil (nom)
- Statut du compte (actif/désactivé)
- Informations de contrôle d'accès

## Relations entre les Données

- Chaque film peut avoir plusieurs membres du casting
- Les membres du casting peuvent être associés à plusieurs films
- Les rôles sont flexibles, permettant à une même personne d'être listée comme acteur et réalisateur
- Les utilisateurs peuvent interagir avec les données des films et du casting en fonction de leur authentification
- Toutes les relations sont maintenues via des contraintes appropriées dans la base de données

## Sécurité des Données

- Les opérations sensibles nécessitent une authentification
- Les mots de passe sont sécurisés par hachage
- L'intégrité des données est assurée par des contraintes de base de données
- Des sauvegardes régulières garantissent la persistance des données
- Validation des entrées via les schémas Pydantic
- Authentification basée sur JWT pour des sessions utilisateur sécurisées

# Architecture

L'API est organisée dans une architecture modulaire bien structurée au sein du répertoire `api`. Voici une description détaillée de chaque composant :

## Application Principale (`main.py`)

- Point d'entrée de l'application qui initialise l'instance FastAPI
- Configure les middleware (Prometheus pour les métriques)
- Configure les fichiers statiques et les modèles Jinja2
- Inclut tous les routeurs pour les différents points de terminaison
- Gère le cycle de vie de la base de données à travers des événements de cycle de vie

## Modèles (`/models`)

- Définit les modèles ORM SQLAlchemy pour les tables de la base de données
- `database.py` : Connexion à la base de données et configuration de base
- `post.py` : Contient les modèles de données pour les Films, Casting, et Utilisateurs
- Gère les relations entre les différentes entités

## Routeurs (`/routers`)

Chaque routeur gère une fonctionnalité spécifique avec ses propres points de terminaison :

- `router_film.py` :
  - Opérations CRUD pour les films
  - Points de terminaison de filtrage et de classement avancé
  - Supporte la pagination et les requêtes complexes
- `router_cast.py` :
  - Gère les membres du casting (acteurs, réalisateurs, scénaristes)
  - Lie les membres du casting aux films
  - Supporte le filtrage par nom et film
- `router_user.py` :
  - Points de terminaison de gestion des utilisateurs
  - Opérations sur le profil
- `router_authentication.py` :
  - Gère la connexion/déconnexion
  - Gestion des tokens JWT
- `other_router.py` :
  - Sert la page d'accueil et d'autres points de terminaison généraux

## Points de Terminaison de l'API

L'API est organisée en plusieurs routeurs, chacun gérant une fonctionnalité spécifique :

### Routeur Film (`/films`)

1. **Liste et Recherche**

   - `GET /films/` : Récupérer tous les films avec pagination
   - `GET /films/{title}` : Récupérer un film spécifique par titre
   - `GET /films/filter/` : Filtrage avancé avec plusieurs paramètres :
     - Plage des recettes brutes
     - Plage des budgets
     - Plage de durée
     - Plage d'années
     - Distributeur
     - Classification MPAA
     - Genres
     - Membres du casting
   - `GET /films/byrank/` : Obtenir des films dans une plage de classement spécifique

2. **Gestion**

   - `POST /films/` : Créer un nouveau film avec casting
   - `PUT /films/{title}` : Mettre à jour un film existant
   - `DELETE /films/{title}` : Supprimer un film

### Routeur Casting (`/cast`)

1. **Liste et Recherche**

   - `GET /cast/` : Récupérer tous les membres du casting
   - `GET /cast/{id}` : Récupérer un membre du casting spécifique
   - `GET /cast/cast_name/{name}` : Rechercher un membre du casting par nom
   - `GET /cast/cast_film/{title}` : Récupérer tout le casting pour un film spécifique

2. **Gestion**

   - `POST /cast/` : Ajouter un nouveau membre au casting d'un film
   - `PUT /cast/{id}` : Mettre à jour un membre du casting
   - `DELETE /cast/{id}` : Supprimer un membre du casting

### Routeur Utilisateur (`/user`)

1. **Gestion des Utilisateurs**
   - `POST /user/` : Créer un nouveau compte utilisateur
   - `GET /user/me/` : Récupérer le profil de l'utilisateur actuel

### Routeur d'Authentification

1. **Gestion de Session**
   - `POST /login/` : Connexion de l'utilisateur
   - `POST /logout/` : Déconnexion de l'utilisateur

### Autres Routeurs

- Autres fonctions pour améliorer l'expérience utilisateur

### Fonctionnalités Communes aux Routeurs

1. **Authentification**

   - Tous les points de terminaison (sauf connexion/enregistrement) nécessitent une authentification
   - Utilisation de la dépendance `get_current_active_user`

2. **Modèles de Réponse**

   - Utilisation cohérente des modèles Pydantic
   - Codes d'état appropriés pour différentes opérations :
     - 201 : Ressource créée
     - 202 : Requête acceptée
     - 401 : Non autorisé
     - 404 : Non trouvé
     - 409 : Conflit

3. **Intégration à la Base de Données**

   - Toutes les routes utilisent une session SQLAlchemy
   - Gestion appropriée des erreurs pour les opérations de base de données

4. **Validation des Entrées**

   - Validation des paramètres de requête
   - Validation du corps de la requête via Pydantic
   - Vérification et conversion des types

## Services (`/services`)

Couche de logique métier qui sépare les opérations de base de données des gestionnaires de route :

- `service_film.py` : Logique métier liée aux films
- `service_cast.py` : Opérations de gestion du casting
- `service_user.py` : Logique de gestion des utilisateurs
- `service_authentication.py` : Logique d'authentification et d'autorisation
- `oauth2.py` : Implémentation OAuth2 avec JWT
- `hashing.py` : Utilitaires de hachage de mots de passe
- `auth_token.py` : Génération et validation de tokens

## Couche des Services

La couche des services agit comme la couche d'application, séparant les opérations de base de données des gestionnaires de route. Chaque module de service est responsable d'une fonctionnalité spécifique :

### Service Film

- Gère toutes les opérations liées aux films
- Gère les requêtes et les filtres complexes
- Gère le classement des films
- Coordonne les relations entre films et casting
- Implémente la validation des données et la gestion des erreurs
- Gère les transactions de base de données pour les opérations sur les films

### Service Casting

- Gère les informations des membres du casting
- Lie les membres du casting aux films
- Gère les recherches de membres du casting
- Fournit des capacités de filtrage des membres du casting
- Gère les mises à jour et les suppressions des membres du casting
- Assure l'intégrité des données pour les relations casting-film

### Service d'Authentification

- Implémente une authentification sécurisée des utilisateurs
- Gère la création et la validation des tokens JWT
- Gère la gestion des sessions
- Implémente la gestion sécurisée des cookies
- Fournit des fonctionnalités de déconnexion
- Gère les sessions utilisateur et l'expiration des tokens

### Service Utilisateur

- Gère la gestion des comptes utilisateurs
- Implémente le hachage sécurisé des mots de passe
- Gère les profils utilisateurs
- Gère l'enregistrement des utilisateurs
- Valide les identifiants des utilisateurs
- Gère le statut des utilisateurs (actif/inactif)

### Fonctionnalités Communes aux Services

1. **Gestion des Erreurs**

   - Réponses d'erreur cohérentes
   - Messages d'erreur détaillés
   - Mappage des codes d'état HTTP
   - Gestion des transactions de base de données

2. **Sécurité**

   - Hachage des mots de passe avec bcrypt
   - Gestion sécurisée des tokens
   - Validation des sessions
   - Validation et assainissement des entrées

3. **Opérations sur la Base de Données**

   - Gestion des transactions
   - Opérations CRUD
   - Gestion des relations
   - Optimisation des requêtes

## Schémas (`/schemas`)

Le répertoire schemas contient des modèles Pydantic qui définissent la structure de nos données. Nous utilisons un modèle distinct "In" et "Out" pour chaque entité. Voici pourquoi :

### Schémas d'Entrée vs Schémas de Sortie

#### Schémas de Film (`FilmIn` vs `FilmOut`)

- **Schéma d'Entrée (********`FilmIn`********\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*)** :

  - Utilisé lors de la création ou de la mise à jour des films
  - Contient uniquement les champs que les utilisateurs doivent pouvoir fournir
  - Possède des valeurs par défaut pour les champs optionnels afin de simplifier la création des données
  - N'inclut pas les champs auto-générés comme `rank`
  - Les relations (comme le casting) sont gérées via des points de terminaison séparés

- **Schéma de Sortie (********`FilmOut`********\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*)** :

  - Utilisé lors de l'envoi de données de film aux clients
  - Inclut des champs additionnels calculés ou générés par la base de données (comme `rank`)
  - Contient des relations imbriquées (comprend la liste complète du `casting` des films)
  - Rend certains champs optionnels pour gérer les données partielles
  - Fournit une vue complète du film avec toutes ses relations

#### Schémas de Casting (`CastIn` vs `CastOut`)

- **Schéma d'Entrée (********`CastIn`********\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*)** :

  - Axé sur les données essentielles nécessaires pour créer une entrée de casting
  - Structure plus simple sans données de relation
  - Utilise des valeurs par défaut pour les champs optionnels
  - N'inclut pas les données associées aux films

- **Schéma de Sortie (********`CastOut`********\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*)** :

  - Inclut la relation complète avec le film
  - Fournit plus de contexte en incluant les informations relatives aux films
  - Utilisé lors de la restitution d'informations détaillées sur le casting
  - Gère mieux les champs optionnels à des fins d'affichage

### Pourquoi Cette Séparation ?

1. **Contrôle des Données** :

   - Les schémas d'entrée limitent ce que les utilisateurs peuvent envoyer à l'API
   - Les schémas de sortie fournissent des données plus riches et complètes aux utilisateurs
   - Cette séparation aide à prévenir la manipulation indésirée des données

2. **Gestion des Relations** :

   - Entrée : Garde les relations simples (en utilisant des identifiants ou des requêtes séparées)
   - Sortie : Inclut des données complètes sur les relations pour une meilleure consommation des données

3. **Logique de Validation** :

   - Entrée : Validation plus stricte pour la création/mise à jour des données
   - Sortie : Structure plus flexible pour l'affichage des données

4. **Sécurité** :

   - Entrée : Empêche les utilisateurs de définir des champs sensibles ou calculés
   - Sortie : Inclut des champs additionnels qui sont sûrs à exposer

5. **Expérience Utilisateur** :

   - Entrée : Structure plus simple pour faciliter la création/mise à jour des données
   - Sortie : Structure plus riche pour fournir des informations complètes en une seule réponse

Cette séparation des responsabilités aide à maintenir une API propre, sécurisée, et facile à utiliser tout en garantissant l'intégrité des données et une validation correcte.

## Fichiers Statiques (`/static`)

- Feuilles de style CSS pour le style du frontend
- Fichiers JavaScript pour les fonctionnalités côté client
- Images et autres assets médiatiques
- Organisés par type (css, js, images)

## Modèles (`/templates`)

- Modèles HTML Jinja2 pour le rendu côté serveur
- Inclut des modèles de base et des modèles spécifiques à chaque page
- Supporte l'héritage des modèles et des composants réutilisables

## Caractéristiques de Sécurité

### Système d'Authentification

L'API implémente un système d'authentification robuste utilisant JWT (JSON Web Tokens) avec stockage sécurisé des cookies :

#### Processus de Connexion

1. **Authentification de l'Utilisateur** :

   - Les utilisateurs fournissent leur email et mot de passe via le point de terminaison `/login`
   - Les identifiants sont validés par rapport à la base de données
   - Les mots de passe sont vérifiés en utilisant le hachage bcrypt

2. **Gestion des Tokens** :

   - Après une connexion réussie, un token JWT est généré
   - Le token contient l'email de l'utilisateur dans sa charge utile
   - Le token est signé en utilisant l'algorithme HS256 avec une clé sécurisée

3. **Sécurité des Cookies** :

   - Le token est stocké dans un cookie HTTP-only nommé "authentication"
   - Paramètres du cookie :
     - `httponly` : True (empêche l'accès JavaScript)
     - `secure` : True (uniquement envoyé via HTTPS)
     - `samesite` : "strict" (prévient les attaques CSRF)
     - `max_age` : 12 heures (expiration automatique)

#### Gestion des Sessions

1. **Vérification de Session Active** :

   - Le système prévient les connexions multiples simultanées
   - Vérifie l'existence d'un cookie d'authentification
   - Retourne une erreur appropriée si une session existe déjà

2. **Contrôle d'Accès** :

   - Les points de terminaison protégés nécessitent une authentification valide
   - Le token est automatiquement validé à chaque requête
   - Les tokens invalides ou expirés génèrent des réponses 401 Non autorisé

3. **Vérification du Statut de l'Utilisateur** :

   - Le système vérifie si le compte utilisateur est actif
   - Les comptes désactivés ne peuvent pas accéder aux ressources protégées
   - Validation automatique via `get_current_active_user`

#### Processus de Déconnexion

1. **Fin de Session** :
   - Le point de terminaison `/logout` gère la fin de session
   - Le cookie d'authentification est supprimé
   - Le serveur vérifie l'existence de la session avant la déconnexion

### Bibliothèques et Dépendances

- **FastAPI Security** : Fournit un flux de mot de passe OAuth2
- **Passlib** : Gère le hachage des mots de passe avec bcrypt
- **PyJWT** : Gère la création et la validation des tokens JWT
- **Pydantic** : Assure la sécurité des types dans les schémas de sécurité

### Ressources Protégées

Toutes les opérations sensibles nécessitent une authentification :

- Gestion des films (création, mise à jour, suppression)
- Gestion du casting (création, mise à jour, suppression)
- Accès au profil utilisateur
- Points de terminaison de modification des données

### Meilleures Pratiques de Sécurité

1. **Protection des Mots de Passe** :

   - Les mots de passe ne sont jamais stockés en clair
   - Hachage bcrypt avec sel
   - Vérification sécurisée des mots de passe

2. **Sécurité des Tokens** :

   - Tokens de courte durée (expiration de 12 heures)
   - Stockage sécurisé des tokens dans des cookies HTTP-only
   - Protection contre les attaques XSS et CSRF

3. **Gestion des Erreurs** :

   - Messages d'erreur sécurisés
   - Codes d'état HTTP appropriés
   - Validation de toutes les entrées utilisateur

## Fonctionnalités de l'API

- Points de terminaison REST respectant les standards HTTP
- Opérations CRUD complètes
- Capacites de filtrage et de recherche avancées
- Support de la pagination
- Gestion des erreurs avec des codes d'état appropriés
- Documentation de l'API avec OpenAPI/Swagger

Cette architecture garantit :

- La séparation des responsabilités
- Un code maintenable et extensible
- Une gestion des données sécurisée et efficace
- Une organisation claire de la logique métier
- Des tests et un débogage faciles

