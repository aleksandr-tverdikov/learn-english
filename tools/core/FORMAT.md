# Entry format for the core-vocabulary tier

Each field file is `tools/core/<slug>.json`, a JSON array of entry objects:

```json
[
  {
    "term": "doctor",
    "ipa": "ˈdɑːktər",
    "respell": "DAHK-tur",
    "ru": "врач, доктор",
    "plural": "doctors",
    "countability": "countable",
    "gloss": "Someone qualified to treat sick people.",
    "examples": [
      "She's a *doctor* at the county hospital.",
      "Both *doctors* recommended surgery.",
      "You should see a *doctor* about that."
    ],
    "contrast": "Optional. Only when the word hides a real trap."
  }
]
```

## Hard rules

- **`ipa`** — General American, **no** surrounding slashes (the renderer adds them).
  Use American vowels: *hot* /ɑː/ not /ɒ/, *bath* /æ/ not /ɑː/, rhotic /ər/ not /ə/.
- **`respell`** — plain-English respelling, stressed syllable in CAPITALS, syllables
  hyphenated: `DAHK-tur`, `in-jih-NEER`, `uh-KOWN-tuhnt`.
- **`ru`** — the Russian headword plus at most a short gloss. Not a sentence.
- **`plural`** — the plural form alone, or `""` for an uncountable noun.
- **`countability`** — exactly one of: `countable`, `uncountable`,
  `countable, and uncountable as a substance`, `countable, and uncountable as food`,
  `both — countable and uncountable with different meanings`.
- **`gloss`** — one sentence, ending in a period. Definition, not encyclopedia.
- **`examples`** — exactly 3 natural American sentences. The headword (or its
  plural) appears in each, wrapped in single asterisks: `*doctor*`.
- **`contrast`** — omit unless there is a genuine trap: silent letter, stress
  shift, confusable near-homophone, US/UK split, or an irregular plural.

## Never

- No proper nouns unless the field is explicitly about them.
- No word already listed in `existing-terms.json`.
- No word that is not a noun.
- No invented pronunciations — if unsure of a word's IPA, drop the word.
