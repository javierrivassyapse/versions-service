#!/bin/sh

main() {
  [ $# -lt 1 ] && run_gunicorn
  case "$1" in
    -*) run_gunicorn "$@";;
    *) exec "$@";;
  esac
}

run_gunicorn() {
  export NEW_RELIC_CONFIG_FILE
  if [ -n "${NEW_RELIC_LICENSE_KEY}" ]; then
    echo "Running with New Relic monitoring..."
    exec newrelic-admin run-program gunicorn autoapp:app "$@"
  else
    exec gunicorn autoapp:app "$@"
  fi
}

main "$@"
