#!/bin/bash
export DEBIAN_FRONTEND=noninteractive
apt-get update -qq && apt-get install -y -qq openjdk-8-jdk > /dev/null
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
export PATH=$JAVA_HOME/bin:/defects4j/framework/bin:$PATH

if ! command -v defects4j &> /dev/null; then
    D4J_PATH=$(find / -name defects4j -type f -executable 2>/dev/null | grep bin | head -n 1 | xargs -r dirname)
    if [ ! -z "$D4J_PATH" ]; then
        export PATH=$PATH:$D4J_PATH
    fi
fi

defects4j checkout -p Lang -v 1b -w /tmp/Lang_1_buggy
cd /tmp/Lang_1_buggy
defects4j compile > /dev/null
defects4j test > /dev/null || true

defects4j checkout -p Lang -v 1f -w /tmp/Lang_1_fixed
cd /tmp/Lang_1_fixed
defects4j compile > /dev/null
defects4j test > /dev/null || true

echo "==== BUGGY TEST LOG ===="
if [ -f /tmp/Lang_1_buggy/failing_tests ]; then
    cat /tmp/Lang_1_buggy/failing_tests
else
    echo "No failing_tests file found."
fi

echo "==== FIXED TEST LOG ===="
if [ -f /tmp/Lang_1_fixed/failing_tests ]; then
    cat /tmp/Lang_1_fixed/failing_tests
else
    echo "No failing_tests file found."
fi
