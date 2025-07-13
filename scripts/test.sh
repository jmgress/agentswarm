#!/bin/bash
set -e

cd "$(dirname "$0")/../backend"
pytest -q
