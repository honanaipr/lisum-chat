source .env

docker run -it --rm -d \
    -e REDMINE_URL=${REDMINE_URL} \
    -e REDMINE_KEY=${REDMINE_KEY} \
    -e BOT_TOKEN=${BOT_TOKEN} \
    -e DATABASE_PATH=${DATABASE_PATH} \
    --volume=./data:/data \
lisum_chat
