FROM mcr.microsoft.com/dotnet/sdk:8.0-bookworm-slim

# Build tools are installed once; regression execution needs no external network.
RUN apt-get update \
    && apt-get install -y --no-install-recommends python3 gcc g++ golang-go \
       php-cli ruby rustc nodejs npm default-jdk-headless ca-certificates \
    && npm install --global typescript@5.6.3 \
    && rm -rf /var/lib/apt/lists/*

# Real SQLite drivers for every SQL injection fixture. Network access is needed
# only while building the image; the benchmark itself still runs offline.
RUN apt-get update \
    && apt-get install -y --no-install-recommends libsqlite3-dev php-sqlite3 \
       node-sqlite3 ruby-sqlite3 libxerial-sqlite-jdbc-java \
       golang-github-mattn-go-sqlite3-dev \
    && rm -rf /var/lib/apt/lists/*
COPY labs/dotnet/sql-injection/fixed/Lab.csproj /opt/sqlite-restore/Lab.csproj
RUN dotnet restore /opt/sqlite-restore/Lab.csproj \
       --packages /opt/nuget/packages --property:NuGetAudit=false \
    && mkdir -p /opt/nuget/feed \
    && chmod -R a+rX /opt/nuget
ENV DOTNET_CLI_TELEMETRY_OPTOUT=1 \
    DOTNET_SKIP_FIRST_TIME_EXPERIENCE=1 \
    DOTNET_NOLOGO=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    BADASS_NUGET_PACKAGES=/opt/nuget/packages \
    BADASS_NUGET_SOURCE=/opt/nuget/feed
WORKDIR /lab
USER 65532:65532
ENTRYPOINT ["python3", "tools/lab.py"]
CMD ["test", "--strict", "--output", "reports/container-regression.json"]
