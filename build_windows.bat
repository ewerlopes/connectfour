REM Batch script to build the Connect Four Windows executable.
REM The resulting "connectfour.exe" executable will be available in the "dist" directory.

@ECHO off

pyinstaller ^
    --clean --noconfirm --onefile --windowed ^
    --log-level=WARN ^
    --name=connectfour ^
    --icon="resources/images/icon.ico" ^
    --add-data="resources;resources" ^
    run.py