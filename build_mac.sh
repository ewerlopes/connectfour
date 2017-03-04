# Shell script to build the Connect Four Mac OS executable.
# The resulting "connectfour.app" executable and "connectfour" script will be available in the "dist" directory.

pyinstaller ^
    --clean --noconfirm --onefile --windowed \
    --log-level=WARN \
    --name=connectfour \
    --icon="resources/images/icon.icns" \
    --add-data="resources;resources" \
    --osx-bundle-identifier-"fr.epoc.python.games.connectfour" \
    run.py