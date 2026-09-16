#!/usr/bin/env bash
# Printed each time the container is attached. Points new contributors at the
# workshop ticket instead of leaving them at a bare prompt.
set -u

cyan=$'\033[36m'; bold=$'\033[1m'; dim=$'\033[2m'; reset=$'\033[0m'

cat <<EOF

${bold}${cyan}ATLAS dev container ready${reset}  $(python --version 2>&1)

  ${bold}Your ticket${reset}   backend/Workshop/README.md   ${dim}(ATLAS-101)${reset}

  ${bold}Start the API${reset}
    cd backend && uvicorn Workshop.main:app --host 0.0.0.0 --port 8000 --reload

  ${bold}Then open${reset}     http://localhost:8000/docs
  ${bold}Run the tests${reset} cd backend && pytest -v

EOF
