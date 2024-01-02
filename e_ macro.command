
#!/bin/sh

cd "$(dirname "$0")"
if [ -d bin ]; then
   source ./bin/activate
fi
cd macro
python3 main.py
