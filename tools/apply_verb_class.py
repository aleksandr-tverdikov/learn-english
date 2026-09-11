#!/usr/bin/env python3
"""Label every base verb irregular or regular.

The catalog has always separated them - groups 1-13 are irregular, grouped by how
the three forms change, and groups 23+ are the regular tier - but the division
lived only in the file numbering. An entry never said which it was, so a learner
looking at `carry` had no way to know it was regular and `bear` was not.

Phrasal verbs and verb + preposition patterns (14-22) are deliberately skipped:
their class is whatever their base verb's is, and saying so on each of 925
entries would be noise.

Idempotent: an existing line is replaced, never doubled.
"""
import glob, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import ROOT

CAT = os.path.join(ROOT, 'parts-of-speech/03-verbs/catalog')
LINE = re.compile(r'^\*\*Verb class:\*\*.*$')
# anchor on Forms alone: matching Third person as well would label every entry twice
ANCHOR = re.compile(r'^\*\*Forms:\*\*')


def apply(path, label):
    lines = open(path).read().split('\n')
    out, n = [], 0
    for ln in lines:
        if LINE.match(ln):
            continue                       # drop a previous run's line
        out.append(ln)
        if ANCHOR.match(ln):
            out.append(f'**Verb class:** {label}')
            n += 1
    open(path, 'w').write('\n'.join(out))
    return n


if __name__ == '__main__':
    tot = 0
    for f in sorted(glob.glob(f'{CAT}/[0-9]*.md')):
        num = int(re.match(r'(\d+)', os.path.basename(f)).group(1))
        if num <= 13:
            label = 'irregular'
        elif num >= 23:
            label = 'regular'
        else:
            continue                       # phrasal and v+prep inherit their base's class
        tot += apply(f, label)
    print(f'labeled {tot} base verbs irregular or regular')
