NOT: Proje şu anki hali ile oldukça kullanışlı olsa da ve muhtemelen küçük veya sorunsuz kullanabilseniz de, şimdilik yeni özellikler ekleyemediğimi veya hata analizi yapamayacağımı bilmeniz önemlidir. Bunun harici, Photogimp'in tadını çıkarın! :)

# 🎨 PhotoGIMP

<img src="../.local/share/icons/hicolor/256x256/apps/photogimp.png" align="right" alt="PhotoGimp application icon" title="PhotoGimp application icon">

Adobe Photoshop kullanıcıları için GIMP 2.10+ sürümünü optimize etmek için aşağıdaki gibi özellikleri içeren bir yama:

* Adobe Photoshop'un konumunu taklit etmek için araç organizasyonu;
* "Seçimi iyileştir" gibi varsayılan olarak yüklü gelen yeni Python filtreleri;
* Yeni Açılış Ekranı
* Tuval üzerindeki alanı en üst düzeye çıkarmak için yeni varsayılan ayarlar;
* Adobe'nin Belgelerini izleyerek Windowstaki Photoshop'takilere benzer kısayollar;
* Özel .desktop dosyasından yeni ikon ve ad.
* Sistem dili artık varsayılan olarak kullanılıyor, hala ayarlardan değiştirilebilir.

![PhotoGimp Diolinux Splash Art](../.var/app/org.gimp.GIMP/config/GIMP/2.10/splashes/photogimp-diolinux-splash.png)

## 📷 Screenshots

![PhotoGimp Screenshot OSX](./screenshots/osx.png)

## ⚙ Nasıl Yüklenir (Flatpak kullanarak)

Bu paket tamamen flatpak hakkında, ama aynı zamanda Gimp'in herhangi bir sürümünde (.deb, .rpm, Snap, AppImage, Windows, macOS) kullanabileceğiniz "sadece dosyalar"ı da içerir. Sadece GIMP yapılandırma dosyalarının konumunu kontrol edin.

**Devam etmeden önce Gimp'i açın ve kapatın!**

### Flatpak ortmanını hazırlama

*Eğer GIMP'ı önceden .deb, .rpm, vb., kullanarak indirdiyseniz, Flatpak yapılandırma dosyalarıyla çakışabileceğinden  $HOME/.config/GIMP dizinini sildiğinizden emin olun.*

1. İlk başta, GIMP'I sisteminizded [Flatpak'ı kullanarak](https://flatpak.org/setup/) indirdiğinizden emin olun.
2. GIMP'ı Uygulama Mağazası/Paket Yöneticisi veya terminalle:
   ```flatpak install flathub org.gimp.GIMP``` indirdiğinizden emin olun.

### PhotoGIMP'ı Yükleme

[releases page](https://github.com/Diolinux/PhotoGIMP/releases)'deki .zip dosyasının içinde üç klasör bulacaksınız (adları nokta ile başladığından Windows olmayan sistemlerde gizlidir). Tüm bu klasörlerin $HOME klasörünüze çıkarılması ve eski bir kurulumdan aynı dosyalara zaten sahipseniz her şeyin üzerine yazılması gerekir.

Dosya şu klasörleri içeriyor:

* `.icons` (yeni PhotoGIMP ikonu var)
* `.local` (özelleştirilmiş .desktop dosyası var)
* `.var` (GIMP 2.10+ için flatpak yama özelleştirmesini içerir)

Eğer PhotoGIMP özelleştirmesini orijinal ikon ve adı değiştirmeden kullanmak istiyorsanız, sadece .var dosyasını ec dizininize çıkarın.

## ⚙ Nasıl Yüklenir (diğerleri)

Sadece dosyalar olduğundan, yapmanız gereken tek şey bu paketten /.var/app/org.gimp.GIMP/config/GIMP/2.10 belirli bir klasörde bulunan tüm dosyaları, mevcut olanları geçersiz kılarak, her bir sistemdeki GIMP yapılandırma klasörünüze kopyalamaktır.

**Devam etmeden önce GIMP'ı yükledikten sonra başlatıp kapatın!**

Yeni ikon elle ayarlanmalıdır.

### Ubuntu Snap

Yapılandırma klasörü: `$HOME/snap/gimp/47/.config/GIMP/2.10/`

### Diğer Linux veya Unix(-benzeri) sistemler (.deb, .rpm, etc.)

Yapılandırma klasörü: `$HOME/.config/GIMP/2.1<0/`

### macOS

Yapılandırma klasörü: `"$HOME/Library/Application Support/GIMP/2.10/"`

* [Davies Media Design'dan macOS üzerine Video Eğitimi](https://youtu.be/5nXhtaGQs9U)

Bu tek satırlık işinizi görecektir:
```console
curl -L https://github.com/Diolinux/PhotoGIMP/releases/download/1.0/PhotoGIMP.by.Diolinux.v2020.for.Flatpak.zip -o ~/Downloads/PhotoGIMP.by.Diolinux.v2020.for.Flatpak.zip && unzip ~/Downloads/PhotoGIMP.by.Diolinux.v2020.for.Flatpak.zip -d ~/Downloads && cp -R ~/Downloads/PhotoGIMP\ by\ Diolinux\ v2020\ for\ Flatpak/.var/app/org.gimp.GIMP/config/GIMP/2.10/ ~/Library/Application\ Support/GIMP/2.10 && rm ~/Downloads/PhotoGIMP.by.Diolinux.v2020.for.Flatpak.zip
```
(1.0 sürümünü İndirilenler klasörüne indirir, dosyaları açar ve kopyalar, ardından indirilen .zip dosyasını kaldırır)

Uyarı: macOS üzerindeki GIMP biraz geç yayınlandı. Bu nedenle, bu yama özellikle kısayollar konusunda hala çalışmaktadır, ancak araç kutusu organizasyonu gibi bazı şeyler düzgün çalışmayacaktır. MacOS sürümü 2.10.20 sürümüne ulaşana kadar bu davranış normaldir.

### Mac OS Kolay Yükleyici (yapan: [@MatthijsKamstra](https://github.com/MatthijsKamstra))

> Gimp yüklü olmalı ([brew](https://formulae.brew.sh/cask/gimp) veya [otherwise](https://www.gimp.org/downloads/))

[bash](https://raw.githubusercontent.com/MatthijsKamstra/Mac-setup/master/install/photogimp_osx.sh) skripti nasıl çalışıyor?

* `Flatpak.zip`'i indiriyor ve Gimp klasörüne kopyalıyor
* OSC PhotoGimp ikonu oluşturuyor
* İkonu Gimp klasörüne kopyalıyor
* İndirilmiş/oluşturulmuş tüm dosyaları temizliyor

##### Bash nasıl çalıştırılır

you can [down](https://raw.githubusercontent.com/MatthijsKamstra/Mac-setup/master/install/photogimp_osx.sh) and run the bash script:

```bash
cd /path/to/download/folder
sh photogimp_osx.sh
```

##### Komut dosyasını çalıştırın (kolay yol)


```bash
sh -c "$(curl -fsSL https://raw.githubusercontent.com/MatthijsKamstra/Mac-setup/master/install/photogimp_osx.sh)"
```

### Windows

* [PhotoGIMP.zip](https://github.com/Diolinux/PhotoGIMP/releases) dosyasını indirin
* ZIP'ten `.var\app\org.gimp.GIMP\config\GIMP\2.10` yoluna erişin, dosyaları `%APPDATA%\GIMP\2.10` yoluna kopyalayın
* [Davies Media Design tarafından Windows üzerinde Video Eğitimi](https://youtu.be/57DNUsf4A-0)

Veya [Chocolatey](https://chocolatey.org/) ile indirin:
```powershell
choco install photogimp
```
Bakımını yapan: [André Augusto](https://github.com/AndreAugustoAAQ)

## Katkıda Bulunanlar 

* Bu proje harika GIMP takımı olmasaydı olmazdı.
* Yeni Açılış ekranı [Isabella Mariana](https://www.pexels.com/pt-br/@isabella-mariana-1022505)'dan
* [Twitch](https://twitch.tv/Diolinux) ve [YouTube](https://youtube.com/Diolinux)'taki tüm Diolinux'un destekçilerine BÜYÜK bir teşekkür.

## Katkıda Bulunanlar
<a align="center" href="https://github.com/Diolinux/PhotoGIMP/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=Diolinux/PhotoGIMP" />
</a>

## Yama Notları
-  [Veja as Notas de Lançamento em Português](https://diolinux.com.br/2020/06/photogimp-2020.html)
