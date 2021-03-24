@ECHO OFF
set root=%1
echo Activating Python Virtual Environment...
call %root%\Scripts\activate.bat
call activate %root%
echo hdb_env Activated!
call cd %~dp0
echo Starting CRMMS plots generation...
set errorlevel = %errorlevel%
python crmms_viz_gen.py --config %2 -P --output %3
echo Process Complete!
exit /b 