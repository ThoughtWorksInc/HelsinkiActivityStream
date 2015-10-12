#!/bin/bash
ssh $USER@$IP_ADDRESS "sudo mkdir -p /var/helsinkiAS"
scp -r ../openahjo_activity_streams $USER@$IP_ADDRESS:/var/helsinkiAS
scp ../requirements.txt $USER@$IP_ADDRESS:/var/helsinkiAS
scp helsinkiAS.env $USER@$IP_ADDRESS:/var/helsinkiAS

ssh $USER@$IP_ADDRESS <<EOF
  sudo docker stop helsinki || echo 'Failed to stop helsinki container'
  sudo docker rm helsinki || echo 'Failed to remove helsinki container'
  sudo docker run -d -v /var/helsinkiAS/:/var/helsinkiAS \
                    --env-file=/var/helsinkiAS/helsinkiAS.env \
                    --name helsinki \
                    python:3.4.3 \
                    bash -c 'pip install -r /var/helsinkiAS/requirements.txt && \
                    python -m openahjo_activity_streams.scrape_to_coracle'
EOF