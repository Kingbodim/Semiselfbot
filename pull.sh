if [[ $(git diff --name-only | wc -c) -ne 0 ]]
then
echo Update found, updating...
git add .
git stash
git pull https://Minehacker765:$GIT_TOKEN@github.com/Minehacker765/Semiselfbot &>/dev/null
else
echo Up to date!
fi
