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
task ./install-pkg python3.9 --allow-unauthenticated --allow-downgrades --allow-remove-essential --allow-change-held-packages
echo "Installing Python dist utils..."
task ./install-pkg python3.9-distutils --allow-unauthenticated --allow-downgrades --allow-remove-essential --allow-change-held-packages
wait
echo "Done!"
echo "Installing dependencies..."
task pip uninstall psutil -y
uns=$!
pipnstall aiofiles colorama gpytranslate flask chardet discord.py-self aiodns
wait $uns
pipnstall psutil
wait
echo "Done!"
task python3.9 ./setup.py
