# Entry format for the core-verb tier

The verb catalog has always covered the verbs that **misbehave** — 366 irregular
verbs grouped by how their three forms change, 696 phrasal verbs, and 229
verb + preposition patterns. Regular verbs were never a category, so *work*,
*need*, *want*, *help*, *ask*, *decide* and *explain* are not in the dictionary
at all.

This tier fixes that. Each field file is `tools/verbs/<slug>.json`, a JSON array:

```json
[
  {
    "term": "explain",
    "ipa": "ɪkˈspleɪn",
    "respell": "ik-SPLAYN",
    "ru": "объяснять",
    "third": "explains",
    "past": "explained",
    "participle": "explained",
    "ing": "explaining",
    "transitivity": "transitive",
    "gloss": "To make something clear by describing it in detail.",
    "examples": [
      "Could you *explain* the rules again?",
      "She *explained* why the flight was canceled.",
      "He has *explained* it three times already."
    ],
    "contrast": "Optional. Only for a real trap."
  }
]
```

## Hard rules

- **`ipa`** — General American, **no** slashes. American vowels: *hot* /ɑː/ not /ɒ/,
  *ask* /æ/ not /ɑː/, rhotic /ər/ not /ə/. Use **/ɛ/** for the DRESS vowel, never
  bare /e/ — /e/ belongs only to the /eɪ/ diphthong.
- **`respell`** — stressed syllable in CAPITALS, syllables hyphenated: `ik-SPLAYN`.
  Schwa is written `uh`. No silent final `-e`.
- **`ru`** — the Russian verb, imperfective first, plus a perfective or short gloss
  where it helps: `объяснять, объяснить`. Not a sentence.
- **`third` / `past` / `participle` / `ing`** — all four forms, spelled out. Regular
  verbs still need them, because the spelling changes are where learners fail:
  *carry → carries → carried*, *stop → stopped → stopping*, *agree → agreed*.
- **`transitivity`** — one of: `transitive`, `intransitive`, `both`, or
  `both — transitive (…), intransitive (…)` with a short example of each.
- **`gloss`** — one sentence, ending in a period.
- **`examples`** — exactly 3, natural American English. The verb must appear in each,
  wrapped in single asterisks, and **between them the three examples must use more
  than one form** — a base, a past, and a participle or *-ing* where natural. That is
  the point of a verb entry: showing the forms in use.
- **`contrast`** — omit unless there is a genuine trap: a doubled consonant
  (*plan → planned*), a *-y* change (*try → tried*), a silent letter, a confusable
  near-homophone, a US/UK split (*traveled* / *travelled*), or a preposition the verb
  demands (*listen **to***, *depend **on***).

## Never

- No irregular verbs — they already have fuller entries in groups 1–13. Check
  `existing-terms.json` before writing.
- No phrasal verbs (*give up*, *look after*) — groups 14–22 own those.
- No verb that is not current American English.
- No invented pronunciation. If unsure, drop the verb.
