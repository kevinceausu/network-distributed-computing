@echo off
set /p count=How many servers do you want to start? 

set i=1

:loop
if %i% GTR %count% goto done

start "Server%i%" cmd /k py s.py %i%

set /a i+=1
goto loop

:done
py c.py
pause