alias pip='python3.9 -m pip'
task(){
    $@ &>/dev/null &
}
pipnstall(){
    for e in "$@"
    do
        task pip install $e
        echo "Installing $e..."
    done
}
echo "Installing Python 3.9..."
task install-pkg python3.9 -y
pth=$!
echo "Installing Python dist utils..."
task install-pkg python3.9-distutils -y
#echo "Installing Tesseract..."
#task install-pkg tesseract -y
wait $pth
echo "Done!"
echo "Installing dependencies..."
task python3.9 -m pip uninstall psutil -y
uns=$!
pipnstall aiofiles colorama gpytranslate flask chardet discord.py-self aiodns
wait $uns
pipnstall psutil
wait
echo "Done!"
task python3.9 ./setup.py
