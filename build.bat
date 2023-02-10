pyinstaller --onefile --noconsole -i win32\megaphone.ico src\airalarm.py
xcopy src\data dist\data\ /E
copy win32\root dist
copy LICENSE dist
set name=airalarm_windows_v%1
rename dist "%name%"
tar -cf "%name%.zip" "%name%"
rmdir /S /Q build
