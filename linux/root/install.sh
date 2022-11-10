set -e
SCRIPT_DIR=$(dirname -- "$(readlink -f -- "$BASH_SOURCE")")
LOCAL_DIR="$HOME/.local"
OPT_DIR="$LOCAL_DIR/opt"
mkdir -p OPT_DIR
APP_NAME=airalarm
APP_DIR="$OPT_DIR/$APP_NAME"
cp -r "$SCRIPT_DIR/$APP_NAME" "$APP_DIR"
APPLICATIONS_DIR=~/.local/share/applications
mkdir -p $APPLICATIONS_DIR
DESKTOP_FILE="$APP_NAME.desktop"
cp "$SCRIPT_DIR/$DESKTOP_FILE" $APPLICATIONS_DIR
sed -i "2iIcon=$APP_DIR/megaphone.svg\nExec=$APP_DIR/$APP_NAME" "$APPLICATIONS_DIR/$DESKTOP_FILE"
