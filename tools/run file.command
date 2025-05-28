
#!/bin/sh
read -p "Enter file name: " filename
cd "$(dirname "$0")"
cd ..
if [ -d bin ]; then
   source ./bin/activate
   printf "activating virtual environment"
fi
cd src

runPython() {
	if command -v $1 >/dev/null 2>&1; then
		echo "Trying to run macro with $1"
		$1 $filename
	fi

}
runPython python3.9
