#!/usr/bin/env bash
# Regenerate searching_sorting.html: generator -> flashcards & bank quiz -> quiz shuffle (this page only).
set -euo pipefail
cd "$(dirname "$0")/../../.."
python3 tools/enrich/enrich_search.py
python3 tools/apply_zh.py --pages searching_sorting
python3 -c "import sys; sys.path.insert(0, 'tools'); import shuffle_quiz; print('shuffle changed:', shuffle_quiz.ensure('searching_sorting.html'))"
