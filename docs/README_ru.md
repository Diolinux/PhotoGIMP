# 🎨 PhotoGIMP

<img src="../.local/share/icons/hicolor/256x256/256x256.png" align="right" alt="PhotoGIMP application icon" title="PhotoGIMP application icon">

[![GitHub stars](https://img.shields.io/github/stars/Diolinux/PhotoGIMP?style=social)](https://github.com/Diolinux/PhotoGIMP)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Latest Release](https://img.shields.io/github/v/release/Diolinux/PhotoGIMP)](https://github.com/Diolinux/PhotoGIMP/releases/latest)

**PhotoGIMP** — это бесплатный, разработанный сообществом патч, который преобразует [GIMP](https://www.gimp.org/) (GNU Image Manipulation Program) в интерфейс, знакомый пользователям **Adobe Photoshop**. Если вы переходите с Photoshop на GIMP и хотите сразу почувствовать себя как дома, PhotoGIMP — это то, что вам нужно.

> **Впервые работаете в GIMP?** GIMP — это бесплатный графический редактор с открытым исходным кодом, доступный для Linux, macOS и Windows. Он может делать большинство вещей, которые может делать Photoshop — ретушь фотографий, композицию изображений, графический дизайн и многое другое — и всё это бесплатно. PhotoGIMP просто делает его похожим на Photoshop по *внешнему виду и функциональности*.

---

## ✨ Особенности

- **Расположение инструментов, аналогичное Photoshop** — Инструменты перегруппированы таким образом, чтобы имитировать привычное вам расположение в Adobe Photoshop.
- **Пользовательская заставка** — Уникальная заставка PhotoGIMP приветствует вас при запуске.
- **Максимально увеличенное рабочее пространство** — Настройки по умолчанию оптимизированы для обеспечения максимально возможной рабочей области.
- **Сочетания клавиш Photoshop** — Сочетания клавиш соответствуют [официальной документации Adobe](https://helpx.adobe.com/photoshop/using/default-keyboard-shortcuts.html) для версии Windows.
- **Пользовательский значок и имя** — Специальный `.desktop` файл позволяет присвоить PhotoGIMP собственный значок и имя приложения в системном меню.

---

## 📷 Скриншоты

<p>
  <img src="../.config/GIMP/3.0/splashes/splash-screen-2025-v2.png" alt="PhotoGIMP Diolinux Splash Art">
  <em>PhotoGIMP Diolinux Splash Art</em>
</p>

<p>
  <img src="../screenshots/photogimp_3_-_diolinux.png" alt="PhotoGIMP 3">
  <em>GIMP 3.0 с примененным патчем PhotoGIMP</em>
</p>

---

## 📋 Требования

Перед установкой PhotoGIMP убедитесь, что у вас установлены следующие компоненты:

| Requirement | Details |
|---|---|
| **GIMP 3.0 или более поздняя версия** | Скачать можно с сайта: [gimp.org](https://www.gimp.org/downloads/) или [Flathub](https://flathub.org/apps/org.gimp.GIMP) (Linux) |
| **Запустите GIMP хотя бы один раз.** | GIMP должен сначала создать файлы конфигурации, прежде чем PhotoGIMP сможет их заменить. **Установите GIMP → запустите его → закройте → затем установите PhotoGIMP.** |

---

## ⚙ Инструкция по установке

> [!WARNING]
> **Перед установкой обязательно сделайте резервную копию текущих настроек GIMP!** PhotoGIMP перезаписывает конфигурационные файлы GIMP. Если у вас есть пользовательские настройки, которые вы хотите сохранить, сначала сохраните резервную копию. Инструкции по резервному копированию см. в каждом разделе ниже.

---

### 🐧 Flatpak (Linux)

<img src="https://skillicons.dev/icons?i=linux" align="right" width="40" />

#### Резервное копирование (необязательно)

Если вы хотите сохранить текущие настройки GIMP, сначала сделайте их резервную копию:

```bash
cp -r ~/.config/GIMP/3.0 ~/GIMP-3.0-backup
```

#### Установка

1. Убедитесь, что у вас уже установлен GIMP [из Flathub](https://flathub.org/apps/org.gimp.GIMP).
2. **Откройте GIMP один раз, а затем закройте его** — это создаст папки конфигурации, необходимые для PhotoGIMP.
3. Скачайте последнюю версию:
   👉 **[Скачать PhotoGIMP для Linux (.zip)](https://github.com/Diolinux/PhotoGIMP/releases/download/3.0/PhotoGIMP-linux.zip)**
4. Распакуйте `.zip` файл **в свою домашнюю папку** (`~`).
   - Это позволит поместить файлы в папки `~/.config` и `~/.local`, которые являются скрытыми папками.
   - Чтобы просмотреть скрытые папки в файловом менеджере, нажмите <kbd>Ctrl</kbd> + <kbd>H</kbd>.
   - При появлении запроса о существующих файлах выберите **"Заменить"** или **"Перезаписать"**.
5. Откройте GIMP — вы увидите новый интерфейс PhotoGIMP! 🎉

<details>
<summary><strong>💡 Используете GIMP, не относящийся к Flatpak?</strong></summary>

Если вы установили GIMP через менеджер пакетов вашего дистрибутива (apt, dnf, pacman и т. д.), а не через Flatpak, папка config находится в том же месте (`~/.config/GIMP/3.0`), поэтому описанные выше шаги по-прежнему работают. Просто убедитесь, что у вас установлена ​​версия GIMP 3.0 или новее.
</details>

---

### 🪟 Windows

<img src="https://skillicons.dev/icons?i=windows" align="right" />

#### Резервное копирование (необязательно)

Если вы хотите сохранить текущие настройки GIMP, сначала сделайте их резервную копию:

1. Нажмите <kbd>Windows</kbd> + <kbd>R</kbd> чтобы открыть диалоговое окно "Выполнить".
2. Введите текст `%APPDATA%\GIMP` и нажмите <kbd>Enter</kbd>.
3. Скопируйте всю `3.0` папку в безопасное место (например, на рабочий стол).

#### Установить

1. Убедитесь, что у вас [установлен GIMP с официального сайта](https://www.gimp.org/downloads/).
2. **Откройте GIMP один раз, а затем закройте его** — это создаст папки конфигурации, необходимые для PhotoGIMP.
3. Скачайте последнюю версию:
   👉 **[Скачать PhotoGIMP для Windows (.zip)](https://github.com/Diolinux/PhotoGIMP/releases/download/3.0/PhotoGIMP.zip)**
4. Распакуйте содержимое `PhotoGIMP.zip` в любую папку (например, на рабочий стол).
5. Откройте извлеченную папку и **скопируйте содержимое `3.0` папки**.
6. Нажмите <kbd>Windows</kbd> + <kbd>R</kbd>, чтобы открыть диалоговое окно "Выполнить".
7. Введите `%APPDATA%\GIMP` и нажмите клавишу <kbd>Enter</kbd> — это откроет папку настроек GIMP.
8. **Вставьте** папку `3.0` сюда.
9. При появлении запроса о существующих файлах выберите **"Заменить файлы в папке назначения"**.
10. Откройте GIMP — вы увидите новый интерфейс PhotoGIMP! 🎉

<details>
<summary><strong>💡 (Необязательно): Измените значок ярлыка GIMP</strong></summary>

Вы также можете скачать [photogimp.ico](https://github.com/Diolinux/PhotoGIMP/releases/download/3.0/photogimp.ico) и обновить значок в ярлыке GIMP, расположенном по адресу:

```
%appdata%\Microsoft\Windows\Start Menu\Programs\GIMP 3.0.0
```

Щелкните правой кнопкой мыши по ярлыку → **Свойства** → **Изменить значок** → найдите загруженный `.ico` файл.
</details>

<details>
<summary><strong>🍫 Установка через Chocolatey (альтернативный вариант)</strong></summary>

Если вы используете [Chocolatey](https://chocolatey.org/), вы можете установить PhotoGIMP одной командой:

```powershell
choco install photogimp
```

Поддерживается: [André Augusto](https://github.com/AndreAugustoDev)
</details>

---

### 🍎 macOS

<img src="https://skillicons.dev/icons?i=macos" align="right" />

#### Резервное копирование (необязательно)

Если вы хотите сохранить текущие настройки GIMP, сначала сделайте их резервную копию:

1. Откройте Finder.
2. Нажмите <kbd>Cmd</kbd> + <kbd>Shift</kbd> + <kbd>G</kbd> и перейдите в `~/Library/Application Support/GIMP`.
3. Скопируйте всю `GIMP` папку в безопасное место (например, на рабочий стол).

#### Установить

1. Убедитесь, что у вас [установлен GIMP с официального сайта](https://www.gimp.org/downloads/).
2. **Откройте GIMP один раз, а затем закройте его** — это создаст папки конфигурации, необходимые для PhotoGIMP.
3. Скачайте последнюю версию:
   👉 **[Скачать PhotoGIMP для macOS (.zip)](https://github.com/Diolinux/PhotoGIMP/releases/download/3.0/PhotoGIMP.zip)**
4. Распакуйте содержимое `PhotoGIMP.zip` в любую папку (например, на рабочий стол).
5. Откройте извлеченную папку и **скопируйте содержимое `3.0` папки**.
6. Откройте Finder, нажмите <kbd>Cmd</kbd> + <kbd>Shift</kbd> + <kbd>G</kbd> чтобы открыть «Переход к папке».
7. Введите `~/Library/Application Support/GIMP` и нажмите <kbd>Enter</kbd>.
8. Если вы видите `2.10` папку от предыдущей установки, **удалите её**, чтобы избежать конфликтов.

9. **Вставьте** папку `3.0` внутрь папки GIMP.
10. При появлении запроса о существующих файлах выберите **"Заменить"** or **"Объединить"**.
11. Откройте GIMP — вы увидите новый интерфейс PhotoGIMP! 🎉

---

## 📦 Что входит в патч

PhotoGIMP заменяет или добавляет следующие файлы в каталог конфигурации GIMP:

| Файл / Папка | Что это делает |
|---|---|
| `shortcutsrc` | Клавиатурные сочетания клавиш настроены в соответствии с настройками Photoshop |
| `toolrc` | Настройки инструментов и порядок их расположения в панели |
| `sessionrc` | Расположение окон и панелей |
| `dockrc` | Конфигурация доков и боковых панелей |
| `gimprc` | Общие настройки GIMP (холст, сетка и т.д.) |
| `contextrc` | Активные настройки контекста инструмента/цвета |
| `splashes/` | Пользовательская заставка PhotoGIMP |
| `theme.css` | Незначительные корректировки темы оформления пользовательского интерфейса |
| `templaterc` | Предварительно заданные шаблоны холста |

В Linux этот патч также устанавливает:
- Пользовательский `.desktop` файл (заставка приложения с названием и значком PhotoGIMP)
- Пользовательская иконка приложения в `~/.local/share/icons/`

---

## 🗑 Как удалить

Чтобы удалить PhotoGIMP и восстановить GIMP до состояния по умолчанию, просто удалите папку config GIMP и снова откройте GIMP — он сгенерирует новые настройки по умолчанию.

### Linux

```bash
rm -rf ~/.config/GIMP/3.0
```

Затем снова откройте GIMP — он создаст совершенно новую конфигурацию по умолчанию.

Если вы ранее создали резервную копию, восстановите её:

```bash
cp -r ~/GIMP-3.0-backup ~/.config/GIMP/3.0
```

### Windows

1. Нажмите <kbd>Windows</kbd> + <kbd>R</kbd>, введите `%APPDATA%\GIMP` и нажмите <kbd>Enter</kbd>.
2. Удалите папку `3.0`.
3. Откройте GIMP — он восстановит настройки по умолчанию.

Или восстановите резервную копию, скопировав папку `3.0` из резервной копии обратно.

### macOS

1. Откройте Finder, нажмите <kbd>Cmd</kbd> + <kbd>Shift</kbd> + <kbd>G</kbd>.
2. Перейдите `~/Library/Application Support/GIMP`.
3. Удалите папку `3.0`.
4. Откройте GIMP — он восстановит настройки по умолчанию.

Или восстановите резервную копию, скопировав папку из резервной копии обратно.

---

## ❓ Устранение неполадок / Часто задаваемые вопросы / FAQ

<details>
<summary><strong>PhotoGIMP ничего не изменил — GIMP выглядит так же.</strong></summary>

- Убедитесь, что вы распаковали файлы в **правильное место**. Самая распространённая ошибка — распаковка в неправильную папку.
- **Linux**: Папки `.config` и `.local` должны находиться в вашей домашней директории (`~`). Они скрыты — нажмите <kbd>Ctrl</kbd> + <kbd>H</kbd> в файловом менеджере, чтобы увидеть их.
- **Windows**: Папка `3.0` должна находиться внутри `%APPDATA%\GIMP`, а не рядом с ней.
- **macOS**: Папка `3.0` должна находиться внутри `~/Library/Application Support/GIMP`.
- Вы **закрыли GIMP** перед тем, как вставить файлы? GIMP может перезаписать входящие настройки при выходе.
</details>

<details>
<summary><strong>После установки PhotoGIMP при открытии GIMP возникает ошибка.</strong></summary>

- Обычно это означает, что версия GIMP не совпадает. PhotoGIMP разработан для **GIMP 3.0+**. Если вы используете GIMP 2.x, совместимость будет нарушена.
- Попробуйте удалить папку config и переустановить программу — см. раздел [Как удалить](#-how-to-uninstall).
</details>

<details>
<summary><strong>Можно ли использовать PhotoGIMP с GIMP 2.10?</strong></summary>

Нет. Эта версия PhotoGIMP разработана исключительно для **GIMP 3.0 и новее**. Формат конфигурации значительно изменился между GIMP 2.x и 3.x.
</details>

<details>
<summary><strong>Удалит ли PhotoGIMP мои пользовательские кисти, шрифты или плагины?</strong></summary>

Нет. PhotoGIMP заменяет только файлы конфигурации (ярлыки, макет, настройки). Ваши личные кисти, шрифты, градиенты и плагины остаются неизменными.
</details>

<details>
<summary><strong>Можно ли настроить сочетания клавиш после установки PhotoGIMP?</strong></summary>

Конечно! PhotoGIMP просто задает отправную точку. Вы можете изменить любую комбинацию клавиш в GIMP через меню **Редактировать → Сочетания клавиш**.
</details>

<details>
<summary><strong>Как обновить PhotoGIMP до новой версии?</strong></summary>

Просто скачайте последнюю версию и повторите шаги установки — это перезапишет предыдущую конфигурацию PhotoGIMP.
</details>

---

## 🤝 Вклад в проект

Обнаружили ошибку? Есть предложение? Будем рады вашей помощи!

- **Сообщить о проблеме**: [Открыть заявку](https://github.com/Diolinux/PhotoGIMP/issues)
- **Отправьте исправление**: [создайте запрос на слияние (pull request).](https://github.com/Diolinux/PhotoGIMP/pulls)
- **Перевод**: Help us translate the README into more languages! See the [Переводы](#-translations).

---

## 🌍 Переводы

Данный файл README доступен на других языках:

- 🇧🇷 [Português (Brazilian Portuguese)](./docs/README_pt.md)
- 🇵🇱 [Polski (Polish)](./docs/README_pl.md)

Хотите добавить свой язык? Создайте форк репозитория, создайте в нём файл`docs/README_xx.md` отправьте запрос на слияние!

---

## 🏆 Авторы

- Этот проект был бы невозможен без замечательной команды [GIMP](https://www.gimp.org/).
- Огромное спасибо всем поклонникам Diolinux на [YouTube](https://youtube.com/Diolinux).
- Заставка и иконки от [Adriel Filipe Design](https://bento.me/adrielfilipedesign).

---

## 👥 Участники

<a align="center" href="https://github.com/Diolinux/PhotoGIMP/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=Diolinux/PhotoGIMP" />
</a>

---

## 📄 Лицензия

PhotoGIMP распространяется под лицензией [GNU General Public License v3.0](./LICENSE).
