    #!/usr/bin/env bash
    curl https://raw.githubusercontent.com/skirpichenko/TigerAutoGL/main/containers/autogl/main.py > run.py
    echo "arguments:" "$@"
    python3 run.py "$@"