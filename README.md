# 🎨 PhotoGIMP

<img src="./.local/share/icons/hicolor/256x256/256x256.png" align="right" alt="أيقونة تطبيق PhotoGIMP" title="أيقونة تطبيق PhotoGIMP">

[![GitHub stars](https://img.shields.io/github/stars/Diolinux/PhotoGIMP?style=social)](https://github.com/Diolinux/PhotoGIMP)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Latest Release](https://img.shields.io/github/v/release/Diolinux/PhotoGIMP)](https://github.com/Diolinux/PhotoGIMP/releases/latest)

**PhotoGIMP** هو حزمة تعديل (patch) مجانية ومجتمعية تُحوّل واجهة برنامج [GIMP](https://www.gimp.org/) إلى تخطيط مألوف لمستخدمي **Adobe Photoshop**. إذا كنت تنتقل من Photoshop إلى GIMP وتريد الشعور بالراحة والاعتياد فوراً، فإن PhotoGIMP صُمم خصيصاً لك.

> **جديد على GIMP؟** برنامج GIMP هو محرر صور مجاني ومفتوح المصدر متاح لأنظمة Linux و macOS و Windows. يمكنه القيام بأغلب المهام التي يقدمها Photoshop — من تعديل الصور، والتركيب، والتصميم الجرافيكي، وغير ذلك الكثير — وكل ذلك مجاناً. يقوم PhotoGIMP فقط بجعله _يبدو ويتصرف_ بشكل أقرب إلى Photoshop.

---

## ✨ المميزات

- **تخطيط أدوات يشبه Photoshop** — تم إعادة تنظيم الأدوات لتماثل المواقع التي اعتادت عليها في Adobe Photoshop.
- **شاشة بدء مخصصة (Splash Screen)** — شاشة بدء فريدة لـ PhotoGIMP ترحب بك عند تشغيل البرنامج.
- **توسيع مساحة العمل** — تم تحسين الإعدادات الافتراضية لمنحك أكبر مساحة عمل ممكنة.
- **اختصارات لوحة مفاتيح Photoshop** — تتبع اختصارات المفاتيح [الوثائق الرسمية لشركة Adobe](https://helpx.adobe.com/photoshop/using/default-keyboard-shortcuts.html) الخاصة بنسخة Windows.
- **أيقونة واسم مخصصان** — يوفر ملف `.desktop` مخصص أيقونة واسم تطبيق خاصين بـ PhotoGIMP في قائمة نظامك.

---

## 📷 لقطات الشاشة

| شاشة البداية | نافذة التطبيق |
|-|-|
| ![[PhotoGIMP Diolinux splash screen]](./.config/GIMP/3.0/splashes/splash-screen-2025-v2.png)<br>شاشة بدء PhotoGIMP Diolinux | ![[PhotoGIMP 3]](./screenshots/photogimp_3_-_diolinux.png)<br>PhotoGIMP 3

---

## 📋 المتطلبات

قبل تثبيت PhotoGIMP، تأكد من توفر ما يلي:

| المتطلب | التفاصيل |
| -------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| **GIMP 3.0 أو أحدث** | التحميل من: [gimp.org](https://www.gimp.org/downloads/) أو [Flathub](https://flathub.org/apps/org.gimp.GIMP) (Linux) |
| **تشغيل GIMP مرة واحدة على الأقل** | يحتاج GIMP إلى إنشاء ملفات الإعدادات الخاصة به قبل أن يتمكن PhotoGIMP من استبدالها. **ثبّت GIMP ← افتحه ← أغلقه ← ثم ثبّت PhotoGIMP.** |

---

## ⚙ كيفية التثبيت

> [!WARNING]
> **قم بأخذ نسخة احتياطية من إعدادات GIMP الحالية قبل التثبيت!** يقوم PhotoGIMP باستبدال ملفات إعدادات GIMP. إذا كانت لديك إعدادات مخصصة تريد الاحتفاظ بها، احفظ نسخة احتياطية أولاً. راجع تعليمات النسخ الاحتياطي في كل قسم أدناه.

---

### 🐧 Flatpak (Linux)

<img src="https://skillicons.dev/icons?i=linux" align="right" width="40" />

#### النسخ الاحتياطي (اختياري)

إذا كنت تريد الاحتفاظ بإعدادات GIMP الحالية، قم بأخذ نسخة احتياطية منها أولاً:

```bash
cp -r ~/.config/GIMP/3.0 ~/GIMP-3.0-backup
```

#### التثبيت

1. تأكد من تثبيت GIMP مسبقاً [من Flathub](https://flathub.org/apps/org.gimp.GIMP).
2. **افتح GIMP مرة واحدة، ثم أغلقه** — هذا ينشئ مجلدات الإعدادات التي يحتاجها PhotoGIMP.
3. قم بتنزيل أحدث إصدار:
   👉 **[تحميل PhotoGIMP لنظام Linux (.zip)](https://github.com/Diolinux/PhotoGIMP/releases/download/3.0/PhotoGIMP-linux.zip)**
4. استخرج ملف `.zip` **داخل مجلد المنزل الخاص بك** (`~`).
   - سيؤدي هذا إلى وضع الملفات داخل `~/.config` و `~/.local`، وهي مجلدات مخفية.
   - لإظهار المجلدات المخفية في مدير الملفات، اضغط على <kbd>Ctrl</kbd> + <kbd>H</kbd>.
   - عند مطالبتك بشأن الملفات الموجودة، اختر **"Replace" (استبدال)** أو **"Overwrite" (إعادة كتابة)**.
5. افتح GIMP — ستلاحظ واجهة PhotoGIMP الجديدة! 🎉

<details>
<summary><strong>💡 هل تستخدم نسق تثبيت آخر غير Flatpak لـ GIMP؟</strong></summary>

إذا قمت بتثبيت GIMP من مدير الحزم الخاص بتوزيعتك (apt, dnf, pacman, إلخ) بدلاً من Flatpak، فإن مجلد الإعدادات يوجد في نفس الموقع (`~/.config/GIMP/3.0`)، لذا فإن الخطوات أعلاه لا تزال تعمل. فقط تأكد من أن لديك إصدار GIMP 3.0 أو أحدث.

</details>

---

### 🪟 Windows

<img src="https://skillicons.dev/icons?i=windows" align="right" />

#### النسخ الاحتياطي (اختياري)

إذا كنت تريد الاحتفاظ بإعدادات GIMP الحالية، قم بأخذ نسخة احتياطية منها أولاً:

1. اضغط على <kbd>Windows</kbd> + <kbd>R</kbd> لفتح نافذة التشغيل (Run).
2. اكتب `%APPDATA%\GIMP` واضغط <kbd>Enter</kbd>.
3. انسخ مجلد `3.0` بالكامل إلى مكان آمن (مثل سطح المكتب).

#### التثبيت

1. تأكد من تثبيت [GIMP من الموقع الرسمي](https://www.gimp.org/downloads/).
2. **افتح GIMP مرة واحدة، ثم أغلقه** — هذا ينشئ مجلدات الإعدادات التي يحتاجها PhotoGIMP.
3. قم بتنزيل أحدث إصدار:
   👉 **[تحميل PhotoGIMP لنظام Windows (.zip)](https://github.com/Diolinux/PhotoGIMP/releases/download/3.0/PhotoGIMP.zip)**
4. استخرج محتويات `PhotoGIMP.zip` إلى أي مجلد (مثل سطح المكتب).
5. افتح المجلد المستخرج و**انسخ مجلد `3.0`**.
6. اضغط على <kbd>Windows</kbd> + <kbd>R</kbd> لفتح نافذة التشغيل (Run).
7. اكتب `%APPDATA%\GIMP` واضغط <kbd>Enter</kbd> — سيفتح هذا مجلد إعدادات GIMP.
8. **الصق** مجلد `3.0` هنا.
9. عند مطالبتك بشأن الملفات الموجودة، اختر **"Replace the files in the destination" (استبدال الملفات في الوجهة)**.
10. افتح GIMP — ستلاحظ واجهة PhotoGIMP الجديدة! 🎉

<details>
<summary><strong>💡 اختياري: تغيير أيقونة اختصار GIMP</strong></summary>

يمكنك أيضاً تنزيل [photogimp.ico](https://github.com/Diolinux/PhotoGIMP/releases/download/3.0/photogimp.ico) وتحديث الأيقونة على اختصار GIMP الموجود في:

```
%appdata%\Microsoft\Windows\Start Menu\Programs\GIMP 3.0.0
```

انقر بزر الماوس الأيمن على الاختصار ← **Properties (خصائص)** ← **Change Icon (تغيير الأيقونة)** ← استعرض للوصول إلى ملف `.ico` الذي قمت بتنزيله.

</details>

<details>
<summary><strong>🍫 التثبيت عبر Chocolatey (طريقة بديلة)</strong></summary>

إذا كنت تستخدم [Chocolatey](https://chocolatey.org/)، يمكنك تثبيت PhotoGIMP بأمر واحد:

```powershell
choco install photogimp
```

صيانة وإدارة: [André Augusto](https://github.com/AndreAugustoDev)

</details>

---

### 🍎 macOS

<img src="https://skillicons.dev/icons?i=macos" align="right" />

#### النسخ الاحتياطي (اختياري)

إذا كنت تريد الاحتفاظ بإعدادات GIMP الحالية، قم بأخذ نسخة احتياطية منها أولاً:

1. افتح تطبيق Finder.
2. اضغط على <kbd>Cmd</kbd> + <kbd>Shift</kbd> + <kbd>G</kbd> وانتقل إلى `~/Library/Application Support/GIMP`.
3. انسخ مجلد `GIMP` بالكامل إلى مكان آمن (مثل سطح المكتب).

#### التثبيت

1. تأكد من تثبيت [GIMP من الموقع الرسمي](https://www.gimp.org/downloads/).
2. **افتح GIMP مرة واحدة، ثم أغلقه** — هذا ينشئ مجلدات الإعدادات التي يحتاجها PhotoGIMP.
3. قم بتنزيل أحدث إصدار:
   👉 **[تحميل PhotoGIMP لنظام macOS (.zip)](https://github.com/Diolinux/PhotoGIMP/releases/download/3.0/PhotoGIMP.zip)**
4. استخرج محتويات `PhotoGIMP.zip` إلى أي مجلد (مثل سطح المكتب).
5. افتح المجلد المستخرج و**انسخ مجلد `3.0`**.
6. افتح Finder، واضغط على <kbd>Cmd</kbd> + <kbd>Shift</kbd> + <kbd>G</kbd> لفتح نافذة "الانتقال إلى المجلد".
7. اكتب `~/Library/Application Support/GIMP` واضغط <kbd>Enter</kbd>.
8. إذا رأيت مجلد باسم `2.10` من تثبيت سابق، **قم بحذفه** لتجنب التعارضات.
9. **الصق** مجلد `3.0` داخل مجلد GIMP.
10. عند مطالبتك بشأن الملفات الموجودة، اختر **"Replace" (استبدال)** أو **"Merge" (دمج)**.
11. افتح GIMP — ستلاحظ واجهة PhotoGIMP الجديدة! 🎉

<details>
<summary><strong>طريقة بديلة: التثبيت باستخدام Terminal</strong></summary>

إذا كان خيار **"Merge"** في Finder يتجاهل الملفات الموجودة تلقائياً، أو إذا كنت تفضل استخدام سطر الأوامر، يمكنك نسخ ملفات PhotoGIMP باستخدام `rsync`.

1. افتح موجه الأوامر (Terminal).
2. قم بتشغيل `rsync` مع استبدال `/path/to/extracted/3.0/` بمسار مجلد `3.0` المستخرج:

   ```bash
   rsync -av --ignore-times /path/to/extracted/3.0/ ~/Library/Application\ Support/GIMP/3.0/
   ```

   تأكد من أن كلا المسارين ينتهيان بـ `/`.
3. إذا كان إصدار GIMP المثبت لديك يستخدم مجلد إصدار مختلف، فقم بتغيير الوجهة لتطابقه (على سبيل المثال، استخدم `~/Library/Application\ Support/GIMP/3.2/` لإصدار GIMP 3.2).

</details>

---

## 📦 محتويات حزمة التعديل

يقوم PhotoGIMP باستبدال أو إضافة الملفات التالية في مجلد إعدادات GIMP:

| الملف / المجلد | وظيفته |
| ------------- | --------------------------------------------- |
| `shortcutsrc` | اختصارات لوحة المفاتيح المجهزة لتطابق Photoshop |
| `toolrc` | إعدادات وترتيب الأدوات |
| `sessionrc` | تخطيط النوافذ ومواضع اللوحات |
| `dockrc` | إعدادات اللوحات والأرصفة (Docks) |
| `gimprc` | تفضيلات GIMP العامة (مساحة العمل، الشبكة، إلخ) |
| `contextrc` | إعدادات سياق الأدوات والألوان النشطة |
| `splashes/` | شاشة بدء مخصصة لـ PhotoGIMP |
| `theme.css` | تعديلات بسيطة على مظهر الواجهة |
| `templaterc` | قوالب جاهزة ومحددة مسبقاً لمساحة العمل |

على نظام Linux، يتضمن التعديل أيضاً:

- ملف `.desktop` مخصص (مشغل تطبيق باسم وأيقونة PhotoGIMP)
- أيقونة تطبيق مخصصة في `~/.local/share/icons/`

---

## 🗑 كيفية إلغاء التثبيت

لإزالة PhotoGIMP وإعادة GIMP إلى حالته الافتراضية، قم ببساطة بحذف مجلد إعدادات GIMP وافتح GIMP مرة أخرى — وسيتم إعادة إنشاء الإعدادات الافتراضية تلقائياً.

### Linux

```bash
rm -rf ~/.config/GIMP/3.0
```

ثم افتح GIMP مجدداً — وسيتم إنشاء إعدادات افتراضية جديدة تماماً.

إذا قمت بعمل نسخة احتياطية سابقاً، قم باستعادتها بدلاً من ذلك:

```bash
cp -r ~/GIMP-3.0-backup ~/.config/GIMP/3.0
```

### Windows

1. اضغط على <kbd>Windows</kbd> + <kbd>R</kbd>، واكتب `%APPDATA%\GIMP` واضغط <kbd>Enter</kbd>.
2. احذف مجلد `3.0`.
3. افتح GIMP — وسيتم إعادة إنشاء الإعدادات الافتراضية.

أو قم باستعادة النسخة الاحتياطية عن طريق لصق مجلد `3.0` المنسوخ سابقاً.

### macOS

1. افتح Finder، واضغط على <kbd>Cmd</kbd> + <kbd>Shift</kbd> + <kbd>G</kbd>.
2. انتقل إلى `~/Library/Application Support/GIMP`.
3. احذف مجلد `3.0`.
4. افتح GIMP — وسيتم إعادة إنشاء الإعدادات الافتراضية.

أو قم باستعادة النسخة الاحتياطية عن طريق لصق المجلد المنسوخ سابقاً.

---

## ❓ استكشاف الأخطاء وإصلاحها / الأسئلة الشائعة

> [!CAUTION]
> **ليس لـ PhotoGIMP أي موقع إلكتروني رسمي.** المصدر الرسمي الوحيد للمشروع هو مستودع GitHub الخاص به: https://github.com/Diolinux/PhotoGIMP/

<details>
<summary><strong>لم يتغير أي شيء في PhotoGIMP — مظهر GIMP ما زال كما هو</strong></summary>

- تأكد من استخراج الملفات إلى **الموقع الصحيح**. الخطأ الأكثر شيوعاً هو الاستخراج إلى المجلد الخاطئ.
- **Linux**: يجب أن تكون مجلدات `.config` و `.local` داخل مجلد المنزل الخاص بك (`~`). وهي مجلدات مخفية — اضغط على <kbd>Ctrl</kbd> + <kbd>H</kbd> في مدير الملفات لإظهارها.
- **Windows**: يجب أن يكون مجلد `3.0` داخل `%APPDATA%\GIMP` وليس بجواره.
- **macOS**: يجب أن يكون مجلد `3.0` داخل `~/Library/Application Support/GIMP`.
- هل قمت **بإغلاق GIMP** قبل لصق الملفات؟ قد يقوم GIMP بإعادة كتابة الإعدادات الحالية عند الخروج.
</details>

<details>
<summary><strong>يظهر لي خطأ عند فتح GIMP بعد تثبيت PhotoGIMP</strong></summary>

- يعني هذا عادةً أن إصدار GIMP غير متوافق. PhotoGIMP مصمم لإصدار **GIMP 3.0+**. إذا كنت تشغل إصدار GIMP 2.x، فلن يكون متوافقاً.
- جرب حذف مجلد الإعدادات وإعادة التثبيت — راجع قسم [كيفية إلغاء التثبيت](#-كيفية-إلغاء-التثبيت).
</details>

<details>
<summary><strong>هل يمكنني استخدام PhotoGIMP مع GIMP 2.10؟</strong></summary>

لا. هذا الإصدار من PhotoGIMP مصمم حصرياً لإصدار **GIMP 3.0 وما فوق**. فقد تغيرت صيغ وقواعد الإعدادات بشكل كبير بين إصدارات GIMP 2.x و 3.x.

</details>

<details>
<summary><strong>هل سيقوم PhotoGIMP بحذف الفرش المخصصة أو الخطوط أو الملحقات (Plug-ins) الخاصة بي؟</strong></summary>

لا. يقوم PhotoGIMP باستبدال ملفات الإعدادات فقط (الاختصارات، التخطيط، التفضيلات). بينما تظل الفرش والخطوط والتدرجات والملحقات الشخصية كما هي دون تغيير.

</details>

<details>
<summary><strong>هل يمكنني تخصيص الاختصارات بعد تثبيت PhotoGIMP؟</strong></summary>

بالتأكيد! يحدد PhotoGIMP نقطة البداية فقط. يمكنك تغيير أي اختصار في GIMP من خلال **تعديل ← اختصارات لوحة المفاتيح (Edit → Keyboard Shortcuts)**.

</details>

<details>
<summary><strong>كيف أقوم بتحديث PhotoGIMP إلى إصدار جديد؟</strong></summary>

فقط قم بتنزيل أحدث إصدار واتبع خطوات التثبيت مرة أخرى — وسيتم استبدال إعدادات PhotoGIMP السابقة.

</details>

---

## 🤝 المساهمة

هل وجدت خطأً؟ لديك اقتراح؟ يسعدنا مساعدتك!

- **الإبلاغ عن مشكلة**: [افتح مشكلة (Issue)](https://github.com/Diolinux/PhotoGIMP/issues)
- **إرسال إصلاح**: [أنشئ طلب سحب (Pull Request)](https://github.com/Diolinux/PhotoGIMP/pulls)
- **الترجمة**: ساعدنا في ترجمة README إلى المزيد من اللغات! راجع قسم [الترجمات](#-الترجمات).

---

## 🌍 الترجمات

ملف README هذا متاح بلغات أخرى:

- 🇮🇹 [Italiano (الإيطالية)](./docs/README_it.md)
- 🇵🇱 [Polski (البولندية)](./docs/README_pl.md)
- 🇺🇦 [Українська (الأوكرانية)](./docs/README_ua.md)
- 🇧🇷 [Português (البرتغالية البرازيلية)](./docs/README_pt.md)
- 🇷🇺 [Русский (الروسية)](./docs/README_ru.md)
- 🇪🇸 [Español (الإسبانية)](./docs/README_es.md)
- 🇮🇱 [עברית (العبرية)](https://github.com/Diolinux/PhotoGIMP/blob/master/docs/README_he.md)      (FREE PALESTINE)
- 🇰🇷 [Korean (الكورية)](./docs/README_ko.md)
- 🇨🇳 [简体中文 (الصينية المبسطة)](./docs/README_zh.md)

هل تريد إضافة لغتك؟ قم بعمل Fork للمستودع، وأنشر ملف `docs/README_xx.md` ثم أرسل طلب سحب (Pull Request)!

---

## 🏆 الشكر والتقدير

- لم يكن هذا المشروع ممكناً لولا فريق [GIMP](https://www.gimp.org/) الرائع.
- شكر جزيل لكل داعمي Diolinux على [YouTube](https://youtube.com/Diolinux).
- شاشة البداية والأيقونات من تصميم [Adriel Filipe Design](https://bento.me/adrielfilipedesign).

---

## 👥 المساهمون

<a align="center" href="https://github.com/Diolinux/PhotoGIMP/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=Diolinux/PhotoGIMP" />
</a>

---

## 📄 الترخيص

تخضع حزمة PhotoGIMP لرخصة [GNU General Public License v3.0](./LICENSE).
