cd /Users/zacheryfinley/Desktop/Extra\ Projects/findaforeclosure.github.io
git checkout main
git pull
git checkout -b weekly-update-$(date +%F)
rm -rf ./photos/*.jpg
rm -rf ./js/data.js
cd ./python
python3 findaforeclosure.py 4
git add js/data.js
git add photos/*.jpg
git add python/*.csv
git commit -m "$(date +%F)-update"
git push --set-upstream origin weekly-update-$(date +%F)
git checkout main
