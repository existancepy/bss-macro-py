
#!/bin/sh
pkill -9 Python
pkill -9 Python3
pkill -9 Python3.9
pkill -9 Python3.8
pkill -9 Python3.7
cd "$(dirname "$0")"
if [ -d bin ]; then
   source ./bin/activate
fi
cd macro
python3 main.py
