if [[ $(git diff --name-only origin/main) ]]
then
echo Update found, updating...
git pull https://Minehacker765:$GIT_TOKEN@github.com/Minehacker765/Semiselfbot &>/dev/null
fi
