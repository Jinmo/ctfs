#!/bin/sh

commit=b4d321bbf306528f85f4cd08dd3bcb3c6a4d63fe

echo Downloading proxmark3...
wget https://github.com/Proxmark/proxmark3/archive/$commit.zip -O proxmark3.zip

echo Unzipping files...
unzip -q -o proxmark3.zip

cd proxmark3-$commit
echo Patching files...
patch client/cmddata.c ../proxmark3.diff && make -j5

echo Executing decoder...
(
	echo data printdemodbuff h
	echo data rawdemod am
	) | client/proxmark3 nonexistent_file
echo Flag is Unique TAG ID