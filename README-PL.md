_Original Repository_(https://github.com/Diolinux/PhotoGIMP/)

![](https://github.com/Diolinux/PhotoGIMP/blob/master/.var/app/org.gimp.GIMP/config/GIMP/2.10/splashes/photogimp-diolinux-splash.png)

# PhotoGIMP
Prosta modyfikacja do GIMP 2.10+, aby pomóc użytkownikom <span style="color: blue;">_Photoshop-a_.
_Od Tłumacza: lub dla nowych użytkowników Gimp-a którzy, chcą się czuć jak na Photoshop-ie_</span>

*	Zmiana położenia narzędzi przypominająca Adobe Photoshop-a;
*	Setki nowych domyślnych czcionek;
*	Nowe domyślne filtry dla Python-a, such as "heal selection";
*	Nowy Ekran Ładowania;
*	Nowy domyślne ustawienia z zwiększeniem przestrzeni roboczej;
*	Skróty klawiaturowe, przypominające z Photoshop-a, wzorowane na dokumentacji Adobe;
*	Nowa ikona i nazwa dla dowolnego pliku .desktop ;
*	Nowym domyślnym językiem jest Angielski (możesz, tą opcję zmienić w ustawieniach).


Może ci się przydać:

![](https://github.com/Diolinux/PhotoGIMP/blob/master/2020-06-22_12-06.png
)


<img src="https://github.com/Diolinux/PhotoGIMP/blob/master/.icons/photogimp.png" data-canonical-src="https://github.com/Diolinux/PhotoGIMP/blob/master/.icons/photogimp.png" width="200" height="200" />

## Wbudowane Czczionki

https://github.com/Diolinux/PhotoGIMP/blob/master/fonts.txt

# Jak zainstalować

Ta paczka dotyczy tylko flatpaka, ale można również jej użyć w innych wersjach Gimp-a  (.deb,.rpm, Za pomocą Snap, AppImage, Windows, macOS). Sprawdź lokalizację plików Gimp-a w systemie/programie.
## Przygotowanie do instalacji środowiska Flatpak

*   Na początku, upewnij się że masz najnowszą wersję Gimp-a  *   Zainstaluj Gimp Flatpak z centrum aplikacji/instalatora oprogramowania lub używając komendy w terminalu: 
```flatpak install flathub org.gimp.GIMP```

## Instalowanie modyfikacji (PhotoGIMP)

W pliku ZIP z [strony ukazanych wersji](https://github.com/Diolinux/PhotoGIMP/releases) znajdziesz trzy ukryte foldery (na Linux-ie, użyto kropki przed nazwą folderu). Musisz rozpakować plik ZIP z wszystkimi folderami do  ```/home/$USER```, <span style="color: red;">uwaga musisz zgodzić się nadpisać wszystkie pliki</span> , jeśli masz poprzednią wersję instalacji.

Plik (ZIP) zawiera poniższe foldery:

*  .icons (nowe ikony PhotoGimp)
*  .local (modyfikacja personalizacji pliku .desktop)
*   .var (modyfikacja flatpak dla GIMP 2.10+)


Jeśli chcesz użyć PhotoGimp bez zmieniania ikon i nazwy, rozpakuj tylko folder .var do domyślnej lokalizacji GIMP-a.

## Chcesz skorzystać na Windows, macOS lub Ubuntu(Za pomocą Snap)?

*  Poradnik Wideo stworzony przez Davies Media Design na macOS: [https://youtu.be/5nXhtaGQs9U](https://youtu.be/5nXhtaGQs9U)
*  Poradnik Wideo stworzony przez Davies Media Design na Windows: [https://youtu.be/57DNUsf4A-0](https://youtu.be/57DNUsf4A-0)


Ty tylko kopiujesz wszyskie pliki z lokalizacji ```/.var/app/org.gimp.GIMP/config/GIMP/2.10``` do folderu GIMP-a  na określonym systemie, nadpisując istniejące już pliki:

* Windows: `C:/Users/TWOJA_NAZWA/AppData/Roaming/GIMP/2.10`

* macOS: `~/Library/Application Support/GIMP/2.10/`
  
  Ta jedna poniższa linijka wykona zadanie: pobierz wersję 1.0 do folderu `Downloads` lub do folderu `Pobrane`, rozpakuj i skopiuj zmodyfikowane pliki, usuwając wcześniej pobrany plik ZIP:
  ```bash
  curl -L "https://github.com/Diolinux/PhotoGIMP/releases/download/1.0/PhotoGIMP.by.Diolinux.v2020.for.Flatpak.zip" -o ~/Downloads/PhotoGIMP.by.Diolinux.v2020.for.Flatpak.zip && unzip ~/Downloads/PhotoGIMP.by.Diolinux.v2020.for.Flatpak.zip -d ~/Downloads && sudo cp -R ~/Downloads/PhotoGIMP\ by\ Diolinux\ v2020\ for\ Flatpak/.var/app/org.gimp.GIMP/config/GIMP/2.10/ ~/Library/Application\ Support/GIMP/2.10 && rm ~/Downloads/PhotoGIMP.by.Diolinux.v2020.for.Flatpak.zip
  ```
**Ważne** : GIMP na macOS jest troche opóżnioną wersją. Przez co, ta modyfikacja działa między innymi w skrótach klawiaturowych, ale nie które opcję mogą nie działać, takie jak organizacje zestawu narzędzi. Trzeba poczekać, aż macOS osiągnie wersję 2.10.20, inaczej spodziewaj się takich niedogodności.

* Ubuntu (Za pomocą Snap): `/home/$ /snap/gimp/47/.config/GIMP/2.10/`

* Domyślna intalacja Gimp-a na Linuxi-e (.deb, .rpm): `/home/$USER/.config/GIMP/2.10/`

Nowa ikona będzie tylko działać, podczas poprawek w środowiskach, ale możesz ustawić ją ręcznie w swoim systemie

## Podziękowania

* Projekt, nie mógłby być zrealizowany bez dobrego GIMP Team.
* Za zrobienie nowego zdjęcia do Ekranu Ładowania dla [Isabella Mariana](https://www.pexels.com/pt-br/@isabella-mariana-1022505)
* Specjalne podziękowania do wszystkich pomocników Diolinux's  [Twitch-u](https://twitch.tv/Diolinux) i na [YouTube](https://youtube.com/Diolinux).

Nota de lançamento em Português: https://diolinux.com.br/2020/06/photogimp-2020.html 
