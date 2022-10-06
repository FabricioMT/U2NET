Dim CurDir
Set WshShell = CreateObject("WScript.Shell") 
CurDir = WshShell.CurrentDirectory
WshShell.Run chr(34) & CurDir & "\hide_exec.bat" & Chr(34), 0
Set WshShell = Nothing