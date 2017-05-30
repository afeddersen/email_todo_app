# Simple shell script to push new changes and delete .pyc files

sudo -H find . -name "*.pyc" -exec rm -rf {} \;
git add --all
git commit -m 'witty commit message'
git push -u origin master
