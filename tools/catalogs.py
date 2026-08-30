#!/usr/bin/env python3
"""The dictionaries in the library, and which fields each one surfaces.

`fields` maps a markdown label (lowercased) to the heading shown in the browser.
Order here is the order they appear in an entry. Adding a dictionary means adding
one row — nothing else in the pipeline needs to change.
"""

CATALOGS = [
    dict(
        slug='08-interjections',
        dir='parts-of-speech/08-interjections/catalog',
        title='The Interjection Dictionary',
        eyebrow='08 &middot; Interjections',
        lede='interjections of American English',
        accent='#b4552a', accent_dark='#e8935f',
                tag_fields=['type'],
        fields=[('type', 'Type'), ('variants', 'Variants')],
    ),
    dict(
        slug='07-conjunctions',
        dir='parts-of-speech/07-conjunctions/catalog',
        title='The Conjunction Dictionary',
        eyebrow='07 &middot; Conjunctions',
        lede='conjunctions, subordinators, correlative pairs, and transitional connectors',
        accent='#2f5d8a', accent_dark='#79b0e8',
                tag_fields=['type', 'clause type'],
        fields=[('clause type', 'Builds'), ('pattern', 'Pattern'),
                ('punctuation', 'Punctuation'), ('type', 'Type'), ('variants', 'Variants')],
    ),
    dict(
        slug='06-prepositions',
        dir='parts-of-speech/06-prepositions/catalog',
        title='The Preposition Dictionary',
        eyebrow='06 &middot; Prepositions',
        lede='prepositions — simple, compound, multi-word, and participial',
        accent='#3f6b4a', accent_dark='#7fc08d',
                tag_fields=['type', 'complement'],
        fields=[('complement', 'Complement'), ('pattern', 'Pattern'),
                ('contrast', 'Contrast'), ('type', 'Type'), ('variants', 'Variants')],
    ),
    dict(
        slug='09-determiners',
        dir='parts-of-speech/09-determiners/catalog',
        title='The Determiner Dictionary',
        eyebrow='09 &middot; Determiners',
        lede='determiners — articles, demonstratives, possessives, quantifiers, and numerals',
        accent='#7a4a86', accent_dark='#c193cc',
                tag_fields=['type', 'position', 'goes with'],
        fields=[('goes with', 'Goes with'), ('position', 'Position'), ('with of', 'With <i>of</i>'),
                ('pattern', 'Pattern'), ('contrast', 'Contrast'), ('type', 'Type'),
                ('variants', 'Variants')],
    ),
    dict(
        slug='02-pronouns',
        dir='parts-of-speech/02-pronouns/catalog',
        title='The Pronoun Dictionary',
        eyebrow='02 &middot; Pronouns',
        lede='pronouns — personal, possessive, reflexive, relative, indefinite, and dialectal',
        accent='#2f6f6b', accent_dark='#79c9c2',
                tag_fields=['case', 'type', 'agreement'],
        fields=[('case', 'Case'), ('person / number', 'Person &amp; number'),
                ('refers to', 'Refers to'), ('agreement', 'Agreement'),
                ('pattern', 'Pattern'), ('contrast', 'Contrast'), ('type', 'Type'),
                ('variants', 'Variants')],
    ),
    dict(
        slug='03-verbs',
        dir='parts-of-speech/03-verbs/catalog',
        title='Irregular &amp; Phrasal Verbs',
        eyebrow='03 &middot; Verbs',
        lede='irregular verbs grouped by how their forms change, plus every phrasal verb built on them',
        accent='#8a5a2b', accent_dark='#dda96b',
        # files whose entries are built ON a base verb: listed inside the base
        # entry rather than as their own rows in the A-Z list
        derived_prefixes=('14-', '15-', '16-', '17-', '18-', '19-', '20-', '21-', '22-'),
        fields=[('forms', 'Forms'), ('separable', 'Separable'), ('base verb', 'Base verb'),
                ('transitive', 'Transitive'), ('verb type', 'Verb type'),
                ('transitivity', 'Transitivity'), ('passive', 'Passive'),
                ('pattern', 'Pattern'), ('group', 'Group'),
                ('third person', 'Third person'), ('-ing form', '-ing form'),
                ('type', 'Type'), ('contrast', 'Contrast'),
                ('phrasal verbs', 'Phrasal verbs built on this'), ('variants', 'Variants')],
    ),
    dict(
        slug='reporting-verbs',
        dir='grammar/01-reported-speech/catalog',
        title='Reporting Verbs',
        eyebrow='Grammar &middot; Reported speech',
        lede='reporting verbs, with every grammatical frame each one takes',
        accent='#9a4b52', accent_dark='#e8919a',
                tag_fields=['type'],
        fields=[('patterns', 'Patterns'), ('never', 'Never'), ('subjunctive', 'Subjunctive'),
                ('reports', 'Reports'), ('type', 'Type')],
    ),
]
