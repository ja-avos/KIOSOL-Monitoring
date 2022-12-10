# Windows
#docker run --name mqtt -it -p 1883:1883 -p 9001:9001 -v "//$PWD:/mosquitto/config" eclipse-mosquitto

# Linux
docker run --name mqtt -it -p 1883:1883 -p 9001:9001 -v $(pwd):/mosquitto/config eclipse-mosquitto