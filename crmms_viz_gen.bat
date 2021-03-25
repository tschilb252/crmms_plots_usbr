@ECHO OFF
set root=%1
echo Activating Python Virtual Environment...
call %root%\Scripts\activate.bat
call activate %root%
echo hdb_env Activated!
set wd=%~dp0
call cd wd
echo Starting CRMMS plots generation...
python crmms_viz_gen.py --config %2 --output %3 --config_path %4 --provisional 1>%wd%/logs/run_all.out 2>%wd%/logs/run_all.err
echo Process Complete!
exit %errorlevel%