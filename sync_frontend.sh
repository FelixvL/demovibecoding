#!/bin/sh
# Kopieer de frontend uit ../fe naar be/frontend zodat hij mee gedeployd wordt naar Azure.
cd "$(dirname "$0")" && cp ../fe/*.html frontend/ && echo "frontend gekopieerd"
