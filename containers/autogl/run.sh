    #!/usr/bin/env bash
    #curl https://raw.githubusercontent.com/skirpichenko/TigerAutoGL/main/containers/autogl/main.py > run.py
    echo "passed arguments:" "$@"
    python3 main.py "$@"