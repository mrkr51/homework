#!/usr/bin/env bash
set -Eeuo pipefail

REPO_URL="https://github.com/mrkr51/homework.git"
PORT=8000

die() {
  echo "Error: $*" >&2
  exit 1
}

require_tools() {
  local tools=(git docker curl nginx)
  for t in "${tools[@]}"; do
    command -v "$t" >/dev/null 2>&1 || die "$t not found"
  done
}

parse_args() {
  for arg in "$@"; do
    case "$arg" in
      --app=*)     APP="${arg#*=}" ;;
      --version=*) VERSION="${arg#*=}" ;;
      --env=*)     ENV="${arg#*=}" ;;
      *)           die "Unknown argument: $arg" ;;
    esac
  done
  [[ -n "${APP:-}" && -n "${VERSION:-}" && -n "${ENV:-}" ]] || die "Usage: $0 --app=NAME --version=X.X --env=ENV"
}

backup_if_exists() {
  if [[ -d "$DEPLOY_DIR" ]]; then
    mkdir -p "$BACKUP_DIR"
    cp -r "$DEPLOY_DIR" "$BACKUP_PATH"
  fi
}

deploy() {
  rm -rf "$DEPLOY_DIR"
  git clone "$REPO_URL" "$DEPLOY_DIR"
  cd "$DEPLOY_DIR"

  docker build -t "$IMAGE" .

  docker stop "$APP" >/dev/null 2>&1 || true
  docker rm   "$APP" >/dev/null 2>&1 || true
  docker run -d --name "$APP" -p "${PORT}:${PORT}" "$IMAGE"
}

health_check() {
  sleep 5
  curl -fsS "http://localhost:${PORT}/" >/dev/null
}

rollback() {
  docker stop "$APP" >/dev/null 2>&1 || true
  docker rm   "$APP" >/dev/null 2>&1 || true

  if [[ -d "$BACKUP_PATH" ]]; then
    rm -rf "$DEPLOY_DIR"
    cp -r "$BACKUP_PATH" "$DEPLOY_DIR"
  fi
}

main() {
  parse_args "$@"
  require_tools

  DEPLOY_DIR="/tmp/$APP"
  BACKUP_DIR="/tmp/backups/$APP"
  TIMESTAMP="$(date +%Y%m%d_%H%M%S)"
  BACKUP_PATH="$BACKUP_DIR/backup_$TIMESTAMP"
  IMAGE="$APP:$VERSION"

  backup_if_exists

  if deploy && health_check; then
    echo "Deployment successful!"
  else
    rollback
    exit 1
  fi
}

main "$@"