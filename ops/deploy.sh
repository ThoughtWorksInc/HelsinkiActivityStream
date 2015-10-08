#!/bin/bash

ssh $USER@$IP_ADDRESS <<EOF
cd /var/helsinkiAS/

CORACLE_TIMESTAMP_ENDPOINT=http://coracle.herokuapp.com/latest-published-timestamp \
OPENAHJO_ENDPOINT=http://dev.hel.fi/paatokset/v1/agenda_item/ \
CORACLE_POST_ACTIVITY_ENDPOINT=http://coracle.herokuapp.com/activities \
BEARER_TOKEN=$BEARER_TOKEN \
nohup python3 -m openahjo_activity_streams.scrape_to_coracle > helsinkiAS.log 2> helsinkiAS.err&
EOF