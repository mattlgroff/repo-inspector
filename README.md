## Repo Inspector - AI Plugin

### Local Development

```bash
docker build -t repo-inspector . -f Dockerfile.dev

docker run -v $(pwd):/app -p 5000:5000 repo-inspector
```