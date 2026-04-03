# 🎨 PhotoGIMP

<img src="../.local/share/icons/hicolor/256x256/256x256.png" align="right" alt="Icona dell'applicazione PhotoGIMP" title="Icona dell'applicazione PhotoGIMP">

[![GitHub stars](https://img.shields.io/github/stars/Diolinux/PhotoGIMP?style=social)](https://github.com/Diolinux/PhotoGIMP)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Latest Release](https://img.shields.io/github/v/release/Diolinux/PhotoGIMP)](https://github.com/Diolinux/PhotoGIMP/releases/latest)

**PhotoGIMP** è una patch gratuita e mantenuta dalla comunità che trasforma [GIMP](https://www.gimp.org/) (GNU Image Manipulation Program) in un layout familiare per gli utenti di **Adobe Photoshop**. Se stai passando da Photoshop a GIMP e vuoi sentirti subito a casa, PhotoGIMP fa per te.

> **Nuovo su GIMP?** GIMP è un editor di immagini gratuito e open source disponibile per Linux, macOS e Windows. Può fare quasi tutto ciò che fa Photoshop — ritocco fotografico, composizione di immagini, progettazione grafica e molto altro — tutto gratis. PhotoGIMP lo fa semplicemente *sembrare e funzionare* più come Photoshop.

---

## ✨ Funzionalità

- **Layout degli strumenti in stile Photoshop** — Gli strumenti sono riorganizzati per imitare le posizioni a cui sei abituato in Adobe Photoshop.
- **Schermata iniziale personalizzata** — Una schermata iniziale unica di PhotoGIMP ti accoglie all'avvio.
- **Spazio di lavoro massimizzato** — Le impostazioni predefinite sono ottimizzate per offrirti la più ampia area di lavoro possibile.
- **Scorciatoie da tastiera di Photoshop** — Le scorciatoie da tastiera seguono la [documentazione ufficiale di Adobe](https://helpx.adobe.com/photoshop/using/default-keyboard-shortcuts.html) per la versione Windows.
- **Icona e nome personalizzati** — Un file `.desktop` dedicato assegna a PhotoGIMP la propria icona e il proprio nome nel menu di sistema.

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
| **GIMP 3.0 o più recente** | Scaricalo da: [gimp.org](https://www.gimp.org/downloads/) o [Flathub](https://flathub.org/apps/org.gimp.GIMP) (Linux) |
| **Avvia GIMP almeno una volta** | GIMP deve generare i suoi file di configurazione prima che PhotoGIMP possa sovrascriverli. **Installa GIMP → aprilo → chiudilo → poi installa PhotoGIMP.** |

---

## ⚙ Come Installare

> [!WARNING]
> **Esegui il backup delle tue impostazioni attuali di GIMP prima dell'installazione!** PhotoGIMP sovrascrive i file di configurazione di GIMP. Se hai impostazioni personalizzate che vuoi mantenere, salva prima una copia di backup. Consulta le istruzioni di backup in ogni sezione qui sotto.

---

### 🐧 Flatpak (Linux)

<img src="https://skillicons.dev/icons?i=linux" align="right" width="40" />

#### Backup (opzionale)

Se vuoi mantenere le tue impostazioni attuali di GIMP, esegui prima il backup:

```bash
cp -r ~/.config/GIMP/3.0 ~/GIMP-3.0-backup
```

#### Installazione

1. Assicurati di avere già GIMP installato [da Flathub](https://flathub.org/apps/org.gimp.GIMP).
2. **Apri GIMP una volta, poi chiudilo** — questo crea le cartelle di configurazione necessarie a PhotoGIMP.
3. Scarica l'ultima versione:
   👉 **[Scarica PhotoGIMP per Linux (.zip)](https://github.com/Diolinux/PhotoGIMP/releases/download/3.0/PhotoGIMP-linux.zip)**
4. Estrai il file `.zip` **nella tua cartella home** (`~`).
   - Questo posizionerà i file in `~/.config` e `~/.local`, che sono cartelle nascoste.
   - Per vedere le cartelle nascoste nel tuo file manager, premi <kbd>Ctrl</kbd> + <kbd>H</kbd>.
   - Quando ti viene chiesto dei file esistenti, scegli **"Sostituisci"** o **"Sovrascrivi"**.
5. Apri GIMP — dovresti vedere il nuovo layout di PhotoGIMP! 🎉

<details>
<summary><strong>💡 Usi un GIMP non-Flatpak?</strong></summary>

Se hai installato GIMP dal gestore pacchetti della tua distribuzione (apt, dnf, pacman, ecc.) invece che da Flatpak, la cartella di configurazione si trova nella stessa posizione (`~/.config/GIMP/3.0`), quindi i passaggi sopra funzionano comunque. Assicurati solo di avere GIMP versione 3.0 o più recente.
</details>

---

### 🪟 Windows

<img src="https://skillicons.dev/icons?i=windows" align="right" />

#### Backup (opzionale)

Se vuoi mantenere le tue impostazioni attuali di GIMP, esegui prima il backup:

1. Premi <kbd>Windows</kbd> + <kbd>R</kbd> per aprire la finestra Esegui.
2. Digita `%APPDATA%\GIMP` e premi <kbd>Invio</kbd>.
3. Copia l'intera cartella `3.0` in un luogo sicuro (es. il Desktop).

#### Installazione

1. Assicurati di avere [GIMP installato dal sito ufficiale](https://www.gimp.org/downloads/).
2. **Apri GIMP una volta, poi chiudilo** — questo crea le cartelle di configurazione necessarie a PhotoGIMP.
3. Scarica l'ultima versione:
   👉 **[Scarica PhotoGIMP per Windows (.zip)](https://github.com/Diolinux/PhotoGIMP/releases/download/3.0/PhotoGIMP.zip)**
4. Estrai il contenuto di `PhotoGIMP.zip` in una cartella qualsiasi (es. il Desktop).
5. Apri la cartella estratta e **copia la cartella `3.0`**.
6. Premi <kbd>Windows</kbd> + <kbd>R</kbd> per aprire la finestra Esegui.
7. Digita `%APPDATA%\GIMP` e premi <kbd>Invio</kbd> — si aprirà la cartella delle impostazioni di GIMP.
8. **Incolla** la cartella `3.0` qui.
9. Quando ti viene chiesto dei file esistenti, seleziona **"Sostituisci i file nella destinazione"**.
10. Apri GIMP — dovresti vedere il nuovo layout di PhotoGIMP! 🎉

<details>
<summary><strong>💡 Opzionale: Cambiare l'icona del collegamento di GIMP</strong></summary>

Puoi anche scaricare [photogimp.ico](https://github.com/Diolinux/PhotoGIMP/releases/download/3.0/photogimp.ico) e aggiornare l'icona del collegamento di GIMP che si trova in:

```
%appdata%\Microsoft\Windows\Start Menu\Programs\GIMP 3.0.0
```

Fai clic destro sul collegamento → **Proprietà** → **Cambia icona** → seleziona il file `.ico` scaricato.
</details>

<details>
<summary><strong>🍫 Installazione tramite Chocolatey (alternativa)</strong></summary>

Se usi [Chocolatey](https://chocolatey.org/), puoi installare PhotoGIMP con un singolo comando:

```powershell
choco install photogimp
```

Mantenuto da: [André Augusto](https://github.com/AndreAugustoDev)
</details>

---

### 🍎 macOS

<img src="https://skillicons.dev/icons?i=macos" align="right" />

#### Backup (opzionale)

Se vuoi mantenere le tue impostazioni attuali di GIMP, esegui prima il backup:

1. Apri Finder.
2. Premi <kbd>Cmd</kbd> + <kbd>Shift</kbd> + <kbd>G</kbd> e vai a `~/Library/Application Support/GIMP`.
3. Copia l'intera cartella `GIMP` in un luogo sicuro (es. il Desktop).

#### Installazione

1. Assicurati di avere [GIMP installato dal sito ufficiale](https://www.gimp.org/downloads/).
2. **Apri GIMP una volta, poi chiudilo** — questo crea le cartelle di configurazione necessarie a PhotoGIMP.
3. Scarica l'ultima versione:
   👉 **[Scarica PhotoGIMP per macOS (.zip)](https://github.com/Diolinux/PhotoGIMP/releases/download/3.0/PhotoGIMP.zip)**
4. Estrai il contenuto di `PhotoGIMP.zip` in una cartella qualsiasi (es. il Desktop).
5. Apri la cartella estratta e **copia la cartella `3.0`**.
6. Apri Finder, premi <kbd>Cmd</kbd> + <kbd>Shift</kbd> + <kbd>G</kbd> per aprire "Vai alla cartella".
7. Digita `~/Library/Application Support/GIMP` e premi <kbd>Invio</kbd>.
8. Se vedi una cartella `2.10` da un'installazione precedente, **eliminala** per evitare conflitti.
9. **Incolla** la cartella `3.0` dentro la cartella GIMP.
10. Quando ti viene chiesto dei file esistenti, seleziona **"Sostituisci"** o **"Unisci"**.
11. Apri GIMP — dovresti vedere il nuovo layout di PhotoGIMP! 🎉

---

## 📦 Cosa Include la Patch

PhotoGIMP sostituisce o aggiunge i seguenti file nella directory di configurazione di GIMP:

| File / Cartella | Cosa fa |
|---|---|
| `shortcutsrc` | Scorciatoie da tastiera mappate per corrispondere a Photoshop |
| `toolrc` | Configurazione e ordinamento degli strumenti |
| `sessionrc` | Layout delle finestre e posizioni dei pannelli |
| `dockrc` | Configurazione dei dock / pannelli |
| `gimprc` | Preferenze generali di GIMP (tela, griglia, ecc.) |
| `contextrc` | Impostazioni del contesto strumento/colore attivo |
| `splashes/` | Schermata iniziale personalizzata di PhotoGIMP |
| `theme.css` | Piccole modifiche al tema dell'interfaccia |
| `templaterc` | Modelli di tela predefiniti |

Su Linux, la patch installa anche:
- Un file `.desktop` personalizzato (launcher con nome e icona di PhotoGIMP)
- Un'icona personalizzata dell'applicazione in `~/.local/share/icons/`

---

## 🗑 Come Disinstallare

Per rimuovere PhotoGIMP e ripristinare GIMP allo stato predefinito, è sufficiente eliminare la cartella di configurazione di GIMP e riaprirlo — verranno rigenerate le impostazioni predefinite.

### Linux

```bash
rm -rf ~/.config/GIMP/3.0
```

Poi riapri GIMP — creerà una nuova configurazione predefinita.

Se hai fatto un backup in precedenza, ripristinalo:

```bash
cp -r ~/GIMP-3.0-backup ~/.config/GIMP/3.0
```

### Windows

1. Premi <kbd>Windows</kbd> + <kbd>R</kbd>, digita `%APPDATA%\GIMP` e premi <kbd>Invio</kbd>.
2. Elimina la cartella `3.0`.
3. Apri GIMP — ricrea le impostazioni predefinite.

Oppure ripristina il tuo backup incollando nuovamente la cartella `3.0`.

### macOS

1. Apri Finder, premi <kbd>Cmd</kbd> + <kbd>Shift</kbd> + <kbd>G</kbd>.
2. Vai a `~/Library/Application Support/GIMP`.
3. Elimina la cartella `3.0`.
4. Apri GIMP — ricrea le impostazioni predefinite.

Oppure ripristina il tuo backup incollando nuovamente la cartella.

---

## ❓ Risoluzione dei Problemi / FAQ

<details>
<summary><strong>PhotoGIMP non ha cambiato nulla — GIMP è uguale a prima</strong></summary>

- Assicurati di aver estratto i file nella **posizione corretta**. L'errore più comune è estrarre nella cartella sbagliata.
- **Linux**: Le cartelle `.config` e `.local` devono trovarsi nella tua directory home (`~`). Sono nascoste — premi <kbd>Ctrl</kbd> + <kbd>H</kbd> nel tuo file manager per vederle.
- **Windows**: La cartella `3.0` deve essere **dentro** `%APPDATA%\GIMP`, non accanto.
- **macOS**: La cartella `3.0` deve essere **dentro** `~/Library/Application Support/GIMP`.
- Hai **chiuso GIMP** prima di incollare i file? GIMP potrebbe sovrascrivere le impostazioni in arrivo alla chiusura.
</details>

<details>
<summary><strong>Ricevo un errore all'apertura di GIMP dopo aver installato PhotoGIMP</strong></summary>

- Di solito significa che la versione di GIMP non corrisponde. PhotoGIMP è progettato per **GIMP 3.0+**. Se stai usando GIMP 2.x, non sarà compatibile.
- Prova a eliminare la cartella di configurazione e reinstallare — vedi la sezione [Come Disinstallare](#-come-disinstallare).
</details>

<details>
<summary><strong>Posso usare PhotoGIMP con GIMP 2.10?</strong></summary>

No. Questa versione di PhotoGIMP è progettata esclusivamente per **GIMP 3.0 e versioni successive**. Il formato di configurazione è cambiato significativamente tra GIMP 2.x e 3.x.
</details>

<details>
<summary><strong>PhotoGIMP cancellerà i miei pennelli, font o plug-in personalizzati?</strong></summary>

No. PhotoGIMP sostituisce solo i file di configurazione (scorciatoie, layout, preferenze). I tuoi pennelli, font, gradienti e plug-in personali rimangono intatti.
</details>

<details>
<summary><strong>Posso personalizzare le scorciatoie dopo aver installato PhotoGIMP?</strong></summary>

Assolutamente! PhotoGIMP imposta solo un punto di partenza. Puoi modificare qualsiasi scorciatoia in GIMP tramite **Modifica → Scorciatoie da tastiera**.
</details>

<details>
<summary><strong>Come aggiorno PhotoGIMP a una nuova versione?</strong></summary>

Basta scaricare l'ultima versione e seguire nuovamente i passaggi di installazione — sovrascriverà la configurazione precedente di PhotoGIMP.
</details>

---

## 🤝 Contribuire

Hai trovato un bug? Hai un suggerimento? Ci piacerebbe il tuo aiuto!

- **Segnala un problema**: [Apri una issue](https://github.com/Diolinux/PhotoGIMP/issues)
- **Invia una correzione**: [Crea una pull request](https://github.com/Diolinux/PhotoGIMP/pulls)
- **Traduci**: Aiutaci a tradurre il README in più lingue! Vedi la sezione [Traduzioni](#-traduzioni).

---

## 🌍 Traduzioni

Questo README è disponibile in altre lingue:

- 🇬🇧 [English (Inglese)](../README.md)
- 🇧🇷 [Português (Portoghese)](./README_pt.md)
- 🇵🇱 [Polski (Polacco)](./README_pl.md)

Vuoi aggiungere la tua lingua? Fai un fork del repository, crea un file `docs/README_xx.md` e invia una pull request!

---

## 🏆 Crediti

- Questo progetto non sarebbe possibile senza lo straordinario team di [GIMP](https://www.gimp.org/).
- Un GRANDE grazie a tutti i sostenitori di Diolinux su [YouTube](https://youtube.com/Diolinux).
- Schermata iniziale e icone di [Adriel Filipe Design](https://bento.me/adrielfilipedesign).

---

## 👥 Contributori

<a align="center" href="https://github.com/Diolinux/PhotoGIMP/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=Diolinux/PhotoGIMP" />
</a>

---

## 📄 Licenza

PhotoGIMP è rilasciato sotto la [GNU General Public License v3.0](../LICENSE).
