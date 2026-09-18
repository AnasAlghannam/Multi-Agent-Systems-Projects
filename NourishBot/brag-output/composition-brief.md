# Hyperframes Composition Brief: NourishBot

## Objective
Create a short launch-style brag video for NourishBot.

## Output
- Composition directory: `brag-output/composition/`
- Rendered video: `brag-output/brag.mp4`
- Format: landscape, 1920x1080
- Duration: 23 seconds

## Source Material
- Project root: `Multi-Agent-Systems-Projects/NourishBot`
- Primary files read: README.md, app.py, src/models.py, src/config/agents.yaml, examples/
- Product name: NourishBot
- Strongest claim: four specialised agents hand work to one another
- Key UI to recreate: the "Dietary Restrictions" textbox, the "Workflow Type" recipe/analysis radio, and the structured recipe and analysis results
- Real crew output used verbatim (run 2026-09-17 on examples/food-1.jpg with "vegan" and examples/food-2.jpg):
  - Vegan Fruit Salad, 120 kcal · Roasted Pears with Olive Oil, 150 kcal · Blueberry and Grape Smoothie, 100 kcal
  - corn dogs, 4 corn dogs, 1100 kcal, protein 22g, carbohydrates 140g, fats 50g, "occasional treat"
- Agent roles verbatim: Vision AI Specialist, Nutritionist AI Specialist, Nutrition Analysis Specialist, Recipe Generation Specialist

## Creative Direction
- Tone preset: default
- Creative direction: cheerful kitchen relay race
- Angle, hook, outro: see brag-plan.md
- Avoid: generic SaaS language, abstract filler, restyling the product away from its citrus palette

## Visual Identity
- Background #FFF8EC · Text #2B2118 · Accent #EBA93F · Gold #FFD700 (sparingly)
- Fonts: system sans, heavy display weight

## Storyboard
1. Hook (0–3.2s): fridge photo, "Your fridge." / "Four AI agents."
2. Vision (3.2–7.6s): 7 ingredient chips
3. Nutritionist (7.6–11.8s): type "vegan", strike eggs/milk/ham, "Sorry, ham."
4. Recipes (11.8–16.2s): 3 recipe cards with kcal counters
5. Analysis (16.2–19.8s): corn dogs, 1,100 kcal, macros, verdict
6. Outro (19.8–23s): wordmark and tagline

## Audio
- Music: `assets/music/happy-beats-business-moves-vol-11-by-ende-dot-app.mp3`, bed ~0.5, fades out over the last 1.2s
- Cue locks: 1.60 hook, 8.96 strike, 17.91 kcal landing; beat grid for cards 12.65 / 13.70 / 14.76
- Audio-reactive: skipped (the Hyperframes extraction helper isn't installed; documented, not blocking)
- SFX: keypresses on typing, error_005 on strike, card-slide-1 per card, impactSoft_medium on hook and kcal, impactBell_heavy_000 on the wordmark

## Hyperframes Instructions
Built from `npx hyperframes docs` (compositions, data-attributes, gsap, rendering) and the `init` scaffold conventions, since the Hyperframes domain skills aren't installed. Requirements: one paused root timeline registered on `window.__timelines`, `class="clip"` and data timing on every timed element, deterministic logic only, relative asset paths, and `hyperframes check` passing before render.
