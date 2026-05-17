# 🎨 PhotoGIMP

<img src="../.local/share/icons/hicolor/256x256/256x256.png" align="right" alt="Icona dell'applicazione PhotoGIMP" title="Icona dell'applicazione PhotoGIMP">

[![GitHub stars](https://img.shields.io/github/stars/Diolinux/PhotoGIMP?style=social)](https://github.com/Diolinux/PhotoGIMP)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Latest Release](https://img.shields.io/github/v/release/Diolinux/PhotoGIMP)](https://github.com/Diolinux/PhotoGIMP/releases/latest)

**PhotoGIMP** è una patch gratuita, sviluppata dalla community, che trasforma [GIMP](https://www.gimp.org/) (GNU Image Manipulation Program) in un'interfaccia familiare per gli utenti di **Adobe Photoshop**. Se stai passando da Photoshop a GIMP e vuoi sentirti subito a casa, PhotoGIMP fa al caso tuo.

> **Nuovo su GIMP?** GIMP è un editor di immagini gratuito e open source disponibile per Linux, macOS e Windows. Può fare gran parte di ciò che fa Photoshop: fotoritocco, composizione di immagini, grafica e molto altro, tutto gratis. PhotoGIMP lo rende solo *più simile a Photoshop* nell'aspetto e nell'esperienza d'uso.

---

## ✨ Funzionalità

- **Layout strumenti in stile Photoshop** — Gli strumenti sono riorganizzati per imitare le posizioni a cui sei abituato in Adobe Photoshop.
- **Schermata di avvio personalizzata** — Una splash screen esclusiva di PhotoGIMP ti accoglie all'avvio.
- **Area di lavoro massimizzata** — Le impostazioni predefinite sono ottimizzate per offrirti il maggior spazio di lavoro possibile.
- **Scorciatoie da tastiera in stile Photoshop** — Le scorciatoie seguono la [documentazione ufficiale Adobe](https://helpx.adobe.com/photoshop/using/default-keyboard-shortcuts.html) per la versione Windows.
- **Icona e nome personalizzati** — Un file `.desktop` dedicato assegna a PhotoGIMP un'icona e un nome propri nel menu di sistema.

---

## 📷 Screenshot

<p>
  <img src="../.config/GIMP/3.0/splashes/splash-screen-2025-v2.png" alt="PhotoGIMP Diolinux Splash Art">
  <em>PhotoGIMP Diolinux Splash Art</em>
</p>

<p>
  <img src="../screenshots/photogimp_3_-_diolinux.png" alt="PhotoGIMP 3">
  <em>GIMP 3.0 con la patch PhotoGIMP applicata</em>
</p>

---

## 📋 Requisiti

Prima di installare PhotoGIMP, assicurati di avere:

| Requisito | Dettagli |
|---|---|
| **GIMP 3.0 o successivo** | Scaricalo da: [gimp.org](https://www.gimp.org/downloads/) o [Flathub](https://flathub.org/apps/org.gimp.GIMP) (Linux) |
| **Avvia GIMP almeno una volta** | GIMP deve generare i file di configurazione prima che PhotoGIMP possa sovrascriverli. **Installa GIMP → aprilo → chiudilo → poi installa PhotoGIMP.** |

---

## ⚙ Come Installare

> [!WARNING]
> **Fai un backup delle impostazioni attuali di GIMP prima di installare!** PhotoGIMP sovrascrive i file di configurazione di GIMP. Se hai impostazioni personalizzate che vuoi conservare, salva prima una copia di backup. Vedi le istruzioni di backup in ciascuna sezione qui sotto.

---

### 🐧 Flatpak (Linux)

<img src="https://skillicons.dev/icons?i=linux" align="right" width="40" />

#### Backup (opzionale)

Se vuoi mantenere le impostazioni attuali di GIMP, esegui prima un backup:

```bash
cp -r ~/.config/GIMP/3.0 ~/GIMP-3.0-backup
```

#### Installazione

1. Assicurati di avere già GIMP installato [da Flathub](https://flathub.org/apps/org.gimp.GIMP).
2. **Apri GIMP una volta e poi chiudilo**: questo crea le cartelle di configurazione necessarie a PhotoGIMP.
3. Scarica l'ultima release:
   👉 **[Scarica PhotoGIMP per Linux (.zip)](https://github.com/Diolinux/PhotoGIMP/releases/download/3.0/PhotoGIMP-linux.zip)**
4. Estrai il file `.zip` **nella tua cartella home** (`~`).
   - In questo modo i file verranno copiati in `~/.config` e `~/.local`, che sono cartelle nascoste.
   - Per vedere le cartelle nascoste nel file manager, premi <kbd>Ctrl</kbd> + <kbd>H</kbd>.
   - Quando richiesto sui file esistenti, scegli **"Sostituisci"** o **"Sovrascrivi"**.
5. Apri GIMP: dovresti vedere il nuovo layout di PhotoGIMP. 🎉

<details>
<summary><strong>💡 Usi GIMP non installato da Flatpak?</strong></summary>

Se hai installato GIMP dal package manager della tua distribuzione (apt, dnf, pacman, ecc.) invece di Flatpak, la cartella di configurazione è nello stesso percorso (`~/.config/GIMP/3.0`), quindi i passaggi sopra funzionano ugualmente. Assicurati solo di usare GIMP 3.0 o successivo.
</details>

---

### 🪟 Windows

<img src="https://skillicons.dev/icons?i=windows" align="right" />

#### Backup (opzionale)

Se vuoi mantenere le impostazioni attuali di GIMP, esegui prima un backup:

1. Premi <kbd>Windows</kbd> + <kbd>R</kbd> per aprire la finestra Esegui.
2. Digita `%APPDATA%\GIMP` e premi <kbd>Invio</kbd>.
3. Copia l'intera cartella `3.0` in una posizione sicura (per esempio il Desktop).

#### Installazione

1. Assicurati di avere [GIMP installato dal sito ufficiale](https://www.gimp.org/downloads/).
2. **Apri GIMP una volta e poi chiudilo**: questo crea le cartelle di configurazione necessarie a PhotoGIMP.
3. Scarica l'ultima release:
   👉 **[Scarica PhotoGIMP per Windows (.zip)](https://github.com/Diolinux/PhotoGIMP/releases/download/3.0/PhotoGIMP.zip)**
4. Estrai il contenuto di `PhotoGIMP.zip` in una cartella qualsiasi (per esempio il Desktop).
5. Apri la cartella estratta e **copia la cartella `3.0`**.
6. Premi <kbd>Windows</kbd> + <kbd>R</kbd> per aprire la finestra Esegui.
7. Digita `%APPDATA%\GIMP` e premi <kbd>Invio</kbd>: si aprirà la cartella impostazioni di GIMP.
8. **Incolla** qui la cartella `3.0`.
9. Quando richiesto sui file esistenti, seleziona **"Sostituisci i file nella destinazione"**.
10. Apri GIMP: dovresti vedere il nuovo layout di PhotoGIMP. 🎉

<details>
<summary><strong>💡 Opzionale: cambia l'icona del collegamento di GIMP</strong></summary>

Puoi anche scaricare [photogimp.ico](https://github.com/Diolinux/PhotoGIMP/releases/download/3.0/photogimp.ico) e aggiornare l'icona del collegamento di GIMP che si trova in:

```
%appdata%\Microsoft\Windows\Start Menu\Programs\GIMP 3.0.0
```

Clic destro sul collegamento → **Proprietà** → **Cambia icona** → seleziona il file `.ico` scaricato.
</details>

<details>
<summary><strong>🍫 Installa tramite Chocolatey (alternativa)</strong></summary>

Se usi [Chocolatey](https://chocolatey.org/), puoi installare PhotoGIMP con un solo comando:

```powershell
choco install photogimp
```

Mantenuto da: [André Augusto](https://github.com/AndreAugustoDev)
</details>

---

### 🍎 macOS

<img src="https://skillicons.dev/icons?i=macos" align="right" />

#### Backup (opzionale)

Se vuoi mantenere le impostazioni attuali di GIMP, esegui prima un backup:

1. Apri Finder.
2. Premi <kbd>Cmd</kbd> + <kbd>Shift</kbd> + <kbd>G</kbd> e vai in `~/Library/Application Support/GIMP`.
3. Copia l'intera cartella `GIMP` in una posizione sicura (per esempio il Desktop).

#### Installazione

1. Assicurati di avere [GIMP installato dal sito ufficiale](https://www.gimp.org/downloads/).
2. **Apri GIMP una volta e poi chiudilo**: questo crea le cartelle di configurazione necessarie a PhotoGIMP.
3. Scarica l'ultima release:
   👉 **[Scarica PhotoGIMP per macOS (.zip)](https://github.com/Diolinux/PhotoGIMP/releases/download/3.0/PhotoGIMP.zip)**
4. Estrai il contenuto di `PhotoGIMP.zip` in una cartella qualsiasi (per esempio il Desktop).
5. Apri la cartella estratta e **copia la cartella `3.0`**.
6. Apri Finder, premi <kbd>Cmd</kbd> + <kbd>Shift</kbd> + <kbd>G</kbd> per aprire "Vai alla cartella".
7. Digita `~/Library/Application Support/GIMP` e premi <kbd>Invio</kbd>.
8. Se vedi una cartella `2.10` da una precedente installazione, **eliminala** per evitare conflitti.
9. **Incolla** la cartella `3.0` dentro la cartella di GIMP.
10. Quando richiesto sui file esistenti, seleziona **"Sostituisci"** o **"Unisci"**.
11. Apri GIMP: dovresti vedere il nuovo layout di PhotoGIMP. 🎉

---

## 📦 Cosa Contiene la Patch

PhotoGIMP sostituisce o aggiunge i seguenti file nella directory di configurazione di GIMP:

| File / Cartella | Cosa fa |
|---|---|
| `shortcutsrc` | Scorciatoie da tastiera mappate per assomigliare a Photoshop |
| `toolrc` | Configurazione e ordinamento degli strumenti |
| `sessionrc` | Layout delle finestre e posizione dei pannelli |
| `dockrc` | Configurazione dei dock / pannelli |
| `gimprc` | Preferenze generali di GIMP (canvas, griglia, ecc.) |
| `contextrc` | Impostazioni del contesto attivo (strumento/colore) |
| `splashes/` | Splash screen personalizzate PhotoGIMP |
| `theme.css` | Piccole regolazioni al tema dell'interfaccia |
| `templaterc` | Modelli di canvas predefiniti |

Su Linux, la patch installa anche:
- Un file `.desktop` personalizzato (launcher con nome e icona PhotoGIMP)
- Un'icona applicazione personalizzata in `~/.local/share/icons/`

---

## 🗑 Come Disinstallare

Per rimuovere PhotoGIMP e ripristinare GIMP allo stato predefinito, elimina semplicemente la cartella di configurazione di GIMP e riaprilo: verranno rigenerate le impostazioni di default.

### Linux

```bash
rm -rf ~/.config/GIMP/3.0
```

Poi apri di nuovo GIMP: verrà creata una nuova configurazione predefinita.

Se avevi fatto un backup in precedenza, ripristinalo:

```bash
cp -r ~/GIMP-3.0-backup ~/.config/GIMP/3.0
```

### Windows

1. Premi <kbd>Windows</kbd> + <kbd>R</kbd>, digita `%APPDATA%\GIMP` e premi <kbd>Invio</kbd>.
2. Elimina la cartella `3.0`.
3. Apri GIMP: verranno ricreate le impostazioni predefinite.

Oppure ripristina il backup incollando nuovamente la cartella `3.0` salvata.

### macOS

1. Apri Finder, premi <kbd>Cmd</kbd> + <kbd>Shift</kbd> + <kbd>G</kbd>.
2. Vai in `~/Library/Application Support/GIMP`.
3. Elimina la cartella `3.0`.
4. Apri GIMP: verranno ricreate le impostazioni predefinite.

Oppure ripristina il backup incollando di nuovo la cartella salvata.

---

## ❓ Risoluzione dei Problemi / FAQ

> [!CAUTION]
> **PhotoGIMP non ha un sito web ufficiale.** L'unica fonte ufficiale del progetto è il repository GitHub: https://github.com/Diolinux/PhotoGIMP/

<details>
<summary><strong>PhotoGIMP non ha cambiato nulla: GIMP è uguale a prima</strong></summary>

- Assicurati di aver estratto i file nella **posizione corretta**. L'errore più comune è estrarre nella cartella sbagliata.
- **Linux**: le cartelle `.config` e `.local` devono trovarsi nella tua home (`~`). Sono nascoste: premi <kbd>Ctrl</kbd> + <kbd>H</kbd> nel file manager per visualizzarle.
- **Windows**: la cartella `3.0` deve trovarsi dentro `%APPDATA%\GIMP`, non accanto.
- **macOS**: la cartella `3.0` deve trovarsi dentro `~/Library/Application Support/GIMP`.
- Hai **chiuso GIMP** prima di incollare i file? In uscita, GIMP può sovrascrivere le impostazioni appena copiate.
</details>

<details>
<summary><strong>Ricevo un errore quando apro GIMP dopo aver installato PhotoGIMP</strong></summary>

- Di solito significa che la versione di GIMP non è compatibile. PhotoGIMP è pensato per **GIMP 3.0+**. Se stai usando GIMP 2.x, non funzionerà.
- Prova a eliminare la cartella di configurazione e reinstallare: vedi la sezione [Come Disinstallare](#-come-disinstallare).
</details>

<details>
<summary><strong>Posso usare PhotoGIMP con GIMP 2.10?</strong></summary>

No. Questa versione di PhotoGIMP è progettata esclusivamente per **GIMP 3.0 e versioni successive**. Il formato di configurazione è cambiato in modo significativo tra GIMP 2.x e 3.x.
</details>

<details>
<summary><strong>PhotoGIMP eliminerà pennelli, font o plug-in personalizzati?</strong></summary>

No. PhotoGIMP sostituisce solo i file di configurazione (scorciatoie, layout, preferenze). I tuoi pennelli, font, gradienti e plug-in personali non vengono toccati.
</details>

<details>
<summary><strong>Posso personalizzare le scorciatoie dopo l'installazione di PhotoGIMP?</strong></summary>

Assolutamente sì. PhotoGIMP imposta solo un punto di partenza. Puoi modificare qualsiasi scorciatoia in GIMP da **Modifica → Scorciatoie da Tastiera**.
</details>

<details>
<summary><strong>Come aggiorno PhotoGIMP a una nuova versione?</strong></summary>

Scarica semplicemente l'ultima release e segui di nuovo i passaggi di installazione: la configurazione precedente di PhotoGIMP verrà sovrascritta.
</details>

---

## 🤝 Contribuire

Hai trovato un bug? Hai un suggerimento? Il tuo aiuto è benvenuto.

- **Segnala un problema**: [Apri una issue](https://github.com/Diolinux/PhotoGIMP/issues)
- **Invia una correzione**: [Crea una pull request](https://github.com/Diolinux/PhotoGIMP/pulls)
- **Traduci**: Aiutaci a tradurre il README in altre lingue! Vedi la sezione [Traduzioni](#-traduzioni).

---

## 🌍 Traduzioni

This README is available in other languages:

- 🇬🇧 [English](../README.md)
- 🇵🇱 [Polski (Polish)](./README_pl.md)
- 🇧🇷 [Português (Brazilian Portuguese)](./README_pt.md)
- 🇷🇺 [Русский (Russian)](./README_ru.md)

Vuoi aggiungere la tua lingua? Fai un fork del repository, crea un file `docs/README_xx.md` e invia una pull request.

---

## 🏆 Crediti

- Questo progetto non sarebbe possibile senza il fantastico team di [GIMP](https://www.gimp.org/).
- Un GRANDE grazie a tutti i sostenitori di Diolinux su [YouTube](https://youtube.com/Diolinux).
- Splash screen e icone di [Adriel Filipe Design](https://bento.me/adrielfilipedesign).

---

## 👥 Contributori

<a align="center" href="https://github.com/Diolinux/PhotoGIMP/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=Diolinux/PhotoGIMP" />
</a>

---

## 📄 Licenza

PhotoGIMP è distribuito sotto licenza [GNU General Public License v3.0](../LICENSE).
