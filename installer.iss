; EquationGenerator Installer
; Inno Setup Script

[Setup]
AppName=Генератор уравнений и неравенств
AppVersion=1.0
AppPublisher=Kango911 *K9-Team*
DefaultDirName={pf}\EquationK9Generator
DefaultGroupName=EquationK9Generator
UninstallDisplayIcon={app}\EquationK9Generator.exe
Compression=lzma2
SolidCompression=yes
OutputDir=.
OutputBaseFilename=EK9G_Setup
WizardStyle=modern
Uninstallable=yes
CreateUninstallRegKey=yes

[Files]
; Основной исполняемый файл
Source: "dist\EquationK9Generator.exe"; DestDir: "{app}"; Flags: ignoreversion

; Если есть дополнительные файлы (README, иконка и т.д.)
; Source: "icon.ico"; DestDir: "{app}"; Flags: ignoreversion
; Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
; Ярлык в меню Пуск
Name: "{group}\Генератор уравнений"; Filename: "{app}\EquationGenerator.exe"
; Ярлык на рабочем столе
Name: "{autodesktop}\Генератор уравнений"; Filename: "{app}\EquationGenerator.exe"

[Run]
; Запуск программы после установки (опционально)
Filename: "{app}\EquationGenerator.exe"; Description: "Запустить приложение"; Flags: postinstall nowait skipifsilent

[UninstallDelete]
; Удаление папки приложения
Type: filesandordirs; Name: "{app}"