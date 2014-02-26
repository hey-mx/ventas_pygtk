[Setup]
AppName=Control de Productos
AppVerName=Control de Productos 1.0
AppPublisher=Particular
DefaultDirName={pf}\Control de Productos
DefaultGroupName=Control de Productos
DisableProgramGroupPage=true
OutputBaseFilename=setup
Compression=lzma
SolidCompression=true
AllowUNCPath=false
VersionInfoVersion=1.0
VersionInfoCompany=me inc
VersionInfoDescription=Control de Productos


[Dirs]
Name: {app}; Flags: uninsalwaysuninstall;

[Files]
Source: dist\*; DestDir: {app}; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: {group}\Control de Productos; IconFilename: "{app}\System-Calc-icon.png"; Filename: {app}\puntoventa.exe; WorkingDir: {app}
Name: {commondesktop}\Control de Productos; IconFilename: "{app}\System-Calc-icon.png"; Filename: {app}\puntoventa.exe; WorkingDir: {app}

[Run]
; If you are using GTK's built-in SVG support, uncomment the following line.
;Filename: {cmd}; WorkingDir: "{app}"; Parameters: "/C gdk-pixbuf-query-loaders.exe > lib/gdk-pixbuf-2.0/2.10.0/loaders.cache"; Description: "GDK Pixbuf Loader Cache Update"; Flags: nowait runhidden
Filename: {app}\puntoventa.exe; Description: {cm:LaunchProgram,Control de Productos}; Flags: nowait postinstall skipifsilent
