# 🎨 PhotoGIMP

<img src="./.local/share/icons/hicolor/256x256/256x256.png" align="right" alt="PhotoGIMP application icon" title="PhotoGIMP application icon">

[![GitHub stars](https://img.shields.io/github/stars/Diolinux/PhotoGIMP?style=social)](https://github.com/Diolinux/PhotoGIMP)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Latest Release](https://img.shields.io/github/v/release/Diolinux/PhotoGIMP)](https://github.com/Diolinux/PhotoGIMP/releases/latest)

**PhotoGIMP** là một bản patch miễn phí và được phát triển bởi cộng đồng có thể chuyển giao diện của phần mềm [GIMP](https://www.gimp.org/) (GNU Image Manipulation Program) thành giao diện của **Adobe Photoshop**. Nếu bạn là người dùng Photoshop muốn chuyển qua GIMP mà muốn có giao diện quen thuộc thì PhotoGIMP là bản patch dành cho bạn.

> **GIMP là gì?** GIMP là phần mềm chỉnh sửa ảnh mã nguồn mở cho Linux, macOS, và Windows. Nó có hầu hết các tính năng cơ bản của Photoshop — chỉnh sửa ảnh, chỉnh sửa bố cục, thiết kế đồ họa, và nhiều tính năng khác nữa — hoàn toàn miễn phí. PhotoGIMP chỉ giúp cho GIMP có giao diện _trông giống_ như Photoshop.

---

## ✨ Các tính năng

- **Giao diện giống Photoshop** — Các công cụ và vị trí được sắp xếp giống như Photoshop.
- **Splash Screen tùy chỉnh** — Bạn có thể tùy chỉnh Splash Screen khi phần mềm khởi động theo ý thích của bạn.
- **Tối ưu không gian thiết kế** — Các thông số được tùy chỉnh tối ưu giúp cho bạn có phần không gian làm việc lớn nhất có thể.
- **Các phím tắt của Photoshop** — Các phím tắt được cài đặt theo [bảng tài liệu chính thức của Adobe](https://helpx.adobe.com/photoshop/using/default-keyboard-shortcuts.html) dành cho phiên bản Windows.
- **Tùy chỉnh Icons và Tên ứng dụng** — File `.desktop` giúp bạn tùy chỉnh Icons và Tên ứng dụng của PhotoGIMP trong system menu.

---

## 📷 Một vài hình ảnh

| Splash Screen | Giao diện của PhotoGIMP |
|-|-|
| ![[PhotoGIMP Diolinux splash screen]](./.config/GIMP/3.0/splashes/splash-screen-2025-v2.png)<br>PhotoGIMP Diolinux splash screen | ![[PhotoGIMP 3]](./screenshots/photogimp_3_-_diolinux.png)<br>PhotoGIMP 3

---

## 📋 Một vài yêu cầu khi cài đặt

Trước khi cài đặt PhotoGIMP, hãy chắc rằng bạn đã làm các bước sau:

| Yêu cầu                | Chi tiết                                                                                                                                      |
| -------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| **Phần mềm GIMP 3.0 hoặc phiên bản cao hơn**      | |Tải về từ: [gimp.org](https://www.gimp.org/downloads/) hoặc [Flathub](https://flathub.org/apps/org.gimp.GIMP) (Linux)                      |
| **Khởi chạy GIMP 1 lần trước khi cài đặt PhotoGIMP** | GIMP cần phải được khởi chạy để tạo các file cần thiết trước khi PhotoGIMP có thể ghi đè lên chúng. **Cài đặt GIMP → khởi chạy → thoát GIMP → sau đó cài PhotoGIMP.** |

---

## ⚙ Hướng dẫn cài đặt

> [!Lưu ý]
> **Hãy lưu lại thông số cài đặt của GIMP trước khi cài đặt** PhotoGIMP sẽ ghi đè các thông số cài đặt của GIMP. Nếu bạn muốn dùng lại thông số cũ, hãy lưu lại config file cũ. Xem hướng dẫn sao lưu thông số cài đặt bên dưới.

---

### 🐧 Flatpak (Linux)

<img src="https://skillicons.dev/icons?i=linux" align="right" width="40" />

#### Sao lưu dữ liệu (không bắt buộc)

Nếu bạn muốn giữ lại các thông số cài đặt của GIMP, hãy sao lưu lại bằng câu lệnh sau:

```bash
cp -r ~/.config/GIMP/3.0 ~/GIMP-3.0-backup
```

#### Cài đặt

1. Hãy chắc rằng bạn đã cài đặt GIMP [từ Flathub](https://flathub.org/apps/org.gimp.GIMP).
2. **Khởi chạy GIMP sau đó đóng lại** — GIMP sẽ tạo ra 1 thư mục chứa các tập tin cần thiết để chạy.
3. Tải bản cài đặt PhotoGIMP mới nhất:
   👉 **[Tải PhotoGIMP cho Linux (.zip)](https://github.com/Diolinux/PhotoGIMP/releases/download/3.0/PhotoGIMP-linux.zip)**
4. Giải nén tập tin `.zip` vừa tải **vào home thư mục của bạn** (`~`).
    - Các tập tin sẽ được đặt vào thư mục ẩn `~/.config` và `~/.local`.
    - Nếu bạn muốn xem được các thư mục ẩn trong trình quản lý file, hãy nhấn <kbd>Ctrl</kbd> + <kbd>H</kbd>.
    - Khi bảng thông báo "existed files" hiện lên, chọn **"Replace"** hoặc **"Overwrite"**.
5. Mở GIMP — Bạn sẽ thấy được giao diện PhotoGIMP mới toanh! 🎉

<details>
<summary><strong>💡 Nếu bạn không cài đặt GIMP từ Flatpak?</strong></summary>

Nếu bạn cài đặt GIMP từ distro's package manager (apt, dnf, pacman, etc.) chứ không phải từ Flatpak, thư mục "config" sẽ được tạo ở `~/.config/GIMP/3.0`, vì vậy bạn cũng có thể làm theo các bước hướng dẫn trên. Chỉ cần chắc chắn là bạn đã cài đặt GIMP phiên bản 3.0 hoặc cao hơn.

</details>

---

### 🪟 Windows

<img src="https://skillicons.dev/icons?i=windows" align="right" />

#### Sao lưu dữ liệu (không bắt buộc)

Nếu bạn muốn giữ lại các thông số cài đặt của GIMP, hãy làm theo các bước sau:

1. Nhấn tổ hợp phím <kbd>Windows</kbd> + <kbd>R</kbd> để mở hộp thoại Run.
2. Nhập `%APPDATA%\GIMP` và nhấn <kbd>Enter</kbd>.
3. Copy toàn bộ thư mục `3.0` sang 1 vị trí khác (ví dụ như Desktop).

#### Cài đặt

1. Hãy chắc chắn rằng bạn đã [cài đặt GIMP từ trang chủ chính thức](https://www.gimp.org/downloads/).
2. **Khởi chạy GIMP sau đó đóng lại** — GIMP sẽ tạo ra 1 thư mục chứa các tập tin cần thiết để chạy.
3. Tải bản cài đặt PhotoGIMP mới nhất:
   👉 **[Tải PhotoGIMP cho Windows (.zip)](https://github.com/Diolinux/PhotoGIMP/releases/download/3.0/PhotoGIMP.zip)**
4. Giải nén file `PhotoGIMP.zip` vừa tải về.
5. Mở thư mục vừa được giải nén và **copy thư mục `3.0`**.
6. Nhấn tổ hợp phím <kbd>Windows</kbd> + <kbd>R</kbd> để mở hộp thoại Run.
7. Nhập `%APPDATA%\GIMP` và nhấn <kbd>Enter</kbd> — Bước này sẽ mở thư mục dữ liệu của GIMP.
8. **Paste** thư mục `3.0` tại đây (Lưu ý, tùy vào bản GIMP mà bạn cài đặt thì có thể sẽ là 3.x (3.1, 3.2,...) chứ không hẳn là 3.0 như mặc định, bạn hãy đổi tên thư mục trước khi copy và paste.
9. Khi bảng thông báo "existed files" hiện lên, chọn **"Replace the files in the destination"**.
10. Mở GIMP — Bạn sẽ thấy được giao diện PhotoGIMP mới toanh! 🎉

<details>
<summary><strong>💡 Tùy chọn: Thay đổi shortcut icon của GIMP</strong></summary>

Bạn có thể tải [photogimp.ico](https://github.com/Diolinux/PhotoGIMP/releases/download/3.0/photogimp.ico) để thay đổi shortcut icon của GIMP tại:

```
%appdata%\Microsoft\Windows\Start Menu\Programs\GIMP 3.0.0
```
Lưu ý là tùy vào bản cài đặt GIMP của bạn mà thư mục GIMP sẽ là 3.x.x (Ví dụ: GIMP 3.2.4).
Chuột phải vào shortcut → **Properties** → **Change Icon** → Chọn file `.ico` vừa tải về.

</details>

<details>
<summary><strong>🍫 Cài đặt qua Chocolatey</strong></summary>

Nếu bạn sử dụng [Chocolatey](https://chocolatey.org/), bạn có thể cài đặt PhotoGIMP chỉ với 1 câu lệnh:

```powershell
choco install photogimp
```

Duy trì bởi: [André Augusto](https://github.com/AndreAugustoDev)

</details>

---

### 🍎 macOS

<img src="https://skillicons.dev/icons?i=macos" align="right" />

#### Sao lưu dữ liệu (không bắt buộc)

Nếu bạn muốn giữ lại các thông số cài đặt của GIMP, hãy làm theo các bước sau:

1. Mở Finder.
2. Nhấn tổ hợp phím <kbd>Cmd</kbd> + <kbd>Shift</kbd> + <kbd>G</kbd> và đi đến thư mục `~/Library/Application Support/GIMP`.
3. Copy toàn bộ thư mục `GIMP` sang vị trí khác (Ví dụ: Desktop).

#### Cài đặt

1. Hãy chắc chắn rằng bạn đã [cài đặt GIMP từ trang chủ chính thức](https://www.gimp.org/downloads/).
2. **Khởi chạy GIMP sau đó đóng lại** — GIMP sẽ tạo ra 1 thư mục chứa các tập tin cần thiết để chạy.
3. Tải bản cài đặt PhotoGIMP mới nhất::
   👉 **[Tải PhotoGIMP cho macOS (.zip)](https://github.com/Diolinux/PhotoGIMP/releases/download/3.0/PhotoGIMP.zip)**
4. Giải nén file `PhotoGIMP.zip` vừa tải về.
5. Mở thư mục vừa được giải nén và **copy thư mục `3.0`**.
6. Mở Finder, nhấn tổ hợp phím <kbd>Cmd</kbd> + <kbd>Shift</kbd> + <kbd>G</kbd> để mở "Go to thư mục".
7. Nhập `~/Library/Application Support/GIMP` và nhấn <kbd>Enter</kbd>.
8. Nếu bạn thấy thư mục `2.10` từ các phiên bản cũ, hãy **xóa** để tránh xung đột.
9. **Paste** thư mục `3.0` trong thư mục GIMP.
10. Khi bảng thông báo "existed files" hiện lên, chọn **"Replace"** hoặc **"Merge"**.
11. Mở GIMP — Bạn sẽ thấy được giao diện PhotoGIMP mới toanh! 🎉

<details>
<summary><strong>Nếu bạn cài đặt bằng Terminal</strong></summary>

Nếu tùy chọn **"Merge"** của Finder tự động bỏ qua các tập tin đã tồn tại, hoặc nếu bạn muốn
sử dụng command line, bạn có thể copy PhotoGIMP files với `rsync`.

1. Mở Terminal.
2. Chạy lệnh `rsync`, thay thế `/path/to/extracted/3.0/` bằng vị trí của thư mục `3.0`

   ```bash
   rsync -av --ignore-times /path/to/extracted/3.0/ ~/Library/Application\ Support/GIMP/3.0/
   ```

   Hãy chắc rằng cả 2 đường dẫn đều kết thúc bằng `/`.
3. Nếu bạn cài đặt GIMP phiên bản khác, hãy thay đổi
   đường dẫn sao cho phù hợp (ví dụ, đường dẫn
   `~/Library/Application\ Support/GIMP/3.2/` cho phiên bản GIMP 3.2).

</details>

---

## 📦 Bản Patch này bao gồm những gì?

PhotoGIMP sẽ thay thế hoặc thêm vào các file sau trong thư mục cấu hình của GIMP:

| File / Thư mục | Chức năng                                  	 |
| -------------  | --------------------------------------------- |
| `shortcutsrc`  | Phím tắt được cài đặt theo Photoshop  		 |
| `toolrc`       | Cấu hình và thứ tự sắp xếp các công cụ        |
| `sessionrc`    | Bố cục phần mềm và vị trí các panel           |
| `dockrc`       | Cấu hình Dock / panel                    	 |
| `gimprc`       | Tùy chỉnh chung của GIMP (canvas, grid, etc.) |
| `contextrc`    | Cài đặt ngữ cảnh công cụ/màu đang dùng        |
| `splashes/`    | Splash Screen tùy chỉnh của PhotoGIMP       	 |
| `theme.css`    | Một số điều chỉnh nhỏ về giao diện            |
| `templaterc`   | Các mẫu canvas dựng sẵn                  	 |

Trên Linux, patch còn cài thêm:

- File `.desktop` tùy chỉnh (icon và tên PhotoGIMP trong trình khởi chạy ứng dụng)
- Icon ứng dụng tùy chỉnh đặt tại `~/.local/share/icons/`

---

## 🗑 Hướng dẫn gỡ cài đặt PhotoGIMP

Muốn gỡ PhotoGIMP và đưa GIMP về trạng thái mặc định, chỉ cần xóa thư mục cấu hình của GIMP rồi mở lại chương trình — nó sẽ tự tạo lại cấu hình mặc định ban đầu.

### Linux

```bash
rm -rf ~/.config/GIMP/3.0
```

Sau đó mở GIMP lên — nó sẽ tạo cấu hình mặc định hoàn toàn mới.

Nếu trước đó bạn đã sao lưu dữ liệu, hãy khôi phục lại thay vì làm bước trên:

```bash
cp -r ~/GIMP-3.0-backup ~/.config/GIMP/3.0
```

### Windows

1. Nhấn tổ hợp phím <kbd>Windows</kbd> + <kbd>R</kbd>, type `%APPDATA%\GIMP` và nhấn <kbd>Enter</kbd>.
2. Xóa thư mục `3.0` (Hoặc `3.x` tùy vào phiên bản cài đặt).
3. Khởi chạy GIMP — nó sẽ tự tạo lại cấu hình mặc định ban đầu.

Hoặc khôi phục bản sao lưu bằng cách paste thư mục `3.0` đã lưu trở lại vị trí cũ.

### macOS

1. Mở Finder, nhấn tổ hợp phím <kbd>Cmd</kbd> + <kbd>Shift</kbd> + <kbd>G</kbd>.
2. Đi đến đường dẫn `~/Library/Application Support/GIMP`.
3. Xóa thư mục `3.0`.
4. Sau đó mở GIMP lên — nó sẽ tự tạo lại cấu hình mặc định ban đầu.

Hoặc khôi phục bản sao lưu bằng cách dán lại thư mục đã lưu.

---

## ❓ Khắc phục sự cố / Câu hỏi thường gặp

> [!Cảnh báo]
> **PhotoGIMP không có website chính thức.** Nguồn chính thức duy nhất của dự án là tại GitHub: https://github.com/Diolinux/PhotoGIMP/

<details>
<summary><strong>Cài PhotoGIMP xong nhưng GIMP vẫn không đổi gì cả</strong></summary>

- Kiểm tra lại xem bạn đã giải nén file vào đúng vị trí chưa. Lỗi phổ biến nhất là giải nén nhầm **thư mục**.
- **Linux**: 2 mục `.config` và `.local` phải nằm trong thư mục home (`~`). TChúng là thư mục ẩn — nhấn tổ hợp phím <kbd>Ctrl</kbd> + <kbd>H</kbd> trong trình quản lý file để hiện chúng lên.
- **Windows**: thư mục `3.0` phải nằm trong thư mục `%APPDATA%\GIMP`, không phải nằm cạnh nó.
- **macOS**: thư mục `3.0` phải nằm trong thư mục `~/Library/Application Support/GIMP`.
- Bạn đã **đóng GIMP** trước khi paste file vào chưa? Nếu chưa, GIMP có thể ghi đè lại các file vừa paste sau khi thoát.
  </details>

<details>
<summary><strong>Mở GIMP lên bị báo lỗi sau khi cài PhotoGIMP</strong></summary>

- Thường là do phiên bản GIMP không khớp. PhotoGIMP được xây dựng cho GIMP **3.0 trở lên**. Nếu bạn đang dùng GIMP 2.x thì sẽ không tương thích..
- Thử xóa thư mục cấu hình rồi cài lại — xem hướng dẫn gỡ cài đặt ở phần [Hướng dẫn gỡ cài đặt PhotoGIMP](#-hướng-dẫn-gỡ-cài-đặt-photogimp).
  </details>

<details>
<summary><strong>Dùng PhotoGIMP với GIMP 2.10 được không?</strong></summary>

Không được. Phiên bản PhotoGIMP này chỉ dành riêng cho GIMP **3.0 trở lên**. Định dạng cấu hình đã thay đổi khá nhiều giữa GIMP 2.x và 3.x..

</details>

<details>
<summary><strong>PhotoGIMP có xóa mất brush, font hay plug-in tôi đã cài không?</strong></summary>

Không. PhotoGIMP chỉ thay đổi các file cấu hình (phím tắt, bố cục, tùy chỉnh). Brush, font, gradient và plug-in cá nhân của bạn vẫn giữ nguyên, không bị đụng tới.

</details>

<details>
<summary><strong>Sau khi cài PhotoGIMP có đổi lại phím tắt được không?</strong></summary>

Được chứ! PhotoGIMP chỉ là điểm khởi đầu thôi. Bạn có thể đổi bất kỳ phím tắt nào trong GIMP qua **Edit → Keyboard Shortcuts**.

</details>

<details>
<summary><strong>Cập nhật PhotoGIMP lên bản mới bằng cách nào?</strong></summary>

Chỉ cần tải bản mới nhất rồi làm lại các bước cài đặt như cũ — nó sẽ tự ghi đè lên cấu hình PhotoGIMP cũ.

</details>

---

## 🤝 Đóng góp cho dự án

Phát hiện lỗi? Có ý tưởng hay? Rất mong nhận được sự đóng góp từ bạn!

- **Báo lỗi**: [Mở issue mới](https://github.com/Diolinux/PhotoGIMP/issues)
- **Gửi bản sửa lỗi**: [Tạo pull request](https://github.com/Diolinux/PhotoGIMP/pulls)
- **Dịch thuật**: Giúp chúng tôi dịch README sang thêm nhiều ngôn ngữ! Xem phần [Bản dịch](#-bản-dịch) section.

---

## 🌍 Bản dịch

README này hiện có sẵn ở các ngôn ngữ khác:

- 🇮🇹 [Italiano (Italian)](./docs/README_it.md)
- 🇵🇱 [Polski (Polish)](./docs/README_pl.md)
- 🇺🇦 [Українська (Ukrainian)](./docs/README_ua.md)
- 🇧🇷 [Português (Brazilian Portuguese)](./docs/README_pt.md)
- 🇷🇺 [Русский (Russian)](./docs/README_ru.md)
- 🇪🇸 [Español (Spanish)](./docs/README_es.md)
- 🇮🇱 [עברית (Hebrew)](https://github.com/Diolinux/PhotoGIMP/blob/master/docs/README_he.md)
- 🇰🇷 [Korean (한국어)](./docs/README_ko.md)
- 🇨🇳 [简体中文 (Simplified Chinese)](./docs/README_zh.md)
- 🇨🇿 [Čeština (Czech)](./docs/README_cs.md)
- 🇻🇳 [Vietnam (Tiếng Việt)](./docs/README_vn.md)

Muốn thêm bản dịch tiếng của bạn? Fork repo này, tạo file `docs/README_xx.md` rồi gửi pull request nhé!

---

## 🏆 Lời cảm ơn

- Dự án này sẽ không thể được tạo ra nếu không có đội ngũ [GIMP](https://www.gimp.org/) tuyệt vời.
- Cảm ơn rất nhiều đến toàn thể những người ủng hộ Diolinux trên [YouTube](https://youtube.com/Diolinux).
- Splash screen & icon do [Adriel Filipe Design](https://bento.me/adrielfilipedesign) thực hiện.

---

## 💙 Ủng hộ dự án

PhotoGIMP được duy trì bởi những người dành thời gian của mình để giữ cho dự án luôn sẵn có, có tài liệu đầy đủ và tương thích với các phiên bản GIMP mới nhất. Bạn có thể ủng hộ quá trình phát triển này thông qua những người đóng góp chính:

- **Dionatan Simioni (Diolinux)** — người sáng lập PhotoGIMP và cộng đồng Diolinux. theo dõi kênh [YouTube Diolinux](https://youtube.com/Diolinux) và ghé thăm [blog Diolinux](https://diolinux.com.br/).
- **[Gabriel Almir](https://github.com/gabrielalmir)** — người duy trì dự án từ năm 2021. Bạn có thể ủng hộ công sức bảo trì của anh ấy qua [Ko-fi](https://ko-fi.com/gabrielalmir).

Đóng góp code, báo lỗi, dịch thuật hay cải thiện tài liệu — tất cả đều là những cách giúp ích rất nhiều cho PhotoGIMP.

---

## 👥 Người đóng góp

<a align="center" href="https://github.com/Diolinux/PhotoGIMP/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=Diolinux/PhotoGIMP" />
</a>

---

## 📄 Giấy phép

PhotoGIMP được phát hành theo giấy phép [GNU General Public License v3.0](./LICENSE).
