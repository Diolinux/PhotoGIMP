@echo off

echo "Instalation started..."
mkdir %userprofile%/.gimp-2.10./AppData/Roaming/Gimp/2.10/
xcopy /s "%~dp0/.var./app/org.gimp.GIMP/config/GIMP/2.10/" "%userprofile%/.gimp-2.10./AppData/Roaming/Gimp/2.10/"

echo "Instalation finished..."




