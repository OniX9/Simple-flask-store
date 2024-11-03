#How to run Dockerfile locally 

## 1. Build Docker image:
### Skip this step if already run before.
```
docker build -t "flask_deployment_image" .
```

## 2. Run Docker container from the image:
```
docker run -dp 5007:5000 -w /app -v '$(pwd):/app' flask_deployment_image sh -c "flask run"
```

## 3. Rename Docker container:
```
docker rename '<container_autogen_name> simple_flask_store
```