## Repo Inspector - AI Plugin

## Usage in ChatGPT
* Install an unverified plugin with the following domain: `https://repoinspector.onrender.com`
* Enable the plugin
* Ask ChatGPT about a GitHub repo (e.g. `Tell me about this Git Repo https://github.com/mattlgroff/estimation-party.git`)
* Ask follow ups about tech stack, what dependencies it needs to run, how to install, etc.
### Local Development

```bash
docker build -t repo-inspector . -f Dockerfile.dev

docker run -v $(pwd):/app -p 5000:5000 repo-inspector
```