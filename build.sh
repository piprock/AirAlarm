pyinstaller --add-data="data:data" --add-data "megaphone.svg:." airalarm.py
cp linux/* dist
cp LICENSE dist
name=airalarm_linux_v$1
mv dist "$name"
tar -zcvf "$name.tar.gz" "$name"
rm -r build
