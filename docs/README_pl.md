# 🎨 PhotoGIMP

<img src="../.local/share/icons/hicolor/256x256/256x256.png" align="right" alt="Ikona aplikacji PhotoGIMP" title="Ikona aplikacji PhotoGIMP">

[![GitHub stars](https://img.shields.io/github/stars/Diolinux/PhotoGIMP?style=social)](https://github.com/Diolinux/PhotoGIMP)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Latest Release](https://img.shields.io/github/v/release/Diolinux/PhotoGIMP)](https://github.com/Diolinux/PhotoGIMP/releases/latest)

**PhotoGIMP** to darmowa, utrzymywana przez społeczność modyfikacja, która przekształca [GIMP](https://www.gimp.org/) (GNU Image Manipulation Program) w układ znany użytkownikom **Adobe Photoshop**. Jeśli przechodzisz z Photoshopa na GIMP i chcesz od razu poczuć się jak w domu, PhotoGIMP jest dla Ciebie.

> **Nowy w GIMP-ie?** GIMP to darmowy edytor graficzny o otwartym kodzie źródłowym, dostępny na Linuxa, macOS i Windows. Potrafi zrobić większość rzeczy, które robi Photoshop — retusz zdjęć, kompozycja obrazów, projektowanie graficzne i wiele więcej — wszystko za darmo. PhotoGIMP sprawia jedynie, że GIMP *wygląda i działa* bardziej jak Photoshop.

---

## ✨ Funkcje

- **Układ narzędzi w stylu Photoshopa** — Narzędzia są uporządkowane tak, aby naśladować pozycje znane z Adobe Photoshop.
- **Własny ekran powitalny** — Unikalny ekran powitalny PhotoGIMP wita Cię przy każdym uruchomieniu.
- **Zmaksymalizowana przestrzeń robocza** — Domyślne ustawienia są zoptymalizowane, aby zapewnić jak największy obszar roboczy.
- **Skróty klawiaturowe z Photoshopa** — Skróty klawiaturowe zgodne z [oficjalną dokumentacją Adobe](https://helpx.adobe.com/photoshop/using/default-keyboard-shortcuts.html) dla wersji Windows.
- **Własna ikona i nazwa** — Dedykowany plik `.desktop` nadaje PhotoGIMP własną ikonę i nazwę w menu systemowym.

---

## 📷 Zrzuty Ekranu

<p>
  <img src="../.config/GIMP/3.0/splashes/splash-screen-2025-v2.png" alt="PhotoGIMP Diolinux Splash Art">
  <em>PhotoGIMP Diolinux Splash Art</em>
</p>

<p>
  <img src="../screenshots/photogimp_3_-_diolinux.png" alt="PhotoGIMP 3">
  <em>GIMP 3.0 z zastosowanym patchem PhotoGIMP</em>
</p>

---

## 📋 Wymagania

Przed zainstalowaniem PhotoGIMP, upewnij się, że masz:

| Wymaganie | Szczegóły |
|---|---|
| **GIMP 3.0 lub nowszy** | Pobierz z: [gimp.org](https://www.gimp.org/downloads/) lub [Flathub](https://flathub.org/apps/org.gimp.GIMP) (Linux) |
| **Uruchom GIMP co najmniej raz** | GIMP musi wygenerować swoje pliki konfiguracyjne zanim PhotoGIMP będzie mógł je nadpisać. **Zainstaluj GIMP → otwórz go → zamknij go → następnie zainstaluj PhotoGIMP.** |

---

## ⚙ Jak Zainstalować

> [!WARNING]
> **Zrób kopię zapasową obecnych ustawień GIMP-a przed instalacją!** PhotoGIMP nadpisuje pliki konfiguracyjne GIMP-a. Jeśli masz własne ustawienia, które chcesz zachować, najpierw zapisz ich kopię zapasową. Zobacz instrukcje tworzenia kopii zapasowej w każdej sekcji poniżej.

---

### 🐧 Flatpak (Linux)

<img src="https://skillicons.dev/icons?i=linux" align="right" width="40" />

#### Kopia zapasowa (opcjonalnie)

Jeśli chcesz zachować obecne ustawienia GIMP-a, najpierw zrób kopię zapasową:

```bash
cp -r ~/.config/GIMP/3.0 ~/GIMP-3.0-backup
```

#### Instalacja

1. Upewnij się, że masz już zainstalowany GIMP [z Flathub](https://flathub.org/apps/org.gimp.GIMP).
2. **Otwórz GIMP-a raz, a następnie go zamknij** — to tworzy foldery konfiguracyjne potrzebne dla PhotoGIMP.
3. Pobierz najnowszą wersję:
   👉 **[Pobierz PhotoGIMP dla Linux (.zip)](https://github.com/Diolinux/PhotoGIMP/releases/download/3.0/PhotoGIMP-linux.zip)**
4. Rozpakuj plik `.zip` **do swojego folderu domowego** (`~`).
   - Umieści to pliki w `~/.config` i `~/.local`, które są folderami ukrytymi.
   - Aby zobaczyć ukryte foldery w menedżerze plików, naciśnij <kbd>Ctrl</kbd> + <kbd>H</kbd>.
   - Gdy pojawi się pytanie o istniejące pliki, wybierz **"Zastąp"** lub **"Nadpisz"**.
5. Otwórz GIMP — powinieneś zobaczyć nowy układ PhotoGIMP! 🎉

<details>
<summary><strong>💡 Używasz GIMP-a spoza Flatpak?</strong></summary>

Jeśli zainstalowałeś GIMP-a z menedżera pakietów dystrybucji (apt, dnf, pacman, itp.) zamiast z Flatpaka, folder konfiguracyjny znajduje się w tym samym miejscu (`~/.config/GIMP/3.0`), więc powyższe kroki nadal działają. Upewnij się tylko, że masz GIMP w wersji 3.0 lub nowszej.
</details>

---

### 🪟 Windows

<img src="https://skillicons.dev/icons?i=windows" align="right" />

#### Kopia zapasowa (opcjonalnie)

Jeśli chcesz zachować obecne ustawienia GIMP-a, najpierw zrób kopię zapasową:

1. Naciśnij <kbd>Windows</kbd> + <kbd>R</kbd>, aby otworzyć okno Uruchom.
2. Wpisz `%APPDATA%\GIMP` i naciśnij <kbd>Enter</kbd>.
3. Skopiuj cały folder `3.0` w bezpieczne miejsce (np. na Pulpit).

#### Instalacja

1. Upewnij się, że masz [GIMP zainstalowany ze strony oficjalnej](https://www.gimp.org/downloads/).
2. **Otwórz GIMP-a raz, a następnie go zamknij** — to tworzy foldery konfiguracyjne potrzebne dla PhotoGIMP.
3. Pobierz najnowszą wersję:
   👉 **[Pobierz PhotoGIMP dla Windows (.zip)](https://github.com/Diolinux/PhotoGIMP/releases/download/3.0/PhotoGIMP.zip)**
4. Rozpakuj zawartość `PhotoGIMP.zip` do dowolnego folderu (np. na Pulpit).
5. Otwórz rozpakowany folder i **skopiuj folder `3.0`**.
6. Naciśnij <kbd>Windows</kbd> + <kbd>R</kbd>, aby otworzyć okno Uruchom.
7. Wpisz `%APPDATA%\GIMP` i naciśnij <kbd>Enter</kbd> — to otworzy folder ustawień GIMP-a.
8. **Wklej** folder `3.0` tutaj.
9. Gdy pojawi się pytanie o istniejące pliki, wybierz **"Zastąp pliki w miejscu docelowym"**.
10. Otwórz GIMP — powinieneś zobaczyć nowy układ PhotoGIMP! 🎉

<details>
<summary><strong>💡 Opcjonalnie: Zmień ikonę skrótu GIMP-a</strong></summary>

Możesz również pobrać [photogimp.ico](https://github.com/Diolinux/PhotoGIMP/releases/download/3.0/photogimp.ico) i zaktualizować ikonę skrótu GIMP-a znajdującego się w:

```
%appdata%\Microsoft\Windows\Start Menu\Programs\GIMP 3.0.0
```

Kliknij prawym przyciskiem myszy na skrót → **Właściwości** → **Zmień ikonę** → wskaż pobrany plik `.ico`.
</details>

<details>
<summary><strong>🍫 Instalacja przez Chocolatey (alternatywa)</strong></summary>

Jeśli używasz [Chocolatey](https://chocolatey.org/), możesz zainstalować PhotoGIMP jednym poleceniem:

```powershell
choco install photogimp
```

Opiekun pakietu: [André Augusto](https://github.com/AndreAugustoDev)
</details>

---

### 🍎 macOS

<img src="https://skillicons.dev/icons?i=macos" align="right" />

#### Kopia zapasowa (opcjonalnie)

Jeśli chcesz zachować obecne ustawienia GIMP-a, najpierw zrób kopię zapasową:

1. Otwórz Finder.
2. Naciśnij <kbd>Cmd</kbd> + <kbd>Shift</kbd> + <kbd>G</kbd> i przejdź do `~/Library/Application Support/GIMP`.
3. Skopiuj cały folder `GIMP` w bezpieczne miejsce (np. na Pulpit).

#### Instalacja

1. Upewnij się, że masz [GIMP zainstalowany ze strony oficjalnej](https://www.gimp.org/downloads/).
2. **Otwórz GIMP-a raz, a następnie go zamknij** — to tworzy foldery konfiguracyjne potrzebne dla PhotoGIMP.
3. Pobierz najnowszą wersję:
   👉 **[Pobierz PhotoGIMP dla macOS (.zip)](https://github.com/Diolinux/PhotoGIMP/releases/download/3.0/PhotoGIMP.zip)**
4. Rozpakuj zawartość `PhotoGIMP.zip` do dowolnego folderu (np. na Pulpit).
5. Otwórz rozpakowany folder i **skopiuj folder `3.0`**.
6. Otwórz Finder, naciśnij <kbd>Cmd</kbd> + <kbd>Shift</kbd> + <kbd>G</kbd>, aby otworzyć "Idź do folderu".
7. Wpisz `~/Library/Application Support/GIMP` i naciśnij <kbd>Enter</kbd>.
8. Jeśli masz folder `2.10` z poprzedniej instalacji, **usuń go**, aby uniknąć konfliktów.
9. **Wklej** folder `3.0` do folderu GIMP.
10. Gdy pojawi się pytanie o istniejące pliki, wybierz **"Zastąp"** lub **"Scal"**.
11. Otwórz GIMP — powinieneś zobaczyć nowy układ PhotoGIMP! 🎉

---

## 📦 Co Zawiera Patch

PhotoGIMP zastępuje lub dodaje następujące pliki w katalogu konfiguracyjnym GIMP-a:

| Plik / Folder | Co robi |
|---|---|
| `shortcutsrc` | Skróty klawiaturowe zmapowane tak, aby odpowiadały Photoshopowi |
| `toolrc` | Konfiguracja i kolejność narzędzi |
| `sessionrc` | Układ okien i pozycje paneli |
| `dockrc` | Konfiguracja doków / paneli |
| `gimprc` | Ogólne preferencje GIMP-a (płótno, siatka, itp.) |
| `contextrc` | Ustawienia aktywnego narzędzia/koloru |
| `splashes/` | Własny ekran powitalny PhotoGIMP |
| `theme.css` | Drobne korekty motywu interfejsu |
| `templaterc` | Predefiniowane szablony płótna |

Na Linuxie patch instaluje również:
- Własny plik `.desktop` (launcher z nazwą i ikoną PhotoGIMP)
- Własną ikonę aplikacji w `~/.local/share/icons/`

---

## 🗑 Jak Odinstalować

Aby usunąć PhotoGIMP i przywrócić GIMP do stanu domyślnego, wystarczy usunąć folder konfiguracyjny GIMP-a i ponownie go otworzyć — wygeneruje on nowe domyślne ustawienia.

### Linux

```bash
rm -rf ~/.config/GIMP/3.0
```

Następnie otwórz GIMP ponownie — utworzy on nową domyślną konfigurację.

Jeśli wcześniej zrobiłeś kopię zapasową, przywróć ją:

```bash
cp -r ~/GIMP-3.0-backup ~/.config/GIMP/3.0
```

### Windows

1. Naciśnij <kbd>Windows</kbd> + <kbd>R</kbd>, wpisz `%APPDATA%\GIMP` i naciśnij <kbd>Enter</kbd>.
2. Usuń folder `3.0`.
3. Otwórz GIMP — odtworzy on domyślne ustawienia.

Lub przywróć kopię zapasową, wklejając folder `3.0` z powrotem.

### macOS

1. Otwórz Finder, naciśnij <kbd>Cmd</kbd> + <kbd>Shift</kbd> + <kbd>G</kbd>.
2. Przejdź do `~/Library/Application Support/GIMP`.
3. Usuń folder `3.0`.
4. Otwórz GIMP — odtworzy on domyślne ustawienia.

Lub przywróć kopię zapasową, wklejając folder z powrotem.

---

## ❓ Rozwiązywanie Problemów / FAQ

<details>
<summary><strong>PhotoGIMP nic nie zmienił — GIMP wygląda tak samo</strong></summary>

- Upewnij się, że rozpakowałeś pliki we **właściwym miejscu**. Najczęstszym błędem jest rozpakowanie do złego folderu.
- **Linux**: Foldery `.config` i `.local` muszą znajdować się w Twoim katalogu domowym (`~`). Są one ukryte — naciśnij <kbd>Ctrl</kbd> + <kbd>H</kbd> w menedżerze plików, aby je zobaczyć.
- **Windows**: Folder `3.0` musi znajdować się **wewnątrz** `%APPDATA%\GIMP`, nie obok niego.
- **macOS**: Folder `3.0` musi znajdować się **wewnątrz** `~/Library/Application Support/GIMP`.
- Czy **zamknąłeś GIMP-a** przed wklejeniem plików? GIMP może nadpisać przychodzące ustawienia przy zamykaniu.
</details>

<details>
<summary><strong>Otrzymuję błąd po otwarciu GIMP-a po zainstalowaniu PhotoGIMP</strong></summary>

- To zwykle oznacza, że wersja GIMP-a nie pasuje. PhotoGIMP jest przeznaczony dla **GIMP 3.0+**. Jeśli używasz GIMP 2.x, nie będzie kompatybilny.
- Spróbuj usunąć folder konfiguracyjny i zainstalować ponownie — zobacz sekcję [Jak Odinstalować](#-jak-odinstalować).
</details>

<details>
<summary><strong>Czy mogę używać PhotoGIMP z GIMP 2.10?</strong></summary>

Nie. Ta wersja PhotoGIMP została zaprojektowana wyłącznie dla **GIMP 3.0 i nowszego**. Format konfiguracji zmienił się znacząco między GIMP 2.x a 3.x.
</details>

<details>
<summary><strong>Czy PhotoGIMP usunie moje własne pędzle, czcionki lub wtyczki?</strong></summary>

Nie. PhotoGIMP zastępuje jedynie pliki konfiguracyjne (skróty, układ, preferencje). Twoje osobiste pędzle, czcionki, gradienty i wtyczki pozostają nietknięte.
</details>

<details>
<summary><strong>Czy mogę dostosować skróty po zainstalowaniu PhotoGIMP?</strong></summary>

Oczywiście! PhotoGIMP ustawia jedynie punkt wyjścia. Możesz zmienić dowolny skrót w GIMP-ie przez **Edycja → Skróty klawiaturowe**.
</details>

<details>
<summary><strong>Jak zaktualizować PhotoGIMP do nowej wersji?</strong></summary>

Wystarczy pobrać najnowszą wersję i ponownie wykonać kroki instalacji — nadpisze to poprzednią konfigurację PhotoGIMP.
</details>

---

## 🤝 Współpraca

Znalazłeś błąd? Masz sugestię? Chętnie przyjmiemy Twoją pomoc!

- **Zgłoś problem**: [Otwórz issue](https://github.com/Diolinux/PhotoGIMP/issues)
- **Wyślij poprawkę**: [Utwórz pull request](https://github.com/Diolinux/PhotoGIMP/pulls)
- **Tłumacz**: Pomóż nam przetłumaczyć README na więcej języków! Zobacz sekcję [Tłumaczenia](#-tłumaczenia).

---

## 🌍 Tłumaczenia

Ten README jest dostępny w innych językach:

- 🇬🇧 [English](../README.md)
- 🇮🇹 [Italiano](./README_it.md)
- 🇧🇷 [Português (Brazilian Portuguese)](./README_pt.md)
- 🇷🇺 [Русский](./README_ru.md)

Chcesz dodać swój język? Zrób fork repozytorium, utwórz plik `docs/README_xx.md` i wyślij pull request!

---

## 🏆 Podziękowania

- Ten projekt nie byłby możliwy bez wspaniałego zespołu [GIMP-a](https://www.gimp.org/).
- Wielkie podziękowania dla wszystkich wspierających Diolinux na [YouTube](https://youtube.com/Diolinux).
- Ekran powitalny i ikony od [Adriel Filipe Design](https://bento.me/adrielfilipedesign).

---

## 👥 Współtwórcy

<a align="center" href="https://github.com/Diolinux/PhotoGIMP/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=Diolinux/PhotoGIMP" />
</a>

---

## 📄 Licencja

PhotoGIMP jest objęty licencją [GNU General Public License v3.0](../LICENSE).
