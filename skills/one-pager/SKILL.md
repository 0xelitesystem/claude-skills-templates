---
name: one-pager
description: Turn raw notes, transcripts, or longform content into a tight one-page executive brief. Use whenever the user wants a one-pager, exec brief, briefing doc, or asks to compress longer content into a structured one-page summary. Triggers on phrases like "write a one-pager", "make this a brief", "summarize for an exec", "turn these notes into a brief", or when the user uploads notes or meeting transcripts and wants a tight structured summary. Always use this skill rather than free-form summarizing when the user asks for a "brief" or "one-pager", even if they do not say "use the one-pager skill".
---

# One-Pager Writer

Converts raw input (notes, transcripts, source articles, research dumps) into a structured one-page brief.

## Output structure

Always use these five sections in this order.

### TL;DR

One sentence. The headline finding or recommendation. If the reader stops here, they should know what changed.

### Context

Two to four sentences. What prompted this? What is the reader supposed to know to make sense of the rest?

### Findings

Three to five bullets. Each is a specific, sourced claim. If a claim has a number, include the number. If it has a source, attribute it.

### Recommendation

One paragraph. What should the reader do, decide, or believe? If there is a decision to make, state it. If the recommendation is conditional, state the condition.

### Next Steps

Three to five concrete actions, each with an owner placeholder if known. Each action should be doable in a week or less.

## Style rules

- No em-dashes. Use commas, semicolons, or split into two sentences.
- No filler openings. Skip "In today's...", "It is worth noting that...", "When it comes to...".
- No banned vocabulary: delve, leverage as a verb, seamless, robust for non-statistical claims, navigate the landscape, paradigm shift, journey as a metaphor, unlock the power, harness the power, foster as a verb.
- Concrete over abstract. "Revenue rose 18% in Q3" beats "significant revenue growth was observed".
- Active voice. Name the actor.
- Length cap: roughly 350 words total. If you exceed it, cut bullets, not sections.

## When you do not have enough input

If the source content is too thin to fill all five sections honestly, do not invent content. Mark the thin section with `[needs input: <what is missing>]` and ask the user one specific question per gap.

## Output format

Render as plain markdown. Section headings as `###`. No tables unless the user asks for one. No code blocks unless the source contains code worth quoting.
