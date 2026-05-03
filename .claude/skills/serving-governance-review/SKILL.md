# Serving Governance Review

Review migrated knowledge pages to decide whether they are ready to serve as default constrained-QA entry surfaces.

## Use this when
- A batch of Paper / Method / Concept / Task / Scenario / Benchmark / Evidence pages has been migrated to the serving-layer model.
- You need to decide whether pages are `serving-ready`, `partial`, or `legacy`.
- Structural lint and ontology semantic review have already been run or are available.

## Inputs
- A git diff, file list, directory, or migration batch description.

## What to check
1. **Serving completeness**
   - Does every migrated page have `## Formal relations`, `### Outgoing`, and `### Incoming`?
   - Are the required one-hop relations present for the node type?
   - Are evidence links present and useful for drill-down?

2. **Serving readability alignment**
   - Do the human-readable sections match the formal projection?
   - Is there prose that would mislead a reader or LLM relative to the formal edges?

3. **QA traversability**
   - Can an LLM identify the next-hop nodes and relation types directly from the page?
   - Are there missing key neighbors that would force runtime fallback to `wiki/relations/`?

4. **Release readiness**
   - Is this page or batch safe to promote as the default QA serving surface?

## Output states
- `pass`: serving-ready
- `needs_fixes`: structurally or semantically usable, but not ready as default serving surface
- `blocked`: should not be promoted to serving-ready

## Constraints
- Do not redo structure lint.
- Do not redo ontology-semantic-review.
- Focus only on the distinct serving-surface quality gate.
