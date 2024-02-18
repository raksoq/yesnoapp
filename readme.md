# YESNO App , docker, helm, redis

## Update structure based on best practices

https://medium.com/code-factory-berlin/github-repository-structure-best-practices-248e6effc405

```bash
docker buildx create --name multiarch-builder --driver docker-container --use

docker buildx inspect multiarch-builder --bootstrap

docker buildx ls

docker buildx build -f .build/Dockerfile  --platform linux/amd64,linux/arm64 -t oskarq/yesnoapp:redis-helm-structo --push .
```

## helm install
```bash

helm install yesnoapp ./.config/yesnoapp --namespace yesnoapp --create-namespace

helm upgrade yesnoapp ./.config//yesnoapp

helm delete yesnoapp
```

## redis secret creation
`kubectl create secret generic redis-secret --from-literal=redis-password=redis-passw0rd -n yesnoapp`

## lint
`helm lint ./.config//yesnoapp`

