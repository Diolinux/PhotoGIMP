# 🎨 PhotoGIMP

<img src="../.local/share/icons/hicolor/256x256/256x256.png" align="right" alt="PhotoGIMP uygulama simgesi" title="PhotoGIMP uygulama simgesi">

[![GitHub yıldızları](https://img.shields.io/github/stars/Diolinux/PhotoGIMP?style=social)](https://github.com/Diolinux/PhotoGIMP)
[![Lisans: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Son sürüm](https://img.shields.io/github/v/release/Diolinux/PhotoGIMP)](https://github.com/Diolinux/PhotoGIMP/releases/latest)

<details id="-translations">
<summary><strong>🌍 Çeviriler</strong></summary>

Bu README başka dillerde de mevcuttur:

- 🇬🇧 [English (İngilizce)](../README.md)
- 🇮🇹 [Italiano (İtalyanca)](./README_it.md)
- 🇵🇱 [Polski (Lehçe)](./README_pl.md)
- 🇺🇦 [Українська (Ukraynaca)](./README_ua.md)
- 🇧🇷 [Português (Brezilya Portekizcesi)](./README_pt.md)
- 🇷🇺 [Русский (Rusça)](./README_ru.md)
- 🇪🇸 [Español (İspanyolca)](./README_es.md)
- 🇮🇱 [עברית (İbranice)](https://github.com/Diolinux/PhotoGIMP/blob/master/docs/README_he.md)
- 🇰🇷 [Korean (Korece)](./README_ko.md)
- 🇨🇳 [简体中文 (Basitleştirilmiş Çince)](./README_zh.md)
- 🇨🇿 [Čeština (Çekçe)](./README_cs.md)

Kendi dilinizi eklemek ister misiniz? Depoyu çatallayın (fork), `docs/README_xx.md` dosyasını oluşturun ve bir çekme isteği (pull request) gönderin!

</details>

**PhotoGIMP**, [GIMP](https://www.gimp.org/) (GNU Image Manipulation Program) arayüzünü **Adobe Photoshop** kullanıcılarına tanıdık gelecek bir düzene dönüştüren, topluluk tarafından geliştirilen ücretsiz bir yamadır. Photoshop'tan GIMP'e geçiyorsanız ve yeni arayüze hemen alışmak istiyorsanız PhotoGIMP tam size göre.

> **GIMP'i ilk kez mi kullanıyorsunuz?** GIMP; Linux, macOS ve Windows için sunulan, ücretsiz ve açık kaynaklı bir görüntü düzenleyicidir. Photoshop'un yapabildiği çoğu işi yapabilir: fotoğraf rötuşlama, görüntü birleştirme, grafik tasarım ve daha fazlası. Üstelik hepsi ücretsizdir. PhotoGIMP yalnızca _görünümünü ve kullanımını_ Photoshop'a daha çok benzetir.

---

## ✨ Özellikler

- **Photoshop benzeri araç düzeni**. Araçlar, Adobe Photoshop'ta alıştığınız konumlara benzer şekilde yeniden düzenlenir.
- **Özel açılış ekranı**. Uygulamayı başlattığınızda sizi PhotoGIMP'e özgü bir açılış ekranı karşılar.
- **En geniş tuval alanı**. Varsayılan ayarlar, mümkün olan en geniş çalışma alanını sunacak şekilde düzenlenmiştir.
- **Photoshop klavye kısayolları**. Klavye kısayolları, Windows sürümü için [Adobe'nin resmî belgelerini](https://helpx.adobe.com/photoshop/using/default-keyboard-shortcuts.html) temel alır.
- **Özel simge ve ad**. Özel bir `.desktop` dosyası, sistem menünüzde PhotoGIMP'in kendi simgesi ve uygulama adıyla görünmesini sağlar.

---

## 📷 Ekran görüntüleri

| Açılış ekranı | Uygulama penceresi |
|-|-|
| ![[PhotoGIMP Diolinux açılış ekranı]](../.config/GIMP/3.0/splashes/splash-screen-2025-v2.png)<br>PhotoGIMP Diolinux açılış ekranı | ![[PhotoGIMP 3]](../screenshots/photogimp_3_-_diolinux.png)<br>PhotoGIMP 3

---

## 📋 Gereksinimler

PhotoGIMP'i kurmadan önce aşağıdaki gereksinimleri karşıladığınızdan emin olun:

| Gereksinim | Ayrıntılar |
| ---------- | ---------- |
| **GIMP 3.0 veya daha yeni bir sürüm** | İndirme adresleri: [gimp.org](https://www.gimp.org/downloads/) veya [Flathub](https://flathub.org/apps/org.gimp.GIMP) (Linux) |
| **GIMP'i en az bir kez çalıştırın** | PhotoGIMP'in yapılandırma dosyalarının üzerine yazabilmesi için GIMP'in önce bu dosyaları oluşturması gerekir. **GIMP'i kurun → açın → kapatın → ardından PhotoGIMP'i kurun.** |

---

## ⚙ Kurulum

> [!WARNING]
> **Kurulumdan önce mevcut GIMP ayarlarınızı yedekleyin!** PhotoGIMP, GIMP'in yapılandırma dosyalarının üzerine yazar. Korumak istediğiniz özel ayarlarınız varsa önce bir yedek kopya alın. Aşağıdaki her bölümde yedekleme talimatlarını bulabilirsiniz.

---

### 🐧 Flatpak (Linux)

<img src="https://skillicons.dev/icons?i=linux" align="right" width="40" />

#### Yedekleme (isteğe bağlı)

Aşağıda kullanılan `install.sh` betiği **mevcut yapılandırmanızı otomatik olarak yedekler**. Bu nedenle bu adım yalnızca dosyaları elle kopyalamayı planlıyorsanız gereklidir:

```bash
cp -r ~/.config/GIMP/<version> ~/GIMP-<version>-backup
```

#### Kurulum

1. GIMP'i daha önce [Flathub'dan](https://flathub.org/apps/org.gimp.GIMP) kurmuş olduğunuzdan emin olun.
2. **GIMP'i bir kez açın, ardından kapatın**. Bu işlem, PhotoGIMP'in ihtiyaç duyduğu yapılandırma klasörlerini oluşturur.
3. Son sürümü indirin:
   👉 **[Linux için PhotoGIMP'i indirin (.zip)](https://github.com/Diolinux/PhotoGIMP/releases/latest/download/PhotoGIMP-linux.zip)**
4. `.zip` dosyasını **istediğiniz bir konuma** çıkarın (örneğin `Downloads` klasörünüze). Bu işlem, `.config` ve `.local` klasörlerini ve `install.sh` dosyasını içeren `PhotoGIMP-linux/` adlı bir klasör oluşturur.
   - ⚠️ `.zip` dosyasını ev klasörünüze çıkarmak PhotoGIMP'i **kurmaz**. Yalnızca `~/PhotoGIMP-linux/` klasörünü oluşturur. Yine de 5. adımı uygulamanız gerekir.
5. Klasörün içinden, paketteki kurulum betiğini çalıştırın:

   ```bash
   cd ~/Downloads/PhotoGIMP-linux
   chmod +x install.sh
   ./install.sh
   ```

   Betik, GIMP'in Flatpak ile mi yoksa sistemin paket yöneticisiyle mi kurulduğunu algılar, mevcut yapılandırmanızı yedekler ve dosyaları doğru yere kopyalar.
6. GIMP'i açın. Yeni PhotoGIMP düzenini görmelisiniz! 🎉

<details>
<summary><strong>📂 Dosyaları elle kopyalamayı mı tercih ediyorsunuz?</strong></summary>

`.config` ve `.local` klasörlerinin **içeriğini** ev klasörünüze kopyalayın; `PhotoGIMP-linux` klasörünün kendisini kopyalamayın. Yolların sonundaki `/.`, gizli dosyaların da kopyalanmasını sağlar:

```bash
cp -a ~/Downloads/PhotoGIMP-linux/.config/. ~/.config/
cp -a ~/Downloads/PhotoGIMP-linux/.local/.  ~/.local/
```

Dosya yöneticinizi kullanmayı tercih ediyorsanız:

- Dosyalar, gizli klasörler olan `~/.config` ve `~/.local` içine yerleştirilmelidir.
- Dosya yöneticinizde gizli klasörleri görmek için <kbd>Ctrl</kbd> + <kbd>H</kbd> tuşlarına basın.
- Mevcut dosyalarla ilgili bir soru çıkarsa **"Değiştir"** veya **"Üzerine yaz"** seçeneğini seçin.

</details>

<details>
<summary><strong>💡 Flatpak dışında bir yöntemle kurulmuş GIMP mi kullanıyorsunuz?</strong></summary>

GIMP'i Flatpak yerine dağıtımınızın paket yöneticisiyle (apt, dnf, pacman vb.) kurduysanız yapılandırma klasörü aynı konumdadır (`~/.config/GIMP/3.0`). Bu nedenle yukarıdaki adımlar yine geçerlidir. GIMP sürümünüzün 3.0 veya daha yeni olduğundan emin olun.

`install.sh`, paket yöneticisiyle yapılan kurulumları da algılar. Hem Flatpak hem de paket yöneticisiyle kurulmuş GIMP varsa hangisine yama uygulanacağını sorar. Paket yöneticisiyle yapılan kurulumlarda yalnızca GIMP yapılandırmasını değiştirir. `.local` içindeki özel başlatıcı ve simgeler Flatpak kurulumu için uygulanır.

</details>

---

### 🪟 Windows

<img src="https://skillicons.dev/icons?i=windows" align="right" />

#### Yedekleme (isteğe bağlı)

Mevcut GIMP ayarlarınızı korumak istiyorsanız önce yedekleyin:

1. Çalıştır iletişim kutusunu açmak için <kbd>Windows</kbd> + <kbd>R</kbd> tuşlarına basın.
2. `%APPDATA%\GIMP` yazın ve <kbd>Enter</kbd> tuşuna basın.
3. Sürüm klasörünün tamamını (örneğin `3.0`, `3.2`) güvenli bir konuma (örneğin Masaüstünüze) kopyalayın.

#### Kurulum

1. [GIMP'i resmî web sitesinden kurmuş](https://www.gimp.org/downloads/) olduğunuzdan emin olun.
2. **GIMP'i bir kez açın, ardından kapatın**. Bu işlem, PhotoGIMP'in ihtiyaç duyduğu yapılandırma klasörlerini oluşturur.
3. Son sürümü indirin:
   👉 **[Windows için PhotoGIMP'i indirin (.zip)](https://github.com/Diolinux/PhotoGIMP/releases/latest/download/PhotoGIMP.zip)**
4. `PhotoGIMP.zip` dosyasının içeriğini herhangi bir klasöre (örneğin Masaüstünüze) çıkarın.
5. Çıkarılan klasörü açın ve **içindeki sürüm klasörünü kopyalayın** (örneğin `3.0`).
6. Çalıştır iletişim kutusunu açmak için <kbd>Windows</kbd> + <kbd>R</kbd> tuşlarına basın.
7. `%APPDATA%\GIMP` yazın ve <kbd>Enter</kbd> tuşuna basın. GIMP'in ayarlar klasörü açılır.
8. Sürüm klasörünü buraya **yapıştırın**.
9. Mevcut dosyalarla ilgili bir soru çıkarsa **"Hedefteki dosyaları değiştir"** seçeneğini seçin.
10. GIMP'i açın. Yeni PhotoGIMP düzenini görmelisiniz! 🎉

<details>
<summary><strong>💡 İsteğe bağlı: GIMP kısayolunun simgesini değiştirin</strong></summary>

[photogimp.ico](https://github.com/Diolinux/PhotoGIMP/releases/latest/download/photogimp.ico) dosyasını indirip aşağıdaki konumda bulunan GIMP kısayolunun simgesini de değiştirebilirsiniz:

```
%appdata%\Microsoft\Windows\Start Menu\Programs\GIMP 3.0.0
```

Kısayola sağ tıklayın → **Özellikler** → **Simge Değiştir** → indirdiğiniz `.ico` dosyasını seçin.

</details>

<details>
<summary><strong>🍫 Chocolatey ile kurulum (alternatif)</strong></summary>

[Chocolatey](https://chocolatey.org/) kullanıyorsanız PhotoGIMP'i tek bir komutla kurabilirsiniz:

```powershell
choco install photogimp
```

Paketin bakımını yapan: [André Augusto](https://github.com/AndreAugustoDev)

</details>

---

### 🍎 macOS

<img src="https://skillicons.dev/icons?i=macos" align="right" />

#### Yedekleme (isteğe bağlı)

Mevcut GIMP ayarlarınızı korumak istiyorsanız önce yedekleyin:

1. Finder'ı açın.
2. <kbd>Cmd</kbd> + <kbd>Shift</kbd> + <kbd>G</kbd> tuşlarına basın ve `~/Library/Application Support/GIMP` konumuna gidin.
3. `GIMP` klasörünün tamamını güvenli bir konuma (örneğin Masaüstünüze) kopyalayın.

#### Kurulum

1. [GIMP'i resmî web sitesinden kurmuş](https://www.gimp.org/downloads/) olduğunuzdan emin olun.
2. **GIMP'i bir kez açın, ardından kapatın**. Bu işlem, PhotoGIMP'in ihtiyaç duyduğu yapılandırma klasörlerini oluşturur.
3. Son sürümü indirin:
   👉 **[macOS için PhotoGIMP'i indirin (.zip)](https://github.com/Diolinux/PhotoGIMP/releases/latest/download/PhotoGIMP.zip)**
4. `PhotoGIMP.zip` dosyasının içeriğini herhangi bir klasöre (örneğin Masaüstünüze) çıkarın.
5. Çıkarılan klasörü açın ve **`3.0` klasörünü kopyalayın**.
6. Finder'ı açın ve "Klasöre Git" penceresini açmak için <kbd>Cmd</kbd> + <kbd>Shift</kbd> + <kbd>G</kbd> tuşlarına basın.
7. `~/Library/Application Support/GIMP` yazın ve <kbd>Enter</kbd> tuşuna basın.
8. Önceki bir kurulumdan kalan `2.10` klasörünü görürseniz çakışmaları önlemek için **silin**.
9. `3.0` klasörünü GIMP klasörünün içine **yapıştırın**.
10. Mevcut dosyalarla ilgili bir soru çıkarsa **"Değiştir"** veya **"Birleştir"** seçeneğini seçin.
11. GIMP'i açın. Yeni PhotoGIMP düzenini görmelisiniz! 🎉

<details>
<summary><strong>Alternatif: Terminal ile kurulum</strong></summary>

Finder'ın **"Birleştir"** seçeneği mevcut dosyaları herhangi bir uyarı vermeden atlarsa veya komut satırını tercih ediyorsanız PhotoGIMP dosyalarını `rsync` ile kopyalayabilirsiniz.

1. Terminal'i açın.
2. `/path/to/extracted/3.0/` yerine çıkardığınız `3.0` klasörünün konumunu yazarak `rsync` komutunu çalıştırın:

   ```bash
   rsync -av --ignore-times /path/to/extracted/3.0/ ~/Library/Application\ Support/GIMP/3.0/
   ```

   Her iki yolun da `/` ile bittiğinden emin olun.
3. Kurulu GIMP sürümünüz farklı bir sürüm klasörü kullanıyorsa hedef yolu bu klasöre göre değiştirin (örneğin GIMP 3.2 için `~/Library/Application\ Support/GIMP/3.2/` kullanın).

</details>

---

## 📦 Yamanın içeriği

PhotoGIMP, GIMP'in yapılandırma dizininde aşağıdaki dosyaları değiştirir veya ekler:

| Dosya / klasör | İşlevi |
| ------------- | ------ |
| `shortcutsrc` | Photoshop ile eşleşecek şekilde atanmış klavye kısayolları |
| `toolrc` | Araç yapılandırması ve sıralaması |
| `sessionrc` | Pencere düzeni ve panel konumları |
| `dockrc` | Kenetlenebilir panel yapılandırması |
| `gimprc` | Genel GIMP tercihleri (tuval, ızgara vb.) |
| `contextrc` | Etkin araç ve renk bağlamı ayarları |
| `splashes/` | Özel PhotoGIMP açılış ekranı |
| `theme.css` | Arayüz temasında küçük düzenlemeler |
| `templaterc` | Önceden tanımlanmış tuval şablonları |

Linux'ta yama ayrıca şunları kurar:

- Özel bir `.desktop` dosyası (PhotoGIMP adı ve simgesiyle uygulama başlatıcı)
- `~/.local/share/icons/` içinde özel bir uygulama simgesi

---

<a id="-how-to-uninstall"></a>

## 🗑 Kaldırma

PhotoGIMP'i kaldırıp GIMP'i varsayılan durumuna döndürmek için GIMP'in yapılandırma klasörünü silip GIMP'i yeniden açmanız yeterlidir. GIMP, varsayılan ayarları yeniden oluşturur.

### Linux

```bash
rm -rf ~/.config/GIMP/3.0
```

Ardından GIMP'i yeniden açın. Yeni bir varsayılan yapılandırma oluşturacaktır.

Daha önce yedek aldıysanız bunun yerine yedeğinizi geri yükleyin:

```bash
cp -r ~/GIMP-3.0-backup ~/.config/GIMP/3.0
```

### Windows

1. <kbd>Windows</kbd> + <kbd>R</kbd> tuşlarına basın, `%APPDATA%\GIMP` yazın ve <kbd>Enter</kbd> tuşuna basın.
2. `3.0` klasörünü silin.
3. GIMP'i açın. Varsayılan ayarları yeniden oluşturacaktır.

Ya da yedeklediğiniz `3.0` klasörünü aynı konuma tekrar yapıştırarak yedeğinizi geri yükleyin.

### macOS

1. Finder'ı açın, <kbd>Cmd</kbd> + <kbd>Shift</kbd> + <kbd>G</kbd> tuşlarına basın.
2. `~/Library/Application Support/GIMP` konumuna gidin.
3. `3.0` klasörünü silin.
4. GIMP'i açın. Varsayılan ayarları yeniden oluşturacaktır.

Ya da yedeklediğiniz klasörü aynı konuma tekrar yapıştırarak yedeğinizi geri yükleyin.

---

## ❓ Sorun giderme / Sık sorulan sorular

> [!CAUTION]
> **PhotoGIMP'in resmî bir web sitesi yoktur.** Projenin tek resmî kaynağı GitHub deposudur: https://github.com/Diolinux/PhotoGIMP/

<details>
<summary><strong>PhotoGIMP hiçbir şeyi değiştirmedi. GIMP hâlâ aynı görünüyor</strong></summary>

- Dosyaları **doğru konuma** çıkardığınızdan emin olun. En yaygın hata, dosyaları yanlış klasöre çıkarmaktır.
- **Linux**: `.config` ve `.local` klasörleri ev dizininizde (`~`) bulunmalıdır. Bunlar gizlidir; görmek için dosya yöneticinizde <kbd>Ctrl</kbd> + <kbd>H</kbd> tuşlarına basın. `~/PhotoGIMP-linux/` klasörünüz varsa arşivi çıkarmış ancak kurulumu yapmamışsınız demektir. Bu klasörü açın ve `./install.sh` komutunu çalıştırın.
- **Windows**: `3.0` klasörü, `%APPDATA%\GIMP` klasörünün yanında değil, içinde olmalıdır.
- **macOS**: `3.0` klasörü, `~/Library/Application Support/GIMP` içinde olmalıdır.
- Dosyaları yapıştırmadan önce **GIMP'i kapattınız mı**? GIMP, kapanırken yeni kopyalanan ayarların üzerine yazabilir.
  </details>

<details>
<summary><strong>PhotoGIMP'i kurduktan sonra GIMP'i açarken hata alıyorum</strong></summary>

- Bu genellikle GIMP sürümünün uyumlu olmadığı anlamına gelir. PhotoGIMP, **GIMP 3.0+** için hazırlanmıştır. GIMP 2.x kullanıyorsanız uyumlu olmayacaktır.
- Yapılandırma klasörünü silip yeniden kurmayı deneyin. [Kaldırma](#-how-to-uninstall) bölümüne bakın.
  </details>

<details>
<summary><strong>PhotoGIMP'i GIMP 2.10 ile kullanabilir miyim?</strong></summary>

Hayır. PhotoGIMP'in bu sürümü yalnızca **GIMP 3.0 ve daha yeni sürümler** için tasarlanmıştır. GIMP 2.x ile 3.x arasında yapılandırma biçimi önemli ölçüde değişmiştir.

</details>

<details>
<summary><strong>PhotoGIMP özel fırçalarımı, yazı tiplerimi veya eklentilerimi siler mi?</strong></summary>

Hayır. PhotoGIMP yalnızca yapılandırma dosyalarını (kısayollar, düzen, tercihler) değiştirir. Kişisel fırçalarınıza, yazı tiplerinize, renk geçişlerinize ve eklentilerinize dokunmaz.

</details>

<details>
<summary><strong>PhotoGIMP'i kurduktan sonra kısayolları özelleştirebilir miyim?</strong></summary>

Evet! PhotoGIMP yalnızca başlangıç ayarlarını sağlar. GIMP'te **Düzenle → Klavye Kısayolları** menüsünden istediğiniz kısayolu değiştirebilirsiniz.

</details>

<details>
<summary><strong>PhotoGIMP'i yeni bir sürüme nasıl güncellerim?</strong></summary>

Son sürümü indirip kurulum adımlarını tekrar uygulamanız yeterlidir. Önceki PhotoGIMP yapılandırmasının üzerine yazılacaktır.

</details>

---

## 🤝 Katkıda bulunma

Bir hata mı buldunuz? Bir öneriniz mi var? Yardımınızı bekliyoruz!

- **Sorun bildirin**: [Bir sorun kaydı açın](https://github.com/Diolinux/PhotoGIMP/issues)
- **Düzeltme gönderin**: [Bir çekme isteği oluşturun](https://github.com/Diolinux/PhotoGIMP/pulls)
- **Çeviri yapın**: README'yi daha fazla dile çevirmemize yardımcı olun! [Çeviriler](#-translations) bölümüne bakın.

---

## 🏆 Teşekkürler

- Harika [GIMP](https://www.gimp.org/) ekibi olmasaydı bu proje mümkün olmazdı.
- Diolinux'u [YouTube](https://youtube.com/Diolinux) üzerinden destekleyen herkese çok teşekkürler.
- Açılış ekranı ve simgeler: [Adriel Filipe Design](https://bento.me/adrielfilipedesign).

---

## 💙 Projeyi destekleyin

PhotoGIMP'in bakımı; projeyi erişilebilir, belgelenmiş ve güncel GIMP sürümleriyle uyumlu tutmak için zaman ayıran kişiler tarafından yapılır. Başlıca katkıda bulunanları destekleyerek projenin geliştirilmesine katkı sağlayabilirsiniz:

- **Dionatan Simioni (Diolinux)**. PhotoGIMP'in ve Diolinux topluluğunun kurucusu. [Diolinux YouTube kanalını](https://youtube.com/Diolinux) takip edin ve [Diolinux blogunu](https://diolinux.com.br/) ziyaret edin.
- **[Gabriel Almir](https://github.com/gabrielalmir)**. 2021'den beri projenin bakımını yapıyor. Bakım çalışmalarını [Ko-fi](https://ko-fi.com/gabrielalmir) üzerinden destekleyebilirsiniz.

Kod katkıları, sorun bildirimleri, çeviriler ve belgelendirme iyileştirmeleri de PhotoGIMP'in devamlılığına yardımcı olmanın değerli yollarıdır.

---

## 👥 Katkıda bulunanlar

<a align="center" href="https://github.com/Diolinux/PhotoGIMP/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=Diolinux/PhotoGIMP" />
</a>

---

## 📄 Lisans

PhotoGIMP, [GNU Genel Kamu Lisansı v3.0](../LICENSE) kapsamında lisanslanmıştır.
