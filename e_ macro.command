
#!/bin/sh
cd "$(dirname "$0")"
source ./bin/activate
cd macro
python3 main.py
