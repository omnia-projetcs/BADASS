LAB_ARGS ?= test --strict --output reports/container-regression.json
.PHONY: validate test test-strict unit smoke docs coverage container-build container-test dependency-prepare dependency-test
dependency-prepare:
	@set -e; for case in vulnerable-dependency vulnerable-transitive-dependency; do \
	  for variant in vulnerable fixed; do \
	    npm ci --prefix "labs/node/$$case/$$variant" --install-links \
	      --ignore-scripts --no-audit --no-fund --cache "$(CURDIR)/.build/npm-cache"; \
	  done; \
	done
dependency-test:
	node labs/node/dependency-regression.cjs
validate:
	python3 tools/lab.py validate
test:
	python3 tools/lab.py test --output reports/regression.json
test-strict:
	python3 tools/lab.py test --strict --output reports/regression.json
unit:
	python3 -m unittest discover -s tests -v
smoke:
	python3 tools/smoke.py --output reports/smoke.json
docs:
	python3 tools/render_docs.py
coverage:
	python3 tools/lab.py coverage --output reports/coverage.json
container-build:
	docker build -t badass-lab:local .
container-test:
	mkdir -p reports .build
	docker run --rm --network none --read-only --cap-drop ALL \
	  --security-opt no-new-privileges --pids-limit 256 --memory 2g --cpus 2 \
	  --env PYTHONUNBUFFERED=1 \
	  --user "$$(id -u):$$(id -g)" \
	  --mount type=bind,src="$(CURDIR)",dst=/lab,readonly \
	  --mount type=bind,src="$(CURDIR)/reports",dst=/lab/reports \
	  --tmpfs /tmp:rw,nosuid,size=256m \
	  --tmpfs /lab/.build:rw,exec,nosuid,mode=1777,size=1g \
	  badass-lab:local $(LAB_ARGS)
