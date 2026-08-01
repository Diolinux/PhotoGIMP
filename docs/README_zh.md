# 🎨 PhotoGIMP

<img src="../.local/share/icons/hicolor/256x256/256x256.png" align="right" alt="PhotoGIMP 应用图标" title="PhotoGIMP 应用图标">

[![GitHub stars](https://img.shields.io/github/stars/Diolinux/PhotoGIMP?style=social)](https://github.com/Diolinux/PhotoGIMP)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Latest Release](https://img.shields.io/github/v/release/Diolinux/PhotoGIMP)](https://github.com/Diolinux/PhotoGIMP/releases/latest)

**PhotoGIMP** 是一个由社区驱动的免费补丁，可将 [GIMP](https://www.gimp.org/)（GNU Image Manipulation Program）转变为一套 **Adobe Photoshop** 用户感到熟悉的界面布局。如果你正从 Photoshop 转向 GIMP 并希望快速上手，PhotoGIMP 就是为你准备的。

> **第一次接触 GIMP？** GIMP 是一款免费开源的图像编辑器，适用于 Linux、macOS 和 Windows。Photoshop 能做的，它大部分也能做——照片修饰、图像合成、图形设计等——而且完全免费。PhotoGIMP 只是让它*看起来和用起来*更像 Photoshop。

---

## ✨ 特性

- **类 Photoshop 的工具布局** — 工具按照 Adobe Photoshop 中的位置重新排列，还原你熟悉的操作感。
- **自定义启动画面** — 启动时迎接你的是 PhotoGIMP 专属 Splash Screen。
- **最大化画布空间** — 默认设置经过优化，为你提供尽可能大的工作区域。
- **Photoshop 键盘快捷键** — 快捷键参考 [Adobe 官方文档](https://helpx.adobe.com/photoshop/using/default-keyboard-shortcuts.html) 中 Windows 版本的设定。
- **自定义图标和名称** — 专属的 `.desktop` 文件让 PhotoGIMP 在系统菜单中拥有独立的图标和应用名称。

---

## 📷 截图

<p>
  <img src="../.config/GIMP/3.0/splashes/splash-screen-2025-v2.png" alt="PhotoGIMP Diolinux 启动画面">
  <em>PhotoGIMP Diolinux 启动画面</em>
</p>

<p>
  <img src="../screenshots/photogimp_3_-_diolinux.png" alt="PhotoGIMP 3">
  <em>GIMP 3.0 应用 PhotoGIMP 补丁后的效果</em>
</p>

---

## 📋 安装要求

安装 PhotoGIMP 之前，请确保满足以下条件：

| 要求 | 详情 |
|---|---|
| **GIMP 3.0 或更高版本** | 下载地址：[gimp.org](https://www.gimp.org/downloads/) 或 [Flathub](https://flathub.org/apps/org.gimp.GIMP)（Linux） |
| **至少运行过一次 GIMP** | GIMP 需要先生成配置文件，然后 PhotoGIMP 才能覆盖它们。**先安装 GIMP → 打开 → 关闭 → 再安装 PhotoGIMP。** |

---

## ⚙ 安装方法

> [!WARNING]
> **安装前请备份你的 GIMP 当前设置！** PhotoGIMP 会覆盖 GIMP 的配置文件。如果你想保留自定义设置，请先保存一份备份。具体备份步骤见下方各平台说明。

---

### 🐧 Flatpak（Linux）

<img src="https://skillicons.dev/icons?i=linux" align="right" width="40" />

#### 备份（可选）

如果你想保留当前 GIMP 设置，请先备份：

```bash
cp -r ~/.config/GIMP/3.0 ~/GIMP-3.0-backup
```

#### 安装

1. 确保已[从 Flathub](https://flathub.org/apps/org.gimp.GIMP) 安装 GIMP。
2. **先打开一次 GIMP，然后关闭**——这将创建 PhotoGIMP 所需的配置文件夹。
3. 下载最新 release：
   👉 **[下载 PhotoGIMP for Linux (.zip)](https://github.com/Diolinux/PhotoGIMP/releases/download/3.0/PhotoGIMP-linux.zip)**
4. 将 `.zip` 文件解压**到你的主目录**（`~`）中。
   - 这会将文件放入 `~/.config` 和 `~/.local`，这些是隐藏文件夹。
   - 要在文件管理器中查看隐藏文件夹，请按 <kbd>Ctrl</kbd> + <kbd>H</kbd>。
   - 当提示覆盖已有文件时，选择 **"Replace"** 或 **"Overwrite"**。
5. 打开 GIMP——你应该看到全新的 PhotoGIMP 布局了！🎉

<details>
<summary><strong>💡 使用的是非 Flatpak 版 GIMP？</strong></summary>

如果你是使用发行版包管理器（apt、dnf、pacman 等）而非 Flatpak 安装的 GIMP，配置文件夹的位置相同（`~/.config/GIMP/3.0`），因此上述步骤同样适用。只需确保 GIMP 版本为 3.0 或更高。
</details>

---

### 🪟 Windows

<img src="https://skillicons.dev/icons?i=windows" align="right" />

#### 备份（可选）

如果你想保留当前 GIMP 设置，请先备份：

1. 按下 <kbd>Windows</kbd> + <kbd>R</kbd> 打开运行对话框。
2. 输入 `%APPDATA%\GIMP` 并按 <kbd>Enter</kbd>。
3. 将整个 `3.0` 文件夹复制到安全位置（例如桌面）。

#### 安装

1. 确保已[从官方站点](https://www.gimp.org/downloads/)安装 GIMP。
2. **先打开一次 GIMP，然后关闭**——这将创建 PhotoGIMP 所需的配置文件夹。
3. 下载最新 release：
   👉 **[下载 PhotoGIMP for Windows (.zip)](https://github.com/Diolinux/PhotoGIMP/releases/download/3.0/PhotoGIMP.zip)**
4. 将 `PhotoGIMP.zip` 的内容解压到任意文件夹（例如桌面）。
5. 打开解压后的文件夹，**复制其中的 `3.0` 文件夹**。
6. 按下 <kbd>Windows</kbd> + <kbd>R</kbd> 打开运行对话框。
7. 输入 `%APPDATA%\GIMP` 并按 <kbd>Enter</kbd>——这将打开 GIMP 的设置文件夹。
8. 将 `3.0` 文件夹**粘贴**到此处。
9. 当提示覆盖已有文件时，选择 **"Replace the files in the destination"**。
10. 打开 GIMP——你应该看到全新的 PhotoGIMP 布局了！🎉

<details>
<summary><strong>💡 可选：更改 GIMP 快捷方式图标</strong></summary>

你也可以下载 [photogimp.ico](https://github.com/Diolinux/PhotoGIMP/releases/download/3.0/photogimp.ico)，然后更新以下路径中 GIMP 快捷方式的图标：

```
%appdata%\Microsoft\Windows\Start Menu\Programs\GIMP 3.0.0
```

右键点击快捷方式 → **属性** → **更改图标** → 浏览到下载的 `.ico` 文件。
</details>

<details>
<summary><strong>🍫 通过 Chocolatey 安装（替代方式）</strong></summary>

如果你使用 [Chocolatey](https://chocolatey.org/)，可以通过一条命令安装 PhotoGIMP：

```powershell
choco install photogimp
```

维护者：[André Augusto](https://github.com/AndreAugustoDev)
</details>

---

### 🍎 macOS

<img src="https://skillicons.dev/icons?i=macos" align="right" />

#### 备份（可选）

如果你想保留当前 GIMP 设置，请先备份：

1. 打开 Finder。
2. 按下 <kbd>Cmd</kbd> + <kbd>Shift</kbd> + <kbd>G</kbd>，前往 `~/Library/Application Support/GIMP`。
3. 将整个 `GIMP` 文件夹复制到安全位置（例如桌面）。

#### 安装

1. 确保已[从官方站点](https://www.gimp.org/downloads/)安装 GIMP。
2. **先打开一次 GIMP，然后关闭**——这将创建 PhotoGIMP 所需的配置文件夹。
3. 下载最新 release：
   👉 **[下载 PhotoGIMP for macOS (.zip)](https://github.com/Diolinux/PhotoGIMP/releases/download/3.0/PhotoGIMP.zip)**
4. 将 `PhotoGIMP.zip` 的内容解压到任意文件夹（例如桌面）。
5. 打开解压后的文件夹，**复制其中的 `3.0` 文件夹**。
6. 打开 Finder，按下 <kbd>Cmd</kbd> + <kbd>Shift</kbd> + <kbd>G</kbd> 打开"前往文件夹"。
7. 输入 `~/Library/Application Support/GIMP` 并按 <kbd>Enter</kbd>。
8. 如果你看到之前安装遗留的 `2.10` 文件夹，请**将其删除**以避免冲突。
9. 将 `3.0` 文件夹**粘贴**到 GIMP 文件夹内。
10. 当提示覆盖已有文件时，选择 **"Replace"** 或 **"Merge"**。
11. 打开 GIMP——你应该看到全新的 PhotoGIMP 布局了！🎉

---

## 📦 补丁内容说明

PhotoGIMP 会替换或添加 GIMP 配置目录中的以下文件：

| 文件 / 文件夹 | 作用 |
|---|---|
| `shortcutsrc` | 映射为 Photoshop 风格的键盘快捷键 |
| `toolrc` | 工具配置和排序 |
| `sessionrc` | 窗口布局和面板位置 |
| `dockrc` | 面板 / 停靠栏配置 |
| `gimprc` | GIMP 通用偏好设置（画布、网格等） |
| `contextrc` | 当前工具 / 颜色上下文设置 |
| `splashes/` | 自定义 PhotoGIMP 启动画面 |
| `theme.css` | 轻微调整的 UI 主题 |
| `templaterc` | 预设画布模板 |

在 Linux 上，此补丁还会安装：
- 一个自定义的 `.desktop` 文件（带有 PhotoGIMP 名称和图标的启动器）
- 一个位于 `~/.local/share/icons/` 的自定义应用图标

---

## 🗑 如何卸载

要移除 PhotoGIMP 并将 GIMP 恢复为默认状态，只需删除 GIMP 的配置文件夹然后重新打开 GIMP——它会自动生成全新的默认设置。

### Linux

```bash
rm -rf ~/.config/GIMP/3.0
```

然后重新打开 GIMP——它会生成全新的默认配置。

如果你之前做过备份，可以恢复它：

```bash
cp -r ~/GIMP-3.0-backup ~/.config/GIMP/3.0
```

### Windows

1. 按下 <kbd>Windows</kbd> + <kbd>R</kbd>，输入 `%APPDATA%\GIMP` 并按 <kbd>Enter</kbd>。
2. 删除 `3.0` 文件夹。
3. 打开 GIMP——它会重新创建默认设置。

或者将之前备份的 `3.0` 文件夹粘贴回来以恢复设置。

### macOS

1. 打开 Finder，按下 <kbd>Cmd</kbd> + <kbd>Shift</kbd> + <kbd>G</kbd>。
2. 前往 `~/Library/Application Support/GIMP`。
3. 删除 `3.0` 文件夹。
4. 打开 GIMP——它会重新创建默认设置。

或者将之前备份的文件夹粘贴回来以恢复设置。

---

## ❓ 故障排除 / 常见问题

> [!CAUTION]
> **PhotoGIMP 没有官方网站。** 该项目的唯一官方来源是其 GitHub 仓库：https://github.com/Diolinux/PhotoGIMP/

<details>
<summary><strong>PhotoGIMP 没有任何变化——GIMP 看起来和原来一样</strong></summary>

- 请确认你将文件解压到了**正确的位置**。最常见的问题就是解压到了错误的文件夹。
- **Linux**：`.config` 和 `.local` 文件夹必须位于你的主目录（`~`）中。它们是隐藏文件夹——在文件管理器中按 <kbd>Ctrl</kbd> + <kbd>H</kbd> 即可看到。
- **Windows**：`3.0` 文件夹必须在 `%APPDATA%\GIMP` 里面，而不是靠在外面。
- **macOS**：`3.0` 文件夹必须在 `~/Library/Application Support/GIMP` 里面。
- 你在粘贴文件之前**关闭 GIMP** 了吗？GIMP 退出时可能会覆盖传入的设置。
</details>

<details>
<summary><strong>安装 PhotoGIMP 后打开 GIMP 时报错</strong></summary>

- 这通常意味着 GIMP 版本不匹配。PhotoGIMP 专为 **GIMP 3.0+** 构建。如果你运行的是 GIMP 2.x，将不兼容。
- 尝试删除配置文件夹后重新安装——参见[如何卸载](#-如何卸载)部分。
</details>

<details>
<summary><strong>可以在 GIMP 2.10 上使用 PhotoGIMP 吗？</strong></summary>

不可以。此版本的 PhotoGIMP 专为 **GIMP 3.0 及更高版本**设计。GIMP 2.x 和 3.x 之间的配置格式发生了重大变化。
</details>

<details>
<summary><strong>PhotoGIMP 会删除我的自定义画笔、字体或插件吗？</strong></summary>

不会。PhotoGIMP 只替换配置文件（快捷键、布局、偏好设置）。你的个人画笔、字体、渐变和插件不会受到影响。
</details>

<details>
<summary><strong>安装 PhotoGIMP 后可以自定义快捷键吗？</strong></summary>

当然可以！PhotoGIMP 只是提供一个起点。你可以在 GIMP 中通过 **编辑（Edit）→ 键盘快捷键（Keyboard Shortcuts）** 修改任何快捷键。
</details>

<details>
<summary><strong>如何将 PhotoGIMP 更新到新版本？</strong></summary>

只需下载最新 release 并按照安装步骤重新操作即可——它会覆盖之前的 PhotoGIMP 配置。
</details>

---

## 🤝 贡献

发现 Bug？有建议？欢迎你的帮助！

- **报告问题**：[提交 Issue](https://github.com/Diolinux/PhotoGIMP/issues)
- **提交修复**：[创建 Pull Request](https://github.com/Diolinux/PhotoGIMP/pulls)
- **翻译**：帮助我们将 README 翻译成更多语言！参见[翻译](#-翻译)部分。

---

## 🌍 翻译

本 README 提供以下语言的版本：

- 🇮🇹 [Italiano（意大利语）](./docs/README_it.md)
- 🇵🇱 [Polski（波兰语）](./docs/README_pl.md)
- 🇧🇷 [Português（巴西葡萄牙语）](./docs/README_pt.md)
- 🇷🇺 [Русский（俄语）](./docs/README_ru.md)
- 🇨🇳 [简体中文](./docs/README_zh.md)

想要添加你的语言？Fork 本仓库，创建 `docs/README_xx.md` 文件，然后提交 Pull Request！

---

## 🏆 致谢

- 没有出色的 [GIMP](https://www.gimp.org/) 团队，就不会有这个项目。
- 衷心感谢 [YouTube](https://youtube.com/Diolinux) 上所有 Diolinux 的支持者。
- 启动画面和图标由 [Adriel Filipe Design](https://bento.me/adrielfilipedesign) 提供。

---

## 👥 贡献者

<a align="center" href="https://github.com/Diolinux/PhotoGIMP/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=Diolinux/PhotoGIMP" />
</a>

---

## 📄 许可证

PhotoGIMP 基于 [GNU General Public License v3.0](../LICENSE) 许可。
