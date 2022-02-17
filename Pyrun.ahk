#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
; #Warn  ; Enable warnings to assist with detecting common errors.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.

#Enter::
TempFile=%A_Temp%\pyrun_temp.txt ; Define temp file
RunWait %comspec% /c "python pyrun.py > %TempFile%",,Hide
