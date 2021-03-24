@ECHO OFF
set root=%1
echo Activating Python Virtual Environment...
call %root%\Scripts\activate.bat
call activate %root%
echo hdb_env Activated!
call cd %~dp0
echo Starting CRMMS plots generation...
python crmms_viz_gen.py --config %2 --output %3 --config_path %4 --provisional
echo Process Complete!
exit %errorlevel%