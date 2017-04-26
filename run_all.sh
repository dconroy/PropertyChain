#!/bin/bash
DIR="$(pwd)"
BC="$DIR/blockchain"
NETWORK_PEER="dev-"
OPERATING_ENV="hyperledger"
NPM_SCRIPT="start"

printf "#################################################\n"
printf "#####  HYPERLEDGER FABRIC V0.6 DEMO SCRIPT  #####\n"
printf "#################################################\n\n"

clear_all() {
# clear chaincode 
  printf "clearing blockchain directory: $BC \n"
  rm -rf $BC/deployLocal/* 2>/dev/null
  printf "keyValStore removed\n"
  printf "Latest deployed removed\n"

# clear out docker containers and images 
  docker rm -f $(docker ps -a -q) 2>/dev/null
  printf "All docker containers removed\n"
  docker rmi -f `docker images | grep $NETWORK_PEER | awk '{print $3}'` 2>/dev/null
  docker rmi -f `docker images | grep $OPERATING_ENV | awk '{print $3}'` 2>/dev/null
  printf "All images removed\n"
  docker rmi $(docker images -qf "dangling=true") 2>/dev/null
  printf "All untagged images removed\n"

#  pull fabric V0.6 images 
  docker pull hyperledger/fabric-peer:x86_64-0.6.1-preview
  docker pull hyperledger/fabric-membersrvc:x86_64-0.6.1-preview
  docker pull hyperledger/fabric-baseimage:x86_64-0.2.1
  docker tag hyperledger/fabric-baseimage:x86_64-0.2.1 hyperledger/fabric-baseimage:latest
  docker images

# build node.js modules 
  if [ -d "node_modules" ]; then
printf "Remove modules directory\n" 
  fi
printf "Build modules directory\n" 
  npm install
}

ask() {
  local response
  local msg="${1:-$1} [y/N] "; shift
  read -r $4 -p "$msg" response || echo
  case "$response" in
    [yY][eE][sS]|[yY]) $1 ;;
    *) $2 ;;
  esac
}

ask "Do you want to clear the environment?" clear_all return

# run docker-compose
docker-compose up -d 2>/dev/null
printf "Starting docker containers...\n"
sleep 10
printf "Docker containers up and running\n"
printf "Hit ctrl+c to stop\n"

# start server, catch ctrl+c to clean up
trap 'kill -TERM "$PID" 2>/dev/null' SIGINT
npm run $NPM_SCRIPT &
PID=$!
wait $PID

exit 0

