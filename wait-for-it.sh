#!/usr/bin/env bash
#   Use this script to test if a given TCP host/port are available

set -e

TIMEOUT=15
QUIET=0
HOST=""
PORT=""
STRICT=0
CHILD=0
CLI=""
WAITFORIT_cmdname=${0##*/}

echoerr() {
    if [[ $QUIET -ne 1 ]]; then echo "$@" 1>&2; fi
}

usage() {
    cat << USAGE >&2
Usage:
    $WAITFORIT_cmdname host:port [-s] [-t timeout] [-- command args]
    -h HOST | --host=HOST       Host or IP under test
    -p PORT | --port=PORT       TCP port under test
                                Alternatively, specify host and port as host:port
    -s | --strict               Only execute subcommand if the test succeeds
    -q | --quiet                Suppress output messages
    -t TIMEOUT | --timeout=TIMEOUT
                                Timeout in seconds, zero for no timeout
    -- COMMAND ARGS             Execute COMMAND with ARGS after the test
USAGE
    exit 1
}

wait_for() {
    if [[ $TIMEOUT -gt 0 ]]; then
        echoerr "$WAITFORIT_cmdname: waiting $TIMEOUT seconds for $HOST:$PORT"
    else
        echoerr "$WAITFORIT_cmdname: waiting for $HOST:$PORT without a timeout"
    fi
    start_ts=$(date +%s)
    while :
    do
        if nc -z $HOST $PORT; then
            end_ts=$(date +%s)
            echoerr "$WAITFORIT_cmdname: $HOST:$PORT is available after $((end_ts - start_ts)) seconds"
            return 0
        fi
        sleep 1
    done
}

wait_for_wrapper() {
    if [[ $QUIET -eq 1 ]]; then
        timeout $TIMEOUT $0 --quiet --child --host=$HOST --port=$PORT --timeout=$TIMEOUT &
    else
        timeout $TIMEOUT $0 --child --host=$HOST --port=$PORT --timeout=$TIMEOUT &
    fi
    PID=$!
    trap "kill -INT -$PID" INT
    wait $PID
    RESULT=$?
    if [[ $RESULT -ne 0 ]]; then
        echoerr "$WAITFORIT_cmdname: timeout after waiting $TIMEOUT seconds for $HOST:$PORT"
    fi
    return $RESULT
}

# process arguments
while [[ $# -gt 0 ]]
do
    case "$1" in
        *:* )
        HOST=$(printf "%s" "$1" | cut -d : -f 1)
        PORT=$(printf "%s" "$1" | cut -d : -f 2)
        shift 1
        ;;
        -h|--host)
        HOST="$2"; shift 2
        ;;
        --host=*)
        HOST="${1#*=}"; shift 1
        ;;
        -p|--port)
        PORT="$2"; shift 2
        ;;
        --port=*)
        PORT="${1#*=}"; shift 1
        ;;
        -t|--timeout)
        TIMEOUT="$2"; shift 2
        ;;
        --timeout=*)
        TIMEOUT="${1#*=}"; shift 1
        ;;
        -q|--quiet)
        QUIET=1; shift 1
        ;;
        -s|--strict)
        STRICT=1; shift 1
        ;;
        --child)
        CHILD=1; shift 1
        ;;
        --)
        shift; CLI="$@"; break
        ;;
        --help)
        usage
        ;;
        *)
        echoerr "Unknown argument: $1"; usage
        ;;
    esac
done

if [[ -z "$HOST" || -z "$PORT" ]]; then
    echoerr "Error: You need to provide a host and port."
    usage
fi

if [[ $CHILD -gt 0 ]]; then
    wait_for
    RESULT=$?
    exit $RESULT
else
    if [[ $TIMEOUT -gt 0 ]]; then
        wait_for_wrapper
        RESULT=$?
    else
        wait_for
        RESULT=$?
    fi
fi

if [[ -n "$CLI" ]]; then
    if [[ $RESULT -ne 0 && $STRICT -eq 1 ]]; then
        echoerr "$WAITFORIT_cmdname: strict mode, refusing to execute subprocess"
        exit $RESULT
    fi
    exec $CLI
else
    exit $RESULT
fi
