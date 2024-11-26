# Système de Combat Donjons & Dragons - Projet POO

## Objectif
Créer un système de combat inspiré de Donjons & Dragons, permettant à 1 ou plusieurs héros de combattre 1 ou plusieurs monstres. Le projet utilise les concepts d'objets, de classes, d'héritage et de méthodes de la programmation orientée objet (POO) pour modéliser les créatures, leurs actions et les règles de combat.

## Fonctionnalités
- Système de combat au tour par tour avec initiative.
- Actions variées : attaque, soin, et buff.
- Jet de dés pour l'initiative et les actions.
- Gestion de la victoire ou de la défaite selon les créatures restantes.

## Architecture logicielle

### Classes Principales
1. **`Creature`** (classe abstraite)  
   - Attributs : `nom`, `description`, `pv` (points de vie), `defense`, `initiative`, `degatsMax`, `typeDegats`, `etats`.
   - Méthodes : `attaque()`.
   - But : Représente les caractéristiques communes aux créatures du jeu.

2. **`Heros`** (hérite de `Creature`)  
   - Attributs supplémentaires : `arme`, `inventaire`.
   - Méthodes : Hérite des méthodes de `Creature` et ajoute des spécificités liées aux héros.

3. **`Monstre`** (hérite de `Creature`)  
   - Attributs supplémentaires : `resistance` (liste des résistances aux types de dégâts).
   - Méthodes : Hérite des méthodes de `Creature` avec des spécificités pour les monstres.

### Classes Supplémentaires
1. **`Arme`**  
   - Attributs : `typeDegats`, `degatsMax`.
   - Méthodes : `attaquer()`, retourne les dégâts infligés en fonction de l’arme.

2. **`Action`** (classe abstraite)
   - Attributs : `lanceur` (créature qui exécute l'action), `cible` (cible de l'action).
   - Méthode abstraite : `executer()`.
   - But : Modèle générique pour toutes les actions.

3. **`Attaque`, `Soin`, `Buff`** (héritent de `Action`)  
   - Implémentent la méthode `executer()` :
     - `Attaque` : Vérifie si l’attaque touche la cible et applique les dégâts.
     - `Soin` : Applique des soins aux points de vie de la cible.
     - `Buff` : Applique un effet bénéfique à la cible (ajustable).

4. **`Jeu`**
   - Attributs : `heros`, `monstres`, `ordreInitiative`.
   - Méthodes : 
     - `initialiserCombat()` : Lance l’initiative pour toutes les créatures.
     - `tourDeCombat()` : Gère le tour de chaque créature selon l’ordre d’initiative.
     - `verifierVictoire()` : Vérifie si tous les monstres ou tous les héros sont vaincus.
   - But : Contrôle le déroulement du combat et gère les tours.

5. **`Dé`**
   - Méthode statique : `lancer(nb_faces)` - Génère un nombre aléatoire entre `1` et `nb_faces`.
   - But : Centralise la logique des jets de dés pour les initiatives et les dégâts.

## Déroulement du Combat
1. **Initialisation** : Le joueur choisit le nombre de héros et de monstres. Ensuite, chaque créature lance un jet d'initiative (`d20`) pour déterminer l'ordre des tours.
2. **Tour de jeu** :
   - La créature active choisit une action (`Attaque`, `Soin`, ou `Buff`) et la cible.
   - Si besoin, un jet de dé est effectué pour déterminer les dégâts ou la réussite de l'action.
   - Si une créature atteint 0 PV ou moins, elle ne peut plus agir.
3. **Fin du Combat** : Le combat se termine lorsque tous les monstres ou tous les héros sont vaincus. Le vainqueur est annoncé, et le joueur peut choisir de relancer un nouveau combat.

## Choix de Conception

### Abstraction et Héritage
- `Creature` centralise les attributs communs et utilise l’héritage pour les classes `Heros` et `Monstre`, évitant la redondance de code.
- Les actions `Attaque`, `Soin`, et `Buff` sont des sous-classes de `Action`, ce qui permet d'ajouter facilement de nouveaux types d'actions.

### Modularité et Séparation des Responsabilités
- `Jeu` gère la logique de déroulement des combats, tandis que les classes de créatures et d’actions sont focalisées sur leurs caractéristiques spécifiques.
- La classe `Dé` permet de gérer les jets de dés de manière centralisée, ce qui améliore la testabilité et la lisibilité.

### Extensibilité
Grâce aux classes abstraites et à la modularité, il est possible d'ajouter des fonctionnalités (nouveaux types de créatures, d'actions, etc.) sans modifier la structure de base du code.

## Améliorations Optionnelles
- Permettre au joueur de configurer les caractéristiques de base des héros.
- Modifier le nombre de monstres ou de héros pour ajuster la difficulté.
- Ajouter d'autres options de combat pour plus de complexité.

## Conseils d'Utilisation
- Utilisez la fonction `print()` pour déboguer et vérifier le contenu des variables.
- Prenez le temps de lire les erreurs et d’en comprendre la cause avant de chercher une solution.

## Conclusion
Ce projet met en application les concepts de la POO pour créer un jeu de combat inspiré de Donjons & Dragons, intégrant héritage, encapsulation, et modularité pour offrir une architecture claire et extensible.

---

## Licence
Projet éducatif pour l'apprentissage de la programmation orientée objet.
