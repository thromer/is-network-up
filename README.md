# is-network-up
report network status to a cloud observability provider

# bootstrap

* install gcloud CLI https://cloud.google.com/sdk/docs/install#deb
* gcloud init  # If no display, paste the initial URL into a browser, grab the final URL and open it on the local machine
* gcloud auth application-default login  # As above
* sudo apt -y install pipx
* pipx ensurepath
* pipx install poetry
* eval $(poetry env activate)
* poetry install


