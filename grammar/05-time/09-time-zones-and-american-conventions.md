# Time zones and American conventions

> The clock facts an American never stops to explain — six zones with two names apiece, the two Sundays that move the clock, the quarters that are not January to March, and the words that mean one thing in Boston and the opposite in London.

[← Time](README.md) &middot; [All grammar topics](../README.md)

Almost nothing in this section is grammar. It is the layer of shared assumption underneath every American sentence about time: that *3 o'clock* without a zone means the speaker's zone, that *Q1* might start in October, that *next Friday* is a coin flip, that *5 business days* is not five days. None of it is taught to Americans, because none of it has to be. All of it is guessable wrong by someone who learned English somewhere else.

Three ideas run through the whole file.

**A time without a zone is not a time.** An American writing to another American drops the zone because the default is obvious; an American writing to Moscow drops it out of habit, and the habit is the bug. *Let's talk at 3* is an incomplete sentence in an international thread. *Let's talk at 3 p.m. ET* is a complete one.

**The American clock moves; the Russian one does not.** Since 2014 Russia has not changed its clocks at all. The United States changes them twice a year. So the gap between Moscow and New York is seven hours for most of the year and eight hours for the rest, and it changes on American dates, for American reasons, with no warning anyone in Russia will notice.

**When a word is genuinely ambiguous, the fix is not to learn the right meaning — there isn't one.** *Biweekly* has two live readings among native speakers. *Next Friday* has two. The professional move is to write the unambiguous version: *every two weeks*, *Friday the 13th*. Half of this file is a list of places where the honest advice is "say it another way."

## The six US time zones

### The zones, their two names, and their offsets

The contiguous United States has four zones, and the states outside it add two more. Every zone has a **standard** name used in winter and a **daylight** name used in summer, and a **generic** name that covers both and is the one to write.

| Zone | Standard (winter) | Daylight (summer) | Generic | Offset (std / DST) | Where |
|---|---|---|---|---|---|
| **Eastern** | **EST** | **EDT** | **ET** | UTC−5 / UTC−4 | New York, Boston, Washington, Atlanta, Miami, Detroit |
| **Central** | **CST** | **CDT** | **CT** | UTC−6 / UTC−5 | Chicago, Dallas, Houston, Minneapolis, Nashville, New Orleans |
| **Mountain** | **MST** | **MDT** | **MT** | UTC−7 / UTC−6 | Denver, Salt Lake City, Albuquerque, Boise, Phoenix* |
| **Pacific** | **PST** | **PDT** | **PT** | UTC−8 / UTC−7 | Los Angeles, San Francisco, Seattle, Portland, Las Vegas |
| **Alaska** | **AKST** | **AKDT** | **AKT** | UTC−9 / UTC−8 | Anchorage, Juneau, Fairbanks |
| **Hawaii–Aleutian** | **HST** | **HDT** | **HT** | UTC−10 / UTC−9 | Honolulu (no DST) and the far Aleutians (DST) |

\* Phoenix is in the Mountain zone but does not change its clocks, which is its own problem — see [who opts out](#the-states-that-opt-out).

Three more that Americans meet on paperwork rather than on the phone: **Atlantic Standard Time (AST, UTC−4)** in Puerto Rico and the US Virgin Islands, which never changes; **Chamorro Standard Time (ChST, UTC+10)** in Guam and the Northern Mariana Islands; and **Samoa Standard Time (SST, UTC−11)** in American Samoa.

The four mainland zones are one hour apart in a row, which gives the single most useful fact on this page:

```
   Pacific      Mountain      Central       Eastern
    9:00          10:00        11:00         12:00
      |—— +1 ——————|—— +1 ———————|—— +1 ———————|

   Eastern is three hours ahead of Pacific.
   Pacific is three hours behind Eastern.
```

### Standard versus daylight, and why *ET* is the safe written form

This is the mistake almost every learner makes, and a great many Americans make it too. **EST is not a synonym for Eastern time.** It is Eastern time *in the winter*. From the second Sunday in March to the first Sunday in November, the correct abbreviation is **EDT**, and the offset is an hour different.

> The call is at 2 p.m. **EST** on July 9. — ✗ wrong by an hour; July is EDT  
> The call is at 2 p.m. **EDT** on July 9. — correct, but you had to know the date  
> The call is at 2 p.m. **ET** on July 9. — correct all year, and no one has to check

*ET*, *CT*, *MT*, *PT* mean "whatever Eastern (Central, Mountain, Pacific) time is on that date." They are shorter, they are always right, and they are what careful American business writing uses. Calendar invitations, airline schedules, and broadcast listings use them for exactly this reason: `8/7c` on a television promo means 8 p.m. Eastern, 7 p.m. Central, no season specified.

The one place to use the full four-letter form is when the offset itself matters — a contract deadline, a server cutover, a legal filing. There, write both: *by 5:00 p.m. EST (UTC−5) on January 14*.

> ✗ *The webinar is at 11 a.m. EST on June 3.* → *…at 11 a.m. **ET** on June 3.*  
> ✗ *We're on PST right now.* (said in August) → *We're on **PDT** right now.* / *We're on **Pacific time** right now.*

### How they are said out loud

Spoken American English almost never uses the three-letter abbreviation in full. What people say is the bare zone name, with *time* optional:

> The meeting's at three **Eastern**.  
> Nine a.m. **Pacific**, so that's noon for you.  
> He's on **Central time**.  
> Can we do 4:30 **your time**?  
> It airs at eight, seven **Central**.

When the letters are used aloud, they are spelled out one at a time — *E-S-T*, *P-S-T* — never pronounced as a word. And in speech Americans say *EST* and *PST* year-round as loose shorthand for "Eastern" and "Pacific," which is harmless in conversation and wrong in writing. Do not copy the spoken habit into an email.

Two more spoken shapes worth having:

> What time is it **there**?  
> It's three hours **earlier** on the West Coast. / It's three hours **later** back east.

*Back east* and *out west* are ordinary American directional phrases, and both carry a time implication without stating one.

### Ahead, behind, and whose time we mean

**English states the difference from the point of view of the clock, not of the traveler.** A place whose clock reads a larger number is *ahead*.

| Phrase | Means | Example |
|---|---|---|
| *X is three hours ahead of Y* | X's clock reads later | *New York is three hours ahead of Los Angeles.* |
| *X is two hours behind Y* | X's clock reads earlier | *Denver is two hours behind New York.* |
| *the time difference* | the gap, unsigned | *The time difference is seven hours.* |
| *my time* / *your time* | the speaker's or listener's zone | *That's 9 a.m. your time.* |
| *local time* | the zone of the place under discussion | *The flight lands at 6:40 local time.* |
| *their time* | a third party's zone | *It'll be the middle of the night their time.* |

> Moscow is **eight hours ahead of** New York in the winter.  
> Chicago is **an hour behind** New York.  
> We're **three hours apart**, so mornings are the only overlap.  
> I'll call at four **my time** — that's eleven at night **yours**.

Note the bare possessive in *my time*, *your time*, *their time*: no preposition, no article. ✗ *at my time*, ✗ *in the your time*. And *local time* takes no article either: *arrives 6:40 local time*, not ✗ *the local time* in that slot.

## Daylight saving time

### Spring forward, fall back

The name is **daylight saving time** — singular *saving*, no `-s`. *Daylight savings time* is extremely common in American speech and is still corrected in edited writing. The abbreviation is **DST**.

The mnemonic every American child learns is four words:

> **Spring forward, fall back.**

In spring the clocks move **forward** one hour. In fall they move **back** one hour. *Fall* is doing double duty — the season and the direction — which is why the phrase sticks.

### When it happens in the US

| Event | When | What the clock does | The hour |
|---|---|---|---|
| **DST begins** | second Sunday in **March**, 2:00 a.m. local | 2:00 a.m. → 3:00 a.m. | you **lose an hour** |
| **DST ends** | first Sunday in **November**, 2:00 a.m. local | 2:00 a.m. → 1:00 a.m. | you **gain an hour** |

Those dates have been fixed since 2007. Because the change happens at 2:00 a.m. *local* time in each zone, it rolls across the country — the East Coast springs forward three hours before the West Coast does.

The idiom is worth learning as a pair, because it is what people actually say:

> We **lose an hour** tonight. — the March change; everyone complains  
> We **gain an hour** tonight. — the November change; everyone is pleased  
> The clocks **go forward** this weekend. / The clocks **change** this weekend.  
> Don't forget to **set your clocks back** Saturday night.  
> It gets dark at five now — I hate **the time change**.

Two useful facts about the rest of the world. **Europe does not change on the same days**: the EU and the UK switch on the last Sunday in March and the last Sunday in October, so for about three weeks in March and one week in October the gap between New York and London is not its usual five hours. And **the Southern Hemisphere is on the opposite cycle** — Australian DST begins in October and ends in April.

### The states that opt out

A state may leave DST, but under federal law it may not adopt it permanently on its own. Two states and several territories sit out:

- **Arizona** — except the Navajo Nation, which does observe DST. So in summer Phoenix is on the same clock as Los Angeles, and in winter the same clock as Denver. Scheduling anything with Phoenix is an exercise in checking twice.
- **Hawaii** — stays on HST all year. In winter Hawaii is two hours behind Pacific; in summer, three.
- **Puerto Rico, the US Virgin Islands, Guam, American Samoa, and the Northern Marianas** — none observes DST.

Bills to make DST permanent nationwide come up in Congress regularly and have not passed. Assume the two Sundays.

### Russia does not change its clocks — so the offset is not constant

Russia abolished seasonal clock changes. After a short period on permanent summer time, the country settled in October 2014 onto permanent standard time, and Moscow has been **UTC+3 year-round** ever since.

The consequence matters more than the history. **The Moscow–US gap changes twice a year, and both changes are American.**

| Period | Moscow ↔ New York | Moscow ↔ Chicago | Moscow ↔ Denver | Moscow ↔ Los Angeles |
|---|---|---|---|---|
| **Nov → Mar** (US standard) | **+8** | +9 | +10 | **+11** |
| **Mar → Nov** (US daylight) | **+7** | +8 | +9 | **+10** |

> In January, 9 a.m. in New York is **5 p.m.** in Moscow.  
> In July, 9 a.m. in New York is **4 p.m.** in Moscow.  
> Nothing moved in Moscow. New York moved.

This is the single most practical paragraph in the file for a Russian speaker, and it has a plain operational form: **a standing call that is comfortable in December will be an hour earlier in Moscow from mid-March**, and an American calendar invitation will quietly do this to you without saying so, because it stores the American local time.

## Coordinating across zones

### Asking and offering

The phrase book for setting up a call across zones is short and highly fixed. These are the sentences Americans actually send.

> **What time works for you?**  
> **Does 10 a.m. ET work on your end?**  
> **What's your availability** Thursday?  
> I'm **flexible** — mornings are better for me.  
> Anything **before 3 your time** is fine.  
> **That's 9 a.m. your time**, if I did the math right.  
> Would **earlier in your day** be easier?  
> I'll **send an invite** — it'll show up in your local time.  
> Let's **find a window** that isn't the middle of the night for you.  
> **Can we push it an hour?** / **Can we move it up an hour?**

Two idioms that reliably confuse learners, because they point in opposite directions and neither one says which:

| Phrase | Means |
|---|---|
| *push it back* / *push it* | make it **later** |
| *move it up* / *bump it up* | make it **earlier** |
| *move it back* | usually later, occasionally earlier — **ask** |

*Move it back* is genuinely ambiguous even among Americans. If you hear it, confirm with a time: *So 4 instead of 3?*

### UTC, GMT, and Zulu

**UTC** — Coordinated Universal Time — is the reference all other zones are offsets from. The letters match neither the English name nor the French one; they are a compromise nobody defends. **GMT**, Greenwich Mean Time, is the older British term, and in ordinary American usage the two are treated as the same thing. They differ by less than a second, which matters to astronomers and to nobody else in this section.

> The maintenance window is 02:00–04:00 **UTC**.  
> The deadline is midnight **GMT**.  
> Moscow is **UTC+3**. New York is **UTC−5** in winter, **UTC−4** in summer.

**Zulu** is the letter *Z* in the NATO phonetic alphabet, and *Z* is the suffix ISO 8601 uses for UTC. Aviation, the military, and machine-readable timestamps all use it; civilians do not.

> Wheels up at **1400 Zulu**.  
> The log entry reads `2026-03-08T14:00:00Z` — that final **Z** is UTC.

Note the offset signs. **Ahead of UTC is a plus, behind is a minus**, and American zones are all minus. Say them as *UTC minus five*, *UTC plus three*.

### The 24-hour clock

Americans call it **military time** and, outside the military, aviation, hospitals, and transit, they do not use it. The 12-hour clock with *a.m.* and *p.m.* is the civilian default in speech, in writing, and on most American clock faces.

| Written | Said (American, 24-hour) | Said (American, ordinary) |
|---|---|---|
| 08:00 | *oh eight hundred* | *eight a.m.* |
| 13:00 | *thirteen hundred* | *one p.m.* |
| 14:30 | *fourteen thirty* | *two thirty* |
| 00:00 | *zero hundred* / *twenty-four hundred* | *midnight* |

Scheduling software is the exception. Calendar applications, booking systems, airline manifests, and server logs offer a 24-hour setting, and international teams turn it on precisely because it removes the a.m./p.m. question. If a colleague writes *15:00 CET*, they are not being military; they are being careful.

Two related traps belong to [Telling the time](01-telling-the-time.md) but are worth flagging here: **12 p.m. is noon and 12 a.m. is midnight**, which almost nobody can reproduce under pressure, so write *noon* and *midnight*; and *midnight Friday* is ambiguous between the start and the end of Friday, so write *Friday at 11:59 p.m.* or *Saturday at 12:01 a.m.*

### Jet lag, red-eyes, and the rest of the travel vocabulary

| Word | Means |
|---|---|
| **jet lag** | the physical effect of crossing zones — *I'm still jet-lagged* |
| **red-eye** | an overnight flight, usually west to east — *I took the red-eye* |
| **layover** / **stopover** | time on the ground between flights |
| **turnaround trip** | out and back in a day or two |
| **body clock** | your internal sense of time — *my body clock is off* |
| **acclimate** / **adjust** | to get used to a new zone |
| **the time change** | either the DST switch or the shift from traveling |

> I flew in on the **red-eye** and I'm useless today.  
> Give me a day to get over the **jet lag**.  
> Going east is worse — you **lose** the hours.  
> My **body clock** still thinks it's four in the morning.

*Jet lag* is two words as a noun and hyphenated as an adjective: *jet lag* / *jet-lagged*. There is no verb ✗ *to jet lag*.
## Dates, weeks, quarters, and the school year

### Month, day, year

**The United States writes the month first.** This is the convention that reverses most dangerously, because half the possible dates look valid either way.

| Written | American reading | Russian / European reading |
|---|---|---|
| **3/8/2026** | March 8 | 3 August |
| **11/12/2026** | November 12 | 11 December |
| **07/04** | July 4 — Independence Day | 7 April |
| **1/2/27** | January 2 | 1 February |

The American long forms, with their punctuation:

> **March 8, 2026** — month, day, comma, year  
> **March 8** — no comma when the year is absent  
> **Sunday, March 8, 2026** — commas around the date  
> *The contract was signed on **March 8, 2026**, in Denver.* — and a comma **after** the year too, mid-sentence

Two safe formats when the audience is international: spell the month (*8 March 2026* and *March 8, 2026* are both unambiguous), or use ISO 8601 (**2026-03-08**), which is unambiguous by construction and is what databases, filenames, and careful engineers use.

Said aloud, Americans put the month first there too: *March eighth*, *July fourth*, *the eighth of March* being a possible but distinctly less common alternative. Years: *nineteen ninety-nine*, *two thousand eight*, *twenty twenty-six*.

A number convention that travels with dates: American English uses a **period for the decimal point and a comma for thousands** — `1,500.75` — which is exactly reversed from the Russian `1 500,75`. It shows up in durations and rates (*1,200 hours*, *$1,250.00 per month*) more often than people expect.

### The week starts on Sunday

American calendars, payroll weeks, and date pickers put **Sunday** in the first column. The ISO standard, and every Russian calendar, starts the week on **Monday**.

This has three consequences that bite.

- **"The first day of the week" is Sunday** to an American and Monday to you. *Early in the week* still means Monday or Tuesday, because nobody counts Sunday as a working day, but the grid is different.
- **The weekend is Saturday and Sunday**, and it sits at the two ends of the American grid rather than together at the right. A calendar app with the wrong locale will show you a week you cannot read at a glance.
- **A "week ending" date** on a timesheet or a sales report is typically a Saturday in the US and a Sunday in Europe.

American prepositions for the weekend are covered in [the British comparison](#american-versus-british-time-usage) below, but the headline is that Americans say ***on* the weekend** and the British say ***at* the weekend**, and both say *this weekend* with no preposition at all.

### Week 1 and ISO weeks

"Week 32" in an email from a European colleague and "week 32" in an American spreadsheet are frequently not the same week.

| System | Week 1 is | Week starts |
|---|---|---|
| **ISO 8601** (Europe, Russia, most tools' default outside the US) | the week containing the first **Thursday** of January — equivalently, the week containing January 4 | Monday |
| **US common practice** | the week containing **January 1** | Sunday |
| **US retail (4-5-4)** | the week containing a fiscal-year start in late January or early February | Sunday |

Americans outside manufacturing, logistics, and retail barely use week numbers at all. If someone writes *W32* or *KW32* to you, they are almost certainly using ISO, and the safe reply names the dates: *Week 32 — that's August 3–9, right?*

### Fiscal quarters: *Q1* is not January to March for everyone

A quarter is three months of a **fiscal year**, and a fiscal year does not have to start in January. This is the convention that most reliably causes an expensive misunderstanding.

| Organization | Fiscal year runs | So Q1 is |
|---|---|---|
| Most companies, and all ordinary speech | Jan 1 – Dec 31 | **January–March** |
| **US federal government** | Oct 1 – Sep 30 | **October–December** |
| Many large tech firms | Oct 1 – Sep 30 | October–December |
| Many US retailers | late Jan – late Jan | **February–April** |
| Many universities | Jul 1 – Jun 30 | July–September |

So *Q1 FY27* for a federal agency means **October, November, and December of 2026** — a quarter that is mostly in the previous calendar year. The naming convention is that the fiscal year takes the number of the calendar year it **ends** in.

The disambiguating vocabulary is the fix:

> **calendar Q1** — January through March, whatever the company's books do  
> **fiscal Q1** / **FQ1** / **Q1 FY27** — the first quarter of that fiscal year  
> **H1** and **H2** — the two halves of a year  
> **YTD** (year to date), **QoQ** (quarter over quarter), **YoY** (year over year)  
> *We'll ship it **by end of quarter**.* — ask which one  
> *That slipped to **next quarter**.*

> ✗ *Q1 means January, February, March.* → *Q1 means January through March **on a calendar fiscal year**. Check theirs.*

### Semester, trimester, quarter, and the school year

| Term | Length | Who uses it |
|---|---|---|
| **semester** | about 15 weeks, two per year | most US colleges and universities; many high schools |
| **quarter** | about 10 weeks, three or four per year | a minority of universities |
| **trimester** | three terms per year | some K–12 districts — and, in ordinary life, pregnancy |
| **school year** | about ten months, spanning two calendar years | everywhere |
| **summer session** / **summer school** | short terms in June–August | optional, remedial, or accelerated |

The **school year** is the piece that surprises people. It does not line up with the calendar year, so it is written with a span: *the 2026–27 school year*. It starts in **August or early September** — often the week before or after **Labor Day**, the first Monday in September — and ends in **May or June**.

> She's a junior this year. — the **third** of four years of high school or college  
> The fall semester starts August 24.  
> He graduated with the **class of 2027**.  
> We're off for **spring break** the third week of March.

**Summer break** — also *summer vacation*, and just *the summer* — runs roughly ten to twelve weeks. Combined with *winter break* (about two weeks around Christmas and New Year's) and *spring break* (one week, usually in March), it is the rhythm that American family and business calendars actually run on. American offices empty out in July and in the week between Christmas and New Year's, and nothing gets decided in either period.

## The ambiguous words

Every item here has two live readings among educated native speakers. The advice in each case is the same: recognize both, write neither.

### *Biweekly* and *bimonthly*

| Word | Reading A | Reading B | Verdict |
|---|---|---|---|
| **biweekly** | every two weeks | twice a week | genuinely both |
| **bimonthly** | every two months | twice a month | genuinely both |
| **biannual** | twice a year | every two years | mostly A, but contested |
| **biennial** | every two years | — | unambiguous, and rarer |
| **semiweekly** | twice a week | — | unambiguous, and stilted |
| **semimonthly** | twice a month | — | unambiguous, and used in payroll |

Dictionaries list both readings for *biweekly* and *bimonthly* because both are in use, and [Duration and frequency](04-duration-and-frequency.md) works the same problem from the frequency side. No amount of insisting on the "correct" one will make your reader parse it your way.

> ✗ *We meet biweekly.* → *We meet **every two weeks**.* / *We meet **twice a week**.*  
> ✗ *The bimonthly report is due Friday.* → *The **monthly** report…* / *The report we send **every other month**…*

The one place American English does hold the distinction firmly is **payroll**, where the two words name two different legal arrangements: ***biweekly*** **pay is every two weeks — 26 paychecks a year**, and ***semimonthly*** **pay is twice a month — 24 paychecks**. If an HR document says *biweekly*, it means every two weeks.

The safe replacements, in order of naturalness: *every two weeks*, *every other week*, *twice a week*, *twice a month*, *every other Tuesday*, *the 1st and the 15th*.

### *Next Friday*

Say it on a Wednesday. Does it mean the Friday two days from now, or the Friday of the following week? **Americans split roughly down the middle, and the split is regional and personal rather than right and wrong.**

| Said on Wednesday the 4th | Speaker A means | Speaker B means |
|---|---|---|
| *this Friday* | the 6th | the 6th |
| *next Friday* | the 6th | the 13th |
| *a week from Friday* | the 13th | the 13th |
| *Friday week* | — | British only |

The two unambiguous constructions are worth memorizing, because they are what careful people use:

> **a week from Friday** — the Friday after the coming one  
> **Friday the 13th** — name the date and stop worrying  
> **this coming Friday** — the next one to occur  
> **not this Friday, the one after**

The same ambiguity runs through *next weekend*, *next month*, and *next Tuesday*. It does **not** affect *next week*, *next year*, or *next summer*, where the unit itself is the next one along and nobody hesitates.

> ✗ *See you next Friday.* → *See you **Friday the 13th**.*

### *This weekend*, said on a Monday

*This weekend* means **the coming weekend** for almost everyone, on almost every day of the week. The trouble is Sunday, and to a lesser degree Saturday.

| Said on | *this weekend* | *last weekend* | *next weekend* |
|---|---|---|---|
| Monday | the coming one | the one just finished | the one after the coming one |
| Wednesday | the coming one | the one just finished | the one after |
| Saturday | the one you are in | the previous one | the one after |
| Sunday night | ambiguous — the one ending, or the coming one | the previous one | the coming one, for some speakers |

The fix is the same as everywhere else in this section: attach a date or a day. *This Saturday*, *the 14th*, *this coming weekend*.

### *Half five*, *quarter of*, *quarter after*

**British *half five* means 5:30. An American will not understand it**, and the ones who guess usually guess 4:30, reasoning from *half to five* — which is, incidentally, what Russian «полшестого» means. The construction does not exist in American English at all — not as a variant, not as a regionalism. Say *five thirty*.

The American clock idioms that go the other way and baffle the British:

| American | Means | Note |
|---|---|---|
| *quarter of six* | **5:45** | *of* = "before"; Northeast and mid-Atlantic especially |
| *quarter till six* / *quarter to six* | 5:45 | *till* is the general American form |
| *ten of seven* | **6:50** | same *of* |
| *twenty of nine* | 8:40 | same |
| *quarter after six* | 6:15 | British says *quarter past* |
| *five after two* | 2:05 | British says *five past* |
| *half past five* | 5:30 | used in the US, but *five thirty* is far commoner |

***Of* means "before."** That is the whole rule, and it is the one American time idiom that is genuinely opaque to outsiders, because nothing else in the language uses *of* that way. *Ten of seven* is 6:50; *ten after seven* is 7:10.

> ✗ *Let's meet at half six.* → *Let's meet at **six thirty**.*  
> ✗ *"Quarter of six" means 6:15.* → *It means **5:45**.*

### *Momentarily* and *presently*

Two adverbs where American and British usage have drifted apart, and where an American sentence can mean the opposite of what a British-trained learner hears.

| Word | American | British | Advice |
|---|---|---|---|
| **momentarily** | **in a moment**, very soon | **for a moment**, briefly | say *in a moment* or *briefly* |
| **presently** | **currently**, at present — and also *soon* | **soon**, shortly | say *currently* or *soon* |

> *We'll be landing **momentarily**.* — American: in a few minutes. British ear: we will touch down and immediately take off again.  
> *The door opened **momentarily**.* — British: for a moment. American ear: strange.  
> *The office is **presently** closed.* — American: it is closed now.  
> *He'll be with you **presently**.* — both: shortly. This one is safe.

*Presently* meaning "currently" is standard American English and appears in edited prose, though a minority of style guides still object to it. *Currently* is shorter and offends nobody. The full entries are with the [adverbs of time](../../parts-of-speech/05-adverbs/catalog/06-time.md#presently) and the [frequency and duration adverbs](../../parts-of-speech/05-adverbs/catalog/07-frequency-duration.md#momentarily).

Two more in the same family. ***Directly*** in the American South can mean "soon" (*I'll be along directly*), which elsewhere sounds like "immediately." And ***in a minute*** never means sixty seconds — it means "shortly," and *give me a second* means considerably more than a second.

## American versus British time usage

The full comparison. Both columns are correct English; only one of them is American.

| | American | British |
|---|---|---|
| The weekend | ***on* the weekend** | ***at* the weekend** |
| Ranges of days | *Monday **through** Friday* | *Monday **to** Friday* |
| Quarter past | *a quarter **after** five*, *five fifteen* | *a quarter **past** five* |
| Quarter to | *a quarter **of** six*, *a quarter **till** six* | *a quarter **to** six* |
| Minutes before | *ten **of** seven*, *ten **till** seven* | *ten **to** seven* |
| 5:30 | *five thirty* | *half five*, *half past five* |
| Two weeks | *two weeks* | *a **fortnight*** |
| A week from Friday | *a week from Friday* | *Friday week*, *a week on Friday* |
| Days off in law | *federal holiday*, *public holiday* | *bank holiday*, *public holiday* |
| Time off work | ***vacation***, *PTO*, *time off* | ***holiday***, *annual leave* |
| On leave | *on vacation*, *out of the office* | *on holiday* |
| *schedule* | /ˈskɛdʒuəl/ — "SKEJ-ool" | /ˈʃɛdjuːl/ — "SHED-yool" |
| Bare day adverbs | *I work **Saturdays**.* *See you **Tuesday**.* | *I work **on** Saturdays.* |
| Dates in figures | **3/8/2026** = March 8 | **8/3/2026** = 8 March |
| Dates spoken | *March eighth* | *the eighth of March* |
| The season | ***fall***, also *autumn* | *autumn* |
| Summer clock | *daylight saving time*, *DST* | *British Summer Time*, *BST* |
| School stages | *fifth **grade***, *a senior* | *Year 5*, *Year 13* |
| University period | *semester*, *quarter* | *term* |
| A long time | *forever*, *ages* | *ages*, *donkey's years* |

Two notes on the entries that matter most.

***Monday through Friday*** **is the American inclusive range**, and it is unambiguous: Friday is included. British *Monday to Friday* is the same span, but *to* alone leaves Americans momentarily unsure whether the endpoint is in, which is why American contracts, store hours, and schedules all use *through*. The abbreviation is *M–F*, and the hyphen form *Monday-Friday* is ordinary in signage.

***Fortnight* is not American.** It is not archaic, it is not formal, it is not rare — it simply is not used. Americans understand it from books, and they do not say it. Use *two weeks* or *every two weeks*.

## Units of time and their quirks

### The vague small numbers

| Expression | Usually means | Notes |
|---|---|---|
| **a couple of** | 2, sometimes 2–3 | *a couple days* without *of* is normal speech, informal in writing |
| **a few** | 3–5 | positive: there are some |
| **few** | almost none | negative: *few people came* |
| **several** | 3–7, more than a few | vaguer and larger than *a few* |
| **a number of** | unspecified, plural | deliberately vague; takes a plural verb |
| **a while** | minutes to years | *in a while*, *for a while*, *a while back* |
| **forever** | far too long | hyperbole: *That took forever.* |

> I'll be back in **a couple of** minutes.  
> Give it **a few** days and call them again.  
> **Few** people showed up. — a complaint  
> **A few** people showed up. — a modest success  
> He's been gone **several** weeks now.

The *a few* / *few* split is the one that changes the meaning of a sentence rather than its precision. *A few* is positive; bare *few* is close to negative. The same goes for *a little* and *little*.

### The big ones

| Word | Length | Note |
|---|---|---|
| **fortnight** | 14 nights = 2 weeks | **British**; not used in the US |
| **decade** | 10 years | *the eighties*, *the 2010s* |
| **score** | 20 years | archaic; survives in *Four score and seven years ago* |
| **generation** | 20–30 years | also the named cohorts below |
| **century** | 100 years | *the twentieth century* = 1901–2000 |
| **the turn of the century** | around 1900 or 2000 | say which |
| **an era**, **an age** | indefinite and long | *the end of an era* |

The American named generations, treated at length in [Age, life stages and eras](10-age-life-stages-and-eras.md), come up constantly in business writing and in conversation: **Baby Boomers** (born roughly 1946–64), **Gen X** (1965–80), **Millennials** (1981–96), **Gen Z** (1997–2012), **Gen Alpha** (2013 on). The boundaries are soft and the words are used loosely.

### Business days versus calendar days

**This is the distinction that costs money.** A **business day** is a Monday through Friday that is not a federal holiday. A **calendar day** is any day at all.

| Phrase | Counts | Five of them, starting Thursday |
|---|---|---|
| *5 **calendar** days* | every day | ends the following Tuesday |
| *5 **business** days* | weekdays only, minus holidays | ends the following **Thursday** |
| *within 30 days* | calendar, unless it says otherwise | about a month |
| *within 30 business days* | weekdays only | about **six weeks** |

> Allow **7 to 10 business days** for delivery.  
> Refunds post in **3–5 business days**.  
> Payment is due **within 30 days** of the invoice date.  
> We'll respond by **the next business day**.

**Unqualified *days* in an American contract means calendar days.** If a document matters, look for the definition; well-drafted ones say *"days" means calendar days unless otherwise specified*.

The eleven **federal holidays** are the ones that stop the business-day count: New Year's Day, Martin Luther King Jr. Day (third Monday in January), Presidents' Day (third Monday in February), Memorial Day (last Monday in May), Juneteenth (June 19), Independence Day (July 4), Labor Day (first Monday in September), Columbus Day (second Monday in October), Veterans Day (November 11), Thanksgiving (fourth Thursday in November), and Christmas Day. When one falls on a Saturday it is **observed** on the Friday before; on a Sunday, the Monday after — and *observed* is the word on the calendar. Two more days stop work without being federal holidays at all: **the Friday after Thanksgiving**, and the stretch between **Christmas and New Year's**.
### The work week and its shapes

| Term | Means |
|---|---|
| **work week** (American) / *working week* (British) | Monday through Friday |
| **business hours** | roughly 9 a.m. to 5 p.m. local |
| **banker's hours** | short hours — mildly sarcastic |
| **after hours** | outside business hours |
| **off-hours** | outside the busy period |
| **COB** / **EOB** / **EOD** | close, end of business, end of day — about 5 p.m. |
| **9 to 5** | an ordinary office job, often dismissive |
| **24/7** | all the time — *said "twenty-four seven"* |
| **around the clock** | continuously |
| **overtime** | hours past 40 in a week, usually paid at 1.5× |
| **a four-day work week** | a compressed or shortened schedule |

***COB* and *EOD* are time-zone traps in themselves**, and the rest of the deadline vocabulary is in [Schedules, appointments and deadlines](08-schedules-appointments-and-deadlines.md). *By EOD Friday* means 5 p.m. in somebody's zone, and the sender rarely says whose. For a deadline that crosses zones, write the hour: *by 5 p.m. ET Friday*.

## Digital-era time words

The vocabulary of software, remote work, and the internet. Most of it is now ordinary American business English, not jargon.

| Word | Means | Example |
|---|---|---|
| **real time** | as it happens — noun phrase two words, adjective hyphenated | *We can see it **in real time**.* &middot; *a **real-time** dashboard* |
| **asynchronous**, **async** | not at the same time; each person at their own hour | *Let's keep this **async**.* |
| **synchronous**, **a sync** | at the same time — and, as a noun, a meeting | *Let's set up a **sync** Thursday.* |
| **lag**, **latency**, **laggy** | delay between action and result | *There's about a second of **lag**.* |
| **timestamp** | the recorded moment of an event; also a verb | *Check the **timestamp** on the file.* |
| **time-boxed**, **timebox** | limited to a fixed duration in advance | *The discussion is **time-boxed** to ten minutes.* |
| **sprint** | a fixed work cycle, usually one or two weeks | *We'll pick it up next **sprint**.* |
| **standup** | a short daily status meeting | *Standup is at 9:15.* |
| **turnaround** | the time to complete and return something | *a 48-hour **turnaround*** &middot; *a quick **turnaround*** |
| **lead time** | how far ahead you must order or plan | *Six weeks' **lead time** on the parts.* |
| **SLA** | service-level agreement — a promised response or uptime | *We're **within SLA**.* &middot; *a four-hour **SLA*** |
| **uptime** / **downtime** | time a system is running / not running | *99.9% **uptime*** &middot; *scheduled **downtime*** |
| **maintenance window** | a planned period when a system is off | *The window is 02:00–04:00 UTC.* |
| **screen time** | hours spent looking at devices | *I'm cutting down my **screen time**.* |
| **doomscrolling** | compulsively reading bad news | *I lost an hour **doomscrolling**.* |
| **hard stop** | a fixed end time for a meeting | *I have a **hard stop** at three.* |
| **bandwidth** | capacity, stated as if it were time | *I don't have the **bandwidth** this week.* |
| **slip** | to miss a planned date | *The launch **slipped** to June.* |
| **sunset**, **EOL** | to retire a product; end of life | *They're **sunsetting** the old plan.* |

Four notes on the ones that misbehave.

***Async* is now an adjective, an adverb, and almost a verb** in American work talk: *async communication*, *let's do it async*, *we've gone async*. It is informal and extremely current. In writing to someone outside tech, *asynchronous* or *on your own schedule*.

***A sync*** as a countable noun meaning "a short meeting" is recent, common, and invisible in dictionaries. *Let's get a sync on the calendar.*

***Turnaround*** is one word as a noun, two as a verb: *a quick turnaround*, but *turn it around by Friday*. And ***real time*** takes *in*: *in real time*, never ✗ *at real time* or ✗ *on real time*.

## For Russian speakers

Five interference points, in order of how much trouble they cause.

**1. The Moscow–US gap is not a constant, and both of its changes are American.**

Russia has not changed its clocks since 2014. The United States changes twice a year. So an offset you learned in February is wrong in April.

| | Nov → Mar | Mar → Nov |
|---|---|---|
| Moscow ↔ New York | **8 hours** | **7 hours** |
| Moscow ↔ Los Angeles | **11 hours** | **10 hours** |
| Moscow ↔ London | 3 hours | 2 hours |

Practical consequences. A recurring call stored in an American calendar keeps the **American** hour and moves the Moscow hour. An American colleague who says *same time as always* means the same American time. And in the three weeks between the American change in March and the European change at the end of the month, the Moscow–London gap and the Moscow–New York gap are both temporarily unusual.

**2. The date order reverses, and both readings are plausible.**

Russian writes `08.03.2026` and means 8 March. American writes `3/8/2026` and means March 8. Neither format tells you which convention it is in, and roughly two-thirds of all dates in a year are valid under both readings.

> ✗ *The invoice is dated 05.11.2026, so it's November 5.* → In an American document, `11/5/2026` is November 5 and `5/11/2026` is **May 11**.

Three defenses: spell the month, use ISO `2026-03-08`, or say the date back to the person. Note also the punctuation — Americans use slashes where Russians use periods, and Americans do not write a leading zero in speech-adjacent contexts (*March 8*, not *March 08*).

**3. *Биweekly* — the *раз в две недели* trap.**

Russian is precise here and English is not. «Раз в две недели» is unambiguous; *biweekly* is not, and «два раза в неделю» is also *biweekly* to some readers.

| Russian | Write in English | Do not write |
|---|---|---|
| раз в две недели | *every two weeks*, *every other week* | ✗ *biweekly* |
| два раза в неделю | *twice a week* | ✗ *biweekly* |
| раз в два месяца | *every two months* | ✗ *bimonthly* |
| два раза в месяц | *twice a month*, *semimonthly* | ✗ *bimonthly* |
| раз в полгода | *twice a year*, *every six months* | ✗ *biannually* |

**4. Business days versus calendar days — the concept transfers, the calendar does not.**

The Russian distinction between «рабочих дней» and «календарных дней» maps exactly onto *business days* and *calendar days*, so the idea needs no explanation. What does not transfer is which days are which. There are **eleven American federal holidays**, none of them in the first week of January, and there is no long New Year's holiday — American offices reopen on January 2. Conversely, late November and late December are effectively dead, and no American will say so in the contract.

> «в течение 10 рабочих дней» → *within **10 business days*** — about two calendar weeks, longer if a holiday falls inside  
> «в течение 30 календарных дней» → *within **30 calendar days***  
> ✗ *within 30 working days* → *within 30 **business** days* — *working days* is the British form

**5. The 24-hour clock is your default and not theirs.**

Russian writing uses `19:00` without comment. American writing uses `7 p.m.`, and a bare `19:00` in an email to an American reader will be understood but will read as technical or foreign. In scheduling tools, 24-hour is a perfectly good setting and international teams use it deliberately — but in prose, convert.

> «Встреча в 19:00» → *The meeting is at **7 p.m.*** — and add the zone: *7 p.m. Moscow time*.

**What transfers for free.** Russian already distinguishes «рабочий день» from «календарный день», already has «часовой пояс» for *time zone*, already names quarters «квартал» — though with the same fiscal-year caveat — and already uses «полугодие» for *H1* and *H2*. The vocabulary is there. It is the American defaults underneath it that have to be replaced one by one.

## Common mistakes

| Wrong | Right | Why |
|---|---|---|
| ✗ *The webinar is at 11 a.m. EST on June 3.* | *…at 11 a.m. **ET** on June 3.* | June is daylight time. *ET* covers both. |
| ✗ *We're on PST in August.* | *We're on **PDT** in August.* / *…on **Pacific time**.* | *PST* is winter only. |
| ✗ *Let's talk at 3.* (to another country) | *Let's talk at 3 p.m. **ET**.* | A time with no zone is incomplete. |
| ✗ *daylight savings time* | *daylight **saving** time* | Singular *saving*, no `-s`. |
| ✗ *Moscow is always 8 hours ahead of New York.* | *…**8 hours in winter, 7 in summer**.* | The US clock moves; the Russian one does not. |
| ✗ *Arizona is on Pacific time.* | *Arizona is on **Mountain** time and skips DST.* | It only matches Pacific in the summer. |
| ✗ *at my time* | ***my** time* | No preposition: *3 p.m. my time*. |
| ✗ *I'll call you at the local time.* | *…at 6:40 **local time**.* | No article. |
| ✗ *See you at the weekend.* | *See you **on** the weekend.* / *…**this** weekend.* | *At the weekend* is British. |
| ✗ *We're open Monday to Friday.* | *We're open Monday **through** Friday.* | *Through* is the American inclusive range. |
| ✗ *Let's meet at half six.* | *Let's meet at **six thirty**.* | *Half six* does not exist in American English. |
| ✗ *"Quarter of six" is 6:15.* | *It is **5:45**.* | American *of* means "before." |
| ✗ *We'll be landing momentarily — for about a minute.* | *We'll be landing **in a moment**.* | American *momentarily* = soon, not briefly. |
| ✗ *We meet biweekly.* | *We meet **every two weeks**.* | *Biweekly* has two live readings. |
| ✗ *See you next Friday.* (said Wednesday) | *See you **Friday the 13th**.* | *Next Friday* is a coin flip. |
| ✗ *Q1 is January through March for everyone.* | *Q1 is the first quarter of **their** fiscal year.* | Federal and tech Q1 is October–December. |
| ✗ *within 30 working days* | *within 30 **business** days* | *Working days* is British. |
| ✗ *5 business days from Thursday is Tuesday.* | *…is the following **Thursday**.* | Weekends and holidays do not count. |
| ✗ *The report is due 3/8 — that's 3 August.* | *…that's **March 8**.* | American dates are month first. |
| ✗ *a fortnight from Tuesday* | *two weeks from Tuesday* | *Fortnight* is not used in the US. |
| ✗ *Send it by EOD.* (across zones) | *Send it by **5 p.m. ET**.* | *EOD* has no zone attached. |
| ✗ *updates at real time* | *updates **in real time*** | *Real time* takes *in*. |

## Quick reference

**The four mainland zones, west to east.**

```
   PT  ──  MT  ──  CT  ──  ET
   9am    10am    11am    12pm      Eastern is +3 from Pacific
   −8/−7  −7/−6   −6/−5   −5/−4     UTC offset: standard / daylight
```

**The two Sundays.**

```
   second Sunday in March     2am → 3am   spring forward   lose an hour
   first Sunday in November   2am → 1am   fall back        gain an hour
   Opting out: Arizona (not the Navajo Nation), Hawaii, PR, USVI, Guam, Samoa
   Russia: no change since 2014. Moscow is UTC+3 all year.
```

**Six rules that prevent most of the damage.**

1. **Write *ET*, *CT*, *MT*, *PT***, not *EST* and *PST*, unless the offset itself is the point.
2. **Never send a time without a zone** to anyone outside your own.
3. **Never write a date in all figures** to an international reader. Spell the month, or use `2026-03-08`.
4. **Never write *biweekly*, *bimonthly*, or *next Friday***. Write *every two weeks*, *twice a month*, *Friday the 13th*.
5. **Ask which fiscal year** before you believe a *Q1*, and ask *business or calendar?* before you believe a deadline in days.
6. **Convert 19:00 to 7 p.m.** in prose, and keep 24-hour for tools and logs.

**The words that mean the opposite of what you think.**

```
   half five        5:30 — British only; Americans do not say it
   quarter of six   5:45 — American "of" means "before"
   ten of seven     6:50
   momentarily      US: in a moment  |  UK: for a moment
   presently        US: currently, or soon  |  UK: soon
   push it back     later            |  move it up   earlier
   biweekly         every two weeks  |  twice a week — both are in use
```

## Practice

Rewrite, answer, or convert. Several items have more than one acceptable answer; the key gives the safest.

1. Fix the zone: *The kickoff is at 9 a.m. EST on July 14.*
2. It is 10 a.m. Tuesday in Chicago. What time is it in Los Angeles? In New York?
3. It is January. A Moscow colleague wants a 5 p.m. Moscow call. What time is that in New York?
4. The same call, in July. What time in New York now, and what moved?
5. An American writes *the deadline is 4/5/2026*. A Russian reader assumes 4 May. What is it actually, and how should it have been written?
6. Your American manager writes *let's sync biweekly*. What are the two possible readings, and what do you ask?
7. Today is Wednesday the 4th. A colleague says *see you next Friday*. What are the two candidate dates, and what do you reply?
8. Convert to natural American prose: *Встреча в 19:30 по московскому времени, 8 марта.*
9. An order placed Thursday afternoon promises delivery in *5 business days*. What is the earliest day it arrives, assuming no holidays?
10. Same order, but Monday is a federal holiday. Now what?
11. A US federal agency says a report is due *in Q1 FY27*. Which three months are those?
12. What does *quarter of eight* mean? What does *quarter after eight* mean?
13. A British colleague says *I'll be there momentarily*. An American says the same thing. Who is staying longer?
14. Fix: *We're open Monday to Friday, and we're closed at the weekend.*
15. Fix: *The clocks change on the same weekend in the US and Europe, so the difference is always five hours.*
16. What is the difference between *biweekly* pay and *semimonthly* pay, and how many paychecks does each produce?
17. Why is *EOD Friday* a bad deadline for a team spread across three zones, and what would you write instead?

### Answers

| # | Answer | Why |
|---|---|---|
| 1 | *The kickoff is at 9 a.m. **ET** on July 14.* (Or *EDT*, if the offset matters.) | July is daylight time, so *EST* is wrong by an hour. *ET* is right all year. |
| 2 | **8 a.m.** in Los Angeles, **11 a.m.** in New York. | Central is one hour behind Eastern and two ahead of Pacific. |
| 3 | **9 a.m.** in New York. | January is US standard time: Moscow is 8 hours ahead. |
| 4 | **10 a.m.** in New York. **New York moved**, not Moscow — the gap drops to 7 hours during US daylight time. | Russia has not changed its clocks since 2014. |
| 5 | It is **April 5**. It should have been written *April 5, 2026* or `2026-04-05`. | American dates are month first. |
| 6 | Either *every two weeks* or *twice a week*. Ask: *Every other week, or twice a week?* | Both readings are live among native speakers. |
| 7 | Friday the 6th or Friday the 13th. Reply: *The 6th or the 13th?* — or propose one: *Friday the 13th works for me.* | *Next Friday* splits American speakers roughly evenly. |
| 8 | *The meeting is at **7:30 p.m. Moscow time on March 8**.* | Convert 24-hour to 12-hour in prose, put the month first, and name the zone. |
| 9 | The following **Thursday**. | Thursday is day zero; Friday, Monday, Tuesday, Wednesday, Thursday are the five business days. |
| 10 | The following **Friday**. | A federal holiday does not count as a business day. |
| 11 | **October, November, and December 2026**. | The federal fiscal year starts October 1, and FY27 is the year ending September 30, 2027. |
| 12 | **7:45** and **8:15**. | American *of* means "before"; *after* means "past." |
| 13 | The **American** — *momentarily* means "in a moment" in the US and "for a moment" in Britain, so the British speaker is announcing a brief appearance. | The two usages are opposites. |
| 14 | *We're open Monday **through** Friday, and we're closed **on** the weekend.* | *Through* for the inclusive range; *on the weekend* is the American preposition. |
| 15 | *The clocks change on **different** weekends, so for about three weeks in March the difference is **not** the usual five hours.* | The US switches the second Sunday in March, Europe the last Sunday. |
| 16 | *Biweekly* = every two weeks = **26 paychecks** a year. *Semimonthly* = twice a month = **24 paychecks**. | Payroll is the one context where American English holds the distinction firmly. |
| 17 | *EOD* names an hour but no zone, so it is three different deadlines. Write *by **5 p.m. ET** Friday*. | A time without a zone is not a time. |

---

## See also

- [Time](README.md) — the section index, and the rest of what English does with clocks, calendars and durations
- [Telling the time](01-telling-the-time.md) — a.m. and p.m., noon and midnight, *quarter of* and *ten till*, and military time in full
- [Dates, days and years](02-dates-days-and-years.md) — the month/day/year order at length, ordinals, decades, and the American holiday calendar
- [Duration and frequency](04-duration-and-frequency.md) — *for* against *since*, the frequency scale, and the *biweekly* problem approached from the other side
- [Schedules, appointments and deadlines](08-schedules-appointments-and-deadlines.md) — *EOD*, *COB*, *lead time*, and the emails that move a meeting across three zones
- [Age, life stages and eras](10-age-life-stages-and-eras.md) — the American school years and the named generations in full
- [Common mistakes](11-common-mistakes.md) — this page's error table set inside the whole topic's
- [Prepositions of time](../../parts-of-speech/06-prepositions/catalog/05-time.md) — *at*, *on*, *in*, *by*, [*until*](../../parts-of-speech/06-prepositions/catalog/05-time.md#until), *through* and *within*, each with its full range
- [Adverbs of time](../../parts-of-speech/05-adverbs/catalog/06-time.md) and [frequency adverbs](../../parts-of-speech/05-adverbs/catalog/07-frequency-duration.md) — [*presently*](../../parts-of-speech/05-adverbs/catalog/06-time.md#presently), [*currently*](../../parts-of-speech/05-adverbs/catalog/06-time.md#currently) and [*momentarily*](../../parts-of-speech/05-adverbs/catalog/07-frequency-duration.md#momentarily) as dictionary entries
- [The future](../04-tenses/09-the-future.md) — *will*, *be going to* and the present forms that carry a scheduled time, and [the present simple](../04-tenses/01-present-simple.md) for the timetable use
- [Pronunciation](../../10-pronunciation/README.md) — *schedule*, *hour*, *quarter*, and the American vowels in the zone names

---

**Next:** [Age, life stages and eras](10-age-life-stages-and-eras.md) — *I'm thirty* and never ✗ *I have thirty years*, the American school years, the named generations, and the vocabulary of historical periods.

[← Time](README.md) &middot; [All grammar topics](../README.md)
