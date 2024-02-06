```bash
docker buildx create --name multiarch-builder --driver docker-container --use

docker buildx inspect multiarch-builder --bootstrap

docker buildx ls

docker buildx build --platform linux/amd64,linux/arm64 -t oskarq/yesnoapp:redis-helm --push .
```

## helm install
```bash
helm install yesnoapp ./yesnoapp
helm upgrade yesnoapp ./yesnoapp
```