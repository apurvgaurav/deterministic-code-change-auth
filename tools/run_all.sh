#!/bin/bash
export DEBIAN_FRONTEND=noninteractive
echo "Installing Java 8 and dependencies natively..."
# Using --allow-unauthenticated as old 18.04 keys might be expired
apt-get update -qq --allow-insecure-repositories || true
apt-get install -y -qq --allow-unauthenticated openjdk-8-jdk patchutils python3 > /dev/null

export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
export PATH=$JAVA_HOME/bin:/defects4j/framework/bin:$PATH

if ! command -v defects4j &> /dev/null; then
    D4J_PATH=$(find / -name defects4j -type f -executable 2>/dev/null | grep bin | head -n 1 | xargs -r dirname)
    if [ ! -z "$D4J_PATH" ]; then
        export PATH=$PATH:$D4J_PATH
    fi
fi

echo "=========================================================="
echo "STARTING MASS EXECUTION OF 20 DEFECTS4J PROTOTYPE TRACTS"
echo "=========================================================="
python3 /eval_workspace/deterministic-code-change-auth/scripts/defects4j_evaluator.py

if [ -f /tmp/d4j_workspace/defects4j_results.jsonl ]; then
    echo "Processing complete. Saving outputs to host local desktop..."
    cp /tmp/d4j_workspace/defects4j_results.jsonl /eval_workspace/final_ieee_results.jsonl
    echo "** FINISHED SUCCESSFULLY **"
else
    echo "ERROR: Outcome matrix did not compile correctly."
fi
