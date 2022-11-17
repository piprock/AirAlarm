set -e
pyinstaller --add-data="src/data:data" --add-data "linux/megaphone.svg:." src/airalarm.py
cp linux/root/* dist
cp LICENSE dist
name=airalarm_linux_v$1
mv dist "$name"
tar -zcvf "$name.tar.gz" "$name"
rm -r build
