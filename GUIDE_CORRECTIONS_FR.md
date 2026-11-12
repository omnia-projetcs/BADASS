# BADASS — Guide des corrections et de leur application

Date de mise à jour : 12 novembre 2026.

Ce guide documente l’état des sources, des contrats du catalogue, du jeu
d’entraînement JSONL et de la documentation du banc d’essai BADASS.
BADASS contient volontairement des paires `vulnerable/` et `fixed/` : les
versions vulnérables servent de témoins positifs d’audit et les versions
corrigées de témoins négatifs et de références de réparation.

## 1. Statistiques actuelles du corpus

| Métrique | Valeur |
|---|---:|
| Paires de cas (`catalog/cases.json`) | 395 |
| Variantes vulnérables et corrigées | 790 |
| Faiblesses CWE distinctes couvertes | 102 |
| Sections technologiques (`labs/*`) | 14 |
| Catégories OWASP représentées (Web 2025, API 2023, LLM 2025) | 30 |
| Vecteurs de régression déclarés | 1 999 |
| Contrôles de variantes déclarés (`2 × vecteurs`) | 3 998 |
| Conversations d’entraînement JSONL (`enrichissement/vulnerabilities.training.jsonl`) | 1 185 (0 doublon) |
| Projets multi-fichiers (`projects/*`) | 3 |
| Tests unitaires de la suite `tests/` | 214 |

## 2. Corrections et harmonisations appliquées

| Domaine | Anomalie constatée | Correction appliquée |
|---|---|---|
| **Jeu d’entraînement JSONL (`enrichissement/`)** | 45 enregistrements dupliqués dus à des fichiers identiques entre `python`, `cgi`, `rest-api`, `ai`, `c` et `cpp`. | Contextualisation propre à chaque section (`labs/cgi`, `labs/rest-api`, `labs/ai`) et réécriture idiomatique C++ (`labs/cpp`) : `1 023 / 1 023` exemples uniques (`duplicates_removed: 0`). |
| **Secrets codés en dur (CWE-798)** | Comparaison non constante (`==` ou `strcmp`) dans plusieurs langages. | Comparaison en temps constant généralisée aux 14 sections (`hmac.compare_digest`, `crypto.timingSafeEqual`, `subtle.ConstantTimeCompare`, `CryptographicOperations.FixedTimeEquals`, `MessageDigest.isEqual`, `hash_equals`, `OpenSSL.fixed_length_secure_compare`, `constant_time_equals`). |
| **Permissions de fichiers secrets (CWE-732)** | Fenêtre TOCTOU lors d’un `chmod` par chemin après l’ouverture ou la fermeture du fichier. | Application atomique du mode `0600` dès la création (`O_CREAT`, `umask`, `PosixFilePermissions`, `UnixCreateMode`) ou directement sur le descripteur ouvert (`fchmod` / `SafeFileHandle`) avant écriture. |
| **Suivi de liens symboliques (CWE-59)** | Risque de suivre un lien symbolique final ou de masquer une erreur de fermeture. | Création atomique exclusive (`O_CREAT \| O_EXCL` et `O_NOFOLLOW` lorsque disponible) et vérification explicite de la fermeture du descripteur. |
| **Injection d’en-têtes et de journaux (CWE-113, CWE-117)** | Octets nuls (`\0`) ou caractères de contrôle omis ; `\` non échappé avant `\r`/`\n` en Go. | Rejet strict de `\r`, `\n` et `\0` dans les 14 cas `header-injection` ; échappement préalable de `\\` avant `\r` et `\n` dans `log-injection`. |
| **Pollution de prototype (CWE-1321)** | `Object.assign(target, incoming)` superficiel en Node.js et TypeScript ne polluait pas réellement `Object.prototype`. | Remplacement dans `vulnerable/` par une fusion récursive (`merge`) rendant `{"__proto__": {"isAdmin": true}}` réellement exploitable, et filtrage strict sur objet sans prototype (`Object.create(null)`) dans `fixed/`. |
| **Bornes numériques et logique métier (CWE-190, CWE-400, CWE-1284)** | Dépassements d’entiers signés (UB en C/C++/Rust) ou exceptions non interceptées sur entrées non numériques (Java, .NET, PHP, Ruby, Node.js, TypeScript). | Analyse entière stricte sans dépassement, vérification préalable des bornes (`0..1024` ou `1..100`) et retour propre `"DENIED"` sur toute entrée malformée. |
| **Cas spécifiques Python (`labs/python/*`)** | Profondeur AST non bornée (`code-injection`), `NaN`/`Infinity` acceptés (`unsafe-deserialization`), traversée via répertoire de base symbolique (`zip-slip`, `tar-symlink-escape`), octets de contrôle dans `unrestricted-upload`, journalisation récursive (`sensitive-logging`), comparaison non constante (`unverified-update`). | Durcissement complet des variantes `fixed/` (limites AST/exposants, `allow_nan=False`, `O_NOFOLLOW`, filtrage des octets de contrôle, rédaction récursive, `hmac.compare_digest`, restriction de `__builtins__`). |
| **Projets complets (`projects/*`)** | `requirements.lock` et `package.json` pointant encore sur des versions vulnérables dans `fixed/` ; absence de migration dans `tenant-billing/vulnerable` ; TOCTOU sur invitations et faiblesses sur exports/signatures dans `tenant-billing/fixed`. | Mise à jour vers Django `5.1.14` et Next.js `14.2.25` dans `fixed/`, ajout de la migration initiale, `hmac.compare_digest`, validation stricte des chemins/liens symboliques d’export et verrouillage atomique `select_for_update()` des invitations. |
| **Outils et oracles (`tools/*`)** | Contournements potentiels par sous-classement `int` de `bool` ou mutation du dictionnaire de session retourné. | Vérification stricte de type (`type(x) is int`) et copie défensive dans `tools/repair_oracles.py` ; nettoyage de `tools/invoke.py`. |

## 3. Commandes de vérification et de régénération

Exécuter depuis la racine du dépôt (Python 3.11+ couvre les outils ainsi que
les sections `python`, `cgi`, `rest-api` et `ai`) :

```sh
# 1. Valider les 341 contrats du catalogue
python3 tools/lab.py validate

# 2. Régénérer et vérifier la documentation et les matrices CWE / OWASP / Technologies
python3 tools/render_docs.py
python3 tools/render_docs.py --check

# 3. Régénérer et vérifier le jeu d'entraînement JSONL (1 023 exemples uniques)
python3 tools/export_training.py
python3 tools/export_training.py --check

# 4. Exécuter la suite complète de tests unitaires (211 tests)
python3 -m unittest discover -s tests -v

# 5. Exécuter les régressions strictes Python, CGI, REST API et IA
python3 tools/lab.py test --language python --strict
python3 tools/lab.py test --language cgi --strict
python3 tools/lab.py test --language rest-api --strict
python3 tools/lab.py test --language ai --strict
```

Pour exécuter l’intégralité des 14 sections technologiques (incluant C, C++, Go,
PHP, Node.js, TypeScript, .NET, Java, Ruby et Rust) dans un environnement isolé
sans réseau externe :

```sh
make container-build
make container-test
```

Pour préparer et tester les cas de dépendances npm (`CWE-1395`) :

```sh
make dependency-prepare
make dependency-test
```

## 4. Évaluer un scanner ou une réparation à l’aveugle

L’export à chemins neutres sépare les sources à scanner de leur table de vérité :

```sh
python3 tools/export_blind.py --output ../badass-blind --mapping ../badass-map.json
python3 tools/export_blind.py --normalize scanner-findings.json --mapping ../badass-map.json --output normalized.json
python3 tools/lab.py score --findings normalized.json
```

Chaque constat du scanner doit fournir `path` (chemin relatif exact dans
l’export) et `cwe`. Le mapping est conservé hors du corpus et les chemins inconnus
sont refusés.

## 5. Portée des garanties

Ces corrections garantissent que chaque variante `vulnerable/` présente une
faiblesse réelle et exploitable par les vecteurs du catalogue, et que chaque
variante `fixed/` applique une remédiation saine, idiomatique et exempte d’effets
de bord ou de contournements triviaux. Les tests demeurent des fixtures bornées
utilisant des données synthétiques locales.

Méthodologie complète : [`docs/BENCHMARK.md`](docs/BENCHMARK.md).
Contrats d’évaluation IA : [`docs/AI-TESTING.md`](docs/AI-TESTING.md).
Notes de revue en anglais : [`docs/REVIEW-CHANGES.md`](docs/REVIEW-CHANGES.md).
