#!/bin/bash
# PhotoGIMP installer for Linux
# Detects the installed GIMP version and copies config files accordingly.

set -eu

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CONFIG_SRC="$SCRIPT_DIR/.config/GIMP/3.0"

# Source - https://stackoverflow.com/a/37939589
# Posted by yairchu, modified by community. See post 'Timeline' for change history
# Retrieved 2026-08-02, License - CC BY-SA 4.0

function version { echo "$@" | awk -F. '{ printf("%d%03d%03d%03d\n", $1,$2,$3,$4); }'; }

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

	local flatpak_config=""
	local flatpak_version=""
	local flatpak_command=""
	local selection

	# Check for flatpak installation
	if command -v flatpak >/dev/null && flatpak info org.gimp.GIMP >/dev/null 2>&1; then
		GIMP_SOURCE="flatpak"
		flatpak_config=$(
			set -o pipefail
			flatpak run org.gimp.GIMP "${gimp_params[@]}" 2>&1 | sed -n 's/^GIMP_CONFIG_DIR=//p'
		)

		flatpak_version=$(flatpak run org.gimp.GIMP --version 2>/dev/null | grep -oE '[0-9]+\.[0-9]+' | head -1)
		flatpak_command="org.gimp.GIMP"
	fi

	# Check for native installation
	for cmd in gimp gimp-3.2 gimp-3.0; do
		if command -v "$cmd" >/dev/null; then
			GIMP_SOURCE="native"
			GIMP_CONFIG=$(
				set -o pipefail
				"$cmd" "${gimp_params[@]}" 2>&1 | sed -n 's/^GIMP_CONFIG_DIR=//p'
			)

			GIMP_VERSION=$("$cmd" --version 2>/dev/null | grep -oE '[0-9]+\.[0-9]+' | head -1)
			GIMP_COMMAND="$cmd"

			# If flatpak was also detected then we need to prompt the user, otherwise we're done
			if [ -n "$flatpak_command" ]; then
				break
			fi

			return
		fi
	done

	# If GIMP_SOURCE is not native at this point then no native was detected so flatpak only
	case "$GIMP_SOURCE" in
		flatpak)
			;;
		native)
			echo ""
			echo "Flatpak and Native installations of GIMP were detected"
			echo "1) Flatpak (recommended)"
			echo "2) Native"

			while true; do
				printf "Select installation [1]: "
				if ! IFS= read -r selection; then
					echo ""
					echo "No selection received. Run the installer interactively"
					exit 1
				fi

				# For flatpak, break to set flatpak values, else native is already set so return
				case "$selection" in
					""|1) break ;;
					2) return ;;
					*) echo "Please enter 1 or 2" ;;
				esac
			done
			;;
		*)
			# Nothing detected return error
			return 1;;
	esac

	# Only flatpak was detected or the user selected flatpak
	GIMP_SOURCE="flatpak"
	GIMP_CONFIG="$flatpak_config"
	GIMP_VERSION="$flatpak_version"
	GIMP_COMMAND="$flatpak_command"
}

# --- Main ---

echo "PhotoGIMP Installer"
echo "==================="

# Check that a supported GIMP installation exists and has been run at least once
GIMP_SOURCE=""
GIMP_CONFIG=""
GIMP_VERSION=""
GIMP_COMMAND=""
if ! detect_gimp; then
	echo ""
	echo "No supported GIMP 3.x installation was detected."
	echo "Install GIMP 3.x, start it once, then run this script again."
	exit 1
fi

if [ $(version $GIMP_VERSION) -lt $(version "3.0") ]; then
	echo ""
	echo "Your version of GIMP $GIMP_VERSION is not supported."
	echo "Please install GIMP 3.x, start it once, then run this script again."
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

# Ensure GIMP isn't currently running before installation
case "$GIMP_SOURCE" in
	flatpak)
		if flatpak ps --columns=application | grep -Fxq -- "$GIMP_COMMAND"; then
			echo ""
			echo "GIMP is currently running"
			echo "Please close GIMP before running the installer"
			exit 1
		fi
		;;
	native)
		if pgrep -x "$GIMP_COMMAND" >/dev/null; then
			echo ""
			echo "GIMP is currently running"
			echo "Please close GIMP before running the installer"
			exit 1
		fi
		;;
esac

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

	# Install desktop file
	if [ -f "$DESKTOP_SRC" ]; then
		mkdir -p "$(dirname "$DESKTOP_DST")"
		cat -- "$DESKTOP_SRC" > "$DESKTOP_DST"
		echo "Desktop file installed."
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
