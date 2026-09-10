#!/usr/bin/env python3
"""Repair the mechanical errors in agent-authored core-vocabulary JSON.

The fan-out that wrote these files had a verification agent per field, but most
verifiers died on a session limit before running. The checks below are the
subset of that audit that can be done *deterministically*, so they do not need
an agent and cannot themselves hallucinate.

The systematic risk in agent-written IPA is British transcription bleeding into
what is supposed to be General American. Four substitutions are unambiguous and
are applied automatically:

    ɒ  -> ɑː    LOT vowel:      British /hɒt/     -> American /hɑːt/
    ɪə -> ɪr    NEAR:           British /bɪə/     -> American /bɪr/
    eə -> ɛr    SQUARE:         British /beə/     -> American /bɛr/
    ʊə -> ʊr    CURE:           British /pjʊə/    -> American /pjʊr/

A fifth is applied only with spelling evidence: a word spelled with a final
-er/-or/-ar/-our but transcribed with a bare final /ə/ is missing its rhotic r,
so the r is restored.

A sixth normalizes the DRESS vowel. Both /e/ and /ɛ/ are used for it by real
dictionaries - Cambridge writes /e/, Wells and Merriam-Webster write /ɛ/ - but a
single dictionary has to pick one. The hand-written grammar tier uses /ɛ/ without
exception, so the core tier is normalized to match. The lookahead protects the
/eɪ/ diphthong, which is a different vowel: `agent` stays /ˈeɪdʒənt/ while
`leather` becomes /ˈlɛðər/.

Anything else is reported, not silently rewritten.
"""
import glob, json, os, re, sys

CORE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'core')

# These must NOT fire across a syllable boundary. A blind str.replace of 'ɪə'
# turns /ˈvaɪələns/ into /ˈvaɪrləns/, because PRICE + schwa contains the same two
# symbols as British NEAR. The lookbehind requires that the ə is not the second
# half of a preceding diphthong.
SUBS = [(re.compile('ɒ'), 'ɑː'),
        (re.compile('(?<![aɔe])ɪə'), 'ɪr'),
        (re.compile('(?<![aoiu])eə'), 'ɛr'),
        (re.compile('(?<![ao])ʊə'), 'ʊr')]
DRESS = re.compile(r'e(?!ɪ)')   # bare e is the DRESS vowel; eɪ is left alone
RHOTIC_SPELLING = re.compile(r'(er|or|ar|our|re)$', re.I)


VOWELS = set('iɪeɛæaɑɒɔoʊuʌɜəyː')
DIPH_R = re.compile(r'(aɪ|aʊ|oʊ|eɪ|ɔɪ)r')


def undo_diphthong_damage(ipa):
    """Repair transcriptions an earlier, blunter version of this script broke.

    That version replaced 'ɪə' and 'ʊə' with str.replace, which also matched the
    tail of /aɪə/, /aʊə/, /oʊə/ and /eɪə/. `fire` became /ˈfaɪrr/, `towel`
    /ˈtaʊrl/, `lion` /ˈlaɪrn/, `society` /səˈsaɪrti/ — 287 entries in all.

    The damage is decidable from the result alone. A diphthong followed by r and
    then a consonant cannot occur in General American without an intervening
    schwa, so:

        Xrr + anything  ->  Xər   the schwa had a real r after it   (fire)
        Xr  + consonant ->  Xə    the schwa itself became the r     (towel)
        Xr  + vowel     ->  left alone; genuine (iris, spiral, environment)

    Idempotent: correct transcriptions match none of these shapes.
    """
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


def stem(term):
    """crude stem so `doctors` in an example still matches `doctor`"""
    t = term.lower()
    return t[:-1] if len(t) > 4 and t.endswith('s') else t


def lint(path):
    data = json.load(open(path))
    if isinstance(data, dict):
        data = data.get('entries') or []
    fixed_ipa = fixed_rhotic = dropped = 0
    out, notes = [], []

    for e in data:
        if not isinstance(e, dict) or not (e.get('term') or '').strip():
            dropped += 1
            continue
        term = e['term'].strip()
        ipa = (e.get('ipa') or '').strip().strip('/')

        before = ipa
        for pat, rep in SUBS:
            ipa = pat.sub(rep, ipa)
        ipa, _ = undo_diphthong_damage(ipa)
        ipa = DRESS.sub('ɛ', ipa)
        if ipa != before:
            fixed_ipa += 1

        # restore a dropped rhotic r when the spelling clearly has one
        if ipa.endswith('ə') and RHOTIC_SPELLING.search(term):
            ipa += 'r'
            fixed_rhotic += 1
        e['ipa'] = ipa

        if not ipa or not (e.get('ru') or '').strip() or not (e.get('gloss') or '').strip():
            dropped += 1
            notes.append(f'{term}: missing required field')
            continue

        ex = [x for x in (e.get('examples') or []) if isinstance(x, str) and x.strip()]
        if len(ex) < 3:
            dropped += 1
            notes.append(f'{term}: only {len(ex)} examples')
            continue
        s = stem(term)
        if not any(s in x.lower() for x in ex[:3]):
            dropped += 1
            notes.append(f'{term}: headword absent from its own examples')
            continue
        e['examples'] = ex[:3]
        out.append(e)

    json.dump(out, open(path, 'w'), ensure_ascii=False, indent=1)
    return len(data), len(out), fixed_ipa, fixed_rhotic, dropped, notes


if __name__ == '__main__':
    tot_in = tot_out = tot_ipa = tot_rh = tot_drop = 0
    allnotes = []
    for p in sorted(glob.glob(os.path.join(CORE, '*.json'))):
        if p.endswith('existing-terms.json'):
            continue
        n_in, n_out, ipa, rh, drop, notes = lint(p)
        tot_in += n_in; tot_out += n_out; tot_ipa += ipa; tot_rh += rh; tot_drop += drop
        allnotes += [f'{os.path.basename(p)[:-5]}: {n}' for n in notes]
        print(f'  {os.path.basename(p)[:-5]:<26}{n_in:>4} -> {n_out:<4} '
              f'ipa {ipa:>3}  rhotic {rh:>3}  dropped {drop:>2}')
    print(f'\n{tot_in} in, {tot_out} kept')
    print(f'British IPA vowels corrected: {tot_ipa}')
    print(f'missing rhotic r restored:    {tot_rh}')
    print(f'entries dropped:              {tot_drop}')
    for n in allnotes[:15]:
        print('   ', n)
    if len(allnotes) > 15:
        print(f'    ... and {len(allnotes)-15} more')
