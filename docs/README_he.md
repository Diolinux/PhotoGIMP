# 🎨 PhotoGIMP

> תרגום: [ליאור בלול](https://lior-ai.com) | lior_Ai

<img src="../.local/share/icons/hicolor/256x256/256x256.png" align="right" alt="סמל היישום PhotoGIMP" title="סמל היישום PhotoGIMP">

[![GitHub stars](https://img.shields.io/github/stars/Diolinux/PhotoGIMP?style=social)](https://github.com/Diolinux/PhotoGIMP)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Latest Release](https://img.shields.io/github/v/release/Diolinux/PhotoGIMP)](https://github.com/Diolinux/PhotoGIMP/releases/latest)

**PhotoGIMP** היא הרחבה (patch) חינמית, מבוססת קהילה, שהופכת את [GIMP](https://www.gimp.org/) (GNU Image Manipulation Program) לסביבת עבודה שמרגישה מוכרת למשתמשי **Adobe Photoshop**. אם אתם עוברים מ‑Photoshop ל‑GIMP ורוצים להרגיש בבית כבר מהרגע הראשון — PhotoGIMP נוצרה בשבילכם.

> **חדשים ב‑GIMP?** ‏GIMP הוא עורך תמונות חינמי וקוד פתוח, הזמין ל‑Linux, ל‑macOS ול‑Windows. הוא יודע לעשות כמעט כל מה ש‑Photoshop יודע — ריטוש תמונות, הרכבת תמונות, עיצוב גרפי ועוד — והכול בחינם. ‏PhotoGIMP פשוט גורמת לו *להיראות ולהתנהג* יותר כמו Photoshop.

---

## ✨ יכולות

- **פריסת כלים בסגנון Photoshop** — הכלים מסודרים מחדש כדי לחקות את המיקומים שאתם רגילים אליהם ב‑Adobe Photoshop.
- **מסך פתיחה מותאם אישית** — מסך פתיחה (Splash Screen) ייחודי של PhotoGIMP מקבל אתכם בעת ההפעלה.
- **שטח עבודה מוגדל** — הגדרות ברירת המחדל מכוונות כדי להעניק לכם את שטח העבודה הגדול ביותר האפשרי.
- **קיצורי מקלדת של Photoshop** — קיצורי המקלדת עוקבים אחר [התיעוד הרשמי של Adobe](https://helpx.adobe.com/photoshop/using/default-keyboard-shortcuts.html) עבור גרסת Windows.
- **סמל ושם מותאמים אישית** — קובץ `.desktop` ייעודי מעניק ל‑PhotoGIMP סמל ושם יישום משלה בתפריט המערכת.

---

## 📷 צילומי מסך

<p>
  <img src="../.config/GIMP/3.0/splashes/splash-screen-2025-v2.png" alt="PhotoGIMP Diolinux Splash Art">
  <em>מסך הפתיחה של PhotoGIMP מבית Diolinux</em>
</p>

<p>
  <img src="../screenshots/photogimp_3_-_diolinux.png" alt="PhotoGIMP 3">
  <em>‏GIMP 3.0 עם הרחבת PhotoGIMP מותקנת</em>
</p>

---

## 📋 דרישות

לפני התקנת PhotoGIMP, ודאו שברשותכם:

| דרישה | פרטים |
|---|---|
| **GIMP 3.0 ומעלה** | להורדה מ: [gimp.org](https://www.gimp.org/downloads/) או [Flathub](https://flathub.org/apps/org.gimp.GIMP) (ל‑Linux) |
| **הפעלת GIMP לפחות פעם אחת** | ‏GIMP צריך לייצר את קובצי התצורה שלו לפני ש‑PhotoGIMP יכולה לדרוס אותם. **התקינו את GIMP ← פתחו אותו ← סגרו אותו ← ורק אז התקינו את PhotoGIMP.** |

---

## ⚙ איך מתקינים

> [!WARNING]
> **גבו את הגדרות ה‑GIMP הנוכחיות שלכם לפני ההתקנה!** ‏PhotoGIMP דורסת את קובצי התצורה של GIMP. אם יש לכם הגדרות מותאמות אישית שברצונכם לשמור, צרו קודם עותק גיבוי. ראו את הוראות הגיבוי בכל אחת מהמדריכים למטה.

---

### 🐧 Flatpak (Linux)

<img src="https://skillicons.dev/icons?i=linux" align="right" width="40" />

#### גיבוי (אופציונלי)

אם ברצונכם לשמור על הגדרות ה‑GIMP הנוכחיות, גבו אותן קודם:

```bash
cp -r ~/.config/GIMP/3.0 ~/GIMP-3.0-backup
```

#### התקנה

1. ודאו ש‑GIMP כבר מותקן אצלכם [מ‑Flathub](https://flathub.org/apps/org.gimp.GIMP).
2. **פתחו את GIMP פעם אחת ואז סגרו אותו** — פעולה זו יוצרת את תיקיות התצורה ש‑PhotoGIMP זקוקה להן.
3. הורידו את הגרסה האחרונה:
   👈 **[הורדת PhotoGIMP ל‑Linux‏ (.zip)](https://github.com/Diolinux/PhotoGIMP/releases/download/3.0/PhotoGIMP-linux.zip)**
4. חלצו את קובץ ה‑`.zip` **אל תוך תיקיית הבית שלכם** (`~`).
   - פעולה זו תניח קבצים בתוך `~/.config` ו‑`~/.local`, שהן תיקיות מוסתרות.
   - כדי לראות תיקיות מוסתרות במנהל הקבצים, לחצו <kbd>Ctrl</kbd> + <kbd>H</kbd>.
   - כאשר תישאלו לגבי קבצים קיימים, בחרו **"Replace"** (החלף) או **"Overwrite"** (דרוס).
5. פתחו את GIMP — אמורה להופיע פריסת PhotoGIMP החדשה! 🎉

<details>
<summary><strong>💡 משתמשים ב‑GIMP שאינו מ‑Flatpak?</strong></summary>

אם התקנתם את GIMP ממנהל החבילות של ההפצה שלכם (apt, dnf, pacman וכו') במקום מ‑Flatpak, תיקיית התצורה נמצאת באותו מיקום (`~/.config/GIMP/3.0`), כך שהשלבים שלמעלה עדיין תקפים. פשוט ודאו שברשותכם GIMP בגרסה 3.0 ומעלה.
</details>

---

### 🪟 Windows

<img src="https://skillicons.dev/icons?i=windows" align="right" />

#### גיבוי (אופציונלי)

אם ברצונכם לשמור על הגדרות ה‑GIMP הנוכחיות, גבו אותן קודם:

1. לחצו <kbd>Windows</kbd> + <kbd>R</kbd> כדי לפתוח את חלון ההרצה (Run).
2. הקלידו `%APPDATA%\GIMP` והקישו <kbd>Enter</kbd>.
3. העתיקו את כל תיקיית `3.0` למקום בטוח (למשל, לשולחן העבודה).

#### התקנה

1. ודאו שברשותכם [GIMP מותקן מהאתר הרשמי](https://www.gimp.org/downloads/).
2. **פתחו את GIMP פעם אחת ואז סגרו אותו** — פעולה זו יוצרת את תיקיות התצורה ש‑PhotoGIMP זקוקה להן.
3. הורידו את הגרסה האחרונה:
   👈 **[הורדת PhotoGIMP ל‑Windows‏ (.zip)](https://github.com/Diolinux/PhotoGIMP/releases/download/3.0/PhotoGIMP.zip)**
4. חלצו את תוכן הקובץ `PhotoGIMP.zip` לכל תיקייה שהיא (למשל, לשולחן העבודה).
5. פתחו את התיקייה שחולצה **והעתיקו את תיקיית `3.0`**.
6. לחצו <kbd>Windows</kbd> + <kbd>R</kbd> כדי לפתוח את חלון ההרצה (Run).
7. הקלידו `%APPDATA%\GIMP` והקישו <kbd>Enter</kbd> — פעולה זו פותחת את תיקיית ההגדרות של GIMP.
8. **הדביקו** כאן את תיקיית `3.0`.
9. כאשר תישאלו לגבי קבצים קיימים, בחרו **"Replace the files in the destination"** (החלף את הקבצים ביעד).
10. פתחו את GIMP — אמורה להופיע פריסת PhotoGIMP החדשה! 🎉

<details>
<summary><strong>💡 אופציונלי: שינוי סמל קיצור הדרך של GIMP</strong></summary>

ניתן גם להוריד את [photogimp.ico](https://github.com/Diolinux/PhotoGIMP/releases/download/3.0/photogimp.ico) ולעדכן את הסמל של קיצור הדרך ל‑GIMP הנמצא בנתיב:

```
%appdata%\Microsoft\Windows\Start Menu\Programs\GIMP 3.0.0
```

לחצו לחיצה ימנית על קיצור הדרך ← **Properties** (מאפיינים) ← **Change Icon** (שינוי סמל) ← נווטו לקובץ ה‑`.ico` שהורדתם.
</details>

<details>
<summary><strong>🍫 התקנה באמצעות Chocolatey (חלופה)</strong></summary>

אם אתם משתמשים ב‑[Chocolatey](https://chocolatey.org/), ניתן להתקין את PhotoGIMP בפקודה אחת:

```powershell
choco install photogimp
```

מתוחזק על ידי: [André Augusto](https://github.com/AndreAugustoDev)
</details>

---

### 🍎 macOS

<img src="https://skillicons.dev/icons?i=macos" align="right" />

#### גיבוי (אופציונלי)

אם ברצונכם לשמור על הגדרות ה‑GIMP הנוכחיות, גבו אותן קודם:

1. פתחו את Finder.
2. לחצו <kbd>Cmd</kbd> + <kbd>Shift</kbd> + <kbd>G</kbd> ועברו אל `~/Library/Application Support/GIMP`.
3. העתיקו את כל תיקיית `GIMP` למקום בטוח (למשל, לשולחן העבודה).

#### התקנה

1. ודאו שברשותכם [GIMP מותקן מהאתר הרשמי](https://www.gimp.org/downloads/).
2. **פתחו את GIMP פעם אחת ואז סגרו אותו** — פעולה זו יוצרת את תיקיות התצורה ש‑PhotoGIMP זקוקה להן.
3. הורידו את הגרסה האחרונה:
   👈 **[הורדת PhotoGIMP ל‑macOS‏ (.zip)](https://github.com/Diolinux/PhotoGIMP/releases/download/3.0/PhotoGIMP.zip)**
4. חלצו את תוכן הקובץ `PhotoGIMP.zip` לכל תיקייה שהיא (למשל, לשולחן העבודה).
5. פתחו את התיקייה שחולצה **והעתיקו את תיקיית `3.0`**.
6. פתחו את Finder, לחצו <kbd>Cmd</kbd> + <kbd>Shift</kbd> + <kbd>G</kbd> כדי לפתוח את "Go to Folder" (מעבר לתיקייה).
7. הקלידו `~/Library/Application Support/GIMP` והקישו <kbd>Enter</kbd>.
8. אם אתם רואים תיקיית `2.10` מהתקנה קודמת, **מחקו אותה** כדי למנוע התנגשויות.
9. **הדביקו** את תיקיית `3.0` בתוך תיקיית ה‑GIMP.
10. כאשר תישאלו לגבי קבצים קיימים, בחרו **"Replace"** (החלף) או **"Merge"** (מזג).
11. פתחו את GIMP — אמורה להופיע פריסת PhotoGIMP החדשה! 🎉

---

## 📦 מה יש בתוך ההרחבה

‏PhotoGIMP מחליפה או מוסיפה את הקבצים הבאים בתיקיית התצורה של GIMP:

| קובץ / תיקייה | מה זה עושה |
|---|---|
| `shortcutsrc` | קיצורי מקלדת ממופים כך שיתאימו ל‑Photoshop |
| `toolrc` | הגדרות וסידור הכלים |
| `sessionrc` | פריסת החלונות ומיקומי הפאנלים |
| `dockrc` | הגדרות העגינה (Dock) / הפאנלים |
| `gimprc` | העדפות GIMP כלליות (בד ציור, רשת וכו') |
| `contextrc` | הגדרות ההקשר של הכלי/הצבע הפעילים |
| `splashes/` | מסך הפתיחה המותאם של PhotoGIMP |
| `theme.css` | התאמות עיצוב קלות בממשק המשתמש |
| `templaterc` | תבניות בד ציור מוגדרות מראש |

ב‑Linux, ההרחבה מתקינה בנוסף:
- קובץ `.desktop` מותאם אישית (מפעיל יישום עם השם והסמל של PhotoGIMP)
- סמל יישום מותאם אישית בתוך `~/.local/share/icons/`

---

## 🗑 איך מסירים את ההתקנה

כדי להסיר את PhotoGIMP ולהחזיר את GIMP למצב ברירת המחדל, פשוט מחקו את תיקיית התצורה של GIMP ופתחו אותו מחדש — הוא ייצר הגדרות ברירת מחדל חדשות ונקיות.

### Linux

```bash
rm -rf ~/.config/GIMP/3.0
```

לאחר מכן פתחו שוב את GIMP — הוא ייצור תצורת ברירת מחדל חדשה לגמרי.

אם יצרתם גיבוי קודם לכן, שחזרו אותו במקום זאת:

```bash
cp -r ~/GIMP-3.0-backup ~/.config/GIMP/3.0
```

### Windows

1. לחצו <kbd>Windows</kbd> + <kbd>R</kbd>, הקלידו `%APPDATA%\GIMP` והקישו <kbd>Enter</kbd>.
2. מחקו את תיקיית `3.0`.
3. פתחו את GIMP — הוא ייצור מחדש את הגדרות ברירת המחדל.

לחלופין, שחזרו את הגיבוי שלכם על ידי הדבקת תיקיית `3.0` המגובה בחזרה.

### macOS

1. פתחו את Finder, לחצו <kbd>Cmd</kbd> + <kbd>Shift</kbd> + <kbd>G</kbd>.
2. עברו אל `~/Library/Application Support/GIMP`.
3. מחקו את תיקיית `3.0`.
4. פתחו את GIMP — הוא ייצור מחדש את הגדרות ברירת המחדל.

לחלופין, שחזרו את הגיבוי שלכם על ידי הדבקת התיקייה המגובה בחזרה.

---

## ❓ פתרון תקלות / שאלות נפוצות

> [!CAUTION]
> **ל‑PhotoGIMP אין אתר רשמי.** המקור הרשמי היחיד של הפרויקט הוא מאגר ה‑GitHub שלו: https://github.com/Diolinux/PhotoGIMP/

<details>
<summary><strong>‏PhotoGIMP לא שינתה כלום — GIMP נראה בדיוק אותו הדבר</strong></summary>

- ודאו שחילצתם את הקבצים **למיקום הנכון**. הטעות הנפוצה ביותר היא חילוץ לתיקייה שגויה.
- **Linux**: התיקיות `.config` ו‑`.local` חייבות להיות בתיקיית הבית שלכם (`~`). הן מוסתרות — לחצו <kbd>Ctrl</kbd> + <kbd>H</kbd> במנהל הקבצים כדי לראות אותן.
- **Windows**: תיקיית `3.0` חייבת להיות **בתוך** `%APPDATA%\GIMP`, ולא לצידה.
- **macOS**: תיקיית `3.0` חייבת להיות בתוך `~/Library/Application Support/GIMP`.
- האם **סגרתם את GIMP** לפני הדבקת הקבצים? ‏GIMP עלול לדרוס הגדרות נכנסות בעת היציאה.
</details>

<details>
<summary><strong>אני מקבל שגיאה בעת פתיחת GIMP אחרי התקנת PhotoGIMP</strong></summary>

- בדרך כלל זה אומר שגרסת ה‑GIMP אינה תואמת. ‏PhotoGIMP נבנתה עבור **GIMP 3.0 ומעלה**. אם אתם מריצים GIMP 2.x, היא לא תהיה תואמת.
- נסו למחוק את תיקיית התצורה ולהתקין מחדש — ראו את הסעיף [איך מסירים את ההתקנה](#-איך-מסירים-את-ההתקנה).
</details>

<details>
<summary><strong>אפשר להשתמש ב‑PhotoGIMP עם GIMP 2.10?</strong></summary>

לא. גרסה זו של PhotoGIMP מיועדת אך ורק ל‑**GIMP 3.0 ומעלה**. מבנה קובצי התצורה השתנה באופן משמעותי בין GIMP 2.x ל‑3.x.
</details>

<details>
<summary><strong>האם PhotoGIMP תמחק את המברשות, הגופנים או התוספים המותאמים שלי?</strong></summary>

לא. ‏PhotoGIMP מחליפה רק קובצי תצורה (קיצורים, פריסה, העדפות). המברשות, הגופנים, המעברי‑הצבע (gradients) והתוספים האישיים שלכם נשארים ללא שינוי.
</details>

<details>
<summary><strong>אפשר להתאים אישית את הקיצורים אחרי התקנת PhotoGIMP?</strong></summary>

בהחלט! ‏PhotoGIMP רק מגדירה נקודת פתיחה. ניתן לשנות כל קיצור ב‑GIMP דרך **Edit ← Keyboard Shortcuts** (עריכה ← קיצורי מקלדת).
</details>

<details>
<summary><strong>איך מעדכנים את PhotoGIMP לגרסה חדשה?</strong></summary>

פשוט הורידו את הגרסה האחרונה ובצעו שוב את שלבי ההתקנה — היא תדרוס את תצורת PhotoGIMP הקודמת.
</details>

---

## 🤝 תרומה לפרויקט

מצאתם באג? יש לכם הצעה? נשמח לעזרתכם!

- **דיווח על תקלה**: [פתחו issue](https://github.com/Diolinux/PhotoGIMP/issues)
- **הגשת תיקון**: [צרו pull request](https://github.com/Diolinux/PhotoGIMP/pulls)
- **תרגום**: עזרו לנו לתרגם את ה‑README לשפות נוספות! ראו את סעיף [התרגומים](#-תרגומים).

---

## 🌍 תרגומים

קובץ README זה זמין בשפות נוספות:

- 🇮🇹 [Italiano (איטלקית)](./README_it.md)
- 🇵🇱 [Polski (פולנית)](./README_pl.md)
- 🇺🇦 [Українська (אוקראינית)](./README_ua.md)
- 🇧🇷 [Português (פורטוגזית ברזילאית)](./README_pt.md)
- 🇷🇺 [Русский (רוסית)](./README_ru.md)
- 🇮🇱 [עברית (Hebrew)](./README_he.md)

רוצים להוסיף את השפה שלכם? עשו fork למאגר, צרו קובץ `docs/README_xx.md` והגישו pull request!

---

## 🏆 קרדיטים

- הפרויקט הזה לא היה מתאפשר ללא צוות ה‑[GIMP](https://www.gimp.org/) המדהים.
- תודה ענקית לכל התומכים של Diolinux ב‑[YouTube](https://youtube.com/Diolinux).
- מסך הפתיחה והסמלים מאת [Adriel Filipe Design](https://bento.me/adrielfilipedesign).

---

## 👥 תורמים

<a align="center" href="https://github.com/Diolinux/PhotoGIMP/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=Diolinux/PhotoGIMP" />
</a>

---

## 📄 רישיון

‏PhotoGIMP מופצת תחת רישיון [GNU General Public License v3.0](../LICENSE).
