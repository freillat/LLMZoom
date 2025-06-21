pip install fastembed

pip install -q "qdrant-client[fastembed]>=1.14.2"



Docker
All you need to do is pull the image and start the container using the following commands:

docker pull qdrant/qdrant

docker run -p 6333:6333 -p 6334:6334 \
   -v "$(pwd)/qdrant_storage:/qdrant/storage:z" \
   qdrant/qdrant
The second line in the docker run command mounts local storage to keep your data persistent. So even if you restart or delete the container, your data will still be stored locally.

6333 – REST API port
6334 – gRPC API port
To help you explore your data visually, Qdrant provides a built-in Web UI, available in both Qdrant Cloud and local instances. You can use it to inspect collections, check system health, and even run simple queries.

When you're running Qdrant in Docker, the Web UI is available at http://localhost:6333/dashboard