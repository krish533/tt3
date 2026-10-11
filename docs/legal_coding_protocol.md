# Legal coding protocol — version 2, 10 October 2026

The unit is a legal relationship within a provision, supported by its section, definitions, exceptions and cross-references. Sentences are retrieval units. A provision can yield several relationships. Codes describe claimed allocation, not enforceability. Corpus-wide flags are machine retrieval aids; selected readings are AI-assisted interpretations, not human-validated ground truth.

## Required decision order

1. Record institution, campus, upstream year, filename, immutable row ID, source hash, URL, retrieval date and page/section. Authenticate effective version separately from retrieval. A later reprint is not the earlier original.
2. Classify operative rule, definition, procedure, example, accounting provision, description of external law, or mixed. Headings do not settle the question: rules occur inside definitions sections. Exceptions are operative.
3. Identify object, actor, right and conditions. Resolve pronouns and defined terms through linked records; preserve missing context. Preserve OR versus AND. Distinguish ownership, obligation to assign, purported present assignment and executed transfer.
4. Read sponsor, employment, academic-work, student and resource qualifications. Record exceptions to exceptions. Never infer absence of an exception from failure to retrieve it.
5. Record uncertainty and dependencies. Only fully resolved matched versions enter legal transitions. Keep partial readings separately.

## Multilabel codebook

| Field | Values and rules |
|---|---|
| Holder | Institution; faculty/researcher; student; sponsor; joint; indeterminate. Title, license beneficiary and royalty recipient are different roles. |
| Operation | Ownership presumption; conditional ownership; assignment obligation; purported present assignment; retained creator rights; nonexclusive license; exclusive license; exception; waiver; procedure; nonoperative definition; mixed; indeterminate. Discretionary waiver is not automatic creator title. |
| Category | Patentable inventions; software; algorithms; research datasets; scholarly publications; teaching materials; biological materials; tangible research property; emerging technologies; other explicit object; defined umbrella term; indeterminate. Do not expand umbrella terms without context. |
| Trigger | Employment/duties; sponsorship; resources (retain exact threshold); commission; affiliation; written agreement; other express condition; unconditional within scope; unresolved. Retain Boolean structure. |
| Scope | Broad prospective claim; conditional claim; creator/student protection; academic-work protection; exception to exception; ambiguity. Broad claim plus narrow exception is mixed, not automatically expansion. |
| Source | Exact original; dated official version with relevant context checked; later reprint; contemporary secondary reproduction; cleaned sentences only; inaccessible. Companion-policy availability is separate. |
| Enforceability | Not adjudicated by default. Policy language never establishes execution, state-law validity or adjudicated rights. |

## Actual diagnostics

Creighton C02 is a reciprocal nonexclusive license, not a title transfer. C03 has qualified academic-work exclusions. C04 is a form, not an observed signed contract. Illinois State I01 protects some educational software; an asset mention has no fixed direction. I03 is missed because `will normally own` is outside the old regex. Wake Forest W01 requires an introductory assignment and following trigger paragraphs; defined terms defeat a same-sentence asset/rule intersection. W02 is not ownership of all student work. H01 corroborates historical architecture but modal verbs differ. These selected diagnoses are not population error rates.

## Validation

The frozen probability sample has 178 sentences stratified by decade and original-screen positive/negative status, up to 12 per cell, seed 2031. Its manifest stores stratum sizes and inclusion probabilities. Text is rebuilt locally from the pinned corpus. Including negative cases permits eventual recall estimation. Category coverage is reported, not presumed balanced; rare-category coverage remains inadequate. A separate purposive sample covers clause types and contextual difficulties, and cannot be pooled as a random sample.

No independent human annotator was available. The template remains blank. Twelve AI-assisted readings are neither a second coder nor a reference standard. Precision, recall and agreement remain null. Future expert annotation should be blind to flags, source-contextual and independently adjudicated, retaining all initial decisions. Add rare-category strata with known probabilities before category error estimates. Use inverse inclusion probabilities and institution-cluster uncertainty; agreement is distinct from accuracy. Keep indeterminate cases, report category prevalence and raw disagreements, and never code unknown as negative.

## Historical comparisons

Match campus, policy authority, object, actor, trigger and scope before comparing adjacent observed vintages. Endpoints do not establish exact revision dates. Classify expansion, contraction, unchanged rule, mixed change, terminology-only, or unresolvable. Use common fact patterns: the same nonemployee student using ordinary course resources, for example. Different actors are not an ordered transition. Lexical matrices remain separate from ownership matrices. No institution-year has a completed exhaustive legal adjudication in this release; population legal outcomes remain unidentified.

A separate enrichment manifest draws up to 12 flagged sentences per knowledge-category and operation dictionary (seed 4031 plus stratum index). It covers rare flagged categories and clause types that the probability sample misses. Overlapping stratum membership is preserved; its within-stratum probabilities must not be treated as pooled population weights. It supplies review material, not completed validation.
