#!/bin/bash

strt=$(date +%s)

home="https://infrastructure.fedoraproject.org/infra/rabbitmq-certs"
stagcert_location="$home/staging"
prodcert_location="$home/production"

rm -rf ./certificates/staging
rm -rf ./certificates/production

mkdir -p ./certificates/staging
mkdir -p ./certificates/production

curl -o ./certificates/staging/expiration.txt "$stagcert_location/expiration.txt"
curl -o ./certificates/production/expiration.txt "$prodcert_location/expiration.txt"

cat ./certificates/staging/expiration.txt | while read line; do echo $line | cut -d " " -f 1 | sed "s/$/.crt/" >> ./certificates/staging/staging_certlist.txt; done
cat ./certificates/production/expiration.txt | while read line; do echo $line | cut -d " " -f 1 | sed "s/$/.crt/" >> ./certificates/production/production_certlist.txt; done

cat ./certificates/staging/staging_certlist.txt | while read line; do curl -s -S -o ./certificates/staging/$line "$stagcert_location/$line"; done
cat ./certificates/production/production_certlist.txt | while read line; do curl -s -S -o ./certificates/production/$line "$prodcert_location/$line"; done

stop=$(date +%s)

echo "Operation took $(($stop-$strt)) seconds to complete"
