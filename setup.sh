alias pip='python3.9 -m pip'
task(){
    $@ &>/dev/null &
}
pipnstall(){
    for e in "$@"
    do
        task pip install $e
    done
}
task ./install-pkg python3.9 --allow-unauthenticated --allow-downgrades --allow-remove-essential --allow-change-held-packages
task ./install-pkg python3.9-distutils --allow-unauthenticated --allow-downgrades --allow-remove-essential --allow-change-held-packages
wait
task pip uninstall psutil -y
uns=$!
pipnstall aiofiles colorama gpytranslate flask chardet discord.py-self aiodns
wait $uns
pipnstall psutil
python3.9 ./main.py
