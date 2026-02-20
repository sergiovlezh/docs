#!/bin/bash
set -e

git config --global --add safe.directory ${WORKSPACE_FOLDER}
cd ${WORKSPACE_FOLDER}/backend
uv sync
