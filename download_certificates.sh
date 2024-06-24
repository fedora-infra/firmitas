#!/bin/bash

strt=$(date +%s)

home="https://infrastructure.fedoraproject.org/infra/rabbitmq-certs/"
stag="staging/"
prod="production/"

mkdir /etc/firmitas/

cat "certificates.txt" | while read line
do
	if [[ "" != $line ]]
	then
		if [[ $line =~ "stg" ]]
		then
			link=$home$stag$line
			echo "[STAG] [$(date +%Y%m%d-%H%M%S%Z)] Downloading '$line' from '$link' ..."
		else
			link=$home$prod$line
			echo "[PROD] [$(date +%Y%m%d-%H%M%S%Z)] Downloading '$line' from '$link' ..."
		fi
		curl -s -S -o "/etc/firmitas/$line" -L "$link"
	fi
done

stop=$(date +%s)

echo "Operation took $(($stop-$strt)) seconds to complete"
