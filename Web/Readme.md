docker build -t webapi .  # build cointainer
docker images -a # all images
docker ps # get runing containers
docker run -d -p 8000:8000 webapi #background run
docker run -p 8000:8000 webapi #terminal run
docker image prune #delete unuses images

docker run -i -t web-api:latest /bin/bash #goto container terminal