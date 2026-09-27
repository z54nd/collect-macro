#define MyAppName "CollectMacro"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "Z54ND"
#define MyAppExeName "CollectMacro.exe"

[Setup]
AppId={{C8E6F5D7-6A6C-4E9A-9D3E-CollectMacro}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\CollectMacro
DefaultGroupName={#MyAppName}
OutputDir=installer
OutputBaseFilename=CollectMacro-Setup
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin
SetupIconFile=collect_macro.ico
UninstallDisplayIcon={app}\{#MyAppExeName}

[Files]
Source: "dist\CollectMacro.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\CollectMacro"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\CollectMacro"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\{#MyAppExeName}"

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Launch CollectMacro"; Flags: nowait postinstall skipifsilent
