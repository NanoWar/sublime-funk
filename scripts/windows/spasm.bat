@echo off

if "%1" == """" (
	echo Error: File could not be opened
	goto END
)

echo # Starting SPASM TI83+ build script ...

if defined ProgramFiles(x86) (
	set bit=64
) else (
	set bit=32
)
set Compiler=%~dp0\..\..\funk\spasm\spasm-win%bit%.exe

"%Compiler%" "%1" "%~n1.8xp"

:END
set errorlevel=0