# Workflow

# Local setup
My personal mac hasn't been used in a while so I had to:
- `brew upgrade` to bring everything up to date
- pyenv download 3.11 and set it globally for now for this
- Download docker desktop as it wasn't installed

## Docker
First things first, will the docker file build correctly `docker build -t app .`

It does buil

Now run it and make sure I can view the site `docker run -p 8000:8000 app`

All ok

## Minikube
Before I build the helm chart I will locally install minikube so I can test it:
- `brew install minikube`
I then found out this installs the amd64 version of minikube, not arm64, so:
- `curl -LO https://github.com/kubernetes/minikube/releases/latest/download/minikube-darwin-arm64`
- `sudo install minikube-darwin-arm64 /usr/local/bin/minikube`

## Push local docker image to minikube for speed
tell env to use docker on minikube
- `eval $(minikube docker-env)`
- `docker build -t pokemon-image .`

note - spent ages not realising the chart app version was being fed in to the pull instead of `latest`

## Update helm chart values
- updated liveness and readiness default values from http to 8000 as per dockerfile
- updated service from ClusterIP to LoadBalancer
- created minikube tunnel to expose app to world `minikube tunnel`
- deployed via helm and can browse locally to app

## Fork the repo so I can create Github Actions
note - at this point as this was my local machine I noticed autosave was not on and I lost a few thing, auto-save now on so plough forward again.
- repo forked
- github action added to build image
- changed github action to build and push to my own repo on dockerhub

## Considerations
- Any improvements to be made
- Security
   - App is running as root
- Monitoring
- Resiliency and Production Readiness