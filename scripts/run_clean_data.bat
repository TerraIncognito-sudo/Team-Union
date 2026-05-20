@echo off
setlocal

set "REPO_ROOT=%~dp0.."
set "ANACONDA_PYTHON=%USERPROFILE%\anaconda3\python.exe"

if not exist "%ANACONDA_PYTHON%" (
    echo Anaconda Python was not found at "%ANACONDA_PYTHON%"
    exit /b 1
)

pushd "%REPO_ROOT%"
"%ANACONDA_PYTHON%" -m src.clean_data
set "EXIT_CODE=%ERRORLEVEL%"
popd

exit /b %EXIT_CODE%
