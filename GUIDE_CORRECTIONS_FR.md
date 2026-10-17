# BADASS — Guide des corrections et de leur application

Date : 17 octobre 2026.

Ce lot transforme les recommandations de revue en fichiers de code, tests,
contrats de catalogue et documentation utilisables. BADASS est un banc d’essai
de sécurité : il contient volontairement des paires `vulnerable/` et `fixed/`.
Les versions vulnérables servent de témoins positifs pour l’évaluation.

## 1. Fichiers livrés

| Fichier | Contenu et usage |
|---|---|
| `BADASS-corrige.zip` | Copie complète du projet corrigé, avec sources, catalogue, outils, tests, documentation et rapports de cette vérification. |
| `BADASS-corrections.patch` | Diff Git applicable au commit de base indiqué ci-dessous ; comprend les nouveaux fichiers de code, les tests et la documentation. |
| `GUIDE_CORRECTIONS_FR.md` | Ce guide, également présent à la racine de l’archive. |

Les rapports d’exécution se trouvent dans `reports/` dans l’archive. Ce répertoire
est ignoré par Git et ne fait donc pas partie du patch. L’archive ne contient ni
historique Git, ni compilateurs, ni dépendances téléchargées, ni binaires de test.

**Dépôt d’origine :** [omnia-projetcs/BADASS](https://github.com/omnia-projetcs/BADASS).

**Base exacte du patch :**
[`87f8d5f162a1970becc2909211fabcca8165386d`](https://github.com/omnia-projetcs/BADASS/commit/87f8d5f162a1970becc2909211fabcca8165386d).

Les outils supprimés ont été restaurés depuis le parent
[`80f447c1be08de70042cf9fc6387a98b01dc6d72`](https://github.com/omnia-projetcs/BADASS/commit/80f447c1be08de70042cf9fc6387a98b01dc6d72),
puis adaptés aux nouveaux contrats. Les modifications livrées sont locales ;
aucune branche ni pull request n’a été publiée sur GitHub.

## 2. Corrections principales

| Problème constaté | Changement livré | Effet vérifié ou limite |
|---|---|---|
| Outils de benchmark supprimés | Restauration de `tools/` et des tests, ajout de `tools/smoke.py` et d’un workflow CI. | Une sélection vide, zéro contrôle exécuté ou une exécution entièrement ignorée ne donne plus un succès. |
| Classification incohérente du secret en Go et C# | Une seule distinction détermine contenu et droits : seul `public` autorise un fichier public. | Vecteurs `secret`, valeur inconnue, vide et majuscules ; ces deux runtimes ne sont pas disponibles ici. |
| Tests de fichiers fondés sur la sortie du programme | Contrôle indépendant du contenu, du type, du lien et du mode POSIX dans le runner. | Un retour constant sans création du fichier utile échoue. Les observations incohérentes sont refusées. |
| Jeton de réinitialisation insuffisamment évalué | Émission, validation et consommation réelles ; observation indépendante. | Bon jeton utilisable, mauvais jeton refusé, consommation unique, autres comptes préservés, générateur constant détecté. |
| Verdict de hachage déclaré par le candidat | Enregistrement scrypt réel et vérification indépendante du condensat, du sel et du profil annoncé. | Une mutation MD5 présentée comme scrypt, un sel constant et un vérificateur acceptant tout sont détectés. |
| Correction de session pouvant supprimer la fonction de connexion | Connexion, résolution, rotation et déconnexion effectives. | Nouvelle session authentifiée, ancienne session invalidée, autres utilisateurs préservés et logout effectif. |
| Affirmation IA toujours rejetée, même après réparation valide | Acceptation conditionnée à une preuve externe, non vide, entièrement réussie et liée au SHA-256 de l’artefact courant. | Un résultat valide peut fermer le constat ; une preuve absente, périmée, échouée, ignorée ou forgée dans le texte généré ne le ferme pas. |
| Entrées malformées et comparaisons Unicode | Vérification des objets, des types, de l’ASCII pour les jetons et de l’UTF-8 strict pour les mots de passe. | Les mots de passe configurés Unicode sont utilisables ; les formes invalides sont rejetées proprement. |
| Bornes natives et conversions numériques insuffisantes | Ajout des cas limites C/C++ et analyse complète des nombres avec rejet des suffixes et dépassements. | Les mutations de bornes supérieures, inférieures et de place du terminateur sont détectées sous sanitizers. |
| Fonction utile non exigée dans plusieurs scénarios | Succès avec un secret configuré, arguments contenant des espaces, export réel et propriétés propres légitimes. | Une correction qui refuse systématiquement l’opération utile ne satisfait plus ces contrats. |
| Quantité négative classée comme workflow | Remappage des 14 cas `business-logic` vers CWE-1284 et ajout d’un vrai workflow CWE-841. | La taxonomie correspond à l’opération effectivement exercée. |

Les sources concernées et chaque attente exacte sont listées dans
`catalog/cases.json`. Les README des cas et les matrices ont été régénérés depuis
ce catalogue, afin de conserver une seule source des contrats.

## 3. Huit nouvelles paires

| Identifiant du cas | CWE | Scénario et correction |
|---|---|---|
| `python/sql-order-by` | CWE-89 | Injection dans une expression de tri SQLite ; sélection du nom de colonne parmi des constantes serveur. |
| `python/sql-second-order` | CWE-89 | Valeur enregistrée puis relue dans une seconde requête ; liaison des paramètres également à cette seconde utilisation. |
| `python/xss-attribute` | CWE-79 | Échappement d’un attribut HTML délimité par des guillemets ; contrôle indépendant par un parseur HTML. |
| `rest-api/multi-tenant-authorization` | CWE-863 | Accès croisé entre deux tenants ; identité issue d’une session serveur et contrôle du tenant de la ressource. |
| `rest-api/order-workflow` | CWE-841 | Paiement, livraison et rejeu ; transitions autorisées et journaux de paiement/expédition réellement observés. |
| `rest-api/order-concurrency` | CWE-362 | Deux transactions concurrentes tentent d’expédier une commande ; une transition SQLite atomique réserve l’expédition à une seule. |
| `rest-api/ssrf-redirect` | CWE-918 | Une URL initialement autorisée redirige vers une ressource privée ; contrôle de chaque destination avant toute requête. |
| `ai/tool-argument-scope` | CWE-863 | Un outil d’écriture autorisé reçoit une destination hors de ses capacités ; contrôle serveur des chemins et conservation du fichier source synthétique. |

Le catalogue passe de **272 à 280 paires**, de **772 à 1 075 vecteurs** et de
**50 à 52 CWE distinctes**. Un vecteur possède une attente pour chacune des deux
variantes ; le nombre total théorique est donc de **2 150 contrôles de variantes**.
Ces nombres décrivent le corpus, pas une exécution complète de tous les langages.

## 4. Résultats de vérification

Les preuves sont jointes dans `reports/`. Elles ont été produites sur la copie
corrigée ; les rapports de régression contiennent les empreintes des sources et
des vecteurs réellement exécutés.

| Vérification | Résultat constaté |
|---|---|
| Validation du catalogue | 280 paires valides. |
| Suite `unittest` | 101 tests découverts : 100 réussis, 1 ignoré faute de `tsc`. |
| Test de fumée obligatoire | 6 paires, 102 contrôles réussis. |
| Régression globale locale | 162 paires réussies, 115 ignorées faute de runtime, 3 en échec de dépendance. |
| Contrôles effectivement lancés dans cette régression | 1 338 : 1 324 réussis et 14 échecs de chargement du module SQLite Node. |
| Nouveaux scénarios | Les huit nouvelles paires passent dans la régression globale. |
| Documentation et patch | Documentation régénérée ; contrôle de cohérence et vérification d’application du patch inclus dans le bilan de livraison. |

Les **trois échecs de dépendance** sont conservés comme échecs dans le rapport :

- `c/sql-injection` et `cpp/sql-injection` ne peuvent pas compiler car `sqlite3.h`
  et les fichiers de développement SQLite ne sont pas installés. Aucun de leurs
  vecteurs n’a été exécuté lors de cette régression.
- `node/sql-injection` ne peut pas charger le module `sqlite3`. Ses 14 invocations
  échouent au chargement, avant l’opération de base de données.

Les **115 paires ignorées** appartiennent à TypeScript, PHP, Ruby, Go, Java, Rust
et .NET, dont le compilateur ou runtime requis manque. La présence de `java`
seul ne remplace pas `javac`. Un test ciblé TypeScript a pu être exercé séparément
par la suppression native des annotations de Node 24 ; cela ne constitue pas une
validation de compilation `tsc --strict`.

La commande de régression globale renvoie donc un code d’échec dans cet
environnement. **La suite complète des 14 sections n’est pas déclarée verte.**
Docker n’est pas installé ici et le workflow GitHub Actions n’a pas été exécuté
à distance. Le workflow livré prévoit une exécution complète avec les dépendances
du Dockerfile, à effectuer dans cet environnement avant intégration définitive.

Fichiers de preuve :

- `reports/regression-local.json` et `reports/regression-local.log` ;
- `reports/tooling-tests.log` ;
- `reports/smoke.json` ;
- `reports/delivery-verification.json`, avec le bilan, les versions d’outils et
  les empreintes utiles pour retrouver la copie testée.

## 5. Utiliser directement l’archive

Extraire `BADASS-corrige.zip`, puis ouvrir un terminal dans son dossier
`BADASS-corrige/`. Python 3.11 ou ultérieur permet d’utiliser les outils et les
sections Python, CGI, REST API et IA.

```sh
python3 tools/lab.py validate
python3 -m unittest discover -s tests -v
python3 tools/smoke.py --output reports/smoke.json
python3 tools/lab.py test --language python --strict
```

Pour exercer un nouveau scénario précis :

```sh
python3 tools/lab.py test --case rest-api/order-concurrency --strict
python3 tools/lab.py test --case rest-api/ssrf-redirect --strict
```

Le second exemple crée uniquement un service HTTP éphémère sur la boucle locale.
Un environnement qui interdit les sockets devra autoriser cette opération locale
ou utiliser le conteneur prévu par le projet.

Pour la suite complète, sur un hôte Linux équipé de Docker :

```sh
make container-build
make container-test
```

La construction télécharge les dépendances. L’exécution des tests utilise ensuite
un réseau externe désactivé et écrit son rapport dans
`reports/container-regression.json`. Les prérequis SQL sont détaillés dans
`docs/SQL-INJECTION.md`.

## 6. Appliquer le patch à une copie Git

Placer le patch à côté du dossier de clone. Cette procédure crée une branche
depuis la base exacte, puis vérifie le patch avant de l’appliquer :

```sh
git clone https://github.com/omnia-projetcs/BADASS.git
cd BADASS
git switch -c security/benchmark-corrections 87f8d5f162a1970becc2909211fabcca8165386d
git apply --check ../BADASS-corrections.patch
git apply ../BADASS-corrections.patch
python3 tools/lab.py validate
python3 -m unittest discover -s tests -v
python3 tools/smoke.py --output reports/smoke.json
git diff --check
git status --short
```

Dans un clone existant comportant du travail en cours, créer un worktree dédié
depuis ce commit avant d’appliquer le patch. Si le dépôt a évolué depuis la base,
examiner les conflits et adapter le changement ; ne pas forcer son application
sur des lignes qui ont un autre sens.

Les nouveaux fichiers apparaîtront comme non suivis après `git apply` ; les
inclure lors de la préparation du commit. La publication éventuelle reste une
étape de votre processus de revue habituel.

## 7. Évaluer un scanner ou une correction

L’export à chemins neutres sépare les sources à scanner de leur table de vérité :

```sh
python3 tools/export_blind.py --output ../badass-blind --mapping ../badass-map.json
python3 tools/export_blind.py --normalize scanner-findings.json --mapping ../badass-map.json --output normalized.json
python3 tools/lab.py score --findings normalized.json
```

Chaque constat du scanner doit fournir `path`, chemin relatif exact dans
l’export, et `cwe`. Le mapping est conservé hors du corpus et les chemins inconnus
sont refusés. L’export contient les deux variantes sous des noms aléatoires ;
pour une tâche de réparation, ne fournir que la source candidate et conserver
les attentes, l’oracle et la correction témoin dans l’environnement de test.

Les octets des sources sont préservés : cette fonction retire les étiquettes
de dossiers et la documentation, mais n’élimine pas tous les indices sémantiques
ni un éventuel apprentissage préalable du corpus.

## 8. Portée des garanties

Ces corrections rendent le benchmark plus discriminant et corrigent les défauts
précis décrits. Elles ne constituent pas une certification de sécurité générale.
Les tests restent des fixtures bornées avec des données synthétiques.

Le profil scrypt du laboratoire doit être calibré séparément pour une application
réelle. Les contrôles POSIX n’évaluent pas les ACL Windows. Le scénario de
concurrence vérifie des transactions SQLite locales ; une livraison externe
résistante aux crashs demande un mécanisme de dispatch durable. Le scénario SSRF
n’évalue pas à lui seul le DNS, tous les schémas d’URL ou une politique réseau de
production. Les contrôles IA testent l’application autour du modèle et ne prouvent
pas la résistance d’un modèle aux injections de prompt.

Méthodologie complète : `docs/BENCHMARK.md`. Contrats IA : `docs/AI-TESTING.md`.
Références de classification :
[CWE-1284](https://cwe.mitre.org/data/definitions/1284.html),
[CWE-841](https://cwe.mitre.org/data/definitions/841.html) et
[CWE-362](https://cwe.mitre.org/data/definitions/362.html).
