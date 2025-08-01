
#!/bin/sh
#kill all python processes
pkill -9 Python
pkill -9 Python3
pkill -9 Python3.9
pkill -9 Python3.8
pkill -9 Python3.7

VENV_NAME="bss-macro-env"
VENV_PATH="$HOME/$VENV_NAME"

#get system information
chip=$(arch)
os_ver=$(sw_vers -productVersion)

python_ver="3.9"
if [ $chip = 'i386' ]; then
	if echo -e "$os_ver \n10.15.0" | sort -V | tail -n1 | grep -Fq "10.15.0"; then
		python_ver="3.7"
		printf "Correct python ver: 3.7"
	elif echo -e "$os_ver \n12.0.0" | sort -V | tail -n1 | grep -Fq "12.0.0"; then
		python_ver="3.8"
		printf "Correct python ver: 3.8"
	fi
fi

cd "$(dirname "$0")"



runPython() {
	if command -v $1 >/dev/null 2>&1; then
		echo "Loading macro with $1..."
		python_output=$($1 main.py 2>&1)
		if echo "$python_output" | grep -i "operation not permitted" > /dev/null; then
			osascript -e "display dialog \"Terminal does not have the 'full disk access' permission.\" & return & \"Instructions on enabling it can be found at https://existance-macro.gitbook.io/existance-macro-docs/tutorial/images-and-media/3.-terminal-permissions\" with title \"Permission Error\" buttons {\"OK\"} default button \"OK\" with icon caution"
		fi
		$1 main.py
	fi
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
