# 🎨 PhotoGIMP

<img src="./.local/share/icons/hicolor/256x256/apps/photogimp.png" align="right" alt="PhotoGimp application icon" title="PhotoGimp application icon">

Um patch para otimizar o GIMP 2.10+ para usuários do Adobe Photoshop, incluindo recursos como:

* Organização de ferramentas para imitar a posição do Adobe Photoshop;
* Centenas de novas fontes por padrão;
* Novos filtros Python instalados por padrão, como "heal selection";
* Nova tela inicial;
* Novas configurações padrão para maximizar o espaço na tela;
* Atalhos semelhantes aos do Photoshop para Windows, seguindo a Documentação da Adobe;
* Novo ícone e nome do arquivo .desktop personalizado;
* O idioma do sistema agora é usado por padrão, você ainda pode alterar isso nas configurações, se desejar.

![PhotoGimp Diolinux Splash Art](./.var/app/org.gimp.GIMP/config/GIMP/2.10/splashes/photogimp-diolinux-splash.png)

**📷 Captura de Tela**

![PhotoGimp Screenshot - Editing Google Takeout](./screenshots/2020-06-22_12-06.png)

**🈂 Tenha um grande conjunto de fontes disponíveis a qualquer momento**

Mais de 1800 fontes são incluídas por padrão no PhotoGimp para que você possa acelerar seu fluxo de trabalho criativo.

<!-- TODO: Adicionar captura de tela utilizando uma das fontes incluídas. -->

[Confira todas as fontes incluídas](https://github.com/Diolinux/PhotoGIMP/blob/master/fonts.txt)

## ⚙ Como instalar (usando Flatpak)

Este pacote é sobre flatpak, mas também contém "apenas arquivos" que você pode usar em qualquer versão do GIMP (.deb, .rpm, Snap, AppImage, Windows, macOS). Basta verificar a localização dos arquivos de configuração do GIMP.

**Inicie e saia do GIMP após a instalação antes de continuar!**

### Prepare o ambiente Flatpak

* Antes de tudo, você precisa ter o GIMP mais recente instalado em seu sistema [usando Flatpak](https://flatpak.org/setup/)
* Instale o GIMP Flatpak através do seu AppCenter/Gerenciador de Pacotes ou terminal: ```flatpak install flathub org.gimp.GIMP```

### Instale o PhotoGIMP

Dentro do arquivo .zip da [página de lançamentos](https://github.com/Diolinux/PhotoGIMP/releases) você encontrará três pastas (ocultas em sistemas não Windows, pois seus nomes começam com um ponto). Todas essas pastas devem ser extraídas para sua pasta `$HOME`, substituindo tudo se você já tiver os mesmos arquivos de uma instalação mais antiga.

O arquivo contém estes diretórios:
* `.icons` (que tem um novo ícone do PhotoGIMP)
* `.local` (que contém o arquivo .desktop personalizado)
* `.var` (que contém a personalização do patch flatpak para GIMP 2.10+)

Se você deseja apenas a personalização do PhotoGIMP sem alterar o ícone original do GIMP e seu nome, apenas extraia apenas a pasta ```.var``` para o seu diretório home.

## ⚙ Como instalar (outros)

Como são apenas arquivos, a única coisa que você precisa fazer é copiar todos os arquivos que residem em uma pasta específica deste pacote `/.var/app/org.gimp.GIMP/config/GIMP/2.10` para a configuração do seu GIMP pasta em cada sistema em particular, substituindo os existentes.

**Inicie e saia do GIMP após a instalação antes de continuar!**

O novo ícone precisa ser definido manualmente.

### Snap do Ubuntu

Pasta de configuração: `$HOME/snap/gimp/47/.config/GIMP/2.10/`

### Outros sistemas Linux ou Unix(-like) (.deb, .rpm, etc.)

Pasta de configuração: `$HOME/.config/GIMP/2.10/`

### macOS

Pasta de configuração: `"$HOME/Library/Application Support/GIMP/2.10/"`

* [Video Tutorial de Davies Media Design no macOS](https://youtu.be/5nXhtaGQs9U)

Este one-liner fará o trabalho:
```console
curl -L https://github.com/Diolinux/PhotoGIMP/releases/download/1.0/PhotoGIMP.by.Diolinux.v2020.for.Flatpak.zip -o ~/Downloads/PhotoGIMP.by.Diolinux.v2020.for.Flatpak.zip && unzip ~/Downloads/PhotoGIMP.by.Diolinux.v2020.for.Flatpak.zip -d ~/Downloads && cp -R ~/Downloads/PhotoGIMP\ by\ Diolinux\ v2020\ for\ Flatpak/.var/app/org.gimp.GIMP/config/GIMP/2.10/ ~/Library/Application\ Support/GIMP/2.10 && rm ~/Downloads/PhotoGIMP.by.Diolinux.v2020.for.Flatpak.zip
```
(baixa a versão 1.0 na pasta `Downloads`, descompacta e copia os arquivos, depois remove o arquivo .zip baixado)

*Aviso*: o GIMP no macOS está um pouco atrasado em seu lançamento. Desta forma, este patch ainda funciona, especialmente na questão dos atalhos, mas algumas coisas, como a organização da caixa de ferramentas, não funcionarão corretamente. Até que a versão do macOS atinja a versão 2.10.20, espere esse comportamento.

### Windows

Pasta de configuração: `%APPDATA%\GIMP\2.10`

* [Tutorial em vídeo para Davies Media Design no Windows](https://youtu.be/57DNUsf4A-0)

Ou instale via [Chocolatey](https://chocolatey.org/):
``` powershell
choco install photogimp
```
Mantido por: [André Augusto](https://github.com/AndreAugustoAAQ)

## Créditos

* Este projeto não seria possível sem a incrível equipe do GIMP.
* A Foto no novo Splash é da [Isabella Mariana](https://www.pexels.com/pt-br/@isabella-mariana-1022505).
* Muito obrigado a todos os apoiadores do Diolinux no [Twitch](https://twitch.tv/Diolinux) e no [YouTube](https://youtube.com/Diolinux).

## Notas do patch
- [Veja as Notas de Lançamento em Português](https://diolinux.com.br/2020/06/photogimp-2020.html).
