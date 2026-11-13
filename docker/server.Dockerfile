# BADASS micro-server image: all fixtures and runtimes, served on port 8808.
# Built by ./run.sh and ./update.sh on top of the regression image (Dockerfile).
ARG BASE=badass-lab:local
FROM ${BASE}

USER root
RUN apt-get update \
    && apt-get install -y --no-install-recommends openssl \
    && rm -rf /var/lib/apt/lists/*
COPY --chown=65532:65532 catalog/ /lab/catalog/
COPY --chown=65532:65532 labs/ /lab/labs/
COPY --chown=65532:65532 tools/ /lab/tools/

# Pinned dependency fixtures (lockfiles with integrity hashes); network only at build time.
RUN set -e; for case in vulnerable-dependency vulnerable-transitive-dependency; do \
      for variant in vulnerable fixed; do \
        npm ci --prefix "/lab/labs/node/$case/$variant" --install-links \
          --ignore-scripts --no-audit --no-fund --cache /tmp/npm-cache; \
      done; \
    done; rm -rf /tmp/npm-cache; chown -R 65532:65532 /lab/labs/node \
    && mkdir -p /lab/.build /opt/badass-build && chown 65532:65532 /lab/.build /opt/badass-build

USER 65532:65532
WORKDIR /lab
# Compile every native fixture once, so the container starts in seconds.
RUN python3 tools/netserve.py build --build-dir /opt/badass-build --named \
    && rm -rf /lab/.build/*
EXPOSE 8808 8443 2121 2122 2323 2525 3389 5353/tcp 5353/udp 6379 9001
HEALTHCHECK --interval=30s --timeout=5s --start-period=120s \
  CMD python3 -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8808/targets.json', timeout=4)"
ENTRYPOINT ["python3", "tools/netserve.py", "serve", "--host", "0.0.0.0", "--port", "8808", \
            "--build-dir", "/opt/badass-build"]
CMD ["--named", "--services"]
