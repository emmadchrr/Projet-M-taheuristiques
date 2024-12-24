# Problème de Sac à Dos Multidimensionnel (Multidimensional Knapsack Problem)

## Description

On s’intéresse à un problème d’école en optimisation combinatoire : **Problème du sac à dos multidimensionnel (Multidimensional Knapsack Problem)**.  
Ce problème peut servir à modéliser le problème d’allocation de ressources (capital budgeting).

### Données

Étant donnés :

- **N** projets et **M** ressources.
- **bᵢ**, la quantité de ressource *i* disponible (*i = 1, ..., M*).
- **cⱼ**, le profit (ou gain) associé au projet *j* (*j = 1, ..., N*).
- **aᵢⱼ**, la quantité de ressource *i* consommée par le projet *j* (*i = 1, ..., M* et *j = 1, ..., N*).

### Objectif

Le problème d’allocation de ressources consiste à sélectionner un sous-ensemble de projets tel que le gain total soit maximisé dans la limite des ressources disponibles.

### Formulation mathématique

Une formulation classique de ce problème est la suivante :

**Maximiser :**

\[
f(x) = \sum_{j=1}^N c_j x_j
\]

**Sous contraintes :**

\[
\sum_{j=1}^N a_{ij} x_j \leq b_i \quad \forall i = 1, ..., M \tag{1}
\]

\[
x_j \in \{0, 1\} \quad \forall j = 1, ..., N \tag{2}
\]

avec :

- \( x_j = 1 \) si le projet \( j \) est accepté (\( x_j = 0 \) sinon).

### Hypothèses sur les données

- \( c_j \) et \( b_i \) sont des entiers positifs.
- \( A_j = (a_{ij})_{i=1,...,M} \) est différent du vecteur nul \( \forall j \in \{1, ..., N\} \).

---

## Objectif du projet

L’objectif de ce devoir est la résolution approchée du problème de sac à dos multidimensionnel par l’intermédiaire d’une métaheuristique.
