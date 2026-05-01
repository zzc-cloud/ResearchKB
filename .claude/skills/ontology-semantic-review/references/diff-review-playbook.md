## Diff review playbook
1. Read the current git diff or changed file list.
2. Read `wiki/ontology/graph-standard.md` and the relation hub files.
3. Classify every changed node touched by the diff.
4. For every changed relation, ask:
   - Is this relation real?
   - Is it in the correct relation file?
   - Is it local evidence support rather than ontology-level structure?
5. Produce the standard review report.

## Special checks
- If a survey is represented as a task, flag it.
- If a framework is represented as a method, flag it.
- If concept_links contains concept→paper support edges, flag and suggest moving to concept page or evidence index.
- If method_evolution contains literature support rather than actual lineage, flag it.
