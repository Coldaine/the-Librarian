# Prompt Documentation

This directory contains documentation for all prompts used in the Personal Knowledge Base system.

## Purpose

Prompts are critical components of AI-powered systems. This directory provides:

- **Transparency**: Full visibility into what prompts are being used
- **Rationale**: Understanding WHY each prompt is structured the way it is
- **Version Control**: Track changes to prompts over time
- **Quality Assurance**: Sign-off process for prompt changes

## Documentation Pattern

Each prompt gets its own markdown file following the structure in [TEMPLATE.md](./TEMPLATE.md).

### Key Principles

1. **The Prompt Itself**: The actual prompt text is documented verbatim
2. **Section-by-Section Breakdown**: Each major section of the prompt has:
   - **WHY it's included**: The reasoning behind this section
   - **Research Basis**: Any research, testing, or evidence supporting this approach
   - **Intent**: What behavior we're trying to elicit from the AI
3. **Metadata**: Every prompt document includes:
   - Last reviewed date
   - Sign-off (who approved the current version)
   - Version history
4. **Version Control**: All changes are tracked in git - this is critical for understanding prompt evolution

## Directory Structure

```
docs/prompts/
├── README.md           # This file
├── TEMPLATE.md         # Template for documenting prompts
└── (future prompt docs)
```

## Usage

As prompts are created for the system, they will be documented here following the template structure.

When adding a new prompt:

1. Copy `TEMPLATE.md` to create a new file
2. Name the file descriptively (e.g., `note-summarization.md`)
3. Fill in all sections, especially the WHY for each prompt component
4. Get sign-off before deploying
5. Commit with a meaningful message describing the prompt's purpose

## Why Document Prompts This Way?

Prompts are not just text - they're carefully engineered instructions that significantly impact system behavior. By documenting the reasoning behind each section, we:

- Enable informed iteration and improvement
- Prevent accidental regression when modifying prompts
- Share knowledge about what works and why
- Create accountability through the sign-off process
