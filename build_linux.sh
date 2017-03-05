# Shell script to build the Connect Four Linux executable.
# The resulting "connectfour.app" executable and "connectfour" script will be available in the "dist" directory.

pyinstaller \
    --clean --noconfirm --onefile \
    --log-level=WARN \
    --name=connectfour \
    --add-data="resources:resources" \
    run.py