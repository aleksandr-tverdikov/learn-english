#!/usr/bin/env python3
"""Run the whole pipeline: dictionaries -> HTML site -> home page -> link check."""
import subprocess, sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
for step in ['apply_verb_type.py', 'apply_verb_class.py', 'apply_phrasal_index.py', 'apply_ru.py', 'build_core.py', 'build_browsers.py', 'sync_counts.py', 'build_site.py', 'build_home.py', 'check_links.py']:
    print(f'\n=== {step} ===')
    if subprocess.call([sys.executable, os.path.join(HERE, step)]):
        sys.exit(f'{step} failed')
