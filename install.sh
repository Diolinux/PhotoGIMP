#!/bin/bash
# PhotoGIMP installer for Linux
# Detects the installed GIMP version and copies config files accordingly.

set -eu

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CONFIG_SRC="$SCRIPT_DIR/.config/GIMP/3.0"

# --- Detect GIMP installation and config location ---

detect_gimp() {
    local gimp_params=(
		--no-interface
		--console-messages
		--batch-interpreter=plug-in-script-fu-eval
		--batch
		'(begin
			(display "GIMP_CONFIG_DIR=")
			(display gimp-directory)
			(newline))'
		--quit
	)

    # Ensure flatpak GIMP is actually installed, not just a leftover
    if command -v flatpak >/dev/null && flatpak info org.gimp.GIMP >/dev/null 2>&1; then
		GIMP_SOURCE="flatpak"
        GIMP_CONFIG=$(flatpak run org.gimp.GIMP "${gimp_params[@]}" 2>&1 | sed -n 's/^GIMP_CONFIG_DIR=//p')
		return
    fi

    for cmd in gimp gimp-3.2 gimp-3.0; do
        if command -v "$cmd" >/dev/null; then
            GIMP_SOURCE="native"
			GIMP_CONFIG=$("$cmd" "${gimp_params[@]}" 2>&1 | sed -n 's/^GIMP_CONFIG_DIR=//p')
			return
        fi
    done

    return 1
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

# Check that a supported GIMP installation exists and has been run at least once
GIMP_SOURCE=""
GIMP_CONFIG=""
if ! detect_gimp; then
    echo ""
    echo "No supported GIMP 3.x installation was detected."
    echo "Install GIMP 3.x, start it once, then run this script again."
    exit 1
fi

echo "GIMP installation source: $GIMP_SOURCE"
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

# Only install desktop file and icons for flatpak
if [ "$GIMP_SOURCE" = "flatpak" ]; then
    DESKTOP_SRC="$SCRIPT_DIR/.local/share/applications/org.gimp.GIMP.desktop"
    DESKTOP_DST="$HOME/.local/share/applications/org.gimp.GIMP.desktop"

	# Install desktop file with correct WMClass
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
fi

echo ""
echo "Done! Start GIMP to use PhotoGIMP."
echo "To restore your previous settings: cp -a '$BACKUP'/. '$GIMP_CONFIG'/"
