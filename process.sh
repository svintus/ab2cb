#!/bin/sh

python ab2cb/ab2cb.py easylist.txt > easylist.json
python ab2cb/ab2cb.py easyprivacy.txt > easyprivacy.json
python ab2cb/ab2cb.py antisocial.txt > antisocial.json

cp *.json ../BlockBear/BlockBear/Resources/

cd ../BlockBear/BlockBear/Resources
rm blocklists.zip
zip blocklists.zip *.json
