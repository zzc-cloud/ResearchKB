# Design: Enrich human-friendly prose in Paper and Method pages

Date: 2026-05-13
Status: Draft for user review
Priority: Paper first, Method second

## 1. Problem statement

The current single-paper automation chain in ResearchKB can already produce structured ontology artifacts: Evidence caches, object pages, formal relation candidates, formal ledgers, projections, indexes, and governance results. However, the human-friendly prose on the final object pages—especially Paper pages and Method pages—remains too thin.

This creates a usability gap:
- the graph may be structurally correct,
- but a human reader still cannot quickly judge what the paper really contributes,
- what the method really is,
- how the extracted knowledge should be interpreted,
- and where the extraction remains uncertain.

The core issue is **not** primarily the lack of an extra review document under `docs/`. The deeper issue is that the default human-facing serving surfaces—especially `ontology/entities/papers/*.md` and `ontology/entities/methods/*.md`—do not yet contain enough high-value prose outside `Formal relations`.

## 2. Goal

Strengthen the human-friendly prose of **Paper** and **Method** entity pages so they better support human judgment during reading, review, and downstream interaction.

This is a content-design change, not a graph-truth relocation.

The goal is:
- **not** to make pages longer for its own sake,
- **not** to duplicate Evidence caches,
- **not** to bypass formal relation discipline,
- but to make the final object pages much more useful as human reading and judgment entry points.

## 3. Priority

The enhancement should be designed for both entity types together, but with clear priority:
1. **Paper pages first**
2. **Method pages second**

Rationale:
- the Paper page is usually the first human entry point after ingest,
- strengthening Paper pages gives immediate payoff for single-paper review,
- Method pages should then inherit and refine the relevant semantic understanding into a stronger method-identity surface.

## 4. Non-goals

This design does **not** aim to:
- create a new truth source under `docs/`
- move formal relation truth out of `ontology/relations/*.md`
- move evidence truth out of `ontology/entities/evidence/*.md`
- turn object-page prose into an unconstrained relation surface
- generate long narrative summaries that merely restate the paper
- preserve full historical extraction logs inside Paper or Method pages

## 5. Design principles

### 5.1 Judgment over length
The prose should increase **judgment support**, not just token count.

A richer page is successful only if a human can more easily answer:
- what this paper/method is,
- why it matters,
- how it relates to the current knowledge base,
- and where uncertainty remains.

### 5.2 Paper-first, Method-following
Paper pages should become the primary high-density human reading surface. Method pages should then become stronger identity and positioning surfaces for methods.

### 5.3 Prose explains object meaning, not formal graph truth
Formal graph truth still lives in formal ledgers and projections. Prose should explain the object’s meaning and boundaries, not replace ledgers.

### 5.4 Evidence remains in Evidence pages
Object pages may refer to supported conclusions, but should not copy large sections of cache detail.

### 5.5 Uncertainty must be explicit
When the extraction is incomplete, ambiguous, or provisional, the prose should say so directly instead of presenting weakly-supported interpretations as settled facts.

### 5.6 No prose-driven graph leakage
Human-friendly enrichment must not create uncontrolled graph exposure. Object-page prose must continue to respect the serving discipline around formal adjacency and constrained navigation.

## 6. What “richer” should mean for Paper pages

The Paper page should become a strong human-facing entry point for understanding a single paper in the ontology.

It should help a reader quickly judge:
- what problem the paper addresses,
- what the main contribution is,
- what is most worth remembering,
- how the paper connects to the existing knowledge base,
- and what extraction uncertainty still exists.

### 6.1 Paper-page prose responsibilities
The Paper page should prioritize the following kinds of information:

1. **Core problem framing**
   - What research problem or gap is the paper addressing?
   - Why is that problem worth attention in the current ontology?

2. **Core contribution framing**
   - What is the paper’s main reusable contribution?
   - Is it a method, framework, survey structure, benchmark design, application pattern, or something else?

3. **High-value key judgments**
   - What are the 3–5 most important takeaways a human should remember?
   - These should be high-density judgments, not generic summary sentences.

4. **Knowledge-base relationship framing**
   - How does this paper relate to existing methods, tasks, scenarios, benchmarks, or surveys already in the vault?
   - This section should remain prose-level interpretation, not become an alternate relation ledger.

5. **Extraction boundary / uncertainty framing**
   - Which parts are stable?
   - Which parts remain partial, ambiguous, or evidence-limited?

### 6.2 Recommended Paper-page section structure
The exact headings may be adjusted during implementation, but the target structure is:

- `## 核心问题`
- `## 核心贡献`
- `## 关键判断`
- `## 与知识库现有内容的关系`
- `## 当前抽取边界与不确定性`

### 6.3 Paper-page writing constraints
Paper-page prose should:
- stay concise but information-dense
- prefer ontology-relevant interpretation over paper retelling
- avoid copying long evidence excerpts
- avoid sprawling related-work recap
- avoid introducing uncontrolled formal adjacency through prose

## 7. What “richer” should mean for Method pages

Method pages should become stronger identity pages.

The main deficiency today is not just lack of detail, but lack of **method identity explanation**. A Method page should help a human answer:
- what the method actually is,
- how it is positioned in a method lineage or route,
- what tasks/scenarios it is for,
- what distinguishes it from nearby methods,
- and whether the current knowledge state is mature or partial.

### 7.1 Method-page prose responsibilities
The Method page should prioritize:

1. **Method identity**
   - What kind of method is this?
   - What is its minimal stable semantic identity?

2. **Core mechanism**
   - What is the central mechanism or technical idea?
   - Enough to orient the human reader, without becoming a full implementation tutorial.

3. **Task / scenario positioning**
   - What tasks or scenarios is this method mainly aimed at?
   - This should align with, but not merely repeat, the formal relation surface.

4. **Key distinction from neighboring methods**
   - What makes this method meaningfully different from closely adjacent methods in the vault?

5. **Current knowledge-state framing**
   - Is the method page stable, partial, survey-derived, or still weakly grounded?

### 7.2 Recommended Method-page section structure
The target structure is:

- `## 方法定位`
- `## 核心机制`
- `## 适用任务与场景`
- `## 与相邻方法的关键区别`
- `## 当前知识状态`

### 7.3 Method-page writing constraints
Method-page prose should:
- explain identity, not just provenance
- avoid becoming a paper-summary proxy
- avoid verbose narrative duplication from Paper pages
- clearly distinguish stable method semantics from provisional interpretation

## 8. Implications for the paper-ingest stage

Although the change is primarily about final Paper/Method page quality, the first stage that must change is `paper-ingest`, because it is the earliest stage that generates the object-level semantic draft.

`paper-ingest` should therefore be strengthened to extract richer **human-facing object semantics** for both Paper and Method candidates.

### 8.1 New expectations for ingest output
For Paper candidates, ingest should produce enough structured semantic material to support:
- problem framing
- contribution framing
- 3–5 key judgments
- relation-to-existing-KB prose cues
- extraction-boundary notes

For Method candidates, ingest should produce enough structured semantic material to support:
- method identity
- core mechanism summary
- task/scenario positioning cues
- distinguishing notes vs nearby methods
- current knowledge-state notes

These do not need to be formal relation instances themselves, but they must be extractable, reviewable, and projectable into the final object pages.

### 8.2 What ingest should still avoid
Even after enrichment, `paper-ingest` should still avoid:
- turning prose into a second relation ledger
- copying large cache blocks directly into object pages
- pretending certainty where evidence is weak
- using object-page prose as a substitute for Evidence or formal review stages

## 9. Implications for downstream stages

### 9.1 relation-reconciliation
This stage remains responsible for formal relation truth and reconciliation. It should not become responsible for authoring the rich human-friendly prose itself.

However, it may refine or constrain downstream object-page prose indirectly by clarifying which relations are formal, exempt, or uncertain.

### 9.2 page-projection-sync
This stage is the most likely downstream place to formalize the enriched prose into the final object-page templates.

If ingest produces richer object-level semantic payloads, projection should synchronize them into the relevant Paper/Method human-friendly sections while preserving strong consistency fields and relation projections.

### 9.3 index-sync
No major prose authorship responsibility should move here. Index pages may benefit indirectly from better `object_semantics`, but index-sync should remain navigation-focused.

### 9.4 lint / semantic review / serving governance
These governance steps should continue to validate structure, ontology placement, and serving readiness. They may later gain lightweight checks for whether required human-friendly sections are missing or obviously underfilled, but they should not be the primary authors of the prose.

## 10. Proposed authoring boundary

To keep responsibilities clear, the pipeline should evolve toward this boundary:

- **paper-ingest**: produce richer object-semantic draft content
- **relation-reconciliation**: determine formal relation truth
- **page-projection-sync**: project and synchronize rich human-friendly content into final object pages
- **index-sync**: reflect object availability into navigation
- **governance stages**: validate quality, semantics, and serving readiness

This avoids the bad pattern where every stage writes arbitrary prose into the same place.

## 11. Success criteria

The design is successful if, after implementation, a human reading a Paper page can quickly answer:
- what this paper is about,
- what it mainly contributes,
- what matters most,
- how it fits the existing vault,
- and what remains uncertain.

And a human reading a Method page can quickly answer:
- what the method is,
- how it works at a high level,
- where it belongs in the method landscape,
- what differentiates it,
- and how mature the knowledge representation currently is.

## 12. Recommended rollout

### Phase 1
Enhance Paper-page human-friendly prose generation first.

### Phase 2
Add the corresponding Method-page enrichment flow.

### Phase 3
Refine projection discipline so the enriched prose is stable, compact, and consistent with formal relation surfaces.

### Phase 4
Optionally add lightweight governance checks for required human-friendly section presence/quality.

## 13. Open implementation questions already resolved in this design

The following choices are now considered resolved for planning purposes:
- We are **not** prioritizing a separate `docs/` review dossier as the main solution.
- We are **not** optimizing for historical extraction logs.
- We are designing **Paper and Method together**, with **Paper first**.
- We are optimizing for **human judgment support**, not summary length.
- We are keeping formal relations and Evidence as the existing truth layers.

## 14. Summary recommendation

Proceed with a Paper-first, Method-following redesign of the human-friendly prose on entity pages.

The central change should be: enrich the object-page body so it becomes a stronger default human reading surface, while preserving the existing ontology truth boundaries.
