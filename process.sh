#!/bin/sh

python inhaler.py
python ab2cb/ab2cb.py -o easylist.json processed/easylist.txt
python ab2cb/ab2cb.py -o easyprivacy.json processed/easyprivacy.txt
python ab2cb/ab2cb.py -o antisocial.json processed/antisocial.txt

cp *.json ../BlockBear/BlockBear/Resources/

cd ../BlockBear/BlockBear/Resources
rm blocklists.zip
zip blocklists.zip *.json
