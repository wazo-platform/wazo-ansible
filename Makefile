# use this hubname by default to be compatible with zuul jobs for
# wazo-c4
HUBNAME=wazopbx

ROLES := $(shell ls -d roles/*/docker | sed -e 's@/docker@@g' -e 's@roles/@@g')
IMAGES := $(addsuffix .image,$(ROLES))

# the default target should build the images to be compatible with the
# zuul wazo-c4-build-test-template job
build: $(IMAGES)

%.image : %
	HUBNAME=$(HUBNAME) ./bin/role2docker $<
	touch $@

clean:
	-docker rmi $(HUBNAME)/base
	rm -f $(IMAGES)

venv:
	virtualenv -p python3 venv --no-site-packages

setup:
	pip install -r requirements.txt

.PHONY: clean build setup $(ROLES)
