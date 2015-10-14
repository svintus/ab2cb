#!/bin/sh

mkdir -p update

wget https://easylist-downloads.adblockplus.org/easylist.txt -O update/easylist.txt
wget https://easylist-downloads.adblockplus.org/easyprivacy.txt -O update/easyprivacy.txt
wget https://easylist-downloads.adblockplus.org/fanboy-social.txt -O update/antisocial.txt
