# 🎨 PhotoGIMP

![Icono de la aplicación PhotoGIMP](https://github.com/Diolinux/PhotoGIMP/raw/master/.local/share/icons/hicolor/256x256/256x256.png "Icono de la aplicación PhotoGIMP")

[![GitHub stars](https://img.shields.io/github/stars/Diolinux/PhotoGIMP?style=social)](https://github.com/Diolinux/PhotoGIMP)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Latest Release](https://img.shields.io/github/v/release/Diolinux/PhotoGIMP)](https://github.com/Diolinux/PhotoGIMP/releases/latest)

**PhotoGIMP** es un parche gratuito y mantenido por la comunidad que transforma [GIMP](https://www.gimp.org/) (GNU Image Manipulation Program) en una interfaz familiar para los usuarios de **Adobe Photoshop**. Si te estás pasando de Photoshop a GIMP y quieres sentirte como en casa desde el primer momento, PhotoGIMP es para ti.

> **¿Eres nuevo en GIMP?** GIMP es un editor de imágenes gratuito y de código abierto disponible para Linux, macOS y Windows. Puede hacer casi todo lo que hace Photoshop —retoque fotográfico, composición de imágenes, diseño gráfico y mucho más— y todo de forma gratuita. PhotoGIMP simplemente hace que _se vea y funcione_ de forma más parecida a Photoshop.

---

## ✨ Características

- **Distribución de herramientas al estilo Photoshop** — Las herramientas se reorganizan para imitar las posiciones a las que estás acostumbrado en Adobe Photoshop.
- **Pantalla de inicio personalizada** — Una pantalla de bienvenida (splash screen) exclusiva de PhotoGIMP aparece al iniciar el programa.
- **Espacio de trabajo maximizado** — Los ajustes por defecto están optimizados para ofrecerte la mayor área de trabajo posible.
- **Atajos de teclado de Photoshop** — Los atajos siguen la [documentación oficial de Adobe](https://helpx.adobe.com/photoshop/using/default-keyboard-shortcuts.html) para la versión de Windows.
- **Icono y nombre personalizados** — Un archivo `.desktop` dedicado le da a PhotoGIMP su propio icono y nombre en el menú del sistema.

---

## 📷 Capturas de pantalla

![PhotoGIMP Diolinux Splash Art](https://github.com/Diolinux/PhotoGIMP/raw/master/.config/GIMP/3.0/splashes/splash-screen-2025-v2.png)
_PhotoGIMP Diolinux Splash Art_

![PhotoGIMP 3](https://github.com/Diolinux/PhotoGIMP/raw/master/screenshots/photogimp_3_-_diolinux.png)
_GIMP 3.0 con el parche PhotoGIMP aplicado_

---

## 📋 Requisitos

Antes de instalar PhotoGIMP, asegúrate de tener:

| Requisito                          | Detalles                                                                                                                                                            |
| ---------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **GIMP 3.0 o superior**            | Descárgalo desde: [gimp.org](https://www.gimp.org/downloads/) o [Flathub](https://flathub.org/apps/org.gimp.GIMP) (Linux)                                           |
| **Ejecutar GIMP al menos una vez** | GIMP necesita generar sus archivos de configuración antes de que PhotoGIMP pueda sobrescribirlos. **Instala GIMP → ábrelo → ciérralo → después instala PhotoGIMP.** |

---

## ⚙ Cómo instalar

> [!WARNING]
> **¡Haz una copia de seguridad de tu configuración actual de GIMP antes de instalar!** PhotoGIMP sobrescribe los archivos de configuración de GIMP. Si tienes ajustes personalizados que quieres conservar, guarda primero una copia de seguridad. Consulta las instrucciones de copia de seguridad en cada sección a continuación.

---

### 🐧 Flatpak (Linux)

![](https://skillicons.dev/icons?i=linux)

#### Copia de seguridad (opcional)

Si quieres conservar tu configuración actual de GIMP, haz primero una copia de seguridad:

```bash
cp -r ~/.config/GIMP/3.0 ~/GIMP-3.0-backup
```

#### Instalación

1. Asegúrate de tener GIMP instalado [desde Flathub](https://flathub.org/apps/org.gimp.GIMP).
2. **Abre GIMP una vez y después ciérralo** — esto crea las carpetas de configuración que PhotoGIMP necesita.
3. Descarga la última versión:
   👉 **[Descargar PhotoGIMP para Linux (.zip)](https://github.com/Diolinux/PhotoGIMP/releases/download/3.0/PhotoGIMP-linux.zip)**
4. Extrae el archivo `.zip` **en tu carpeta personal** (`~`).
    - Esto colocará archivos en `~/.config` y `~/.local`, que son carpetas ocultas.
    - Para ver las carpetas ocultas en tu gestor de archivos, pulsa `Ctrl` + `H`.
    - Cuando te pregunte sobre los archivos existentes, elige **«Reemplazar»** o **«Sobrescribir»**.
5. Abre GIMP — ¡deberías ver la nueva interfaz de PhotoGIMP! 🎉

**💡 ¿Usas un GIMP que no es Flatpak?**

Si instalaste GIMP desde el gestor de paquetes de tu distribución (apt, dnf, pacman, etc.) en lugar de Flatpak, la carpeta de configuración se encuentra en la misma ubicación (`~/.config/GIMP/3.0`), así que los pasos anteriores siguen siendo válidos. Solo asegúrate de tener GIMP versión 3.0 o superior.

---

### 🪟 Windows

![](https://skillicons.dev/icons?i=windows)

#### Copia de seguridad (opcional)

Si quieres conservar tu configuración actual de GIMP, haz primero una copia de seguridad:

1. Pulsa `Windows` + `R` para abrir el cuadro de diálogo Ejecutar.
2. Escribe `%APPDATA%\GIMP` y pulsa `Enter`.
3. Copia toda la carpeta `3.0` a un lugar seguro (por ejemplo, tu Escritorio).

#### Instalación

1. Asegúrate de tener [GIMP instalado desde la página web oficial](https://www.gimp.org/downloads/).
2. **Abre GIMP una vez y después ciérralo** — esto crea las carpetas de configuración que PhotoGIMP necesita.
3. Descarga la última versión:
   👉 **[Descargar PhotoGIMP para Windows (.zip)](https://github.com/Diolinux/PhotoGIMP/releases/download/3.0/PhotoGIMP.zip)**
4. Extrae el contenido de `PhotoGIMP.zip` en cualquier carpeta (por ejemplo, tu Escritorio).
5. Abre la carpeta extraída y **copia la carpeta `3.0`**.
6. Pulsa `Windows` + `R` para abrir el cuadro de diálogo Ejecutar.
7. Escribe `%APPDATA%\GIMP` y pulsa `Enter` — esto abre la carpeta de configuración de GIMP.
8. **Pega** la carpeta `3.0` aquí.
9. Cuando te pregunte sobre los archivos existentes, selecciona **«Reemplazar los archivos en el destino»**.
10. Abre GIMP — ¡deberías ver la nueva interfaz de PhotoGIMP! 🎉

**💡 Opcional: Cambiar el icono del acceso directo de GIMP**

También puedes descargar [photogimp.ico](https://github.com/Diolinux/PhotoGIMP/releases/download/3.0/photogimp.ico) y actualizar el icono en el acceso directo de GIMP situado en:

```
%appdata%\Microsoft\Windows\Start Menu\Programs\GIMP 3.0.0
```

Haz clic derecho en el acceso directo → **Propiedades** → **Cambiar icono** → busca el archivo `.ico` descargado.

**🍫 Instalar mediante Chocolatey (alternativa)**

Si usas [Chocolatey](https://chocolatey.org/), puedes instalar PhotoGIMP con un único comando:

```
choco install photogimp
```

Mantenido por: [André Augusto](https://github.com/AndreAugustoDev)

---

### 🍎 macOS

![](https://skillicons.dev/icons?i=macos)

#### Copia de seguridad (opcional)

Si quieres conservar tu configuración actual de GIMP, haz primero una copia de seguridad:

1. Abre el Finder.
2. Pulsa `Cmd` + `Shift` + `G` y ve a `~/Library/Application Support/GIMP`.
3. Copia toda la carpeta `GIMP` a un lugar seguro (por ejemplo, tu Escritorio).

#### Instalación

1. Asegúrate de tener [GIMP instalado desde la página web oficial](https://www.gimp.org/downloads/).
2. **Abre GIMP una vez y después ciérralo** — esto crea las carpetas de configuración que PhotoGIMP necesita.
3. Descarga la última versión:
   👉 **[Descargar PhotoGIMP para macOS (.zip)](https://github.com/Diolinux/PhotoGIMP/releases/download/3.0/PhotoGIMP.zip)**
4. Extrae el contenido de `PhotoGIMP.zip` en cualquier carpeta (por ejemplo, tu Escritorio).
5. Abre la carpeta extraída y **copia la carpeta `3.0`**.
6. Abre el Finder, pulsa `Cmd` + `Shift` + `G` para abrir «Ir a la carpeta».
7. Escribe `~/Library/Application Support/GIMP` y pulsa `Enter`.
8. Si ves una carpeta `2.10` de una instalación anterior, **elimínala** para evitar conflictos.
9. **Pega** la carpeta `3.0` dentro de la carpeta de GIMP.
10. Cuando te pregunte sobre los archivos existentes, selecciona **«Reemplazar»** o **«Combinar»**.
11. Abre GIMP — ¡deberías ver la nueva interfaz de PhotoGIMP! 🎉

---

## 📦 Qué incluye el parche

PhotoGIMP reemplaza o añade los siguientes archivos en el directorio de configuración de GIMP:

| Archivo / Carpeta | Qué hace                                                        |
| ----------------- | --------------------------------------------------------------- |
| `shortcutsrc`     | Atajos de teclado adaptados para coincidir con los de Photoshop |
| `toolrc`          | Configuración y orden de las herramientas                       |
| `sessionrc`       | Disposición de ventanas y posiciones de los paneles             |
| `dockrc`          | Configuración de los paneles acoplables (dock)                  |
| `gimprc`          | Preferencias generales de GIMP (lienzo, rejilla, etc.)          |
| `contextrc`       | Configuración de la herramienta y el color activos              |
| `splashes/`       | Pantalla de inicio personalizada de PhotoGIMP                   |
| `theme.css`       | Pequeños ajustes en el tema de la interfaz                      |
| `templaterc`      | Plantillas de lienzo predefinidas                               |

En Linux, el parche también instala:

- Un archivo `.desktop` personalizado (lanzador con el nombre y el icono de PhotoGIMP)
- Un icono de aplicación personalizado en `~/.local/share/icons/`

---

## 🗑 Cómo desinstalar

Para eliminar PhotoGIMP y restaurar GIMP a su estado por defecto, basta con borrar la carpeta de configuración de GIMP y volver a abrirlo — generará de nuevo unos ajustes por defecto.

### Linux

```bash
rm -rf ~/.config/GIMP/3.0
```

Después abre GIMP de nuevo — creará una configuración por defecto totalmente nueva.

Si hiciste una copia de seguridad anteriormente, restáurala:

```bash
cp -r ~/GIMP-3.0-backup ~/.config/GIMP/3.0
```

### Windows

1. Pulsa `Windows` + `R`, escribe `%APPDATA%\GIMP` y pulsa `Enter`.
2. Elimina la carpeta `3.0`.
3. Abre GIMP — recreará la configuración por defecto.

O restaura tu copia de seguridad pegando de nuevo la carpeta `3.0`.

### macOS

1. Abre el Finder, pulsa `Cmd` + `Shift` + `G`.
2. Ve a `~/Library/Application Support/GIMP`.
3. Elimina la carpeta `3.0`.
4. Abre GIMP — recreará la configuración por defecto.

O restaura tu copia de seguridad pegando de nuevo la carpeta.

---

## ❓ Solución de problemas / Preguntas frecuentes

**PhotoGIMP no ha cambiado nada — GIMP se ve igual**

- Asegúrate de haber extraído los archivos en la **ubicación correcta**. El error más habitual es extraerlos en la carpeta equivocada.
- **Linux**: las carpetas `.config` y `.local` deben estar en tu directorio personal (`~`). Son ocultas — pulsa `Ctrl` + `H` en tu gestor de archivos para verlas.
- **Windows**: la carpeta `3.0` debe estar **dentro** de `%APPDATA%\GIMP`, no al lado.
- **macOS**: la carpeta `3.0` debe estar **dentro** de `~/Library/Application Support/GIMP`.
- ¿**Cerraste GIMP** antes de pegar los archivos? GIMP puede sobrescribir los ajustes recibidos al cerrarse.

**Recibo un error al abrir GIMP después de instalar PhotoGIMP**

- Normalmente esto significa que la versión de GIMP no es compatible. PhotoGIMP está hecho para **GIMP 3.0+**. Si estás usando GIMP 2.x, no será compatible.
- Prueba a borrar la carpeta de configuración y reinstalar — consulta la sección [Cómo desinstalar](#-cómo-desinstalar).

**¿Puedo usar PhotoGIMP con GIMP 2.10?**

No. Esta versión de PhotoGIMP está diseñada exclusivamente para **GIMP 3.0 y superior**. El formato de configuración cambió de forma significativa entre GIMP 2.x y 3.x.

**¿PhotoGIMP eliminará mis pinceles, fuentes o plug-ins personalizados?**

No. PhotoGIMP solo reemplaza archivos de configuración (atajos, disposición, preferencias). Tus pinceles, fuentes, degradados y plug-ins personales no se tocan.

**¿Puedo personalizar los atajos después de instalar PhotoGIMP?**

¡Por supuesto! PhotoGIMP solo establece un punto de partida. Puedes cambiar cualquier atajo en GIMP en **Editar → Atajos de teclado**.

**¿Cómo actualizo PhotoGIMP a una nueva versión?**

Simplemente descarga la versión más reciente y sigue los pasos de instalación de nuevo — esto sobrescribirá la configuración anterior de PhotoGIMP.

---

## 🤝 Contribuir

¿Has encontrado un fallo? ¿Tienes una sugerencia? ¡Nos encantaría contar con tu ayuda!

- **Reportar un problema**: [Abrir una issue](https://github.com/Diolinux/PhotoGIMP/issues)
- **Enviar una corrección**: [Crear un pull request](https://github.com/Diolinux/PhotoGIMP/pulls)
- **Traducir**: ¡Ayúdanos a traducir el README a más idiomas! Consulta la sección [Traducciones](#-traducciones).

---

## 🌍 Traducciones

Este README está disponible en otros idiomas:

- 🇬🇧 [English (Inglés)](../README.md)
- 🇮🇹 [Italiano (Italiano)](./README_it.md)
- 🇺🇦 [Українська (Ucraniano)](./README_ua.md)
- 🇵🇱 [Polski (Polaco)](./README_pl.md)
- 🇧🇷 [Português (Portugués brasileño)](./README_pt.md)
- 🇷🇺 [Русский (Ruso)](./README_ru.md)

¿Quieres añadir tu idioma? Haz un fork del repositorio, crea un archivo `docs/README_xx.md` y envía un pull request.

---

## 🏆 Créditos

- Este proyecto no sería posible sin el increíble equipo de [GIMP](https://www.gimp.org/).
- Un ENORME agradecimiento a todos los seguidores de Diolinux en [YouTube](https://youtube.com/Diolinux).
- Pantalla de inicio e iconos de [Adriel Filipe Design](https://bento.me/adrielfilipedesign).

---

## 👥 Colaboradores

[![](https://contrib.rocks/image?repo=Diolinux/PhotoGIMP)](https://github.com/Diolinux/PhotoGIMP/graphs/contributors)

---

## 📄 Licencia

PhotoGIMP está licenciado bajo la [Licencia Pública General de GNU v3.0](https://github.com/Diolinux/PhotoGIMP/blob/master/LICENSE).
