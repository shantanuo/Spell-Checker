With docker 

docker run -p 5000:5000 -d shantanuo/flaskspell
_____

If you are using ARM processor, use these 4 commands instead:

git clone https://github.com/shantanuo/Spell-Checker.git

cd Spell-Checker/

docker build -t shantanuo/flaskspellarm .

docker run  --restart unless-stopped -p 5000:5000 -d shantanuo/flaskspellarm


