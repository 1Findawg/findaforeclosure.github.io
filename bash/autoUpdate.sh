cd /Users/zacheryfinley/Desktop/Extra Projects/findaforeclosure.github.io
git checkout main
git pull
rm -rf ../photos/*.jpg
rm -rf ../js/data.js
python3 ../python/findaforeclosure.py 4
git commit -m "$(date +%F)-update"
git push
