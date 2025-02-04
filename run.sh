#!/bin/bash
(cd ~/src/is-network-up/ && eval $(~/.local/bin/poetry env activate) && src/main.py) >> ~/is-network-up.log 2>&1

