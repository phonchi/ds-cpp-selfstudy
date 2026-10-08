#!/usr/bin/env bash
# Regenerate trees.html: generator -> flashcards & bank quiz -> quiz shuffle (this page only).
set -euo pipefail
cd "$(dirname "$0")/../../.."
python3 tools/enrich/enrich_trees.py
python3 tools/apply_zh.py --pages trees
python3 -c "import sys; sys.path.insert(0, 'tools'); import shuffle_quiz; print('shuffle changed:', shuffle_quiz.ensure('trees.html'))"
