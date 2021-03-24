@ECHO OFF
set root=%~dp0\..\crmm_py
echo Activating Python Virtual Environment...
call %root%\Scripts\activate.bat
call activate %root%
echo hdb_env Activated!
call cd %~dp0
cmd /k
