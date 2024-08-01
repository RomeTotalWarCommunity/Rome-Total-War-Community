@echo off

for /f "delims=" %%f in ('dir /b "%~dp0*.cas"') do (
    casconv.exe -i "%~dp0%%f" -f fbx
)
pause
cmd /k
