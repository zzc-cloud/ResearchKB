# Page Projection Sync Quality Checklist

## Inputs
- [ ] Reads updated formal ledgers.
- [ ] Reads relation-reconciliation output including `affected_pages`.

## Sync behavior
- [ ] Updates `## Formal relations` consistently.
- [ ] Updates strong-consistency frontmatter fields.
- [ ] Updates templated human-readable relation blocks.
- [ ] Does not rewrite interpretive prose.

## Output quality
- [ ] Emits a structured YAML summary.
- [ ] Lists any manual followups that still require human editing.
