---
name: brand-voice
description: Apply a configured brand voice and tone guide to drafts, rewrites, and edits. Use whenever the user wants text edited to match their team's voice, asks for tone adjustments, or wants drafts brought into compliance with a style guide. Triggers on "rewrite in our voice", "apply our tone", "edit this draft", "make this sound like us", "fix the voice", or any rewrite request where consistency with a brand style is the goal. Always read references/brand-voice.md before making edits, and use this skill rather than free-form rewriting when style consistency matters.
---

# Brand Voice

Applies a configured voice and tone guide to drafts. The voice itself lives in `references/brand-voice.md` so it can be customized without touching the skill logic.

## Workflow

1. Read `references/brand-voice.md` in full before editing anything.
2. Identify the input: a draft pasted by the user, an uploaded file, or a section of an existing document.
3. Run the rewrite pass below.
4. Output the rewritten version, then a short audit of what changed.

## Rewrite pass

For each paragraph in the input:

- Check it against the voice attributes in the reference file.
- Check it against the banned-words list.
- Check it against the preferred-phrasings list.
- Rewrite if any check fails. Leave alone if all pass.
- Preserve the original meaning and key facts. Only change how it is said.

## What to preserve

- Numbers, dates, names, quotes (exact)
- Section structure (headings, ordering, list items)
- Technical accuracy (do not soften precise language into vague language)
- Length within plus or minus 15% unless the user asked for shorter or longer

## What to change

- Word choice that violates the banned-words list
- Sentence rhythm that conflicts with the stated voice (e.g., long flowing prose when the voice is "punchy")
- Formality level (casual versus formal)
- Filler and hedging that is not in the voice
- Default-AI patterns that creep in (em-dashes, "not just X but Y", tricolon abuse)

## Output format

Render in two parts:

````
## Rewritten

<the full rewritten text>

## Changes

- <one-line summary of the most important change>
- <next change>
- (up to 5 total)
````

## When the reference file is missing or empty

If `references/brand-voice.md` is missing, or contains only the placeholder template with no user content, do not guess at the voice. Tell the user the reference file needs content first, and offer to interview them with three specific questions:

1. What three adjectives describe your voice? (e.g., direct, warm, technical)
2. What words or phrases do you ban?
3. Paste two sentences in your voice and two that fail.
