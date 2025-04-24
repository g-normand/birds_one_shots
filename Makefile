### Configure paths. ###
PROJECT_PATH := $(CURDIR)
ENV_PATH := $(CURDIR)/one_shots_env
PYTHON := $(ENV_PATH)/bin/python3.9
TAG_NAME := DEPLOY
TAG_DATE := $(TAG_NAME)_$(shell date -u "+%Y_%m_%d_%H_%M_%S")

### Shell configure. ###
# For shell to bash to be able to use source.
SHELL = /bin/bash

# Shortcut to set env command before each python cmd.
VENV = source $(ENV_PATH)/bin/activate

# Config is based on two environment files, initalized here.
virtualenv: $(ENV_PATH)/bin/activate

$(ENV_PATH)/bin/activate:
	virtualenv -p /usr/bin/python3.9 $(ENV_PATH)

### Manage project installation. ###
# Install python requirements.
pip: virtualenv
	$(VENV) && cd $(CURDIR) && pip3 install -r $(CURDIR)/requirements.txt;

clean:
	find . -name '*.pyc' -delete

serve_big_day:
	$(VENV) && python3 big_day.py $(ARGS)

