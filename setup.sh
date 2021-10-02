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
task install-pkg python3.9 -y
task install-pkg python3.9-distutils -y
wait
task pip uninstall psutil -y
uns=$!
pipnstall aiofiles colorama flask chardet discord.py-self aiodns
wait $uns
pipnstall psutil
