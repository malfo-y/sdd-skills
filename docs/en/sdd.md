# Spec-Driven Development (SDD)

A Paradigm Shift in Development for the Age of AI Agents

## TL;DR (One-Page Summary)

> **SDD (Spec-Driven Development)** is not about "writing documentation" -- it is a development approach that
**positions the Spec as the Source of Truth** so that AI agents stay on track, aligning implementation and verification beneath it.
>

### Three Common Failure Patterns in AI Coding

1. **Interpretation Drift**: The same requirement leads to different implementation decisions every time
2. **Context Window Limitations**: As the codebase grows, context is lost, leading to increased duplication, neglect, and workarounds
3. **Hallucination**: The AI fabricates non-existent APIs or libraries and codes as if they exist

### Three Control Mechanisms SDD Provides

- **Separation of intent declaration (What) and implementation (How)**
- **Drift detection**: Mechanisms to quickly catch the moment Spec and code diverge
- **Guardrails**: Encoding prohibited patterns, principles, and constraints (= constitution) into the Spec to limit the AI's degrees of freedom

## 0. Opening: The Goal of This Document

> "Understand SDD not as a 'theory' but as a **practical tool for working alongside AI agents**"
>

### Why "Intent-Centric" Now

Software engineering is shifting from "implementation-centric" to "intent-centric." Now that AI agents are beginning to take the lead in coding, what matters is not the speed of code generation but **whether the generated output aligns with the overall system design and business intent**.

This document treats SDD not as mere documentation but as an **Executable Spec** -- a contract -- and covers how to align implementation and verification against that contract to "use AI safely and quickly."

## 1. Problem Statement: Why Is AI Agent Development So Anxiety-Inducing?

### Symptoms We Already Experience When Coding with AI Agents

- The same requirement produces different results each time (AI randomness)
- "It should figure this out on its own" -- but results vary wildly
- Prompts are effectively **verbal contracts**
- When people or models change, context evaporates

### Three Failure Patterns of AI Agents (Core)

### 1) Interpretation Drift

- **Symptom**: Implementation choices change when the team, agent, or date changes (AI randomness)
- **Example**: Same "authentication" requirement, but Agent A implements JWT while Agent B uses session cookies -- conflict at integration time
- **SDD prescription**: Lock "decisions" into the Spec for **deterministic reuse**

### 2) Context Window Limitations

- **Symptom**: As the repo grows, the agent misses existing patterns, utilities, and rules, generating duplicate functionality
- **Example**: Ignoring an existing validation utility and creating yet another validator
- **SDD prescription**: The Spec becomes a "compressed essential context," stabilizing the agent's input

### 3) Hallucination and Fabricated Features

- **Symptom**: The AI fabricates non-existent APIs or libraries and writes code as if they work
- **SDD prescription**: Specify I/O, contracts, and constraints in the Spec to make them **verifiable**

#### (Terminology) I/O, Contract, Constraints, "Verifiable"

- **I/O**: What a specific function (especially a library function/module) **takes as Input** and **produces as Output**.
  - Information to include: input/output shapes (types, required/optional, ranges), success/failure results (return values/errors/exceptions), presence of side effects (I/O, state changes)
  - If I/O is left empty, the agent is more likely to fill in the blanks with guesses, increasing hallucinations.

- **Contract**: **Verifiable promises** that both the implementation and the consumer must uphold. (Statements where you can determine "correct/incorrect," not just "plausible.")
  - **Preconditions**: Conditions that must be true before invocation (input validity, prerequisite state)
  - **Postconditions**: Guarantees that must hold after invocation for both success and failure cases (return value properties, state changes)
  - **Invariants**: Rules the system/domain must always maintain (uniqueness, conservation laws, etc.)
  - Key point: When contracts are explicit, the review/test question shifts from "Does the code look plausible?" to "Does it satisfy the contract?"

- **Constraints**: Not "what to implement," but the **boundaries and guardrails that implementation must never cross**.
  - Examples: performance/complexity limits, security/compliance, compatibility (preserving existing behavior), dependencies (no new library additions), determinism/reproducibility requirements, no external I/O, etc.
  - Key point: Constraints block shortcuts the agent might take for convenience (introducing new libraries, calling non-existent APIs, etc.)

- **Verifiable**: A state where Spec statements can be **mechanically translated into tests, static analysis, or review checklists**.
  - Good signal: "Given when/what input, what result should occur" is clear, and counterexamples (failure modes) are also defined
  - Bad signal: Expressions without judgment criteria like "adequately/quickly/securely/working well"

### The Limits of "Prompt = Verbal Contract"

The core problem with vibe coding is that "conversation history" is hard to use as a team contract. Prompts are ambiguous; when people, models, or dates change, interpretation shifts; and as the codebase grows, context evaporates rapidly.

- **Unstructured input** (natural language prompts) does not accumulate team consensus -- results depend on "verbal contracts"
- **Decisions are not reused** -- the next agent, the next day, or a different person solves the same problem again, and the answer differs
- **As the repo scales**, the agent loses context -- duplicate functionality, rule violations, and pattern neglect increase
- When **hallucinations** enter as "code," the lack of traceable contracts/evidence delays recovery

SDD, instead of solving this problem with "better prompts," **externalizes decisions and constraints into a Spec** so that anyone (human or agent) receiving the same input reaches the same conclusion.

## 2. What Is SDD (Engineer's Perspective)

### One-Line Definition

> **SDD = Before code, create a Spec that both humans and AI read simultaneously, and operate that Spec as a contract**
>

Here, Spec means:

- Not just documentation (description), but
- **The system's contract** and **the baseline for change**

### Three Core Philosophies of SDD

1. **Spec is the Source of Truth** (code is the output)
2. **Important decisions are recorded in the Spec** (same conclusion regardless of who implements or when)
3. **Verification criteria also live in the Spec** (review/test/contract verification)

### The Practical Meaning of "Spec Is the Truth"

- From now on, the review/test question shifts from "Does the code look plausible?" to **"Does this implementation satisfy the Spec (contract)?"**
- With the Spec as the SoT, even when agents or developers change, the same inputs (contracts/constraints) converge to the same conclusions (implementation/tests/verification).
- Just remember one operating principle: **Even Specs created by AI are not finalized without human approval.** (The most dangerous moment is when a hallucination solidifies into a "contract.")

### Why SDD Adoption Has Become Easier in AI Agent Development

SDD originally had a reputation of being "good but heavy." However, as AI agents have explosively increased implementation productivity, paradoxically **the cost of Specs has decreased (writing/organizing) while the utility of Specs has increased (guardrails/verification)**, significantly lowering the adoption barrier.

#### Why Adoption Was Difficult in Traditional (Human-Centric) Development

- **Low perceived ROI relative to writing cost**: In environments where humans write code directly, it's easy to drift into "implement first, document later," pushing Specs to the sidelines.
- **Synchronization problem (Spec drift)**: Spec and code easily diverge, and without mechanisms to catch this, the Spec quickly loses trust.
- **Process resistance**: If it sounds like "let's write more documents," teams immediately perceive it as a burden, and adoption feels like "process overhaul," causing pushback.
- **Weak verification leads to futility**: If the Spec doesn't translate into tests or checklists, reviews ultimately regress back to "plausibility."

#### Why the Barrier Has Lowered in the AI Agent Era (and Where SDD Immediately Pays for Itself)

- **The faster implementation gets, the higher the probability of implementing incorrectly**: AI is fast but vulnerable to intent guessing and hallucination. Without Specs (contracts/constraints), rework becomes more expensive.
- **Spec drafting cost has plummeted**: AI can quickly produce Spec drafts, and humans fill in the blanks and decision points through Clarify.
- **Especially well-suited for function/module granularity**: Library development makes it easy to translate I/O and contracts (preconditions/postconditions/invariants) into sentences and tests, enabling short Spec -> Unit test -> Implement loops.
- **"Verifiable" is reinforced by tooling**: Attaching contract tests, schema validation, static analysis, and CI checks automates Spec-code consistency detection, reducing drift.

Additionally, AI can not only "write code on your behalf" but also **perform or automate Spec-centric tasks** such as those below, **lowering SDD's cost and raising its quality**:

- **Filling in Spec drafts/templates**: Quickly generating Goal/Non-goals/Definitions/component skeletons
- **Listing Clarify questions**: Automatically generating questions (with options/risks) that need decisions before implementation
- **Generating Acceptance Criteria (= test candidates)**: Proposing normal/boundary/error cases per interface in Given/When/Then format
- **Detecting omissions/conflicts/ambiguity**: Flagging missing parts in I/O, error models, and constraints, as well as inconsistencies between sections (terminology/policies/prohibitions)
- **Assisting Spec -> Plan/Tasks conversion**: Drafting implementation plans and task breakdowns (priority, impact scope, verification points)
- **Spec-Code drift review**: Examining PR diffs/tests and compiling a report of "in Spec but not implemented / implemented but not in Spec"

#### Conclusion: The Key to Adoption Is Not "Let's Write More Documents" but "Let's Change Our Verification Criteria to Spec"

- The biggest misconception when adopting SDD is that it means "increasing the volume of Spec writing."
- In practice, the starting point is **fixing the PR/review Definition of Done to Spec-based criteria (contracts/constraints/verification)**, and then processes and tools can be incrementally improved.

> (Adoption methods and roadmaps are covered in more detail in the operational process section and the appendix "Adoption" section below.)

### Traditional Development (Code-first) vs SDD (Intent/Spec-first)

| Aspect | Traditional Development (Agile/Code-First) | SDD (Spec-Driven Development) |
| --- | --- | --- |
| Source of Truth | Implementation code | Executable Spec |
| Human's role | Writing code / implementing logic | System design / defining intent (Orchestrator) |
| AI's role | Autocomplete / snippet generation | Spec-based implementation + verification (tests/contracts) |
| Change management | Code modification + post-hoc documentation update | **Spec modification -> code regeneration/realignment** |
| Primary artifacts | Commit, Unit Test | Spec, Plan, Data Model |

### (Bonus) SDD vs TDD / BDD (AI Perspective)

| Perspective | SDD | TDD | BDD |
| --- | --- | --- | --- |
| Starting point | Spec (intent/constraints/contracts) | Tests (correctness) | Scenarios (behavior) |
| Key question | "What must we guarantee?" | "Is this function correct?" | "How does the user use it?" |
| AI-friendliness | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ |
| Large-scale changes | Strong (contract-based) | Weak | Medium |

> Conclusion: **SDD does not replace TDD/BDD. SDD sits above, and TDD/BDD come below.** (Layering)
> For a detailed practical summary, see [Appendix G. TDD/BDD Practical Summary (SDD Context)](#appendix-g-tddbdd-practical-summary-sdd-context).
>

## 3. SDD's 'Control Plane': Three Mechanisms

From a handout perspective, it's faster to understand SDD not as a "documentation technique" but as an **architectural control mechanism**.
That is, it treats architecture not as "recommendations" but as **rules enforced through specifications (executable intent)**.

### The Control Plane in One Sentence

SDD controls the pathway from **intent (What) -> implementation (How)** through the Spec, transforming drift, hallucination, and team rule violations from "individual mistakes" into **system-level verification problems**.

### 1) Separation of Declarative Intent (What) and Implementation (How)

- Spec is what (Goal/Non-goals/Contract/Invariants)
- Implementation is how (language/framework/optimization)

This separation increases the **longevity of business logic** (intent persists even when technology changes) and reduces risk in large changes like legacy modernization (e.g., Node.js -> Go).

### 2) Drift Detection

- Quickly detect the moment Spec and code diverge (= drift)
- Examples: contract tests, schema validation, payload inspection, spec diff review

Treat architecture/contracts like **runtime invariants**, enforcing them continuously even during operation.
It's not "review once and done" -- it can be reinforced to continuously verify spec-code consistency in CI.

### 3) Guardrails

- Prevent AI from producing "plausible but non-standard code"
- Specify **prohibited patterns, principles, and constraints** as a constitution

### Symbiosis with AI Agents (Division of Roles)

- **AI excels at pattern recognition and implementation automation, but has limitations in intent inference**.
- Spec/Constitution is the **top-level guideline/constraint (Guardrail)** that prevents AI from interpreting things "at will."
- Important operating principle: **Even specs generated by AI must be approved by humans** (to prevent the risk of solidifying hallucinations as specs).

## 4. Operational Process: A Loop Your Team Can Follow Starting Tomorrow

The key is not "perfect specs from the start" but **clarifying ambiguity up front and iterating in small loops**.

### Why 10-20 Minutes of Clarify Is the 'Cheapest Insurance'

The draft from the Specify phase usually has "plausible but blank" spots. Clarify quickly surfaces those blanks as questions (what needs to be decided), locks them as decision logs, and **offsets rework that would otherwise explode later**.

| Phase | Purpose | Output (examples) | Key Point |
| --- | --- | --- | --- |
| Constitution | Fix invariant principles / prohibited patterns | constitution.md | Consistency guardrails |
| Specify | Define intent / goals / scope | feature spec | Agree on what to build |
| Clarify | Fill in the blanks | Q&A / decision log | **10-20 min investment reduces rework** |
| Plan | Technical plan / integration points | implementation plan | Dependencies / risks |
| Tasks | Break into small units | task list | 1-3 files per task recommended |
| Implement | Implement / verify / review | code + tests | Review criteria = Spec |

### What to Write at Each Phase

- **Constitution**: "Codify" project invariant rules and prohibited patterns
  - Example: Write **specific prohibition rules** like "Error handling is done only in global middleware; try/catch in routers is prohibited."
- **Specify**: Focus on **user journeys, success criteria, and business constraints** rather than tech stack
- **Clarify**: 10-20 minutes of questions and decision logs **significantly reduce rework risk**
  - Force "where are the blanks" and "what decision points exist" to surface.
- **Plan**: Data models, API contracts, integration points, library/constraint summary
  - Especially in brownfield projects, have AI **"research" the existing codebase first** to reduce duplicate implementations.
- **Tasks**: Each task should be limited to **1-3 files in scope** whenever possible (to prevent quality degradation in large LLM changes)
- **Implement**: Human review shifts focus from syntax to **Spec compliance and architectural fitness**

---

## 5. Minimal Spec Template for Immediate Use

### A "Sufficient for AI" Minimal Spec

This section organizes templates based on **skill documents**.

- **Main Spec (SoT)**: `_sdd/spec/<project>.md` or `_sdd/spec/main.md` created by `/spec-create`
- **Update input (requirements bundle)**: `user_spec.md` (manually written) / `user_draft.md` (`/spec-draft`) -> `/spec-update-todo` applies changes to the main spec

Below is the **minimal skeleton** for keeping the main spec "just sufficient for AI." (The sections we actually use: Description / Component Details / Acceptance Criteria)

```markdown
# <Project Name>

## 0. Description

### Goal
- The purpose of the project/module (what problem does it solve?)

### Non-Goals
- What is explicitly excluded from this scope

### Definitions
- Core terminology / abbreviation definitions

### Success Criteria (optional)
- How "success" is judged (e.g., accuracy/performance/operational metrics)

### Constraints (optional)
- Performance/security/compatibility/dependency/external I/O prohibition, etc.

## 1. Component Details

### <Component Name>

| Aspect | Description |
|---|---|
| **Purpose** | What this component does |
| **Input** | Input type/shape/preconditions |
| **Output** | Output type/shape/success conditions |
| **Dependencies** | Internal modules/external dependencies (if any) |

**Architecture Details (optional)**
- Implementation approach (high-level direction)
- Key classes/functions

**How to Use (optional)**
- Usage examples (brief)

**Known Issues (optional)**
- Limitations/risks/future improvements

## 2. Acceptance Criteria

- [ ] (Normal case) Given input X, output Y is produced
- [ ] (Error case) Under condition Z, an error/exception occurs (including error model)
- [ ] (Constraint) Performance/security/dependency constraints are not violated
```

### Why This Template Is "Sufficient for AI"

1. **Description contains Goal/Non-Goals/Constraints together**, making it hard for AI to freely expand "out of scope."
2. The **Component Details table** fixes I/O, dependencies, and responsibilities, reducing hallucinations that fabricate non-existent APIs or modules.
3. **Acceptance Criteria** become the minimum unit for tests and reviews, enabling quick "correct/incorrect" verification of implementation results.

### Why "Minimal" Matters (Preventing Over-spec)

- A Spec is not a document containing all explanations but should be a **compressed version of decisions, contracts, and constraints**.
- An overly detailed Spec (Over-spec) wastes context and slows things down. Instead, lock scope with Goal/Non-goals, and create **verifiable boundaries** with Inputs/Outputs + Invariants to make it hard for AI to guess freely.

## 5A. Markdown Spec Is the Default (Sufficient for Most Cases)

- **Markdown Spec = Source of Truth (intent/scope/decisions/constraints)**
- **OpenAPI/TypeSpec = Boundary Contract (machine-verifiable/generatable interface contracts)**

Most early-stage and single-team development is **sufficiently served by Markdown Spec alone**.
OpenAPI/TypeSpec is introduced when you need to **automatically verify, generate, and enforce compatibility** for interfaces that cross team/system boundaries.
For introduction signals, checklists, and progressive formalization loops, see **Appendix A** at the bottom of this document.

## 5B. Over-spec Prevention & Leveling Rules

To prevent AI from making specs excessively detailed, **capping with rules** is more effective than "writing well."

### 1) Spec Budget (Upper Limit) -- Limit Length/Depth

- L0/L1 (see level definitions below) combined should not exceed **2-3 pages (or N lines)**
- Examples in the body are limited to **1 key flow + 1 error example**
- Edge cases should be "listed" but without implementation algorithms (use L2 if needed)

### 2) MUST Is a Contract; Explanations Are Separated

- **MUST/SHALL**: Contracts that must be upheld (verification targets)
- **SHOULD/MAY**: Recommendations/optional
- "Why (context/rationale)" is the primary culprit for bloating the body, so separate it into **Rationale/Decision log (L2)**

### 3) What Must NOT Be Written in the Spec (Prohibited)

- **Implementation directives (How)** such as specific file structures, class names, function names, or algorithms
- Optimization/performance-tuning details that have not yet been agreed upon
- Verbose explanations unrelated to team standards (tutorials/textbook-style definitions)

### 4) Leveling (Hierarchy) -- How to "Keep It Short" While Still Capturing Necessary Detail

- **L0: One-pager (intent/scope)**
  - Goal / Non-goals / Success criteria / Core constraints (invariants)
- **L1: Contract Spec (verifiable boundaries)**
  - Inputs/Outputs, error model, state/flow, Invariants
  - (If needed) Promote to OpenAPI/TypeSpec at this stage
- **L2: Rationale / Decision log (Why/alternatives/risks)**
  - Trade-offs, alternative comparisons, operational considerations, rationale links
- **L3: Implementation Plan (How/work units)**
  - Module boundaries, migration/release, task breakdown (1-3 files per task recommended)

### 5) Review Checklist (Detecting Over-spec)

- [ ] Are implementation (How) details mixed into the body (L0/L1)? -> Move to L3
- [ ] Are "obvious explanations" repeated at length? -> Delete/summarize
- [ ] Are highly changeable details (internal structures/function names) fixed as if they were contracts? -> Remove
- [ ] Are MUST (verification targets) and explanations (reference) mixed, bloating the document? -> Separate

### 6) Operational Rules When Delegating to AI (Preventing Runaway)

- First generate 5 Clarify questions; if unanswered, **mark as Assumptions**
- Draft only up to **L0/L1 (+ decision log agreed with the user) and stop** (mark needed details as "additional detail required" only)
- Explicitly state "no implementation directives" in the Constitution/prompt

---

## 6. "Small Start" Roadmap for Your Team

### Week 1: Apply to Just One Feature

- Choose one new feature (or a small improvement) and write the Spec first
- Delegate implementation to AI, but fix the review criteria to the Spec

### Week 2: Build a Spec Review Loop

- Not "no implementation discussions," but **agree on the contract first**
- Use AI as a review assistant: AI reads the Spec and generates a list of questions that need decisions
- Fix questions (Clarify) as a template: blanks/ambiguities/decision points

### Start Adoption as a 'Review Criteria Change,' Not a 'Process Change'

The most realistic first step is not "let's write more Specs" but **fixing the PR's Definition of Done to be Spec-based**. Let AI produce implementations quickly, while humans focus on (1) Spec alignment, (2) Constitution violations, and (3) presence of verification (tests/contracts) -- plant this principle in the team first.

### Anti-patterns (Preventing Waterfall Regression)

- Do not try to write everything in advance (excessive elaboration)
- Iterate in short cycles per feature (hours to days)
- Send detailed rationale/tool comparisons to **appendices** to keep the body lightweight

### Phased Adoption Roadmap (Organizational Perspective)

1. **Spec-Aware**: Keep the coding approach, but build a culture of **agreeing on contracts/decisions first with Markdown Specs**
2. **Spec-Led**: **"Enforce" the Specify -> Plan -> Tasks phases** in the process with **AI (agents) + checklist/artifact rules + review loops**
   - (Example) `/spec-review` generates a question/risk report -> (human approval/decision) -> `/spec-update-done` reflects changes in the Spec (SoT)
3. **Spec-Synced/Automated**: Add **spec-code consistency verification** to CI/CD, and connect automatic SDK/test regeneration when specs change

### Essential Considerations for Adoption

- **Human-AI collaboration model**: AI = implementation efficiency, Human = design/final verification (supervisor)
- **Tool selection**: The core is not the "tool" but the **operational rules (templates/artifact paths/review gates)**; supplement with tools like Spec Kit/Kiro or specification languages (TypeSpec/OpenAPI, etc.) for automation/verification as needed
- **Culture/education**: The mindset that "writing specs is coding" + shifting review focus from syntax to intent/architecture

---

## 7. Q&A Cheat Sheet (10 min)

Structured as "one-line answer + supporting points" so the presenter can respond immediately.

1. **Q. Isn't this just waterfall?**

- A. It's not waterfall where everything is designed in advance; it's a **loop that iterates in short cycles per feature**.
- Supporting: 10-20 minutes of Clarify investment reduces rework, and when changes occur, Spec modification -> code realignment is fast

1. **Q. Isn't the maintenance cost of documentation (specs) too high?**

- A. We maintain only **decisions, contracts, and constraints** -- not "all explanations."
- Supporting: Detailed background/rationale is separated into appendices/links

1. **Q. Do we abandon TDD/BDD?**

- A. No. SDD is the upper layer (intent/contracts), TDD/BDD is the lower layer (verification). For details, see [Appendix G](#appendix-g-tddbdd-practical-summary-sdd-context).

1. **Q. What's the most effective way to instruct AI?**

- A. Instead of "verbal prompts," instruct with **Spec + prohibitions/principles (constitution) + work units (Tasks)**.

1. **Q. How do we measure success?**

- A. Use **operational metrics** like post-deployment defects/rework/review time and onboarding time.

1. **Q. Doesn't writing Specs too detailed actually slow things down?**

- A. Correct. That's why SDD focuses on **essential intent/constraints/contracts** and sends the rest to links/appendices.

1. **Q. If 'why (context)' is missing from the Spec, won't the AI reach wrong conclusions?**

- A. That's a risk. That's why we leave minimal **decision rationale (Why)** through Clarify/Decision logs,
and document at least some "tribal knowledge."

1. **Q. Can we trust Specs generated by AI as-is?**

- A. No. **All Specs require human approval**, and especially for external APIs/libraries, verifiable evidence must be provided.

---

## Appendix A. (Reference) TypeSpec vs OpenAPI (Further Reading)

> Not included in the main body; placed as an appendix for those who want to read more.
>

| Feature | OpenAPI (YAML/JSON) | TypeSpec |
| --- | --- | --- |
| Code readability | Verbose / highly repetitive | Relatively concise, familiar to TS developers |
| Reuse / abstraction | Centered on $ref | Strong abstraction via generics/templates/mixins |
| Validation | Focused on runtime schema validation | Compile-time type checking support (tool-based) |
| Management unit | Difficult to manage at file level | Namespace/package system support |
| Productivity | High error rate when written manually | Strong IDE IntelliSense/autocomplete |
| Output | Is itself the standard | A "higher-level language" that compiles to OpenAPI, etc. |

Practical guide:

- If OpenAPI is already the organizational standard: **Keep OpenAPI + establish the contract/verification culture from the Spec first**
- If APIs are growing and repetition increases: **Consider introducing** a higher-level language like TypeSpec

### Signals That OpenAPI/TypeSpec Would Be Beneficial (Checklist)

If **2 or more** of the following apply, strongly consider adopting OpenAPI/TypeSpec.

1. **APIs that cross team/repo boundaries** (other teams, other services, external customers, mobile apps, etc.)
2. **Interfaces with frequent conflicts due to concurrent development** (FE/BE, inter-service)
3. **Need for SDK/client/mock/documentation portal generation**
4. **Want to apply schema validation to requests/responses/events in CI/runtime**
5. **Version compatibility/migration** needs to be managed systematically
6. "We agreed verbally but implementations differ" keeps happening -> **Insufficient contract enforcement**

### Signals That Markdown Alone Is Sufficient (Checklist)

- Single team / single codebase, limited consumers
- The area is still changing rapidly (exploration/prototype) and it's too early to fix contracts
- **Intent, scope, and decision (Goal/Non-goals) consensus** is more important than automatic schema generation/validation

### Recommended Progressive Formalization Loop

1) First, capture only the **"surface" of the boundary contract** in Markdown (fields/errors/1 example).
2) Once that boundary stabilizes, **promote only that part** to OpenAPI/TypeSpec.
3) Add at least one check in CI (e.g., schema validation/contract test) to make "contract = automatic enforcement."

## Appendix B. Curated Reference Links

- InfoQ: Spec Driven Development (as of 2026-02) -- <https://www.infoq.com/articles/spec-driven-development/>
- GitHub Blog: Spec-driven development with AI -- <https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/>
- github/spec-kit -- <https://github.com/github/spec-kit>
- Martin Fowler: SDD-related tools and perspectives -- <https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html>
- Marmelab: "Is SDD the Return of Waterfall?" Criticism and counterpoints -- <https://marmelab.com/blog/2025/11/12/spec-driven-development-waterfall-strikes-back.html>

---

## Appendix C. Strategic Value and ROI of SDD (Detailed)

> The figures below are directly cited from industry cases/research included in deep_research and may vary by team/domain.
>

### Quantitative Results (Examples)

- **Deployment time reduction**: Up to **50% reduction** in deployment time through clear spec-based AI coding
- **Defect rate reduction**: Approximately **40% reduction** in post-deployment defects through spec-code automated verification
- **API development acceleration**: **75% reduction** in cycle time with a contract-driven approach (case study)
- **Migration efficiency**: **80% of work automated** and **50% total time savings** through spec-based automation (case study)

### Qualitative Value (Long-term Benefits)

1. **Knowledge as an asset & accelerated onboarding**: System knowledge accumulates in the Spec, not in individuals
2. **Easier legacy modernization**: Business rules are separated as intent (What), making technology replacement easier
3. **Eliminating collaboration ambiguity**: FE/BE share specs (OpenAPI/TypeSpec, etc.) to reduce integration conflicts
4. **Strengthened security/compliance**: Security requirements and regulatory rules are proactively enforced in Constitution/Spec

## Appendix D. Risk Management (Detailed): 'The Return of Waterfall'?

### Differences Between SDD and Waterfall (Summary)

- **Time scale**: Waterfall spans months to years; SDD operates in **loops of hours to days per feature**
- **Flexibility**: Waterfall specs are hard to change; SDD enables **code regeneration/realignment** after Spec modifications
- **Feedback loop**: Spec is reviewed and clarified before implementation, with continuous consistency verification

### Operational Constraints / Anti-patterns (Summary)

1. **Spec maintenance cost (maintenance tax)**: Without a Spec-first culture, Specs become useless
2. **Missing context (Why)**: If only "What" remains and "Why" is absent, it can deviate from intent
3. **Over-specification**: Context window waste + slowdown
4. **Blind trust in AI-generated specs**: The worst failure -- solidifying hallucinations as Spec

Recommended Mitigations (Practical)

- Maintain only **contracts/constraints/decisions** as Spec, not "all explanations"
- Leave minimal **Why** through Decision logs
- Break large features into phases, and tasks into 1-3 file units

## Appendix E. SDD Adoption Checklist (Detailed)

### Phased Adoption (Summary)

1. Spec-Aware -> 2) Spec-Led -> 3) Spec-Synced/Automated

### Adoption Checklist (Recommended)

- [ ]  Constitution (principles/prohibited patterns) consensus exists as a document
- [ ]  Spec template is established as a team standard (including Goal/Non-goals/Contract/Invariants)
- [ ]  Clarify question list exists, and decision logs are maintained
- [ ]  Plan phase explicitly specifies integration points/data models/API contracts
- [ ]  CI performs at least one spec-code consistency check (contract tests/schema validation, etc.)
- [ ]  Review criteria are focused on "Spec compliance/architectural fitness" rather than "syntax"

## Appendix F. Future Outlook: Self-healing / Closed-loop Architecture

- The prospect of **self-healing** is emerging, where AI agents automatically correct or alert when runtime behavior diverges from the Spec
- The **closed-loop** pattern is expected to strengthen, where system performance and operational data feed back into the Spec to evolve the design
- The engineer's role is being redefined from "person at the keyboard" to **designer and supervisor of intelligent systems**

## Appendix G. TDD/BDD Practical Summary (SDD Context)

### Why This Appendix Is Needed

- SDD is the upper layer that fixes "intent/contracts (What)."
- TDD/BDD is the lower layer that translates those contracts into "verifiable executable form."
- In other words, **SDD sets the direction, and TDD/BDD proves the quality**.

### TDD (Test-Driven Development) in Detail

One-line definition:

- **TDD is an iterative loop where you write the test first (confirm failure), pass it with minimal implementation, and raise quality through refactoring**.

Core loop (Red-Green-Refactor):

1. **RED**: Translate acceptance criteria (AC) into test cases and confirm failure
2. **GREEN**: Write only the minimal code to pass the test
3. **REFACTOR**: Improve duplication/readability/structure and confirm all tests continue to pass

Practical application checklist (our approach):

- Link at least 1 test per acceptance criterion
- Name tests in `test_<unit>_<scenario>_<expected>` format whenever possible
- Maintain Arrange-Act-Assert (AAA) structure in test bodies
- After passing tests per criterion, run the full test suite at the end to check for regressions
- Refactoring is performed only within a scope that does not change behavior

Where TDD is especially effective:

- Service logic with clear domain rules/error models
- Endpoints with clear API request-response contracts (normal/boundary/error)
- Refactoring/module separation work with high regression risk

### BDD (Behavior-Driven Development) Brief Summary

One-line definition:

- **BDD is an approach that aligns shared team understanding by specifying behavioral scenarios from the user/business perspective in Given-When-Then format**.

Connection with SDD:

- BDD is useful when concretizing SDD's high-level requirements into "user behavior language."
- Written scenarios subsequently serve as input material for TDD test cases.

Short example:

- Given: An existing member email exists
- When: A registration request is made with the same email
- Then: The system returns a 409 response

### Summary: The Layering Principle

- **SDD**: Decides what to guarantee (intent/contracts)
- **BDD**: Converts into scenarios of what user behaviors must be satisfied
- **TDD**: Verifies those scenarios/contracts through tests and code
