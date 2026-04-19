#!/bin/bash
# PhotoGIMP installer for Linux
# Detects the installed GIMP version and copies config files accordingly.

set -eu

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CONFIG_SRC="$SCRIPT_DIR/.config/GIMP/3.0"

# --- Detect GIMP config directory ---

detect_gimp_config_dir() {
    local config_home="${XDG_CONFIG_HOME:-$HOME/.config}"
    local flatpak_config="$HOME/.var/app/org.gimp.GIMP/config"
    local regex='.*/[0-9]+\.[0-9]+'
    local newest

    # Search native and Flatpak config locations
    for base in "$config_home/GIMP" "$flatpak_config/GIMP"; do
        [ -d "$base" ] || continue
        case "$(uname)" in
            Linux)
                newest=$(find "$base" -maxdepth 1 -type d -regextype posix-egrep -regex "$regex" 2>/dev/null | sort -t. -k1,1n -k2,2n | tail -1) ;;
            Darwin|*BSD|DragonFly)
                newest=$(find -E "$base" -maxdepth 1 -type d -regex "$regex" 2>/dev/null | sort -t. -k1,1n -k2,2n | tail -1) ;;
        esac
        if [ -n "${newest:-}" ]; then
            echo "$newest"
            return
        fi
    done

    # Fallback: try to get version from gimp binary
    local version
    for cmd in gimp gimp-3.2 gimp-3.0; do
        if command -v "$cmd" >/dev/null; then
            version=$("$cmd" --version 2>/dev/null | grep -oE '[0-9]+\.[0-9]+' | head -1 || true)
            [ -n "${version:-}" ] && break
        fi
    done

    # Flatpak fallback
    if [ -z "${version:-}" ] && command -v flatpak >/dev/null; then
        version=$(flatpak run org.gimp.GIMP --version 2>/dev/null | grep -oE '[0-9]+\.[0-9]+' | head -1 || true)
    fi

    if [ -n "${version:-}" ]; then
        # Prefer Flatpak path if it exists
        if [ -d "$flatpak_config/GIMP" ]; then
            echo "$flatpak_config/GIMP/$version"
        else
            echo "$config_home/GIMP/$version"
        fi
    else
        echo "$config_home/GIMP/3.0"
    fi
}

# --- Detect StartupWMClass ---

detect_wm_class() {
    local config_dir="$1"
    local version
    version=$(basename "$config_dir")  # e.g. "3.2"
    echo "gimp-$version"
}

# --- Main ---

echo "PhotoGIMP Installer"
echo "==================="

# Check that GIMP has been run at least once
GIMP_CONFIG=$(detect_gimp_config_dir)
echo "GIMP config directory: $GIMP_CONFIG"

if [ ! -d "$GIMP_CONFIG" ]; then
    echo ""
    echo "Config directory does not exist yet."
    echo "Please start GIMP once, close it, then run this script again."
    exit 1
fi

# Backup existing config
BACKUP="$GIMP_CONFIG.backup-$(date +%Y%m%d-%H%M%S)"
echo "Backing up current config to: $BACKUP"
cp -a "$GIMP_CONFIG" "$BACKUP"

# Copy PhotoGIMP config files
echo "Installing PhotoGIMP config..."
cp -a "$CONFIG_SRC"/. "$GIMP_CONFIG"/

# Install desktop file with correct WMClass
DESKTOP_SRC="$SCRIPT_DIR/.local/share/applications/org.gimp.GIMP.desktop"
DESKTOP_DST="$HOME/.local/share/applications/org.gimp.GIMP.desktop"

if [ -f "$DESKTOP_SRC" ]; then
    mkdir -p "$(dirname "$DESKTOP_DST")"
    WM_CLASS=$(detect_wm_class "$GIMP_CONFIG")
    sed "s/StartupWMClass=gimp-3\.0/StartupWMClass=$WM_CLASS/" \
        "$DESKTOP_SRC" > "$DESKTOP_DST"
    echo "Desktop file installed (StartupWMClass=$WM_CLASS)"
fi

# Install icons
if [ -d "$SCRIPT_DIR/.local/share/icons" ]; then
    cp -a "$SCRIPT_DIR/.local/share/icons"/. "$HOME/.local/share/icons"/
    echo "Icons installed."
fi

echo ""
echo "Done! Start GIMP to use PhotoGIMP."
echo "To restore your previous settings: cp -a '$BACKUP'/. '$GIMP_CONFIG'/"
