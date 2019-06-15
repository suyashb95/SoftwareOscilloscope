#!/usr/bin/env bash
PY=$(which python3)
$PY ./SocketPlot-Test.py &
TEST_PID=$!
$PY ./test_run.py 
kill $TEST_PID
