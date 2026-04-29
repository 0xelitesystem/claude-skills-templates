---
name: decision-doc
description: Produce a structured decision document with explicit tradeoffs, weighted criteria, scored options, a recommendation, and a flip condition. Use whenever the user is choosing between options, comparing approaches, evaluating vendors or frameworks, or deciding between architecture patterns. Triggers on "help me decide", "compare X vs Y", "which should I pick", "should I use A or B", framework or vendor decisions, architecture choices, or any decision where a structured tradeoff would be more useful than a casual opinion. Always use this skill rather than free-form pros and cons lists when the user is making a real decision.
---

# Decision Doc

Produces a structured decision document. Forces a recommendation with confidence and a flip condition, instead of hedging.

## When to use

- Two or more options under consideration
- The user wants a recommendation, not just a comparison
- The decision has stakes (money, time, lock-in, reversibility)

## When NOT to use

- The user is exploring a topic without a specific decision in front of them.
- One option has a hard disqualifier. Just say so, no need for the full doc.
- The user explicitly asks for a casual opinion.

## Process

### Step 1: Restate the decision

One sentence in your own words. Flag any ambiguity that would change the answer. If ambiguity is severe, ask one clarifying question before proceeding.

### Step 2: Define criteria

List 4 to 7 evaluation criteria. Assign each a weight from 1 to 5. Total weights must sum to a number between 15 and 25. This constraint prevents flattening the criteria with all-equal weights.

If the user provided criteria, use those. If not, derive them from the decision context.

### Step 3: Score each option

Score each option from 1 to 5 against each criterion. Compute a weighted total per option. Show the work.

### Step 4: State the tradeoff for each option

One sentence per option describing what you give up by choosing it. No option escapes this step. Even the best option has a cost.

### Step 5: Recommend

State the recommendation. Cite the weighted score, but do not let the score override clear qualitative concerns. If a lower-scoring option is the right answer for a reason the score cannot capture, say so.

### Step 6: Flip condition

State one specific change in inputs or context that would make a different option win. This is the most important field. If you cannot articulate a flip condition, the analysis is not done.

### Step 7: Confidence

1 (coin flip) to 5 (clear winner).

## Output format

````
## Decision
<restated decision>

## Ambiguities
<list, or "none">

## Criteria
| Criterion | Weight | Why it matters |
|---|---|---|

## Scoring
| Option | <criterion 1> | <criterion 2> | ... | Weighted Total |
|---|---|---|---|---|

## Tradeoffs
- <Option A>: <what you give up>
- <Option B>: <what you give up>

## Recommendation
<option name>

<2 to 4 sentences explaining why>

## Flip Condition
If <specific input change>, the recommendation becomes <other option>.

## Confidence
<1 to 5> / 5
````

## Stability check

For high-stakes decisions, run the analysis twice with the options listed in opposite order. If the recommendation flips between runs purely from ordering, the analysis is unstable. Widen the criteria or get more information before committing.
