
#!/bin/sh
read -p "Enter file name: " filename
cd "$(dirname "$0")"
cd ..
cd macro

if test -f "$filename"; then
    echo "$filename exists."
else
    echo "$filename does not exist"
fi
