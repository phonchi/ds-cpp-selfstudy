#!/usr/bin/env bash
# Regenerate recursion.html: generator -> flashcards -> quiz shuffle (this page only).
set -euo pipefail
cd "$(dirname "$0")/../../.."
python3 tools/enrich/enrich_recursion.py
python3 tools/apply_zh.py --pages recursion
python3 -c "import sys; sys.path.insert(0, 'tools'); import shuffle_quiz; print('shuffle changed:', shuffle_quiz.ensure('recursion.html'))"
