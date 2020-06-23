#!/usr/bin/env bash
#
#         Name: PhotoGIMP Instaler
#       Author: sudo-give-me-coffee
#  Description: Patches GIMP with a lot of improvment
#        Usage: bash install_linux.sh
#
#-----------------------------------------------------------------------------
#
#   Block execution as root
#
[ "${EUID}" = 0 ] && {
    echo
    echo "This instaler must not be run as root"
    echo "Run it again as a normal user without sudo:"
    echo
    echo "  ${0} ${@}"
    echo
    exit 2
}

#---------------------------------------------------------------------------------------
#
#   Useful environment variables to make this script portable
#
HERE="$(dirname "$(readlink -f "${0}")")"       # Directory with this script

[ "${XDG_CONFIG_HOME}" = "" ] && {
  export XDG_CONFIG_HOME="${HOME}/.config"      # Default configuration directory
}

[ "${XDG_DATA_HOME}" = "" ] && {
  export XDG_DATA_HOME="${HOME}/.local/share"   # Directory with local custom data
}

#---------------------------------------------------------------------------------------
#
#   Script that does the trick
#
function installPatch(){
  echo "  Instalation from ${1} found..."
  echo
  mkdir -p "${2}"
  cp -rfv "${HERE}/.var/app/org.gimp.GIMP/config/GIMP/2.10/"* "${2}" && {
    echo
    echo "PhotoGIMP successfuly installed, have a nice work"
    echo
    exit 0
  } || {
    echo
    echo "An error ocurred, run:"
    echo "  ${0} 2>&1 > report.log"
    echo
    echo "To get more info"
    echo
    exit 1
  }
}
#---------------------------------------------------------------------------------------
#
#   Each common way to use GIMP by popularity
#
# Native
[ -d "${XDG_CONFIG_HOME}/GIMP/2.101/" ] && {
  installPatch "system repository" "${XDG_CONFIG_HOME}/GIMP/2.10"
}

# AppImage
[ -d "${HOME}/.config/GIMP-AppImage/" ] && {
  installPatch "AppImage" "${HOME}/.config/GIMP-AppImage/"
}

# Flatpak
[ -d "${HOME}/.var/app/org.gimp.GIMP/config/GIMP/2.10/" ] && {
  installPatch "Flatpak" "${HOME}/.config/GIMP-AppImage/"
}

# Snap
[ -d "${HOME}/snap/gimp/current/.config/GIMP/2.10/" ] && {
  installPatch "Snap Store" "${HOME}/snap/gimp/current/.config/GIMP/2.10/"
}

