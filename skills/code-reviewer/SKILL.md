---
name: code-reviewer
description: Run a structured five-stage code review on a diff, file, or pull request. Use whenever the user wants code reviewed, audited, or checked before merge. Triggers on "review this code", "audit this PR", "code review", "check this diff", "review my changes", or any time the user pastes code and wants quality, performance, or security feedback. Always use this skill rather than ad-hoc commentary when the user asks for a code review, even if they describe the request in their own words.
---

# Code Reviewer

Five-stage pipeline. Each stage runs independently with its own checklist. Findings get severity tags so the reviewer can decide what blocks merge.

## Severity scale

- `blocker`: must fix before merge
- `major`: fix before next release
- `minor`: improve when convenient
- `nit`: style preference, take or leave

## Stages

### Stage 1: Architecture

- Are module boundaries respected?
- Is coupling between components appropriate?
- Are there leaky abstractions?
- Does this change introduce circular dependencies?
- Is the layer of abstraction consistent within each function?

### Stage 2: Quality

- Are names clear and specific (not "data", "info", "manager")?
- Is there duplication that should be extracted?
- Is there complexity that should be inlined (KISS)?
- Dead code, unreachable branches, commented-out code?
- Inconsistent error handling within the same function?
- Magic numbers or strings that should be named constants?

### Stage 3: Tests

- Are new code paths covered?
- Are edge cases tested (empty, null, boundary, max)?
- Do assertions check behavior, not implementation details?
- Are tests isolated (no shared mutable state)?
- Are test names descriptive of what they verify?
- Any tests that could pass against incorrect code?

### Stage 4: Performance

- Algorithmic complexity reasonable for input size?
- N+1 queries or redundant database round trips?
- Unbounded memory growth (lists, caches, accumulators)?
- Missing caching where output is deterministic and expensive?
- Synchronous operations that could be async?
- Hot paths doing unnecessary allocations?

### Stage 5: Security

- Input validation on all external inputs?
- SQL injection, command injection, path traversal vectors?
- Authentication and authorization on every endpoint?
- Secrets in code, logs, error messages, or commits?
- Cryptographic primitives used correctly (no MD5 for security, no ECB mode, proper IV handling)?
- CSRF, XSS, SSRF surface in web code?
- Race conditions on shared state?

## Output format

For each stage, emit a markdown table with this shape:

````
## Stage 1: Architecture
| Severity | File:Line | Finding | Fix |
|---|---|---|---|
| <tag> | <ref> | <one line> | <one line> |
````

Repeat for stages 2, 3, 4, and 5.

If a stage has zero findings, write `No findings.` under the stage heading.

End with a summary block:

````
## Summary
- Blockers: <count>
- Majors: <count>
- Minors: <count>
- Nits: <count>

## Verdict
<APPROVE | REQUEST_CHANGES | COMMENT>
````

Verdict rules:

- `APPROVE` only if zero blockers and zero majors
- `REQUEST_CHANGES` if any blocker or three or more majors
- `COMMENT` otherwise

## Hard rules

- Run all five stages even if one finds nothing.
- Do not invent issues to look thorough. If the code is clean, say so.
- For diffs over 500 lines, ask the user to split before reviewing.
- Quote exact code in findings. Vague references like "around the validation logic" are not actionable.
