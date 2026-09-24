# Entry format for the adjective dictionary

The adjective dictionary has two tiers, both written as JSON and rendered by
`tools/build_adjectives.py`, so nobody hand-edits the markdown.

- **Grammar tier** — `tools/adjectives/groups/<NN>-<slug>.json`. The adjectives that
  carry grammar: irregular comparison, the *-ing/-ed* pairs, adjectives that only go
  before a noun or only after a verb, extreme and absolute adjectives, adjectives that
  bring a fixed preposition or a *to*-infinitive, spelling changes in comparison,
  nationalities, compounds, *-ly* adjectives, false friends and confused pairs.
  Every sense, and a contrast note wherever there is a trap.
- **Core tier** — `tools/adjectives/core/add-<NN>.json`. The everyday adjectives that
  survived a triage of WordNet's 21,479 adjective lemmas.

Both use the same shape:

```json
[
  {
    "term": "afraid",
    "ipa": "əˈfreɪd",
    "respell": "uh-FRAYD",
    "ru": "испуганный; боящийся",
    "type": "emotion",
    "position": "predicative only — never before a noun: *a frightened child*",
    "comparison": "more/most — *more afraid*, *most afraid*",
    "takes": "*of* + noun or *-ing*; *to*-infinitive; *that*-clause",
    "form": "a- adjective, from an old participle",
    "opposite": "*unafraid*",
    "contrast": "Optional. Only for a real trap.",
    "senses": [
      {
        "gloss": "Feeling fear.",
        "ru": "испуганный, боящийся",
        "examples": [
          "The kids were *afraid* of the dog next door.",
          "Don't be *afraid* to ask.",
          "I was more *afraid* of the dark than of anything else."
        ]
      }
    ]
  }
]
```

## The three label fields open with a fixed word

The browser turns the first clause of `type`, `position` and `comparison` into a filter
tag — everything before the first `—`, `(`, `;` or `,`. So each of those fields **must
open with one of the words below**, and any explanation goes after ` — `.

- **`type`** — `quality`, `emotion`, `evaluative`, `size`, `shape`, `age`, `color`,
  `material`, `origin`, `classifying`, `participial`, `compound`, `emphasizing`,
  `quantity`. A word with several jobs names its main one first and the rest after a
  semicolon: `quality; also emotion`. `classifying` is for relational adjectives that
  say what kind (*medical*, *urban*, *annual*); `participial` for *-ing* and *-ed*
  adjectives; `origin` for nationality, religion and place.
- **`position`** — `both` (before a noun and after a verb), `attributive only`,
  `predicative only`, `after the noun`.
- **`comparison`** — `-er/-est`, `more/most`, `-er/-est or more/most`, `irregular`,
  `not gradable`, then the actual forms after ` — `: `-er/-est — *bigger*, *biggest*`.
  Never a comma before the dash.

## Hard rules

- **`ipa`** — General American, **no** slashes. *hot* /ɑː/ not /ɒ/; rhotic /ər/;
  **/ɛ/** for the DRESS vowel, never bare /e/ (bare /e/ belongs only to /eɪ/);
  /ɪr ɛr ʊr/ not /ɪə eə ʊə/; a diphthong before schwa keeps it (*fiery* /ˈfaɪəri/).
  *-ed* after /t/ or /d/ is /ɪd/; some *-ed* adjectives are always /ɪd/
  (*naked*, *wicked*, *rugged*, *beloved*).
- **`respell`** — stressed syllable in CAPITALS, syllables hyphenated, a space between
  words. Schwa `uh`; /ʊ/ `UU`; /uː/ `OO`; /ər/ `ur`; /ɜːr/ `UR`; /ɔːr/ `OR`;
  word-final /ɛr/ `AIR`; /aɪ/ `Y`. No silent final `-e`.
- **`ru`** — the Russian adjective or short equivalent. Not a sentence.
- **`takes`** — only when the adjective requires or strongly prefers a complement:
  the preposition(s) with what follows, a *to*-infinitive, a *that*-clause. Name every
  preposition that changes the meaning. Omit for adjectives that take nothing.
- **`form`** — how the word is built, when that helps: `-ing — what causes the feeling`,
  `-ful from *care*`, `un- + *happy*`, `compound — adverb + participle`. Omit for simple words.
- **`opposite`** — the usual antonym, when there is a clear one. Optional.
- **`senses`** — one object per **genuinely distinct** adjective meaning, **most common
  first**. *hard* has at least four (solid; difficult; strict; strong, as in *hard
  liquor*); *light* has unrelated ones (not heavy; not dark; mild). Split when the
  Russian translation changes.
- **`examples`** — natural American English, headword in single asterisks in every
  one. A single-sense entry has **exactly 3**; each sense of a multi-sense entry has
  **2 or 3**. When `comparison` lists forms, at least one example in the entry uses
  a comparative or superlative, asterisked (*The box was *heavier* than it looked*).
  Show the adjective in both positions where it takes both.
- **`contrast`** — omit unless there is a trap: a restricted position, a meaning that
  changes with position or preposition, an *-ing/-ed* confusion, a false friend for a
  Russian speaker, a US/UK split, spelling in comparison, a noun that looks like it.

## Never

- **Only adjective uses.** *fast* in *drive fast* is an adverb; *a Russian* is a noun;
  *she bored us* is a verb. Mention them in `contrast` if they cause confusion, but do
  not write them as senses. A participle is an adjective when it can take *very* or
  follow *seem* (*very interested*, *seems tired*).
- No noun used as a modifier (*a glass door*, *a cotton shirt*) — those are nouns.
- No archaic, dialect or British-only adjective unless the `contrast` says so and it
  is still met in American reading. American spelling: *gray*, *woolen*, *colorful*.
- No invented pronunciations — if unsure of a word's IPA, drop the word.
- Single asterisks only, always balanced. Never `**bold**` inside examples.
