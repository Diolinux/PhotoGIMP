# 🎨 PhotoGIMP

<img src="./.local/share/icons/hicolor/256x256/apps/photogimp.png" align="right" alt="PhotoGimp application icon" title="PhotoGimp application icon">

Prosta modyfikacja do GIMP-a 2.10+, aby pomóc użytkownikom <span style="color: blue;">_Photoshop-a_.
_Od Tłumacza: Oraz dla nowych użytkowników GIMP-a, którzy chcą się poczuć jak na Photoshop-ie_</span>

Co zostanie zmienione:

*	Zmiana położenia narzędzi, podobna do Adobe Photoshop-a;
*	Nowe domyślne filtry Python-a, takie jak "heal selection";
*	Nowy Ekran Ładowania;
*	Nowe domyślne ustawienia, zwiększające przestrzeń roboczą;
*	Skróty klawiaturowe, przypominające z Photoshop-a, wzorowane na dokumentacji Adobe;
*	Nowa ikona i nazwa dla dowolnego pliku .desktop ;
*	Po instalacji, domyślnym językiem, będzie systemowy. Możesz to łatwo zmienić w ustawieniach

![PhotoGimp Diolinux - nowy ekran ładowania](./.var/app/org.gimp.GIMP/config/GIMP/2.10/splashes/photogimp-diolinux-splash.png)


**📷 Zrzut Ekranu**

![Zrzut ekranu z PhotoGIMP - edytowany na Google Takeout](./screenshots/2020-06-22_12-06.png)

## ⚙ Jak zainstalować (używając Flatpak)
Ta paczka dotyczy tylko flatpaka, ale można również jej użyć w innych wersjach GIMP-a (.deb, .rpm, Snap, AppImage, Windows, macOS). Sprawdź lokalizację konfiguracyjnych plików GIMP-a

**Aby kontynuować, przed instalacją uruchom i zamknij GIMP-a**

### Przygotowanie do instalacji, z środowiska Flatpak
*Jeśli miałeś, wcześniej zainstalowany GIMP, za pomocą .deb, .rpm itd., to upewnij się, że usunąłeś folder `$HOME/.config/GIMP`, ponieważ może to powodować problemy z plikami konfiguracji Flatpak*
* Na początku, upewnij się że masz najnowszą wersję GIMP-a, [z Flatpak-a](https://flatpak.org/setup/)
*   Zainstaluj GIMP-a [Flatpak] z centrum aplikacji/instalatora oprogramowania lub używając poniższego polecenia, w terminalu: 
```flatpak install flathub org.gimp.GIMP```

### Instalacja (PhotoGIMP)

W pliku ZIP z [strony nowych wydań (Releases)](https://github.com/Diolinux/PhotoGIMP/releases) znajdziesz trzy ukryte foldery (na wszystkich systemach, oprócz Windows-a, ponieważ użyto kropki przed nazwą folderu). Musisz rozpakować plik ZIP z wszystkimi folderami do swojego profilu użytkownika `$HOME`, <span style="color: red;">JUwaga, jeśli masz poprzednią wersję instalacji, musisz zgodzić się na nadpisanie wszystkich plików</span>

Plik (ZIP) zawiera poniższe foldery:

*  `.icons` (nowe ikony PhotoGimp)
*  `.local` (modyfikacja wyglądu, dla pliku .desktop)
*  `.var` (modyfikacja flatpak dla GIMP-a 2.10+)


Jeśli chcesz użyć PhotoGimp bez zmieniania ikon i nazwy, rozpakuj tylko folder .var do domyślnej lokalizacji GIMP-a.

## ⚙ Jak zainstalować (bez Flatpak)

Ponieważ są to tylko pliki, musisz skopiować je do określonego folderu z tego pakietu `/.var/app/org.gimp.GIMP/config/GIMP/2.10`, do folderu konfiguracyjnego GIMP-a w używanym systemie

**Aby kontynuować, przed instalacją uruchom i zamknij GIMP-a**

Nowe ikony musisz ustawić ręcznie

### Ubuntu (przez Snap)

Folder konfiguracyjny (GIMP-a): `$HOME/.config/GIMP/2.10/`


### Pozostałe systemy Linux lub podobne do Unix, używające (.deb, .rpm, itd.)

Folder Konfiguracyjny: `$HOME/.config/GIMP/2.10/`

### macOS
Folder konfiguracyjny: `"$HOME/Library/Application Support/GIMP/2.10/"`
 
* [Poradnik Wideo stworzony przez Davies Media Design na macOS](https://youtu.be/5nXhtaGQs9U)

Ta poniższa linijka zainstaluje wszystko, co potrzebujesz do działania programu:
```console
curl -L "https://github.com/Diolinux/PhotoGIMP/releases/download/1.0/PhotoGIMP.by.Diolinux.v2020.for.Flatpak.zip" -o ~/Downloads/PhotoGIMP.by.Diolinux.v2020.for.Flatpak.zip && unzip ~/Downloads/PhotoGIMP.by.Diolinux.v2020.for.Flatpak.zip -d ~/Downloads && sudo cp -R ~/Downloads/PhotoGIMP\ by\ Diolinux\ v2020\ for\ Flatpak/.var/app/org.gimp.GIMP/config/GIMP/2.10/ ~/Library/Application\ Support/GIMP/2.10 && rm ~/Downloads/PhotoGIMP.by.Diolinux.v2020.for.Flatpak.zip
```
(Pobierze wersję 1.0 do folderu `Downloads` lub do folderu `Pobrane`, rozpakuje i skopiuje zmodyfikowane pliki, a na końcu usunie wcześniej pobrany plik `.zip`)
  
**Ważne** : GIMP na macOS jest troche spóżnioną wersją. Dlatego, ta modyfikacja działa w skrótach klawiszowych, ale nie, które opcję mogą nie działać, takie jak organizacje zestawu narzędzi. Trzeba poczekać, aż dla macOS będzie dostępna wersja 2.10.20, inaczej możesz spodziewać takich problemów.

### Łatwy instalator, dla macOS (stworzony przez: [@MatthijsKamstra](https://github.com/MatthijsKamstra))

```bash
sh -c "$(curl -fsSL https://raw.githubusercontent.com/MatthijsKamstra/Mac-setup/master/install/photogimp_osx.sh)"
```

### Windows

Folder Konfiguracyjny: `%APPDATA%\GIMP\2.10`

* [Poradnik Wideo, stworzony przez Davies Media Design, dla Windows-a](https://youtu.be/57DNUsf4A-0)

Lub zainstaluj przez [Chocolatey](https://chocolatey.org/):
```powershell
choco install photogimp
```
Prowadzone przez: [André Augusto](https://github.com/AndreAugustoAAQ)

## Podziękowania

* Projekt, nie mógłby być nigdy zrealizowany, bez świetnego zespołu GIMP-a.
* Za zrobienie nowego zdjęcia do Ekranu Ładowania dla [Isabella Mariana](https://www.pexels.com/pt-br/@isabella-mariana-1022505)
* Specjalne podziękowania do wszystkich pomocników Diolinux's na [Twitch-u](https://twitch.tv/Diolinux) i na [YouTube](https://youtube.com/Diolinux).

## Lista Zmian
- [w języku, brazylijsko portugalskim]( https://diolinux.com.br/2020/06/photogimp-2020.html)
- [Veja as Notas de Lançamento em Português](https://diolinux.com.br/2020/06/photogimp-2020.html)
