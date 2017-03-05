# Shell script to build the Connect Four Linux executable.

pyinstaller \
    --clean --noconfirm --onefile \
    --log-level=WARN \
    --name=connectfour \
    --add-data="resources:resources" \
    run.py