#!/bin/bash
set -euo pipefail

trap 'cd "${ABSOLUTE_ROOT_DIRECTORY}"' EXIT

cd "${ABSOLUTE_ROOT_DIRECTORY}/database"

atlas migrate hash