# claude-skills-templates

Five production-ready Claude Skills you can drop into Claude Code, Claude.ai, or the Claude API. Each skill demonstrates a different SKILL.md pattern: pure-prompt, structured workflow, configurable reference file, executable script, and decision-support.

Skills follow the [Agent Skills open standard](https://agentskills.io). Each one is a folder with a SKILL.md file plus optional supporting resources.

## Skills index

| Skill | Pattern | What it does |
|---|---|---|
| [`one-pager`](skills/one-pager/) | Pure prompt | Turns notes or transcripts into a structured one-page brief |
| [`code-reviewer`](skills/code-reviewer/) | Structured workflow | Five-stage code review (architecture, quality, tests, performance, security) |
| [`brand-voice`](skills/brand-voice/) | Configurable reference | Applies a tone and voice guide to drafts; user fills in their voice rules |
| [`csv-cleaner`](skills/csv-cleaner/) | Skill plus script | Diagnoses and cleans messy CSV or TSV files |
| [`decision-doc`](skills/decision-doc/) | Decision support | Structured tradeoff analysis with explicit flip conditions |

## How skills work

Skills use progressive disclosure. Three loading levels:

1. **Metadata** (name and description in YAML frontmatter): always visible to Claude, used to decide whether to load the skill.
2. **SKILL.md body**: loaded into context only when the skill triggers.
3. **Bundled resources** (scripts, references, assets): loaded on demand.

The description field is the primary triggering mechanism. Write it to be specific about both what the skill does AND when to use it.

## Installation

### Claude Code (CLI)

Copy the skill folder into your project's `.claude/skills/` directory or your global `~/.claude/skills/` directory:

```bash
cp -r skills/one-pager ~/.claude/skills/
```

Claude Code picks it up on the next session.

### Claude.ai

Zip the skill folder and upload it via the Skills menu:

```bash
cd skills/one-pager && zip -r ../one-pager.skill .
```

Then upload the resulting `.skill` file in Claude.ai under Settings, Skills.

### API

Pass the skill via the `skills` parameter when calling the Messages API. See [Anthropic's Skills documentation](https://docs.claude.com) for the current syntax and supported runtime.

## Customizing

Every skill in this repo is a starting point. Recommended workflow:

1. Copy the skill folder into your project.
2. Open SKILL.md and edit the `description` field to match your trigger phrases.
3. Edit the body to match your team's conventions.
4. For `brand-voice`, fill in `references/brand-voice.md` with your actual voice rules.
5. Test with 5 to 10 sample prompts before deploying.

## Description writing tips

The description field is a single string in the YAML frontmatter. Two failure modes to avoid:

- **Undertriggering**: description is too generic, Claude does not load the skill when it should. Fix: name specific trigger phrases users actually say.
- **Overtriggering**: description is too broad, Claude loads the skill for unrelated requests. Fix: name the contexts where the skill does NOT apply.

A good description includes:
- One sentence on what the skill does
- A list of trigger phrases ("use when the user says X, Y, Z")
- One sentence on a guardrail ("always read references/X.md first" or "do not use for ad-hoc summarizing")

## Contributing

Pull requests welcome. New skills should:

- Have a single, specific purpose, not "do everything"
- Include a description that triggers reliably without overtriggering
- Stay under 500 lines in SKILL.md (use bundled resources for longer content)
- Include 2 to 3 example trigger phrases in the description

## License

MIT. See [LICENSE](LICENSE).
