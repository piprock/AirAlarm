scriptDir=$(dirname -- "$(readlink -f -- "$BASH_SOURCE")")
cp -r "$scriptDir/airalarm" ~/.local/opt/airalarm
mkdir -p ~/.local/share/applications/
cp "$scriptDir/airalarm.desktop" ~/.local/share/applications/
sed -i "2iIcon=$HOME/.local/opt/airalarm/megaphone.svg\nExec=$HOME/.local/opt/airalarm/airalarm" ~/.local/share/applications/airalarm.desktop
