clear
if ! [ -x "$(command -v python3.9)" ]
then
    echo "Python 3.9 is not installed! Installing it..."
    bash setup.sh
fi
python3.9 main.py
