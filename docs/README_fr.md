# 🎨 PhotoGIMP

<img src="../.local/share/icons/hicolor/256x256/256x256.png" align="right" alt="Icône de l'application PhotoGIMP" title="Icône de l'application PhotoGIMP">

[![GitHub stars](https://img.shields.io/github/stars/Diolinux/PhotoGIMP?style=social)](https://github.com/Diolinux/PhotoGIMP)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Latest Release](https://img.shields.io/github/v/release/Diolinux/PhotoGIMP)](https://github.com/Diolinux/PhotoGIMP/releases/latest)

**PhotoGIMP** est un patch gratuit, porté par la communauté, qui transforme [GIMP](https://www.gimp.org/) (GNU Image Manipulation Program) en une interface familière pour les utilisateurs d'**Adobe Photoshop**. Si vous passez de Photoshop à GIMP et que vous voulez vous sentir chez vous dès le départ, PhotoGIMP est fait pour vous.

> **Nouveau sur GIMP ?** GIMP est un éditeur d'images gratuit et open source disponible pour Linux, macOS et Windows. Il peut faire la plupart de ce que fait Photoshop — retouche photo, composition d'images, création graphique et bien plus — le tout gratuitement. PhotoGIMP le rend simplement _plus proche de Photoshop_ dans son apparence et son ergonomie.

---

## ✨ Fonctionnalités

- **Disposition des outils façon Photoshop** — Les outils sont réorganisés pour imiter les positions auxquelles vous êtes habitué dans Adobe Photoshop.
- **Écran de démarrage personnalisé** — Un splash screen exclusif PhotoGIMP vous accueille au lancement.
- **Espace de travail maximisé** — Les réglages par défaut sont optimisés pour vous offrir la plus grande zone de travail possible.
- **Raccourcis clavier Photoshop** — Les raccourcis suivent la [documentation officielle d'Adobe](https://helpx.adobe.com/photoshop/using/default-keyboard-shortcuts.html) pour la version Windows.
- **Icône et nom personnalisés** — Un fichier `.desktop` dédié donne à PhotoGIMP sa propre icône et son propre nom dans le menu de votre système.

---

## 📷 Captures d'écran

| Écran de démarrage | Fenêtre de l'application |
|-|-|
| ![[Splash screen PhotoGIMP Diolinux]](../.config/GIMP/3.0/splashes/splash-screen-2025-v2.png)<br>Splash screen PhotoGIMP Diolinux | ![[PhotoGIMP 3]](../screenshots/photogimp_3_-_diolinux.png)<br>PhotoGIMP 3

---

## 📋 Prérequis

Avant d'installer PhotoGIMP, assurez-vous d'avoir :

| Prérequis                       | Détails                                                                                                                                                        |
| ------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **GIMP 3.0 ou plus récent**     | Téléchargez-le depuis : [gimp.org](https://www.gimp.org/downloads/) ou [Flathub](https://flathub.org/apps/org.gimp.GIMP) (Linux)                               |
| **Lancer GIMP au moins une fois** | GIMP doit générer ses fichiers de configuration avant que PhotoGIMP puisse les remplacer. **Installez GIMP → ouvrez-le → fermez-le → puis installez PhotoGIMP.** |

---

## ⚙ Comment Installer

> [!WARNING]
> **Sauvegardez vos réglages GIMP actuels avant d'installer !** PhotoGIMP écrase les fichiers de configuration de GIMP. Si vous avez des réglages personnalisés que vous souhaitez conserver, faites d'abord une copie de sauvegarde. Consultez les instructions de sauvegarde dans chaque section ci-dessous.

---

### 🐧 Flatpak (Linux)

<img src="https://skillicons.dev/icons?i=linux" align="right" width="40" />

#### Sauvegarde (optionnelle)

Si vous souhaitez conserver vos réglages GIMP actuels, sauvegardez-les d'abord :

```bash
cp -r ~/.config/GIMP/3.0 ~/GIMP-3.0-backup
```

#### Installation

1. Assurez-vous d'avoir déjà GIMP installé [depuis Flathub](https://flathub.org/apps/org.gimp.GIMP).
2. **Ouvrez GIMP une fois, puis fermez-le** — cela crée les dossiers de configuration dont PhotoGIMP a besoin.
3. Téléchargez la dernière version :
   👉 **[Télécharger PhotoGIMP pour Linux (.zip)](https://github.com/Diolinux/PhotoGIMP/releases/download/3.0/PhotoGIMP-linux.zip)**
4. Extrayez le fichier `.zip` **dans votre dossier personnel** (`~`).
    - Cela placera les fichiers dans `~/.config` et `~/.local`, qui sont des dossiers cachés.
    - Pour afficher les dossiers cachés dans votre gestionnaire de fichiers, appuyez sur <kbd>Ctrl</kbd> + <kbd>H</kbd>.
    - Lorsqu'on vous interroge sur les fichiers existants, choisissez **« Remplacer »** ou **« Écraser »**.
5. Ouvrez GIMP — vous devriez voir la nouvelle interface PhotoGIMP ! 🎉

<details>
<summary><strong>💡 Vous utilisez un GIMP non-Flatpak ?</strong></summary>

Si vous avez installé GIMP depuis le gestionnaire de paquets de votre distribution (apt, dnf, pacman, etc.) au lieu de Flatpak, le dossier de configuration se trouve au même endroit (`~/.config/GIMP/3.0`), donc les étapes ci-dessus fonctionnent aussi. Assurez-vous simplement d'avoir GIMP en version 3.0 ou plus récente.

</details>

---

### 🪟 Windows

<img src="https://skillicons.dev/icons?i=windows" align="right" />

#### Sauvegarde (optionnelle)

Si vous souhaitez conserver vos réglages GIMP actuels, sauvegardez-les d'abord :

1. Appuyez sur <kbd>Windows</kbd> + <kbd>R</kbd> pour ouvrir la boîte de dialogue Exécuter.
2. Tapez `%APPDATA%\GIMP` et appuyez sur <kbd>Entrée</kbd>.
3. Copiez l'intégralité du dossier `3.0` vers un emplacement sûr (par exemple votre Bureau).

#### Installation

1. Assurez-vous d'avoir [GIMP installé depuis le site officiel](https://www.gimp.org/downloads/).
2. **Ouvrez GIMP une fois, puis fermez-le** — cela crée les dossiers de configuration dont PhotoGIMP a besoin.
3. Téléchargez la dernière version :
   👉 **[Télécharger PhotoGIMP pour Windows (.zip)](https://github.com/Diolinux/PhotoGIMP/releases/download/3.0/PhotoGIMP.zip)**
4. Extrayez le contenu de `PhotoGIMP.zip` dans n'importe quel dossier (par exemple votre Bureau).
5. Ouvrez le dossier extrait et **copiez le dossier `3.0`**.
6. Appuyez sur <kbd>Windows</kbd> + <kbd>R</kbd> pour ouvrir la boîte de dialogue Exécuter.
7. Tapez `%APPDATA%\GIMP` et appuyez sur <kbd>Entrée</kbd> — cela ouvre le dossier des paramètres de GIMP.
8. **Collez** le dossier `3.0` ici.
9. Lorsqu'on vous interroge sur les fichiers existants, sélectionnez **« Remplacer les fichiers dans la destination »**.
10. Ouvrez GIMP — vous devriez voir la nouvelle interface PhotoGIMP ! 🎉

<details>
<summary><strong>💡 Optionnel : changer l'icône du raccourci GIMP</strong></summary>

Vous pouvez également télécharger [photogimp.ico](https://github.com/Diolinux/PhotoGIMP/releases/download/3.0/photogimp.ico) et mettre à jour l'icône du raccourci GIMP situé dans :

```
%appdata%\Microsoft\Windows\Start Menu\Programs\GIMP 3.0.0
```

Clic droit sur le raccourci → **Propriétés** → **Changer d'icône** → sélectionnez le fichier `.ico` téléchargé.

</details>

<details>
<summary><strong>🍫 Installation via Chocolatey (alternative)</strong></summary>

Si vous utilisez [Chocolatey](https://chocolatey.org/), vous pouvez installer PhotoGIMP avec une seule commande :

```powershell
choco install photogimp
```

Maintenu par : [André Augusto](https://github.com/AndreAugustoDev)

</details>

---

### 🍎 macOS

<img src="https://skillicons.dev/icons?i=macos" align="right" />

#### Sauvegarde (optionnelle)

Si vous souhaitez conserver vos réglages GIMP actuels, sauvegardez-les d'abord :

1. Ouvrez le Finder.
2. Appuyez sur <kbd>Cmd</kbd> + <kbd>Maj</kbd> + <kbd>G</kbd> et allez dans `~/Library/Application Support/GIMP`.
3. Copiez l'intégralité du dossier `GIMP` vers un emplacement sûr (par exemple votre Bureau).

#### Installation

1. Assurez-vous d'avoir [GIMP installé depuis le site officiel](https://www.gimp.org/downloads/).
2. **Ouvrez GIMP une fois, puis fermez-le** — cela crée les dossiers de configuration dont PhotoGIMP a besoin.
3. Téléchargez la dernière version :
   👉 **[Télécharger PhotoGIMP pour macOS (.zip)](https://github.com/Diolinux/PhotoGIMP/releases/download/3.0/PhotoGIMP.zip)**
4. Extrayez le contenu de `PhotoGIMP.zip` dans n'importe quel dossier (par exemple votre Bureau).
5. Ouvrez le dossier extrait et **copiez le dossier `3.0`**.
6. Ouvrez le Finder, appuyez sur <kbd>Cmd</kbd> + <kbd>Maj</kbd> + <kbd>G</kbd> pour ouvrir « Aller au dossier ».
7. Tapez `~/Library/Application Support/GIMP` et appuyez sur <kbd>Entrée</kbd>.
8. Si vous voyez un dossier `2.10` provenant d'une installation précédente, **supprimez-le** pour éviter les conflits.
9. **Collez** le dossier `3.0` à l'intérieur du dossier GIMP.
10. Lorsqu'on vous interroge sur les fichiers existants, sélectionnez **« Remplacer »** ou **« Fusionner »**.
11. Ouvrez GIMP — vous devriez voir la nouvelle interface PhotoGIMP ! 🎉

<details>
<summary><strong>Alternative : installation avec le Terminal</strong></summary>

Si l'option **« Fusionner »** du Finder ignore silencieusement des fichiers existants, ou si vous préférez la ligne de commande, vous pouvez copier les fichiers de PhotoGIMP avec `rsync`.

1. Ouvrez le Terminal.
2. Exécutez `rsync`, en remplaçant `/chemin/vers/extrait/3.0/` par l'emplacement du dossier `3.0` extrait :

   ```bash
   rsync -av --ignore-times /chemin/vers/extrait/3.0/ ~/Library/Application\ Support/GIMP/3.0/
   ```

   Assurez-vous que les deux chemins se terminent par `/`.
3. Si votre installation de GIMP utilise un dossier de version différent, adaptez la destination en conséquence (par exemple, utilisez `~/Library/Application\ Support/GIMP/3.2/` pour GIMP 3.2).

</details>

---

## 📦 Contenu du Patch

PhotoGIMP remplace ou ajoute les fichiers suivants dans le répertoire de configuration de GIMP :

| Fichier / Dossier | Rôle                                                        |
| ----------------- | ------------------------------------------------------------ |
| `shortcutsrc`     | Raccourcis clavier calqués sur ceux de Photoshop             |
| `toolrc`          | Configuration et ordre des outils                            |
| `sessionrc`       | Disposition des fenêtres et position des panneaux            |
| `dockrc`          | Configuration des docks / panneaux                           |
| `gimprc`          | Préférences générales de GIMP (canevas, grille, etc.)        |
| `contextrc`       | Réglages du contexte actif (outil/couleur)                   |
| `splashes/`       | Écran de démarrage personnalisé PhotoGIMP                    |
| `theme.css`       | Petits ajustements du thème de l'interface                   |
| `templaterc`      | Modèles de canevas prédéfinis                                |

Sous Linux, le patch installe également :

- Un fichier `.desktop` personnalisé (lanceur d'application avec le nom et l'icône PhotoGIMP)
- Une icône d'application personnalisée dans `~/.local/share/icons/`

---

## 🗑 Comment Désinstaller

Pour supprimer PhotoGIMP et restaurer GIMP dans son état par défaut, supprimez simplement le dossier de configuration de GIMP et rouvrez GIMP — il régénérera des réglages par défaut tout neufs.

### Linux

```bash
rm -rf ~/.config/GIMP/3.0
```

Puis rouvrez GIMP — il créera une toute nouvelle configuration par défaut.

Si vous avez fait une sauvegarde auparavant, restaurez-la plutôt :

```bash
cp -r ~/GIMP-3.0-backup ~/.config/GIMP/3.0
```

### Windows

1. Appuyez sur <kbd>Windows</kbd> + <kbd>R</kbd>, tapez `%APPDATA%\GIMP` et appuyez sur <kbd>Entrée</kbd>.
2. Supprimez le dossier `3.0`.
3. Ouvrez GIMP — il recréera les réglages par défaut.

Ou restaurez votre sauvegarde en recollant le dossier `3.0` sauvegardé.

### macOS

1. Ouvrez le Finder, appuyez sur <kbd>Cmd</kbd> + <kbd>Maj</kbd> + <kbd>G</kbd>.
2. Allez dans `~/Library/Application Support/GIMP`.
3. Supprimez le dossier `3.0`.
4. Ouvrez GIMP — il recréera les réglages par défaut.

Ou restaurez votre sauvegarde en recollant le dossier sauvegardé.

---

## ❓ Dépannage / FAQ

> [!CAUTION]
> **PhotoGIMP n'a pas de site web officiel.** La seule source officielle du projet est son dépôt GitHub : https://github.com/Diolinux/PhotoGIMP/

<details>
<summary><strong>PhotoGIMP n'a rien changé — GIMP est identique à avant</strong></summary>

- Assurez-vous d'avoir extrait les fichiers au **bon emplacement**. L'erreur la plus courante est d'extraire dans le mauvais dossier.
- **Linux** : les dossiers `.config` et `.local` doivent se trouver dans votre dossier personnel (`~`). Ils sont cachés — appuyez sur <kbd>Ctrl</kbd> + <kbd>H</kbd> dans votre gestionnaire de fichiers pour les afficher.
- **Windows** : le dossier `3.0` doit se trouver à l'intérieur de `%APPDATA%\GIMP`, pas à côté.
- **macOS** : le dossier `3.0` doit se trouver à l'intérieur de `~/Library/Application Support/GIMP`.
- Avez-vous **fermé GIMP** avant de coller les fichiers ? GIMP peut écraser les réglages entrants à sa fermeture.
  </details>

<details>
<summary><strong>J'obtiens une erreur en ouvrant GIMP après avoir installé PhotoGIMP</strong></summary>

- Cela signifie généralement que la version de GIMP ne correspond pas. PhotoGIMP est conçu pour **GIMP 3.0+**. Si vous utilisez GIMP 2.x, il ne sera pas compatible.
- Essayez de supprimer le dossier de configuration et de réinstaller — voir la section [Comment Désinstaller](#-comment-désinstaller).
  </details>

<details>
<summary><strong>Puis-je utiliser PhotoGIMP avec GIMP 2.10 ?</strong></summary>

Non. Cette version de PhotoGIMP est conçue exclusivement pour **GIMP 3.0 et plus récent**. Le format de configuration a changé de manière significative entre GIMP 2.x et 3.x.

</details>

<details>
<summary><strong>PhotoGIMP va-t-il supprimer mes brosses, polices ou plug-ins personnalisés ?</strong></summary>

Non. PhotoGIMP ne remplace que les fichiers de configuration (raccourcis, disposition, préférences). Vos brosses, polices, dégradés et plug-ins personnels restent intacts.

</details>

<details>
<summary><strong>Puis-je personnaliser les raccourcis après avoir installé PhotoGIMP ?</strong></summary>

Absolument ! PhotoGIMP définit simplement un point de départ. Vous pouvez modifier n'importe quel raccourci dans GIMP via **Édition → Raccourcis clavier**.

</details>

<details>
<summary><strong>Comment mettre à jour PhotoGIMP vers une nouvelle version ?</strong></summary>

Téléchargez simplement la dernière version et suivez à nouveau les étapes d'installation — elle écrasera la configuration PhotoGIMP précédente.

</details>

---

## 🤝 Contribuer

Vous avez trouvé un bug ? Vous avez une suggestion ? Votre aide est la bienvenue !

- **Signaler un problème** : [Ouvrir une issue](https://github.com/Diolinux/PhotoGIMP/issues)
- **Proposer un correctif** : [Créer une pull request](https://github.com/Diolinux/PhotoGIMP/pulls)
- **Traduire** : Aidez-nous à traduire le README dans d'autres langues ! Consultez la section [Traductions](#-traductions).

---

## 🌍 Traductions

Ce README est disponible dans d'autres langues :

- 🇬🇧 [English (Anglais)](../README.md)
- 🇮🇹 [Italiano (Italien)](./README_it.md)
- 🇵🇱 [Polski (Polonais)](./README_pl.md)
- 🇺🇦 [Українська (Ukrainien)](./README_ua.md)
- 🇧🇷 [Português (Portugais brésilien)](./README_pt.md)
- 🇷🇺 [Русский (Russe)](./README_ru.md)
- 🇪🇸 [Español (Espagnol)](./README_es.md)
- 🇮🇱 [עברית (Hébreu)](./README_he.md)
- 🇰🇷 [한국어 (Coréen)](./README_ko.md)
- 🇨🇳 [简体中文 (Chinois simplifié)](./README_zh.md)

Vous voulez ajouter votre langue ? Forkez le dépôt, créez un fichier `docs/README_xx.md` et soumettez une pull request !

---

## 🏆 Crédits

- Ce projet ne serait pas possible sans la formidable équipe de [GIMP](https://www.gimp.org/).
- Un GRAND merci à tous les soutiens de Diolinux sur [YouTube](https://youtube.com/Diolinux).
- Splash screen et icônes par [Adriel Filipe Design](https://bento.me/adrielfilipedesign).

---

## 👥 Contributeurs

<a align="center" href="https://github.com/Diolinux/PhotoGIMP/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=Diolinux/PhotoGIMP" />
</a>

---

## 📄 Licence

PhotoGIMP est distribué sous licence [GNU General Public License v3.0](../LICENSE).
