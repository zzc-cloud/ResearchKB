# Relation Reconciliation Quality Checklist

## Input handling
- [ ] Reads `relation_candidates` and `relation_exemptions` from ingest output.
- [ ] Reads affected object pages, evidence caches, and current relation ledgers.

## Reconciliation logic
- [ ] Distinguishes `already_present`, `add_now`, `exempt`, and `needs_human_review`.
- [ ] Routes each relation type to the correct `wiki/relations/*.md` file.
- [ ] Detects prose-ledger drift when a page implies a relation that is missing from the formal ledger.

## Output quality
- [ ] Emits a structured YAML summary.
- [ ] Lists affected pages for downstream page-projection sync.
- [ ] Does not silently drop ambiguous edges.
