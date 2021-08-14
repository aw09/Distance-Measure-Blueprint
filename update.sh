NAME="distance-measure" && \
docker build --rm -t $NAME . && \
docker rm -f $NAME && \
docker run -d --restart always -p 5000:5000 --name $NAME $NAME
