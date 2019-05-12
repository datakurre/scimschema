PYTHON ?= python3

.PHONY: all
all: test

.PHONY: .coverage
.coverage:
	coverage run setup.py test

.PHONY: coverage
coverage: .coverage
	coverage report --fail-under=40

.PHONY: coveralls
coveralls: .coverage
	coveralls

.PHONY: test
test:
ifeq ($(PYTHON), python3)
	black -t py27 -t py36 -t py37 --check src tests
endif
	pylama src tests
	pytest tests

nix-%:
	nix-shell --argstr python $(PYTHON) \
	setup.nix -A develop --run "$(MAKE) $*"

.PHONY: nix-shell
nix-shell:
	nix-shell --pure --argstr python $(PYTHON) \
	setup.nix -A develop

.PHONY: format
format:
ifeq ($(PYTHON), python3)
	black -t py27 src tests
endif
	isort -rc -y src tests

.PHONY: requirements
requirements: requirements-$(PYTHON).nix

requirements-$(PYTHON).nix: requirements.txt
	@nix-shell -p libffi \
	--run 'nix-shell setup.nix -A pip2nix --argstr python $(PYTHON) \
	--run "pip2nix generate -r requirements.txt \
	--output=requirements-$(PYTHON).nix"'
	@grep "name" requirements-$(PYTHON).nix |grep -Eo "\"(.*)\""|grep -Eo "[^\"]+"|sed -r "s|-([0-9\.]+)|==\1|g">requirements-$(PYTHON).txt

.PHONY: setup.nix
setup.nix:
	@echo "Updating nixpkgs 19.03 revision"; \
	rev=$$(curl https://api.github.com/repos/NixOS/nixpkgs-channels/branches/nixos-19.03|jq -r .commit.sha); \
	echo "Updating nixpkgs $$rev hash"; \
	sha=$$(nix-prefetch-url --unpack https://github.com/NixOS/nixpkgs-channels/archive/$$rev.tar.gz); \
	sed -i "2s|.*|    url = \"https://github.com/NixOS/nixpkgs-channels/archive/$$rev.tar.gz\";|" setup.nix; \
	sed -i "3s|.*|    sha256 = \"$$sha\";|" setup.nix;
	@echo "Updating setup.nix version"; \
	rev=$$(curl https://api.github.com/repos/datakurre/setup.nix/branches/master|jq -r ".commit.sha"); \
	echo "Updating setup.nix $$rev hash"; \
	sha=$$(nix-prefetch-url --unpack https://github.com/datakurre/setup.nix/archive/$$rev.tar.gz); \
	sed -i "6s|.*|    url = \"https://github.com/datakurre/setup.nix/archive/$$rev.tar.gz\";|" setup.nix; \
	sed -i "7s|.*|    sha256 = \"$$sha\";|" setup.nix

.PHONY: upgrade
upgrade:
	nix-shell --pure -p curl gnumake jq nix --run "make setup.nix"
