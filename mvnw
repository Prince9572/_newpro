#!/bin/sh
# Maven Wrapper Executable Script
export JAVA_HOME=${JAVA_HOME:-/Library/Java/JavaVirtualMachines/jdk-24.jdk/Contents/Home}

# If system maven is available, use it directly
if command -v mvn >/dev/null 2>&1; then
    exec mvn "$@"
fi

# Fallback: check brew or system paths
for M2_PATH in /usr/local/Cellar/maven/*/bin/mvn /opt/homebrew/bin/mvn /usr/share/maven/bin/mvn; do
    if [ -f "$M2_PATH" ]; then
        exec "$M2_PATH" "$@"
    fi
done

echo "Error: Maven is not installed locally. Please run via Docker (docker-compose up) or install Maven (brew install maven)."
exit 1
