# Brag Plan: NourishBot

## What is this app?
Four CrewAI agents that look at a photo of your fridge (or your plate) and return recipes you can make, or a calorie and nutrient breakdown.

## The angle
A relay race run by four very literal specialists. The vision agent lists what's in the fridge, the nutritionist agent enforces "vegan" without mercy (the eggs, milk and ham are thrown out), the recipe agent makes do with fruit, and on the corn dogs the analysis agent is politely honest. All results on screen are **real output** from the crews, run on the project's own example images.

## Hook (first 2-3 seconds)
The fridge photo scales in as "Your fridge." lands, then "Four AI agents." slams on the first strong beat (1.60s).

## Key moments (the middle)
- Agent 1 reads the fridge: seven ingredient chips pop out of the photo.
- "vegan" is typed into the Dietary Restrictions box. Eggs, milk and ham get struck through and drop off. "Sorry, ham."
- Three recipe cards deal in, each with a kcal counter: Vegan Fruit Salad 120, Roasted Pears 150, Blueberry & Grape Smoothie 100.
- Corn dogs: 1,100 kcal counts up; verdict reads "an occasional treat".

## Outro / punchline
"NourishBot" wordmark. "Snap your fridge. Four agents do the rest."

## User flow worth showing
Upload fridge photo → set a dietary restriction → recipes appear. Then the second workflow: plate photo → nutrition analysis.

## Tone
- Preset: default
- Creative direction: cheerful kitchen relay race
- Interpretation: comfortable pacing, warm citrus palette, one comedic beat (the ham), no sarcasm toward the user.

## Format: landscape — 1920x1080
## Duration: 23s

## Visual identity (from the project)
- Background: warm cream #FFF8EC (Gradio Citrus theme)
- Accent: #EBA93F (the app's welcome animation colour), gold #FFD700 sparingly
- Text: deep ink #2B2118
- Display font: system sans, heavy weight (the app has no custom font)
- Body font: system sans
- Strongest visual element: the example photos, plus the app's labels "Dietary Restrictions" and "Workflow Type: recipe / analysis"

## Share copy (draft)
I built four AI agents that go through your fridge. The vegan one threw out my ham.

## Audio direction
- Role: warm bed
- Music: happy-beats-business-moves-vol-11 (114.84 BPM)
- Music treatment: starts at 0, volume ~0.5, fades out over the last 1.2s
- Music cue guidance: bundled preset read. Strong cues: 1.60s (hook), 8.96s (the vegan strike-out), 17.91s (corn dog kcal lands). Recipe cards on every other beat: 12.65 / 13.70 / 14.76.
- Audio-reactive treatment: none. The Hyperframes extraction helper isn't installed, so this was skipped.
- SFX posture: moderate, matched to motion
- Audio-coupled moments: typed "vegan" (key ticks), strike-out (dry error buzz), cards (card slide), kcal landing (soft impact), wordmark (bell)
- Restraint rule: no SFX on individual ingredient chips (one soft drop for the set)

## Storyboard

### Scene 1 — Hook — 3.2s
Fridge photo zooms in slowly. "Your fridge." then "Four AI agents." (beat-locked 1.60s).
Sequential/interaction: two lines in sequence
Audio intent: music kicks in; soft impact on line 2
Transition mood: clean → Scene 2

### Scene 2 — Agent 1: Vision — 4.4s
Photo on the left, label "Agent 1 · Vision AI Specialist". Chips: eggs, milk, blueberries, grapes, oranges, pears, ham. They pop in quickly, then all seven stay on screen together.
Sequential/interaction: yes, 7 chips
Audio intent: one soft drop for the set
Transition mood: clean → Scene 3

### Scene 3 — Agent 2: Nutritionist — 4.2s
The app's "Dietary Restrictions" field; "vegan" types in. On 8.96s eggs/milk/ham strike through and fall. Caption "Sorry, ham."
Sequential/interaction: yes, typing plus strike-out
Audio intent: key ticks, one dry buzz
Transition mood: slide → Scene 4

### Scene 4 — Agents 3 & 4: Recipes — 4.4s
"Workflow Type: recipe". Three real recipe cards deal in on every other beat, kcal counting up.
Sequential/interaction: yes, 3 cards
Audio intent: card slide per card
Transition mood: slide → Scene 5

### Scene 5 — Analysis — 3.6s
Corn dog photo, "Workflow Type: analysis". 1,100 kcal counts up and lands on 17.91s. Macros 22g protein · 140g carbs · 50g fat. Verdict: "an occasional treat".
Sequential/interaction: count-up
Audio intent: soft impact on landing
Transition mood: clean → Scene 6

### Scene 6 — Outro — 3.2s
Wordmark "NourishBot", "Snap your fridge. Four agents do the rest.", "CrewAI · Gradio".
Audio intent: bell, music fades
Transition mood: hold

**Music mood for this video:** upbeat
**Audio summary:** a warm upbeat bed with light kitchen-UI accents, one comedic buzz and a bell to finish.
