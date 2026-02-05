#!/bin/sh

# kill all python processes
pkill -9 Python
pkill -9 Python3
pkill -9 Python3.9
pkill -9 Python3.8
pkill -9 Python3.7

VENV_NAME="bss-macro-env"
VENV_PATH="$HOME/$VENV_NAME"

# force Python to use certifi for SSL (fixes Discord/aiohttp on macOS)
export SSL_CERT_FILE="$VENV_PATH/lib/python3.9/site-packages/certifi/cacert.pem"

# get system information
chip=$(arch)
os_ver=$(sw_vers -productVersion)

python_ver="3.9"
if [ "$chip" = "i386" ]; then
    if echo -e "$os_ver\n10.15.0" | sort -V | tail -n1 | grep -Fq "10.15.0"; then
        python_ver="3.7"
        printf "Correct python ver: 3.7\n"
    elif echo -e "$os_ver\n12.0.0" | sort -V | tail -n1 | grep -Fq "12.0.0"; then
        python_ver="3.8"
        printf "Correct python ver: 3.8\n"
    fi
fi

cd "$(dirname "$0")"

runPython() {
    echo "Loading macro with $1..."
    $1 main.py
}

cd src
if [ -d "$VENV_PATH" ]; then
    source "$VENV_PATH/bin/activate"
    printf "activating virtual environment\n"
    python --version
    runPython python
else
    runPython python3.7
    runPython python3.8
    runPython python3.9
fi