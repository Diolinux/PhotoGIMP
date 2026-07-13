# 🎨 PhotoGIMP

<img src="../.local/share/icons/hicolor/256x256/256x256.png" align="right" alt="Ícone do PhotoGIMP" title="Ícone do PhotoGIMP">

[![GitHub stars](https://img.shields.io/github/stars/Diolinux/PhotoGIMP?style=social)](https://github.com/Diolinux/PhotoGIMP)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Latest Release](https://img.shields.io/github/v/release/Diolinux/PhotoGIMP)](https://github.com/Diolinux/PhotoGIMP/releases/latest)

**PhotoGIMP** é um patch gratuito e mantido pela comunidade que transforma o [GIMP](https://www.gimp.org/) (GNU Image Manipulation Program) num layout familiar para utilizadores do **Adobe Photoshop**. Se está a migrar do Photoshop para o GIMP e quer sentir-se em casa imediatamente, o PhotoGIMP é para si.

> **Novo no GIMP?** O GIMP é um editor de imagens gratuito e de código aberto disponível para Linux, macOS e Windows. Ele pode fazer quase tudo que o Photoshop faz — retoque de fotos, composição de imagens, design gráfico e muito mais — tudo de graça. O PhotoGIMP apenas faz com que ele _pareça e funcione_ mais como o Photoshop.

---

## ✨ Recursos

- **Layout de ferramentas ao estilo Photoshop** — As ferramentas são reorganizadas para imitar as posições que já conhece do Adobe Photoshop.
- **Ecrã Inicial personalizado** — Um ecrã de arranque (splash screen) exclusivo do PhotoGIMP aparece ao iniciar o programa.
- **Espaço de trabalho maximizado** — As configurações padrão são otimizadas para lhe dar a maior área de trabalho possível.
- **Atalhos de teclado do Photoshop** — Os atalhos seguem a [documentação oficial da Adobe](https://helpx.adobe.com/photoshop/using/default-keyboard-shortcuts.html) para a versão Windows.
- **Ícone e nome personalizados** — Um ficheiro `.desktop` dedicado dá ao PhotoGIMP o seu próprio ícone e nome no menu do sistema.

---

## 📷 Capturas de Ecrã

<p>
  <img src="../.config/GIMP/3.0/splashes/splash-screen-2025-v2.png" alt="PhotoGIMP Diolinux Splash Art">
  <em>PhotoGIMP Diolinux Splash Art</em>
</p>

<p>
  <img src="../screenshots/photogimp_3_-_diolinux.png" alt="PhotoGIMP 3">
  <em>GIMP 3.0 com o patch PhotoGIMP aplicado</em>
</p>

---

## 📋 Requisitos

Antes de instalar o PhotoGIMP, certifique-se de que tem:

| Requisito                              | Detalhes                                                                                                                                                            |
| -------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **GIMP 3.0 ou mais recente**           | Descarregue em: [gimp.org](https://www.gimp.org/downloads/) ou [Flathub](https://flathub.org/apps/org.gimp.GIMP) (Linux)                                                  |
| **Executar o GIMP pelo menos uma vez** | O GIMP precisa gerar os seus ficheiros de configuração antes que o PhotoGIMP possa sobrescrevê-los. **Instale o GIMP → abra-o → feche-o → depois instale o PhotoGIMP.** |

---

## ⚙ Como Instalar

> [!WARNING]
> **Faça uma cópia de segurança das suas configurações atuais do GIMP antes de instalar!** O PhotoGIMP sobrescreve os ficheiros de configuração do GIMP. Se tem configurações personalizadas que deseja manter, guarde uma cópia de segurança primeiro. Veja as instruções de backup em cada secção abaixo.

---

### 🐧 Flatpak (Linux)

<img src="https://skillicons.dev/icons?i=linux" align="right" width="40" />

#### Cópia de Segurança (opcional)

Se deseja manter as suas configurações atuais do GIMP, faça a cópia de segurança primeiro:

```bash
cp -r ~/.config/GIMP/3.0 ~/GIMP-3.0-backup
```

#### Instalação

1. Certifique-se de que o GIMP já está instalado [pelo Flathub](https://flathub.org/apps/org.gimp.GIMP).
2. **Abra o GIMP uma vez e depois feche-o** — isto cria as pastas de configuração que o PhotoGIMP precisa.
3. Descarregue a versão mais recente:
   👉 **[Descarregar PhotoGIMP para Linux (.zip)](https://github.com/Diolinux/PhotoGIMP/releases/download/3.0/PhotoGIMP-linux.zip)**
4. Extraia o ficheiro `.zip` **na sua pasta pessoal** (`~`).
    - Isto colocará ficheiros em `~/.config` e `~/.local`, que são pastas ocultas.
    - Para ver pastas ocultas no seu gestor de ficheiros, pressione <kbd>Ctrl</kbd> + <kbd>H</kbd>.
    - Quando perguntado sobre ficheiros existentes, escolha **"Substituir"** ou **"Sobrescrever"**.
5. Abra o GIMP — deverá ver o novo layout do PhotoGIMP! 🎉

<details>
<summary><strong>💡 A usar um GIMP que não é Flatpak?</strong></summary>

Se instalou o GIMP pelo gestor de pacotes da sua distribuição (apt, dnf, pacman, etc.) em vez do Flatpak, a pasta de configuração está no mesmo local (`~/.config/GIMP/3.0`), portanto os passos acima ainda funcionam. Apenas certifique-se de que tem o GIMP versão 3.0 ou mais recente.

</details>

---

### 🪟 Windows

<img src="https://skillicons.dev/icons?i=windows" align="right" />

#### Cópia de Segurança (opcional)

Se deseja manter as suas configurações atuais do GIMP, faça a cópia de segurança primeiro:

1. Pressione <kbd>Windows</kbd> + <kbd>R</kbd> para abrir o diálogo Executar.
2. Digite `%APPDATA%\GIMP` e pressione <kbd>Enter</kbd>.
3. Copie toda a pasta `3.0` para um local seguro (ex.: a sua Área de Trabalho).

#### Instalação

1. Certifique-se de que o [GIMP está instalado pelo site oficial](https://www.gimp.org/downloads/).
2. **Abra o GIMP uma vez e depois feche-o** — isto cria as pastas de configuração que o PhotoGIMP precisa.
3. Descarregue a versão mais recente:
   👉 **[Descarregar PhotoGIMP para Windows (.zip)](https://github.com/Diolinux/PhotoGIMP/releases/download/3.0/PhotoGIMP.zip)**
4. Extraia o conteúdo de `PhotoGIMP.zip` para qualquer pasta (ex.: a sua Área de Trabalho).
5. Abra a pasta extraída e **copie a pasta `3.0`**.
6. Pressione <kbd>Windows</kbd> + <kbd>R</kbd> para abrir o diálogo Executar.
7. Digite `%APPDATA%\GIMP` e pressione <kbd>Enter</kbd> — isto abre a pasta de configurações do GIMP.
8. **Cole** a pasta `3.0` aqui.
9. Quando perguntado sobre ficheiros existentes, selecione **"Substituir os ficheiros no destino"**.
10. Abra o GIMP — deverá ver o novo layout do PhotoGIMP! 🎉

<details>
<summary><strong>💡 Opcional: Alterar o ícone do atalho do GIMP</strong></summary>

Também pode descarregar o [photogimp.ico](https://github.com/Diolinux/PhotoGIMP/releases/download/3.0/photogimp.ico) e atualizar o ícone no atalho do GIMP localizado em:

```
%appdata%\Microsoft\Windows\Start Menu\Programs\GIMP 3.0.0
```

Clique com o botão direito no atalho → **Propriedades** → **Alterar Ícone** → navegue até ao ficheiro `.ico` descarregado.

</details>

<details>
<summary><strong>🍫 Instalar via Chocolatey (alternativa)</strong></summary>

Se usa o [Chocolatey](https://chocolatey.org/), pode instalar o PhotoGIMP com um único comando:

```powershell
choco install photogimp
```

Mantido por: [André Augusto](https://github.com/AndreAugustoDev)

</details>

---

### 🍎 macOS

<img src="https://skillicons.dev/icons?i=macos" align="right" />

#### Cópia de Segurança (opcional)

Se deseja manter as suas configurações atuais do GIMP, faça a cópia de segurança primeiro:

1. Abra o Finder.
2. Pressione <kbd>Cmd</kbd> + <kbd>Shift</kbd> + <kbd>G</kbd> e vá para `~/Library/Application Support/GIMP`.
3. Copie toda a pasta `GIMP` para um local seguro (ex.: a sua Área de Trabalho).

#### Instalação

1. Certifique-se de que o [GIMP está instalado pelo site oficial](https://www.gimp.org/downloads/).
2. **Abra o GIMP uma vez e depois feche-o** — isto cria as pastas de configuração que o PhotoGIMP precisa.
3. Descarregue a versão mais recente:
   👉 **[Descarregar PhotoGIMP para macOS (.zip)](https://github.com/Diolinux/PhotoGIMP/releases/download/3.0/PhotoGIMP.zip)**
4. Extraia o conteúdo de `PhotoGIMP.zip` para qualquer pasta (ex.: a sua Área de Trabalho).
5. Abra a pasta extraída e **copie a pasta `3.0`**.
6. Abra o Finder, pressione <kbd>Cmd</kbd> + <kbd>Shift</kbd> + <kbd>G</kbd> para abrir "Ir para a Pasta".
7. Digite `~/Library/Application Support/GIMP` e pressione <kbd>Enter</kbd>.
8. Se tiver uma pasta `2.10` de uma instalação anterior, **elimine-a** para evitar conflitos.
9. **Cole** a pasta `3.0` dentro da pasta do GIMP.
10. Quando perguntado sobre ficheiros existentes, selecione **"Substituir"** ou **"Mesclar"**.
11. Abra o GIMP — deverá ver o novo layout do PhotoGIMP! 🎉

---

## 📦 O Que Está Incluído no Patch

O PhotoGIMP substitui ou adiciona os seguintes ficheiros no diretório de configuração do GIMP:

| Ficheiro / Pasta | O que faz                                                  |
| --------------- | ---------------------------------------------------------- |
| `shortcutsrc`   | Atalhos de teclado mapeados para corresponder ao Photoshop |
| `toolrc`        | Configuração e ordenação de ferramentas                    |
| `sessionrc`     | Layout de janelas e posições de painéis                    |
| `dockrc`        | Configuração de painéis / docks                            |
| `gimprc`        | Preferências gerais do GIMP (canvas, grelha, etc.)          |
| `contextrc`     | Configurações de ferramenta/cor ativas                     |
| `splashes/`     | Ecrã inicial personalizado do PhotoGIMP                    |
| `theme.css`     | Pequenos ajustes no tema da interface                      |
| `templaterc`    | Modelos de canvas pré-definidos                            |

No Linux, o patch também instala:

- Um ficheiro `.desktop` personalizado (lançador com nome e ícone do PhotoGIMP)
- Um ícone personalizado em `~/.local/share/icons/`

---

## 🗑 Como Desinstalar

Para remover o PhotoGIMP e restaurar o GIMP ao estado padrão, basta eliminar a pasta de configuração do GIMP e reabri-lo — ele irá regenerar as configurações padrão.

### Linux

```bash
rm -rf ~/.config/GIMP/3.0
```

Depois abra o GIMP novamente — ele criará uma nova configuração padrão.

Se fez uma cópia de segurança anteriormente, restaure-a:

```bash
cp -r ~/GIMP-3.0-backup ~/.config/GIMP/3.0
```

### Windows

1. Pressione <kbd>Windows</kbd> + <kbd>R</kbd>, digite `%APPDATA%\GIMP` e pressione <kbd>Enter</kbd>.
2. Elimine a pasta `3.0`.
3. Abra o GIMP — ele irá recriar as configurações padrão.

Ou restaure a sua cópia de segurança colando a pasta `3.0` de volta.

### macOS

1. Abra o Finder, pressione <kbd>Cmd</kbd> + <kbd>Shift</kbd> + <kbd>G</kbd>.
2. Vá para `~/Library/Application Support/GIMP`.
3. Elimine a pasta `3.0`.
4. Abra o GIMP — ele irá recriar as configurações padrão.

Ou restaure a sua cópia de segurança colando a pasta de volta.

---

## ❓ Solução de Problemas / FAQ

<details>
<summary><strong>O PhotoGIMP não mudou nada — o GIMP está igual</strong></summary>

- Certifique-se de que extraiu os ficheiros no **local correto**. O erro mais comum é extrair na pasta errada.
- **Linux**: As pastas `.config` e `.local` devem estar no seu diretório pessoal (`~`). Elas são ocultas — pressione <kbd>Ctrl</kbd> + <kbd>H</kbd> no seu gestor de ficheiros para vê-las.
- **Windows**: A pasta `3.0` deve estar **dentro** de `%APPDATA%\GIMP`, não ao lado dela.
- **macOS**: A pasta `3.0` deve estar **dentro** de `~/Library/Application Support/GIMP`.
- **Fechou o GIMP** antes de colar os ficheiros? O GIMP pode sobrescrever as configurações recebidas ao sair.
  </details>

<details>
<summary><strong>Recebo um erro ao abrir o GIMP depois de instalar o PhotoGIMP</strong></summary>

- Isto geralmente significa que a versão do GIMP não corresponde. O PhotoGIMP é feito para o **GIMP 3.0+**. Se está a usar o GIMP 2.x, não será compatível.
- Tente eliminar a pasta de configuração e reinstalar — veja a secção [Como Desinstalar](#-como-desinstalar).
  </details>

<details>
<summary><strong>Posso usar o PhotoGIMP com o GIMP 2.10?</strong></summary>

Não. Esta versão do PhotoGIMP foi projetada exclusivamente para o **GIMP 3.0 e mais recente**. O formato de configuração mudou significativamente entre o GIMP 2.x e 3.x.

</details>

<details>
<summary><strong>O PhotoGIMP vai apagar os meus pincéis, fontes ou plug-ins personalizados?</strong></summary>

Não. O PhotoGIMP substitui apenas ficheiros de configuração (atalhos, layout, preferências). Os seus pincéis, fontes, gradientes e plug-ins pessoais permanecem intocados.

</details>

<details>
<summary><strong>Posso personalizar os atalhos depois de instalar o PhotoGIMP?</strong></summary>

Claro que sim! O PhotoGIMP apenas define um ponto de partida. Pode alterar qualquer atalho no GIMP em **Editar → Atalhos de Teclado**.

</details>

<details>
<summary><strong>Como atualizo o PhotoGIMP para uma nova versão?</strong></summary>

Basta descarregar a versão mais recente e seguir os passos de instalação novamente — isto sobrescreverá a configuração anterior do PhotoGIMP.

</details>

---

## 🤝 Contribuindo

Encontrou um bug? Tem uma sugestão? Adoraríamos a sua ajuda!

- **Reportar um problema**: [Abrir uma issue](https://github.com/Diolinux/PhotoGIMP/issues)
- **Enviar uma correção**: [Criar um pull request](https://github.com/Diolinux/PhotoGIMP/pulls)
- **Traduzir**: Ajude-nos a traduzir o README para mais idiomas! Veja a secção [Traduções](#-traduções).

---

## 🌍 Traduções

Este README está disponível noutros idiomas:

- 🇵🇹 [Português (Portugal)](./README_pt-pt.md)
- 🇬🇧 [English (Inglês)](../README.md)
- 🇮🇹 [Italiano (Italiano)](./README_it.md)
- 🇵🇱 [Polski (Polonês)](./README_pl.md)
- 🇺🇦 [Українська (Ucraniano)](./README_ua.md)
- 🇷🇺 [Русский (Russo)](./README_ru.md)
- 🇪🇸 [Español (Espanhol)](./README_es.md)

Quer adicionar o seu idioma? Faça um fork do repositório, crie um ficheiro `docs/README_xx.md` e envie um pull request!

---

## 🏆 Créditos

- Este projeto não seria possível sem a incrível equipa do [GIMP](https://www.gimp.org/).
- Um GRANDE obrigado a todos os apoiadores do Diolinux no [YouTube](https://youtube.com/Diolinux).
- Ecrã inicial e ícones de [Adriel Filipe Design](https://bento.me/adrielfilipedesign).

---

## 👥 Contribuidores

<a align="center" href="https://github.com/Diolinux/PhotoGIMP/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=Diolinux/PhotoGIMP" />
</a>

---

## 📄 Licença

PhotoGIMP é licenciado sob a [GNU General Public License v3.0](../LICENSE).
