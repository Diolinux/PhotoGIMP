# 🎨 PhotoGIMP

<img src="./.local/share/icons/hicolor/256x256/256x256.png" align="right" alt="PhotoGIMP application icon" title="PhotoGIMP application icon">

[![GitHub stars](https://img.shields.io/github/stars/Diolinux/PhotoGIMP?style=social)](https://github.com/Diolinux/PhotoGIMP)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Latest Release](https://img.shields.io/github/v/release/Diolinux/PhotoGIMP)](https://github.com/Diolinux/PhotoGIMP/releases/latest)

**PhotoGIMP**는 무료 커뮤니티 기반 패치로 [GIMP](https://www.gimp.org/) (GNU 이미지 조작 프로그램)를 **Adobe Photoshop** 사용자에게 친숙하게 느껴지는 레이아웃으로 변환합니다. Photoshop에서 GIMP로 전환하고 즉시 집에서 편안함을 느끼고 싶다면 PhotoGIMP가 좋습니다.

> **GIMP가 처음이신가요?** GIMP는 Linux, macOS, Windows에서 사용할 수 있는 무료 오픈 소스 이미지 편집기입니다. 사진 보정, 이미지 합성, 그래픽 디자인 등 Photoshop이 할 수 있는 대부분의 작업을 무료로 수행할 수 있습니다 — PhotoGIMP는 Photoshop 처럼 *보이게 하고 더 느낌*을 줍니다.

---

## ✨ 기능

- **Photoshop과 유사한 도구 배치** — Adobe Photoshop에서 익숙한 위치를 모방하도록 도구가 재구성되었습니다.
- **사용자 지정 시작 화면** — 독특한 PhotoGIMP 시작 화면이 시작 시 여러분을 맞이합니다.
- **최대화된 캔버스 공간** — 기본 설정은 가능한 최대 작업 공간을 제공하도록 최적화되어 있습니다.
- **Photoshop 키보드 단축키** — 키보드 단축키는 [Adobe 공식 문서](https://helpx.adobe.com/photoshop/using/default-keyboard-shortcuts.html)에서 Windows 버전을 확인할 수 있습니다.
- **사용자 지정 아이콘 및 이름** — 전용 `.desktop` 파일은 시스템 메뉴에서 PhotoGIMP 자체 아이콘과 앱 이름을 제공합니다.

---

## 📷 스크린샷

<p>
  <img src="./.config/GIMP/3.0/splashes/splash-screen-2025-v2.png" alt="PhotoGIMP Diolinux Splash Art">
  <em>PhotoGIMP Diolinux 시작 아트</em>
</p>

<p>
  <img src="./screenshots/photogimp_3_-_diolinux.png" alt="PhotoGIMP 3">
  <em>PhotoGIMP 패치가 적용된 GIMP 3.0</em>
</p>

---

## 📋 요구 사항

PhotoGIMP를 설치하기 전에 반드시 설치해야 합니다:

| 요구 사항 | 세부 사항 |
|---|---|
| **GIMP 3.0 이상** | 다운로드 위치: [gimp.org](https://www.gimp.org/downloads/) 또는 [Flathub](https://flathub.org/apps/org.gimp.GIMP) (Linux) |
| **GIMP를 한 번 이상 실행** | GIMP는 PhotoGIMP가 해당 파일을 덮어쓰려면 먼저 구성 파일을 생성해야 합니다. **GIMP 설치 → 열기 → 닫기 → 그런 다음 PhotoGIMP를 설치합니다.** |

---

## ⚙ 설치하는 방법

> [!경고]
> **설치하기 전에 현재 GIMP 설정을 백업하세요!** PhotoGIMP는 GIMP의 구성 파일을 덮어씁니다. 유지하려는 사용자 지정 설정이 있는 경우 먼저 백업 사본을 저장하세요. 아래 각 섹션의 백업 지침을 참조하세요.

---

### 🐧 Flatpak (Linux)

<img src="https://skillicons.dev/icons?i=linux" align="right" width="40" />

#### 백업 (선택 사항)

현재 GIMP 설정을 유지하려면 먼저 백업하세요:

```bash
cp -r ~/.config/GIMP/3.0 ~/GIMP-3.0-backup
```

#### 설치

1. [Flathub에서](https://flathub.org/apps/org.gimp.GIMP) GIMP가 이미 설치되어 있는지 확인합니다.
2. **GIMP를 한 번 연 다음 닫습니다** — 이렇게 하면 PhotoGIMP에 필요한 구성 폴더가 생성됩니다.
3. 최신 릴리스 다운로드:
   👉 **[Linux용 PhotoGIMP 다운로드 (.zip)](https://github.com/Diolinux/PhotoGIMP/releases/download/3.0/PhotoGIMP-linux.zip)**
4. `.zip` 파일을 **홈 폴더** (`~`에 추출합니다).
   - 이렇게 하면 파일이 숨겨진 폴더인 `~/.config` 및 `~/.local`에 배치됩니다.
   - 파일 관리자에서 숨겨진 폴더를 보려면 <kbd>Ctrl</kbd> + <kbd>H</kbd>를 누릅니다.
   - 기존 파일에 대한 메시지가 나타나면 **"교체"** 또는 **"덮어쓰기"**를 선택합니다.
5. GIMP 열기 - 새로운 PhotoGIMP 레이아웃을 확인할 수 있습니다! 🎉

<details>
<summary><strong>💡 Flatpak이 아닌 GIMP를 사용하고 계신가요?</strong></summary>

배포자의 패키지 관리자 (apt, dnf, pacman 등)에서 GIMP를 Flatpak 대신 설치한 경우 구성 폴더가 동일한 위치 (`~/.config/GIMP/3.0`)에 있으므로 위의 단계는 계속 작동합니다. GIMP 버전 3.0 이상이 있는지 확인하기만 하면 됩니다.
</details>

---

### 🪟 Windows

<img src="https://skillicons.dev/icons?i=windows" align="right" />

#### 백업 (선택 사항)

현재 GIMP 설정을 유지하려면 먼저 백업하세요:

1. 실행 대화 상자를 열려면 <kbd>Windows</kbd> + <kbd>R</kbd>를 누릅니다.
2. Type `%APPDATA%\GIMP`를 입력하고 <kbd>Enter</kbd>를 누릅니다.
3. 전체 `3.0` 폴더를 안전한 위치 (예: 바탕 화면)에 복사합니다.

#### 설치

1. [공식 웹사이트에서 GIMP를 설치](https://www.gimp.org/downloads/)했는지 획인하세요.
2. **GIMP를 한 번 연 다음 닫기** — 이렇게 하면 PhotoGIMP에 필요한 구성 폴더가 생성됩니다.
3. 최신 릴리스 다운로드:
   👉 **[Windows용 PhotoGIMP 다운로드 (.zip)](https://github.com/Diolinux/PhotoGIMP/releases/download/3.0/PhotoGIMP.zip)**
4. `PhotoGIMP.zip`의 내용을 모든 폴더 (예: 바탕화면)로 추출합니다.
5. 추출된 폴더를 열고 **`3.0` 폴더를 복사합니다**.
6. 실행 대화 상자를 열려면 <kbd>Windows</kbd> + <kbd>R</kbd>를 누릅니다.
7. `%APPDATA%\GIMP`를 입력하고 <kbd>Enter</kbd> 를 누르면 — GIMP의 설정 폴더가 열립니다.
8. 여기에 `3.0` 폴더를 **붙여넣기** 하세요.
9. 기존 파일에 대한 메시지가 나타나면 **"대상 파일 교체"**를 선택합니다.
10. GIMP 열기  — 새로운 PhotoGIMP 레이아웃을 확인할 수 있습니다! 🎉

<details>
<summary><strong>💡 선택 사항: GIMP 바로 가기 아이콘 변경</strong></summary>

[photogimp.ico](https://github.com/Diolinux/PhotoGIMP/releases/download/3.0/photogimp.ico)를 다운로드하고 GIMP 바로가기에서 아이콘을 업데이트할 수도 있습니다:

```
%appdata%\Microsoft\Windows\Start Menu\Programs\GIMP 3.0.0
```

Right-click the shortcut → **속성** → **아이콘 변경** → 다운로드한 `.ico` 파일을 찾아 마우스 오른쪽 버튼으로 클릭합니다.
</details>

<details>
<summary><strong>🍫 Chocolatey를 통해 설치 (대체)</strong></summary>

[Chocolatey](https://chocolatey.org/)를 사용하는 경우 단일 명령으로 PhotoGIMP를 설치할 수 있습니다:

```powershell
choco install photogimp
```

유지 관리자: [André Augusto](https://github.com/AndreAugustoDev)
</details>

---

### 🍎 macOS

<img src="https://skillicons.dev/icons?i=macos" align="right" />

#### 백업 (선택 사항)

현재 GIMP 설정을 유지하려면 먼저 백업하세요:

1. 파인더를 엽니다.
2. <kbd>Cmd</kbd> + <kbd>Shift</kbd> + <kbd>G</kbd>를 누른 후 `~/Library/Application Support/GIMP`로 이동합니다.
3. 전체 `GIMP` 폴더를 안전한 위치 (예: 바탕 화면)에 복사합니다.

#### 설치

1. [공식 웹사이트에서 GIMP를 설치](https://www.gimp.org/downloads/)했는지 확인하세요.
2. **GIMP를 한 번 연 다음 닫기** — 이렇게 하면 PhotoGIMP에 필요한 구성 폴더가 생성됩니다.
3. 최신 릴리스 다운로드:
   👉 **[macOS용 PhotoGIMP 다운로드 (.zip)](https://github.com/Diolinux/PhotoGIMP/releases/download/3.0/PhotoGIMP.zip)**
4. `PhotoGIMP.zip` 의 내용을 모든 폴더 (예: 바탕 화면)로 추출합니다.
5. 추출된 폴더를 열고 **`3.0` 폴더를 복사합니다**.
6. 파인더를 열고 <kbd>Cmd</kbd> + <kbd>Shift</kbd> + <kbd>G</kbd>를 눌러 "폴더로 이동"을 엽니다.
7. `~/Library/Application Support/GIMP`를 입력하고 <kbd>Enter</kbd>를 누릅니다.
8. 이전 설치에서 `2.10` 폴더가 보이면, **삭제**하여 충돌을 피하세요.
9. `3.0` 폴더 안에 **붙여넣기** 하세요.
10. 기존 파일에 대한 메시지가 나타나면 **"교체"** 또는 **"병합"**을 선택합니다.
11. GIMP 열기 — 새로운 PhotoGIMP 레이아웃을 확인할 수 있습니다! 🎉

---

## 📦 패치 내부 내용

PhotoGIMP는 GIMP의 구성 디렉터리에서 다음 파일을 대체하거나 추가합니다:

| 파일 / 폴더 | 기능 |
|---|---|
| `shortcutsrc` | Photoshop에 맞게 매핑된 키보드 단축키 |
| `toolrc` | 도구 구성 및 순서 |
| `sessionrc` | 창 레이아웃 및 패널 위치 |
| `dockrc` | 도크 / 패널 구성 |
| `gimprc` | 일반 GIMP 선호도(캔버스, 격자 등) |
| `contextrc` | 활성 도구/색상 컨텍스트 설정 |
| `splashes/` | 사용자 지정 PhotoGIMP 시작 화면 |
| `theme.css` | UI 테마의 사소한 조정 |
| `templaterc` | 미리 정의된 캔버스 템플릿 |

Linux에서는 패치도 설치됩니다::
- 사용자 지정 `.desktop` 파일 (PhotoGIMP 이름과 아이콘이 포함된 앱 실행기)
- `~/.local/share/icons/`의 사용자 지정 응용 프로그램 아이콘

---

## 🗑 제거하는 방법

PhotoGIMP를 제거하고 GIMP를 기본 상태로 복원하려면 GIMP의 구성 폴더를 삭제하고 GIMP를 다시 열기만 하면 새 기본 설정이 재생성됩니다.

### Linux

```bash
rm -rf ~/.config/GIMP/3.0
```

그런 다음 GIMP를 다시 열면 새 기본 구성이 생성됩니다.

이전에 백업을 했다면 대신 복원하세요:

```bash
cp -r ~/GIMP-3.0-backup ~/.config/GIMP/3.0
```

### Windows

1. <kbd>Windows</kbd> + <kbd>R</kbd>를 누르고 `%APPDATA%\GIMP`를 입력한 후 <kbd>Enter</kbd>를 누릅니다.
2. `3.0` 폴더를 삭제합니다.
3. GIMP 열기 — 기본 설정이 다시 생성됩니다.

또는 백업된 `3.0` 폴더를 다시 붙여넣어 백업을 복원할 수도 있습니다.

### macOS

1. 파인더를 열고 <kbd>Cmd</kbd> + <kbd>Shift</kbd> + <kbd>G</kbd>를 누릅니다.
2. `~/Library/Application Support/GIMP`로 이동합니다.
3. `3.0` 폴더를 삭제합니다.
4. GIMP 열기 — 기본 설정을 다시 생성합니다.

또는 백업된 폴더를 다시 붙여넣어 백업을 복원할 수도 있습니다.

---

## ❓ 문제 해결 / FAQ

<details>
<summary><strong>PhotoGIMP는 아무것도 바꾸지 않았습니다 - GIMP는 똑같아 보입니다</strong></summary>

- 파일을 **정확한 위치**로 추출했는지 확인하세요. 가장 일반적인 실수는 잘못된 폴더로 추출하는 것입니다..
- **Linux**: `.config` 및 `.local` 폴더는 홈 디렉터리 (`~`)에 있어야 합니다 - 파일 관리자에서 <kbd>Ctrl</kbd> + <kbd>H</kbd>를 눌러 폴더를 확인할 수 있습니다.
- **Windows**: The `3.0` folder must be inside `%APPDATA%\GIMP`, not next to it.
- **macOS**: `3.0` 폴더는 `~/Library/Application Support/GIMP` 폴더 안에 있어야 하며 바로 옆에 있으면 안됩니다.
- 파일을 붙여넣기 전에 **GIMP 닫기** 하셨나요? GIMP는 종료 시 들어오는 설정을 덮어쓸 수 있습니다.
</details>

<details>
<summary><strong>PhotoGIMP를 설치한 후 GIMP를 열 때 오류가 발생합니다</strong></summary>

- 이는 일반적으로 GIMP 버전이 일치하지 않는다는 것을 의미합니다. PhotoGIMP는 **GIMP 3.0+**용으로 제작되었습니다. GIMP 2.x를 실행 중이라면 호환되지 않습니다..
- 구성 폴더를 삭제하고 다시 설치해 보세요 — [제거하는 방법](#-제거하는 방법) 섹션을 참조하세요.
</details>

<details>
<summary><strong>GIMP 2.10과 함께 PhotoGIMP를 사용할 수 있나요?</strong></summary>

아니요. 이 버전의 PhotoGIMP는 **GIMP 3.0 이상** 전용으로 설계되었습니다. 구성 형식은 GIMP 2.x와 3.x 간에서 크게 변경되었습니다.
</details>

<details>
<summary><strong>PhotoGIMP가 사용자 지정 브러시, 글꼴 또는 플러그인을 삭제하나요?</strong></summary>

아니요. PhotoGIMP는 구성 파일 (바로 가기, 레이아웃, 기본 설정)만 교체합니다. 개인 브러시, 글꼴, 그라디언트 및 플러그인은 그대로 유지됩니다.
</details>

<details>
<summary><strong>PhotoGIMP를 설치한 후 바로 가기를 사용자 지정할 수 있나요?</strong></summary>

물론이죠! PhotoGIMP는 이제 시작점을 설정합니다 **편집 → 키보드 단축키**를 통해 GIMP의 모든 단축키를 변경할 수 있습니다.
</details>

<details>
<summary><strong>PhotoGIMP를 새 버전으로 업데이트하려면 어떻게 해야 하나요?</strong></summary>

최신 릴리스를 다운로드하고 설치 단계를 다시 따르기만 하면 이전 PhotoGIMP 구성이 덮어쓰게 됩니다.
</details>

---

## 🤝 기여하기

버그를 발견하셨나요? 제안이 있으신가요? 도와주시면 감사하겠습니다!

- **문제 보고**: [이슈 열기](https://github.com/Diolinux/PhotoGIMP/issues)
- **수정 사항 제출**: [풀 요청 만들기](https://github.com/Diolinux/PhotoGIMP/pulls)
- **번역**: README를 더 많은 언어로 번역할 수 있도록 도와주세요! [번역](#-번역) 섹션을 참조하세요.

---

## 🌍 번역

이 README는 다른 언어로도 제공됩니다:

- 🇬🇧 [English (영어)](../README.md)
- 🇰🇷 [Korean (한국어)](./docs/README_ko.md)
- 🇧🇷 [Português (브라질 포르투칼어)](./docs/README_pt.md)
- 🇵🇱 [Polski (폴란드어)](./docs/README_pl.md)
- 🇷🇺 [Русский (러시아어)](./docs/README_ru.md)

언어를 추가하시겠습니까? 레포를 포크하고 `docs/README_xx.md` 파일을 만든 다음 풀 요청을 제출하세요!

---

## 🏆 크레딧

- 이 프로젝트는 놀라운 [GIMP](https://www.gimp.org/) 팀이 없었다면 불가능했을 것입니다.
- [YouTube](https://youtube.com/Diolinux)에 있는 모든 Diolinux 지지자들께 큰 감사를 드립니다.
- [Adriel Filipe Design](https://bento.me/adrielfilipedesign)의 시작 화면 및 아이콘입니다.

---

## 👥 기여자

<a align="center" href="https://github.com/Diolinux/PhotoGIMP/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=Diolinux/PhotoGIMP" />
</a>

---

## 📄 라이선스

PhotoGIMP는 [GNU General Public License v3.0](./LICENSE)에 따라 라이선스가 부여됩니다.
