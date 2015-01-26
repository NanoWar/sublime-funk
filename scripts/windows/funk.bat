@echo off

if "%1" == """" (
	echo Error: File could not be opened
	goto END
)

if "%2" == "" (
	"%~dp0..\..\funk\build.bat" %1
) else (
	rem Goto sublime project directory and look for configuration there...
	if exist %2\funk.config (
		cd %2
		"%~dp0..\..\funk\build.bat" %1
	) else (
		"%~dp0..\..\funk\build.bat" %1
	)
)

:END