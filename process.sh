#!/bin/sh

python inhaler.py
python ab2cb/ab2cb.py -o json/easylist.json processed/easylist.txt
python ab2cb/ab2cb.py -o json/easyprivacy.json processed/easyprivacy.txt
python ab2cb/ab2cb.py -o json/antisocial.json processed/antisocial.txt

rm blocklists.zip
zip blocklists.zip json/*.json
cp blocklists.zip ../BlockBear/BlockBear/Resources/
