#!/usr/bin/env bash
set -euo pipefail
export EMBED_PROVIDER=${EMBED_PROVIDER:-hash}
python apps/server/scripts/embed_upsert.py --ns bank/policies --src seed_docs/bank/policies
python apps/server/scripts/embed_upsert.py --ns bank/ops --src seed_docs/bank/ops
python apps/server/scripts/embed_upsert.py --ns bank/faqs --src seed_docs/bank/faqs
echo 'Seed complete.'
