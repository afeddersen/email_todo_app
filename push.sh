sudo -H find . -name "*.pyc" -exec rm -rf {} \;
git add --all
git commit -m 'new stuff'
git push -u google master
