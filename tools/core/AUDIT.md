# Russian gloss audit

The one field in this dictionary that no deterministic check can validate.

A wrong IPA vowel has a shape a script can match. A wrong translation does not:
`шеврон` for *chevron* and `шаблон` for *chevron* are equally well-formed Russian,
and only knowing both languages separates them. So this pass is the only part of
the build that genuinely requires judgment rather than rules.

## What is already known-good

Structural checks over all 13,302 entries came back clean:

  * 0 entries missing a Russian gloss
  * 0 glosses without Cyrillic
  * 0 glosses reused across five or more different English headwords
  * 4 glosses containing Latin letters, all legitimate — *V-образная*, *Ethernet*,
    *PhD*, *буквы P*

So the failure mode being hunted here is **semantic**: a gloss that is good Russian
and good for *some* sense of the English word, but not for the sense this entry
actually defines.

## The rule for auditors

Change a gloss only when it is **wrong**, not when it is merely different from the
word you would have picked. `автомобиль` and `машина` are both correct for *car*;
rewriting one to the other is churn, not a fix. The bar is: would a Russian speaker
reading this gloss come away with the wrong idea of what the English word means?

Every change must be logged with its before and after, so the corrections can be
reviewed rather than trusted.
