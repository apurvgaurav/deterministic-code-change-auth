#!/bin/bash
export PATH=$PATH:/defects4j/framework/bin
if ! command -v defects4j &> /dev/null; then
    # Some containers use different paths, try to locate it
    D4J_PATH=$(find / -name defects4j -type f -executable 2>/dev/null | grep bin | head -n 1 | xargs -r dirname)
    if [ ! -z "$D4J_PATH" ]; then
        export PATH=$PATH:$D4J_PATH
    fi
fi

echo "Checking out Buggy Lang-1..."
defects4j checkout -p Lang -v 1b -w /tmp/Lang_1_buggy
cd /tmp/Lang_1_buggy
echo "Compiling Buggy Lang-1..."
defects4j compile
echo "Testing Buggy Lang-1..."
defects4j test > /tmp/buggy_test.log || true

echo "Checking out Fixed Lang-1..."
defects4j checkout -p Lang -v 1f -w /tmp/Lang_1_fixed
cd /tmp/Lang_1_fixed
echo "Compiling Fixed Lang-1..."
defects4j compile
echo "Testing Fixed Lang-1..."
defects4j test > /tmp/fixed_test.log || true

echo "==== BUGGY TEST LOG ===="
cat /tmp/buggy_test.log
echo "==== FIXED TEST LOG ===="
cat /tmp/fixed_test.log
