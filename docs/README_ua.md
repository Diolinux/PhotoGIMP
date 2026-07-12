# 🎨 PhotoGIMP

<img src="./.local/share/icons/hicolor/256x256/256x256.png" align="right" alt="PhotoGIMP application icon" title="PhotoGIMP application icon">

[![GitHub stars](https://img.shields.io/github/stars/Diolinux/PhotoGIMP?style=social)](https://github.com/Diolinux/PhotoGIMP)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Latest Release](https://img.shields.io/github/v/release/Diolinux/PhotoGIMP)](https://github.com/Diolinux/PhotoGIMP/releases/latest)

**PhotoGIMP** — це безкоштовна, створена спільнотою модифікація, яка змінює інтерфейс [GIMP](https://www.gimp.org/) (GNU Image Manipulation Program) на більш звичний для користувачів **Adobe Photoshop**. Якщо ви переходите з Photoshop на GIMP і хочете одразу почуватися як удома, PhotoGIMP — саме для вас.

> **Новачок у GIMP?** GIMP — це безкоштовний редактор зображень з відкритим кодом, доступний для Linux, macOS та Windows. Він може виконувати більшість функцій Photoshop — ретушування фотографій, композицію зображень, графічний дизайн та багато іншого — і все це безкоштовно. PhotoGIMP просто робить його більш схожим на Photoshop за **зовнішнім виглядом та поведінкою**.

---

## ✨ Особливості

- **Photoshop-подібний інтерфейс** — Панелі та інструменти розташовані звично для користувачів Photoshop.
- **Власний екран запуску** — Унікальний екран запуску PhotoGIMP вітає вас при старті.
- **Максимізована робоча область** — Налаштування за замовчуванням налаштовані для максимізованої робочої області.
- **Комбінації клавіш як у Photoshop** — Клавіатурні скорочення відповідають [офіційній документації Adobe](https://helpx.adobe.com/photoshop/using/default-keyboard-shortcuts.html) для версії Windows.
- **Власна іконка та назва** — Спеціальний файл `.desktop` надає PhotoGIMP власний значок та назву в меню вашої системи.

---

## 📷 Знімки екрану

<p>
  <img src="./.config/GIMP/3.0/splashes/splash-screen-2025-v2.png" alt="PhotoGIMP Diolinux Splash Art">
  <em>PhotoGIMP Diolinux Splash Art</em>
</p>

<p>
  <img src="./screenshots/photogimp_3_-_diolinux.png" alt="PhotoGIMP 3">
  <em>GIMP 3.0 із застосованим патчем PhotoGIMP</em>
</p>

---

## 📋 Вимоги

Перед встановленням PhotoGIMP переконайтеся, що у вас є:

| Вимога | Деталі |
|---|---|
| **GIMP 3.0 або новіша версія** | Завантажити з: [gimp.org](https://www.gimp.org/downloads/) або [Flathub](https://flathub.org/apps/org.gimp.GIMP) (Linux) |
| **Запустіть GIMP хоча б один раз** | GIMP потрібно запустити, щоб створити файли налаштувань, перш ніж PhotoGIMP зможе їх перезаписати. **Встановіть GIMP → відкрийте його → закрийте → потім встановіть PhotoGIMP.** |

---

## ⚙ Як встановити

> [!WARNING]
> **Створіть резервну копію ваших поточних налаштувань GIMP перед встановленням!** PhotoGIMP перезаписує файли налаштувань GIMP. Якщо у вас є власні налаштування, які ви хочете зберегти, спочатку збережіть резервну копію. Дивіться інструкції щодо резервного копіювання в кожному розділі нижче.

---

### 🐧 Flatpak (Linux)

<img src="https://skillicons.dev/icons?i=linux" align="right" width="40" />

#### Резервна копія (необов'язково)

Якщо ви хочете зберегти поточні налаштування GIMP, спочатку створіть їхню резервну копію:

```bash
cp -r ~/.config/GIMP/3.0 ~/GIMP-3.0-backup
```

#### Встановлення

1. Переконайтесь, що GIMP встановлено [з Flathub](https://flathub.org/apps/org.gimp.GIMP).
2. **Відкрийте GIMP один раз, потім закрийте його** — це створює папки налаштувань, які потрібні PhotoGIMP.
3. Завантажте останню версію:
   👉 **[Завантажити PhotoGIMP для Linux (.zip)](https://github.com/Diolinux/PhotoGIMP/releases/download/3.0/PhotoGIMP-linux.zip)**
4. Розпакуйте файл `.zip` **у вашу домашню папку** (`~`).
   - Це розмістить файли у `~/.config` та `~/.local`, які є прихованими папками.
   - Щоб побачити приховані папки у вашому файловому менеджері, натисніть <kbd>Ctrl</kbd> + <kbd>H</kbd>.
   - Коли з'явиться запит про існуючі файли, оберіть **"Замінити"** або **"Перезаписати"**.
5. Відкрийте GIMP — ви повинні побачити новий інтерфейс PhotoGIMP! 🎉

<details>
<summary><strong>💡 Використовуєте GIMP не з Flatpak?</strong></summary>

Якщо ви встановили GIMP з менеджера пакетів вашого дистрибутива (apt, dnf, pacman тощо) замість Flatpak, папка налаштувань знаходиться в тому ж місці (`~/.config/GIMP/3.0`), тому наведені вище кроки все одно працюють. Просто переконайтеся, що у вас встановлена версія GIMP 3.0 або новіша.
</details>

---

### 🪟 Windows

<img src="https://skillicons.dev/icons?i=windows" align="right" />

#### Резервна копія (необов'язково)

Якщо ви хочете зберегти поточні налаштування GIMP, спочатку створіть їхню резервну копію:

1. Натисніть <kbd>Windows</kbd> + <kbd>R</kbd>, щоб відкрити діалогове вікно "Виконати".
2. Введіть `%APPDATA%\GIMP` і натисніть <kbd>Enter</kbd>.
3. Скопіюйте всю папку `3.0` у безпечне місце (наприклад, на робочий стіл).

#### Встановлення

1. Переконайтесь, що у вас встановлено [GIMP з офіційного сайту](https://www.gimp.org/downloads/).
2. **Відкрийте GIMP один раз, потім закрийте його** — це створює папки налаштувань, які потрібні PhotoGIMP.
3. Завантажте останню версію:
   👉 **[Завантажити PhotoGIMP для Windows (.zip)](https://github.com/Diolinux/PhotoGIMP/releases/download/3.0/PhotoGIMP.zip)**
4. Розпакуйте вміст `PhotoGIMP.zip` у будь-яку папку (наприклад, на робочий стіл).
5. Відкрийте розпаковану папку і **скопіюйте папку `3.0`**.
6. Натисніть <kbd>Windows</kbd> + <kbd>R</kbd>, щоб відкрити діалогове вікно "Виконати".
7. Введіть `%APPDATA%\GIMP` і натисніть <kbd>Enter</kbd> — це відкриє папку налаштувань GIMP.
8. **Вставте** папку `3.0` сюди.
9. Коли з'явиться запит про існуючі файли, оберіть **"Замінити файли в місці призначення"**.
10. Відкрийте GIMP — ви повинні побачити новий інтерфейс PhotoGIMP! 🎉

<details>
<summary><strong>💡 Необов'язково: Змініть значок ярлика GIMP</strong></summary>

Ви також можете завантажити [photogimp.ico](https://github.com/Diolinux/PhotoGIMP/releases/download/3.0/photogimp.ico) і оновити значок на ярлику GIMP, розташованому за адресою:

```
%appdata%\Microsoft\Windows\Start Menu\Programs\GIMP 3.0.0
```

Клацніть правою кнопкою миші на ярлик → **Властивості** → **Змінити значок** → оберіть завантажений файл `.ico`.
</details>

<details>
<summary><strong>🍫 Встановлення через Chocolatey (альтернатива)</strong></summary>

Якщо ви використовуєте [Chocolatey](https://chocolatey.org/), ви можете встановити PhotoGIMP за допомогою однієї команди:

```powershell
choco install photogimp
```

Підтримується користувачем: [André Augusto](https://github.com/AndreAugustoDev)
</details>

---

### 🍎 macOS

<img src="https://skillicons.dev/icons?i=macos" align="right" />

#### Резервна копія (необов'язково)

Якщо ви хочете зберегти поточні налаштування GIMP, спочатку створіть їхню резервну копію:

1. Відкрийте Finder.
2. Натисніть <kbd>Cmd</kbd> + <kbd>Shift</kbd> + <kbd>G</kbd> і перейдіть до `~/Library/Application Support/GIMP`.
3. Скопіюйте всю папку `GIMP` у безпечне місце (наприклад, на робочий стіл).

#### Встановлення

1. Переконайтесь, що у вас встановлено [GIMP з офіційного сайту](https://www.gimp.org/downloads/).
2. **Відкрийте GIMP один раз, потім закрийте його** — це створює папки налаштувань, які потрібні PhotoGIMP.
3. Завантажте останню версію:
   👉 **[Завантажити PhotoGIMP для macOS (.zip)](https://github.com/Diolinux/PhotoGIMP/releases/download/3.0/PhotoGIMP.zip)**
4. Розпакуйте вміст `PhotoGIMP.zip` у будь-яку папку (наприклад, на робочий стіл).
5. Відкрийте розпаковану папку і **скопіюйте папку `3.0`**.
6. Відкрийте Finder, натисніть <kbd>Cmd</kbd> + <kbd>Shift</kbd> + <kbd>G</kbd>, щоб відкрити "Перейти до папки".
7. Введіть `~/Library/Application Support/GIMP` і натисніть <kbd>Enter</kbd>.
8. Якщо ви бачите папку `2.10` з попередньої установки, **видаліть її**, щоб уникнути конфліктів.
9. **Вставте** папку `3.0` всередину папки GIMP.
10. Коли з'явиться запит про існуючі файли, оберіть **"Замінити"** або **"Об'єднати"**.
11. Відкрийте GIMP — ви повинні побачити новий інтерфейс PhotoGIMP! 🎉

---

## 📦 Що всередині патчу

PhotoGIMP замінює або додає наступні файли в директорії конфігурації GIMP:

| Файл / Папка | Що робить                                              |
|---|--------------------------------------------------------|
| `shortcutsrc` | Комбінації клавіш, які використовуються у Photoshop    |
| `toolrc` | Налаштування інструментів та їх порядок                |
| `sessionrc` | Розташування вікон та панелей                          |
| `dockrc` | Налаштування доку / панелей                            |
| `gimprc` | Загальні налаштування GIMP (полотно, сітка тощо)       |
| `contextrc` | Налаштування контексту активного інструменту / кольору |
| `splashes/` | Власний екран запуску PhotoGIMP                        |
| `theme.css` | Невеликі зміни теми інтерфейсу користувача             |
| `templaterc` | Попередньо визначені шаблони полотна                   |

У Linux, патч також встановлює:
- Власний файл `.desktop` (лаунчер застосунку з ім'ям та іконкою PhotoGIMP)
- Власну іконку застосунку в `~/.local/share/icons/`

---

## 🗑 Як видалити

Щоб видалити PhotoGIMP і відновити GIMP до стану за замовчуванням, просто видаліть папку конфігурації GIMP і знову відкрийте GIMP — він створить нові налаштування за замовчуванням.

### Linux

```bash
rm -rf ~/.config/GIMP/3.0
```

Потім відкрийте GIMP знову — він створить нову конфігурацію за замовчуванням.

Якщо ви зробили резервну копію раніше, відновіть її замість цього:

```bash
cp -r ~/GIMP-3.0-backup ~/.config/GIMP/3.0
```

### Windows

1. Натисніть <kbd>Windows</kbd> + <kbd>R</kbd>, введіть `%APPDATA%\GIMP` і натисніть <kbd>Enter</kbd>.
2. Видаліть папку `3.0`.
3. Відкрийте GIMP — він створить нові налаштування за замовчуванням.

Або відновіть резервну копію, вставивши збережену папку `3.0` назад.

### macOS

1. Відкрийте Finder, натисніть <kbd>Cmd</kbd> + <kbd>Shift</kbd> + <kbd>G</kbd>.
2. Перейдіть до `~/Library/Application Support/GIMP`.
3. Видаліть папку `3.0`.
4. Відкрийте GIMP — він створить нові налаштування за замовчуванням.

Або відновіть резервну копію, вставивши збережену папку `3.0` назад.

---

## ❓ Вирішення проблем / FAQ

> [!CAUTION]
> **PhotoGIMP не має офіційного вебсайту.** Єдиним офіційним джерелом проекту є його репозиторій на GitHub: https://github.com/Diolinux/PhotoGIMP/

<details>
<summary><strong>PhotoGIMP не змінив нічого — GIMP виглядає так само</strong></summary>

- Переконайтеся, що ви витягли файли в **правильне місце**. Найпоширеніша помилка — витягти їх у неправильну папку.
- **Linux**: Папки `.config` та `.local` повинні бути у вашому домашньому каталозі (`~`). Вони приховані — натисніть <kbd>Ctrl</kbd> + <kbd>H</kbd> у вашому файловому менеджері, щоб їх побачити.
- **Windows**: Папка `3.0` повинна бути всередині `%APPDATA%\GIMP`, а не поруч із нею.
- **macOS**: Папка `3.0` повинна бути всередині `~/Library/Application Support/GIMP`.
- Чи **закрили GIMP** перед вставкою файлів? GIMP може перезаписати вхідні налаштування при виході.
</details>

<details>
<summary><strong>Я отримую помилку при відкритті GIMP після встановлення PhotoGIMP</strong></summary>

- Зазвичай це означає, що версія GIMP не збігається. PhotoGIMP створено для **GIMP 3.0+**. Якщо ви використовуєте GIMP 2.x, він не буде сумісним.
- Спробуйте видалити папку конфігурації та перевстановити — див. розділ [Як видалити](#-як-видалити) вище.
</details>

<details>
<summary><strong>Чи можу я використовувати PhotoGIMP з GIMP 2.10?</strong></summary>

Ні. Ця версія PhotoGIMP призначена виключно для **GIMP 3.0 і новіших версій**. Формат конфігурації значно змінився між GIMP 2.x і 3.x.
</details>

<details>
<summary><strong>Чи видалить PhotoGIMP мої власні пензлі, шрифти або плагіни?</strong></summary>

Ні. PhotoGIMP лише замінює файли налаштувань (комбінації клавіш, макет, налаштування). Ваші особисті пензлі, шрифти, градієнти та плагіни залишаються недоторканими.
</details>

<details>
<summary><strong>Чи можу я налаштувати комбінації клавіш після встановлення PhotoGIMP?</strong></summary>

Звичайно! PhotoGIMP лише встановлює початкові налаштування. Ви можете змінювати будь-які комбінації клавіш у GIMP через **Редагувати → Комбінації клавіш**.
</details>

<details>
<summary><strong>Як оновити PhotoGIMP до нової версії?</strong></summary>

Просто завантажте останню версію та повторіть кроки встановлення — це перезапише попередню конфігурацію PhotoGIMP.
</details>

---

## 🤝 Участь у проєкті

Знайшли помилку? Маєте пропозицію? Ми будемо раді вашій допомозі!

- **Повідомити про проблему**: [Відкрити issue](https://github.com/Diolinux/PhotoGIMP/issues)
- **Надіслати виправлення**: [Створити pull request](https://github.com/Diolinux/PhotoGIMP/pulls)
- **Переклад**: Допоможіть нам перекласти README на інші мови! Див. розділ [Переклади](#-переклади).

---

## 🌍 Переклади

Цей README доступний іншими мовами:

- 🇬🇧 [English (Англійська)](../README.md)
- 🇵🇱 [Polski (Польська)](./README_pl.md)
- 🇮🇹 [Italiano (Італійська)](./README_it.md)
- 🇮🇱 [עברית (Іврит)](./README_he.md)
- 🇪🇸 [Español (Іспанська)](./README_es.md)
- 🇧🇷 [Português (Португальська)](./README_pt.md)
- 🇰🇷 [한국어 (Корейська)](./README_ko.md)
- 🇨🇳 [中文 (Китайська)](./README_zh.md)

Хочете додати свою мову? Форкніть репозиторій, створіть файл `docs/README_xx.md` і надішліть запит на злиття!

---

## 🏆 Подяки

- Цей проєкт не був би можливим без неймовірної команди [GIMP](https://www.gimp.org/).
- ВЕЛИКА подяка всім прихильникам Diolinux на [YouTube](https://youtube.com/Diolinux).
- Екран завантаження та значки від [Adriel Filipe Design](https://bento.me/adrielfilipedesign).

---

## 👥 Учасники

<a align="center" href="https://github.com/Diolinux/PhotoGIMP/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=Diolinux/PhotoGIMP" />
</a>

---

## 📄 Ліцензія

PhotoGIMP ліцензовано під [GNU General Public License v3.0](../LICENSE).
