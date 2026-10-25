#!/bin/bash
# PreToolUse(Bash): block commands that would print secret values into the context.
# Allowed: key names (cut -d= -f1 .env), lengths (${#VAR}), grep -c.
cmd=$(jq -r '.tool_input.command // empty')

block() {
  echo "Blocked by block-secrets.sh: $1. Check key names or lengths instead." >&2
  exit 2
}

sep='(^|[;&|[:space:]])'
echo "$cmd" | grep -Eq "${sep}(cat|less|more|head|tail|bat|nl|xxd|strings)[[:space:]][^;&|]*\.env" \
  && block "reads a .env file"
echo "$cmd" | grep -Eq "${sep}printenv([[:space:]]|$)|${sep}env[[:space:]]*($|[|;&])|${sep}export[[:space:]]+-p" \
  && block "prints the environment"
echo "$cmd" | grep -Eiq "(echo|printf)[^;&|]*\\\$\{?[a-z_]*(token|key|secret|password)" \
  && block "prints a secret variable"
exit 0
