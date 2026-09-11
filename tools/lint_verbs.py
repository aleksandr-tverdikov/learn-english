#!/usr/bin/env python3
"""Normalize agent-written core-verb JSON, the way lint_core.py does for nouns.

Same two error classes, because they come from the same place - different agents
bringing different conventions:

  * British transcription bleeding into what must be General American
  * respellings that disagree with the corpus conventions (schwa as UH, DRESS
    as E, no silent final -e)

and one repair specific to a bug this project introduced: a blind str.replace of
'ɪə'/'ʊə' also matches the tail of /aɪə/, /aʊə/, /oʊə/, so `expire` came out as
/ɪkˈspaɪr/. A diphthong followed by r and then a consonant cannot occur in GA
without an intervening schwa, which makes the damage decidable.

The DRESS-before-r case is deliberately NOT handled by rule. Rewriting KEH-ree to
KE-ree produces "kee-ree": the r belongs in the first syllable, giving KER-ee, and
that is a syllabification decision a regex cannot make. Those are listed for a
human instead.
"""
import glob, json, os, re, sys

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'verbs')
SUBS = [(re.compile('ɒ'), 'ɑː'),
        (re.compile('(?<![aɔe])ɪə'), 'ɪr'),
        (re.compile('(?<![aoiu])eə'), 'ɛr'),
        (re.compile('(?<![ao])ʊə'), 'ʊr')]
DRESS = re.compile(r'e(?!ɪ)')
VOWELS = set('iɪeɛæaɑɒɔoʊuʌɜəyː')
DIPH_R = re.compile(r'(aɪ|aʊ|oʊ|eɪ|ɔɪ)r')
EHR = re.compile(r'\b([A-Z]+)EH-(R?)', re.I)


def undo_diphthong_damage(ipa):
    out, i, n = [], 0, 0
    while i < len(ipa):
        m = DIPH_R.match(ipa, i)
        if m:
            nxt = ipa[m.end():m.end() + 1]
            if nxt == 'r':
                out.append(m.group(1) + 'ər'); n += 1; i = m.end() + 1; continue
            if nxt == '' or nxt not in VOWELS:
                out.append(m.group(1) + 'ə'); n += 1; i = m.end(); continue
        out.append(ipa[i]); i += 1
    return ''.join(out), n


def main():
    n_ipa = n_rs = 0
    manual = []
    for p in sorted(glob.glob(os.path.join(SRC, '*.json'))):
        if p.endswith('existing-terms.json'):
            continue
        try:
            data = json.load(open(p))
        except Exception as exc:
            print(f'  BAD JSON {os.path.basename(p)}: {exc}'); continue
        changed = False
        for e in data if isinstance(data, list) else []:
            if not isinstance(e, dict):
                continue
            ipa = (e.get('ipa') or '').strip().strip('/')
            before = ipa
            for pat, rep in SUBS:
                ipa = pat.sub(rep, ipa)
            ipa = DRESS.sub('ɛ', ipa)
            ipa, _ = undo_diphthong_damage(ipa)
            if ipa != before:
                e['ipa'] = ipa; n_ipa += 1; changed = True

            rs = e.get('respell') or ''
            o = rs
            rs = re.sub(r'\b(Y[TDKPSN])E\b', r'\1', rs)      # no silent final -e
            rs = re.sub(r'\b(y[tdkpsn])e\b', r'\1', rs)
            if rs != o:
                e['respell'] = rs; n_rs += 1; changed = True
            if 'EH' in (e.get('respell') or '').upper():
                manual.append(f"{e.get('term')}: {e.get('respell')}")
        if changed:
            json.dump(data, open(p, 'w'), ensure_ascii=False, indent=1)

    print(f'{n_ipa} IPA normalized, {n_rs} respellings normalized')
    if manual:
        print(f'{len(manual)} respellings need a human (DRESS before r — KER-ee, not KE-ree):')
        for m in manual[:12]:
            print('   ', m)


if __name__ == '__main__':
    main()
