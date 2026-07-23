# 🎨 PhotoGIMP

<img src="./.local/share/icons/hicolor/256x256/256x256.png" align="right" alt="أيقونة تطبيق PhotoGIMP" title="أيقونة تطبيق PhotoGIMP">

[![GitHub stars](https://img.shields.io/github/stars/Diolinux/PhotoGIMP?style=social)](https://github.com/Diolinux/PhotoGIMP)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Latest Release](https://img.shields.io/github/v/release/Diolinux/PhotoGIMP)](https://github.com/Diolinux/PhotoGIMP/releases/latest)

**PhotoGIMP** هو حزمة تعديل (patch) مجانية ومجتمعية تحوّل واجهة [GIMP](https://www.gimp.org/) (GNU Image Manipulation Program) إلى تخطيط مألوف لمستخدمي **Adobe Photoshop**. إذا كنت تنتقل من Photoshop إلى GIMP وتريد الشعور بالراحة والاعتياد فوراً، فإن PhotoGIMP مصمم لأجلك.

> **جديد على GIMP؟** برنامج GIMP هو محرر صور مجاني ومفتوح المصدر متاح لأنظمة Linux و macOS و Windows. يمكنه القيام بصلب ما يفعله Photoshop — من تعديل الصور، والتركيب، والتصميم الجرافيكي، وغير ذلك الكثير — وكل ذلك مجاناً. يقوم PhotoGIMP فقط بجعله _يبدو ويتصرف_ بشكل أقرب إلى Photoshop.

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
