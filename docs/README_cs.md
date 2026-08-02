# 🎨 PhotoGIMP

<img src="../.local/share/icons/hicolor/256x256/256x256.png" align="right" alt="Ikona aplikace PhotoGIMP" title="Ikona aplikace PhotoGIMP">

[![GitHub stars](https://img.shields.io/github/stars/Diolinux/PhotoGIMP?style=social)](https://github.com/Diolinux/PhotoGIMP)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Latest Release](https://img.shields.io/github/v/release/Diolinux/PhotoGIMP)](https://github.com/Diolinux/PhotoGIMP/releases/latest)

**PhotoGIMP** je bezplatný komunitní patch, který transformuje [GIMP](https://www.gimp.org/) (GNU Image Manipulation Program) do rozložení, které bude dobře známé uživatelům **Adobe Photoshop**. Pokud přecházíte z Photoshopu na GIMP a chcete se hned cítit jako doma, PhotoGIMP je přímo pro vás.

> **Začínáte s GIMPem?** GIMP je bezplatný open-source editor obrázků dostupný pro Linux, macOS a Windows. Dokáže většinu věcí jako Photoshop — retušování fotek, kompozice obrázků, grafický design a další — a to vše zdarma. PhotoGIMP pouze zajistí, aby *vypadal a fungoval* více jako Photoshop.

---

## ✨ Funkce

- **Rozložení nástrojů jako ve Photoshopu** — Nástroje jsou přeorganizovány tak, aby napodobovaly pozice, na které jste zvyklí z Adobe Photoshop.
- **Vlastní úvodní obrazovka** — Jedinečná úvodní obrazovka PhotoGIMP vás přivítá při spuštění.
- **Maximalizovaný prostor plátna** — Výchozí nastavení je optimalizováno tak, aby vám poskytlo co největší pracovní plochu.
- **Klávesové zkratky z Photoshopu** — Klávesové zkratky se řídí [oficiální dokumentací Adobe](https://helpx.adobe.com/photoshop/using/default-keyboard-shortcuts.html) pro verzi Windows.
- **Vlastní ikona a název** — Dedikovaný soubor `.desktop` dává PhotoGIMP vlastní ikonu a název aplikace v systémové nabídce.

---

## 📷 Snímky obrazovky

| Úvodní obrazovka | Okno aplikace |
|-|-|
| ![[PhotoGIMP Diolinux splash screen]](../.config/GIMP/3.0/splashes/splash-screen-2025-v2.png)<br>Úvodní obrazovka PhotoGIMP Diolinux | ![[PhotoGIMP 3]](../screenshots/photogimp_3_-_diolinux.png)<br>PhotoGIMP 3

---

## 📋 Požadavky

Před instalací PhotoGIMPu se ujistěte, že máte:

| Požadavek | Podrobnosti |
| --- | --- |
| **GIMP 3.0 nebo novější** | Stáhnout z: [gimp.org](https://www.gimp.org/downloads/) nebo [Flathub](https://flathub.org/apps/org.gimp.GIMP) (Linux) |
| **Spusťte GIMP alespoň jednou** | GIMP musí vygenerovat své konfigurační soubory předtím, než je PhotoGIMP může přepsat. **Nainstalujte GIMP → otevřete jej → zavřete jej → poté nainstalujte PhotoGIMP.** |

---

## ⚙ Jak nainstalovat

> [!WARNING]
> **Před instalací si zálohujte své aktuální nastavení GIMPu!** PhotoGIMP přepisuje konfigurační soubory GIMPu. Pokud máte vlastní nastavení, která si chcete ponechat, nejprve si vytvořte záložní kopii. Pokyny k zálohování naleznete v každé sekci níže.

---

### 🐧 Flatpak (Linux)

<img src="https://skillicons.dev/icons?i=linux" align="right" width="40" />

#### Záloha (volitelné)

Pokud si chcete ponechat aktuální nastavení GIMPu, nejprve si ho zálohujte:

```bash
cp -r ~/.config/GIMP/3.0 ~/GIMP-3.0-backup
```

#### Instalace

1. Ujistěte se, že již máte GIMP nainstalován [z Flathubu](https://flathub.org/apps/org.gimp.GIMP).
2. **Jednou GIMP otevřete a poté jej zavřete** — tím se vytvoří konfigurační složky, které PhotoGIMP potřebuje.
3. Stáhněte si nejnovější vydání:
   👉 **[Stáhnout PhotoGIMP pro Linux (.zip)](https://github.com/Diolinux/PhotoGIMP/releases/download/3.0/PhotoGIMP-linux.zip)**
4. Rozbalte soubor `.zip` **do své domovské složky** (`~`).
    - Tím se umístí soubory do `~/.config` a `~/.local`, což jsou skryté složky.
    - Chcete-li zobrazit skryté složky ve správci souborů, stiskněte <kbd>Ctrl</kbd> + <kbd>H</kbd>.
    - Když budete dotázáni na existující soubory, zvolte **„Nahradit“** nebo **„Přepsat“**.
5. Otevřete GIMP — měli byste vidět nové rozložení PhotoGIMP! 🎉

<details>
<summary><strong>💡 Používáte jiný GIMP než Flatpak?</strong></summary>

Pokud jste nainstalovali GIMP přes správce balíčků vaší distribuce (apt, dnf, pacman atd.) namísto Flatpaku, složka s konfigurací je na stejném místě (`~/.config/GIMP/3.0`), takže výše uvedené kroky stále fungují. Jen se ujistěte, že máte verzi GIMPu 3.0 nebo novější.

</details>

---

### 🪟 Windows

<img src="https://skillicons.dev/icons?i=windows" align="right" />

#### Záloha (volitelné)

Pokud si chcete ponechat aktuální nastavení GIMPu, nejprve si ho zálohujte:

1. Stiskněte <kbd>Windows</kbd> + <kbd>R</kbd> pro otevření dialogu Spustit.
2. Napište `%APPDATA%\GIMP` a stiskněte <kbd>Enter</kbd>.
3. Zkopírujte celou složku `3.0` na bezpečné místo (např. na Plochu).

#### Instalace

1. Ujistěte se, že máte [GIMP nainstalovaný z oficiálních stránek](https://www.gimp.org/downloads/).
2. **Jednou GIMP otevřete a poté jej zavřete** — tím se vytvoří konfigurační složky, které PhotoGIMP potřebuje.
3. Stáhněte si nejnovější vydání:
   👉 **[Stáhnout PhotoGIMP pro Windows (.zip)](https://github.com/Diolinux/PhotoGIMP/releases/download/3.0/PhotoGIMP.zip)**
4. Rozbalte obsah `PhotoGIMP.zip` do libovolné složky (např. na Plochu).
5. Otevřete rozbalenou složku a **zkopírujte složku `3.0`**.
6. Stiskněte <kbd>Windows</kbd> + <kbd>R</kbd> pro otevření dialogu Spustit.
7. Napište `%APPDATA%\GIMP` a stiskněte <kbd>Enter</kbd> — to otevře složku s nastavením GIMPu.
8. **Vložte** sem složku `3.0`.
9. Když budete dotázáni na existující soubory, zvolte **„Nahradit soubory v cíli“**.
10. Otevřete GIMP — měli byste vidět nové rozložení PhotoGIMP! 🎉

<details>
<summary><strong>💡 Volitelné: Změna ikony zástupce GIMPu</strong></summary>

Můžete si také stáhnout [photogimp.ico](https://github.com/Diolinux/PhotoGIMP/releases/download/3.0/photogimp.ico) a aktualizovat ikonu u zástupce GIMPu umístěného v:

```
%appdata%\Microsoft\Windows\Start Menu\Programs\GIMP 3.0.0
```

Klikněte pravým tlačítkem na zástupce → **Vlastnosti** → **Změnit ikonu** → najděte stažený soubor `.ico`.

</details>

<details>
<summary><strong>🍫 Instalace přes Chocolatey (alternativa)</strong></summary>

Pokud používáte [Chocolatey](https://chocolatey.org/), můžete PhotoGIMP nainstalovat jedním příkazem:

```powershell
choco install photogimp
```

Spravuje: [André Augusto](https://github.com/AndreAugustoDev)

</details>

---

### 🍎 macOS

<img src="https://skillicons.dev/icons?i=macos" align="right" />

#### Záloha (volitelné)

Pokud si chcete ponechat aktuální nastavení GIMPu, nejprve si ho zálohujte:

1. Otevřete Finder.
2. Stiskněte <kbd>Cmd</kbd> + <kbd>Shift</kbd> + <kbd>G</kbd> a přejděte do `~/Library/Application Support/GIMP`.
3. Zkopírujte celou složku `GIMP` na bezpečné místo (např. na Plochu).

#### Instalace

1. Ujistěte se, že máte [GIMP nainstalovaný z oficiálních stránek](https://www.gimp.org/downloads/).
2. **Jednou GIMP otevřete a poté jej zavřete** — tím se vytvoří konfigurační složky, které PhotoGIMP potřebuje.
3. Stáhněte si nejnovější vydání:
   👉 **[Stáhnout PhotoGIMP pro macOS (.zip)](https://github.com/Diolinux/PhotoGIMP/releases/download/3.0/PhotoGIMP.zip)**
4. Rozbalte obsah `PhotoGIMP.zip` do libovolné složky (např. na Plochu).
5. Otevřete rozbalenou složku a **zkopírujte složku `3.0`**.
6. Otevřete Finder, stiskněte <kbd>Cmd</kbd> + <kbd>Shift</kbd> + <kbd>G</kbd> pro otevření "Otevřít složku".
7. Napište `~/Library/Application Support/GIMP` a stiskněte <kbd>Enter</kbd>.
8. Pokud uvidíte složku `2.10` z předchozí instalace, **smažte ji**, abyste předešli konfliktům.
9. **Vložte** složku `3.0` dovnitř složky GIMP.
10. Když budete dotázáni na existující soubory, zvolte **„Nahradit“** nebo **„Sloučit“**.
11. Otevřete GIMP — měli byste vidět nové rozložení PhotoGIMP! 🎉

<details>
<summary><strong>Alternativa: instalace přes Terminál</strong></summary>

Pokud možnost **„Sloučit“** ve Finderu tiše přeskočí existující soubory, nebo pokud dáváte přednost příkazové řádce, můžete soubory PhotoGIMPu zkopírovat pomocí `rsync`.

1. Otevřete Terminál.
2. Spusťte `rsync`, nahraďte `/path/to/extracted/3.0/` umístěním rozbalené složky `3.0`:

   ```bash
   rsync -av --ignore-times /path/to/extracted/3.0/ ~/Library/Application\ Support/GIMP/3.0/
   ```

   Ujistěte se, že obě cesty končí znakem `/`.
3. Pokud váš nainstalovaný GIMP používá složku s jinou verzí, změňte podle ní cíl (např. použijte `~/Library/Application\ Support/GIMP/3.2/` pro GIMP 3.2).

</details>

---

## 📦 Co obsahuje tento Patch

PhotoGIMP nahrazuje nebo přidává následující soubory v konfiguračním adresáři GIMPu:

| Soubor / Složka | K čemu slouží |
| --- | --- |
| `shortcutsrc` | Klávesové zkratky mapované podle Photoshopu |
| `toolrc` | Konfigurace a pořadí nástrojů |
| `sessionrc` | Rozložení okna a pozice panelů |
| `dockrc` | Konfigurace doků / panelů |
| `gimprc` | Obecné předvolby GIMPu (plátno, mřížka atd.) |
| `contextrc` | Nastavení kontextu aktivního nástroje/barvy |
| `splashes/` | Vlastní úvodní obrazovka PhotoGIMP |
| `theme.css` | Drobné úpravy motivu uživatelského rozhraní |
| `templaterc` | Předdefinované šablony plátna |

V Linuxu patch navíc nainstaluje:

- Vlastní soubor `.desktop` (spouštěč aplikace s názvem a ikonou PhotoGIMP)
- Vlastní ikonu aplikace do `~/.local/share/icons/`

---

## 🗑 Jak odinstalovat

Chcete-li odstranit PhotoGIMP a obnovit GIMP do výchozího stavu, jednoduše smažte konfigurační složku GIMPu a znovu otevřete GIMP — vygeneruje si nová výchozí nastavení.

### Linux

```bash
rm -rf ~/.config/GIMP/3.0
```

Poté GIMP znovu otevřete — vytvoří zcela novou výchozí konfiguraci.

Pokud jste si dříve udělali zálohu, obnovte ji raději takto:

```bash
cp -r ~/GIMP-3.0-backup ~/.config/GIMP/3.0
```

### Windows

1. Stiskněte <kbd>Windows</kbd> + <kbd>R</kbd>, napište `%APPDATA%\GIMP` a stiskněte <kbd>Enter</kbd>.
2. Smažte složku `3.0`.
3. Otevřete GIMP — znovu se vytvoří výchozí nastavení.

Nebo obnovte zálohu tím, že vložíte zpět zálohovanou složku `3.0`.

### macOS

1. Otevřete Finder, stiskněte <kbd>Cmd</kbd> + <kbd>Shift</kbd> + <kbd>G</kbd>.
2. Přejděte do `~/Library/Application Support/GIMP`.
3. Smažte složku `3.0`.
4. Otevřete GIMP — znovu se vytvoří výchozí nastavení.

Nebo obnovte zálohu vložením zpět zálohované složky.

---

## ❓ Řešení problémů / FAQ

> [!CAUTION]
> **PhotoGIMP nemá oficiální web.** Jediným oficiálním zdrojem projektu je jeho repozitář na GitHubu: https://github.com/Diolinux/PhotoGIMP/

<details>
<summary><strong>PhotoGIMP nic nezměnil — GIMP vypadá stejně</strong></summary>

- Ujistěte se, že jste soubory rozbalili do **správného umístění**. Nejčastější chybou je rozbalení do nesprávné složky.
- **Linux**: Složky `.config` a `.local` musí být ve vašem domovském adresáři (`~`). Jsou skryté — stiskněte <kbd>Ctrl</kbd> + <kbd>H</kbd> ve správci souborů pro jejich zobrazení.
- **Windows**: Složka `3.0` musí být uvnitř `%APPDATA%\GIMP`, nikoli vedle ní.
- **macOS**: Složka `3.0` musí být uvnitř `~/Library/Application Support/GIMP`.
- **Zavřeli jste GIMP** před vložením souborů? GIMP může při ukončení přepsat nová nastavení.
  </details>

<details>
<summary><strong>Při otevírání GIMPu po instalaci PhotoGIMPu se zobrazuje chyba</strong></summary>

- To obvykle znamená, že se neshoduje verze GIMPu. PhotoGIMP je vytvořen pro **GIMP 3.0+**. Pokud spouštíte GIMP 2.x, nebude kompatibilní.
- Zkuste smazat konfigurační složku a nainstalovat znovu — viz sekce [Jak odinstalovat](#-jak-odinstalovat).
  </details>

<details>
<summary><strong>Mohu použít PhotoGIMP s GIMPem 2.10?</strong></summary>

Ne. Tato verze PhotoGIMPu je navržena výhradně pro **GIMP 3.0 a novější**. Formát konfigurace se mezi GIMP 2.x a 3.x výrazně změnil.

</details>

<details>
<summary><strong>Smaže PhotoGIMP mé vlastní štětce, písma nebo plug-iny?</strong></summary>

Ne. PhotoGIMP pouze nahrazuje konfigurační soubory (zkratky, rozložení, předvolby). Vaše osobní štětce, písma, přechody a plug-iny zůstanou nedotčeny.

</details>

<details>
<summary><strong>Mohu si upravit zkratky po instalaci PhotoGIMPu?</strong></summary>

Rozhodně! PhotoGIMP nastavuje pouze počáteční bod. Jakoukoli zkratku můžete v GIMPu změnit přes **Úpravy → Klávesové zkratky**.

</details>

<details>
<summary><strong>Jak aktualizuji PhotoGIMP na novou verzi?</strong></summary>

Stačí si stáhnout nejnovější vydání a znovu postupovat podle kroků instalace — tím se přepíše předchozí konfigurace PhotoGIMPu.

</details>

---

## 🤝 Přispívání

Našli jste chybu? Máte návrh? Vaši pomoc oceníme!

- **Nahlásit problém**: [Otevřít problém (issue)](https://github.com/Diolinux/PhotoGIMP/issues)
- **Předložit opravu**: [Vytvořit pull request](https://github.com/Diolinux/PhotoGIMP/pulls)
- **Překlady**: Pomozte nám přeložit README do dalších jazyků! Viz sekce [Překlady](#-překlady).

---

## 🌍 Překlady

Toto README je dostupné v dalších jazycích:

- 🇬🇧 [English (Angličtina)](../README.md)
- 🇮🇹 [Italiano (Italština)](./README_it.md)
- 🇵🇱 [Polski (Polština)](./README_pl.md)
- 🇺🇦 [Українська (Ukrajinština)](./README_ua.md)
- 🇧🇷 [Português (Brazilská portugalština)](./README_pt.md)
- 🇷🇺 [Русский (Ruština)](./README_ru.md)
- 🇪🇸 [Español (Španělština)](./README_es.md)
- 🇮🇱 [עברית (Hebrejština)](https://github.com/Diolinux/PhotoGIMP/blob/master/docs/README_he.md)
- 🇰🇷 [Korean (Korejština)](./README_ko.md)
- 🇨🇳 [简体中文 (Zjednodušená čínština)](./README_zh.md)

Chcete přidat svůj jazyk? Forkněte repozitář, vytvořte soubor `docs/README_xx.md` a odešlete pull request!

---

## 🏆 Zásluhy

- Tento projekt by nebyl možný bez úžasného týmu [GIMP](https://www.gimp.org/).
- VELKÉ díky všem podporovatelům Diolinux na [YouTube](https://youtube.com/Diolinux).
- Úvodní obrazovka a ikony od [Adriel Filipe Design](https://bento.me/adrielfilipedesign).

---

## 👥 Přispěvatelé

<a align="center" href="https://github.com/Diolinux/PhotoGIMP/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=Diolinux/PhotoGIMP" />
</a>

---

## 📄 Licence

PhotoGIMP je licencován pod [GNU General Public License v3.0](../LICENSE).
