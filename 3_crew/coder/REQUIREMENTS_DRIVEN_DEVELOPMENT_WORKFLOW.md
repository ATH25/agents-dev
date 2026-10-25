# Requirements-Driven Development Workflow (RDDW)

## 1. Purpose

This document defines the Requirements-Driven Development Workflow (RDDW) used to develop software incrementally with AI coding agents such as Claude Code CLI and Codex CLI.

The objective is to establish a consistent, traceable, and controlled process for transforming informal business requirements into formal functional requirements, technical implementation plans, executable tasks, and verified software.

The workflow supports incremental development. The complete set of requirements does not need to be known upfront. New functional requirements may be introduced individually or in small groups throughout the development lifecycle.

### Core Principles

1. **Requirements-driven development:** Business requirements drive technical planning and implementation.
2. **Incremental elaboration:** New requirements can be introduced without regenerating previously completed work.
3. **End-to-end traceability:** A common functional requirement identifier connects all development artifacts.
4. **Hierarchical task management:** Implementation work is organized into requirements, tasks, and subtasks.
5. **Controlled execution:** AI agents must respect approval boundaries before implementation.
6. **Preservation of existing work:** Previously approved requirements, plans, completed tasks, and verification evidence must be preserved.
7. **Tool independence:** The workflow applies equally to Claude Code CLI, Codex CLI, and other AI development tools.
8. **Business-first requirements:** Formal requirements must describe business functionality and observable outcomes in language understandable to business analysts, product managers, QA engineers, and business stakeholders.
9. **Separation of requirements and implementation:** Functional requirements describe WHAT the application must accomplish. Technical implementation plans describe HOW those requirements will be satisfied.
10. **Business-verifiable acceptance criteria:** Acceptance criteria must primarily describe observable outcomes that business analysts, product managers, and QA engineers can understand and validate without requiring knowledge of implementation details.

### Business-First Requirements Principle

The primary audience for `requirement.md` is business analysts, product managers, QA engineers, and business stakeholders.

The document must focus on business functionality, expected system behavior, and measurable acceptance criteria.

Technical implementation details should be documented primarily in `plan.md`.

Technical requirements are optional and should generally be defined in `plan.md` under their corresponding functional requirement.

Technical constraints that represent explicit business, regulatory, security, performance, or operational obligations must remain visible in `requirement.md`.

The objective is to ensure that business stakeholders can review, understand, approve, and validate functional requirements without needing detailed knowledge of the underlying technology.

---

## 2. Development Lifecycle

The workflow consists of six stages.

```text
requirement-draft.md
        |
        v
requirement.md
        |
        v
plan.md
        |
        v
tasks.md
        |
        v
Implementation
        |
        v
Validation & Testing
```

### Stage 1: Draft Requirements

**Document:** `requirement-draft.md`

This document contains the original business requirements provided by the project owner.

Requirements may be:

- Informally written.
- Incomplete.
- Expressed in business language.
- Introduced incrementally.
- Modified as the project evolves.

The AI agent must preserve the original business intent.

Only the project owner may introduce or approve new top-level functional requirement identifiers.

The AI agent must not introduce additional top-level functional requirements without approval.

### Stage 2: Formal Requirements

**Document:** `requirement.md`

This document defines **WHAT** the application must accomplish.

The AI agent transforms informal requirements into structured, clear, and testable functional requirements.

The primary audience includes:

- Business analysts.
- Product managers.
- Product owners.
- QA engineers.
- Business stakeholders.

Each functional requirement should contain:

- Functional requirement identifier.
- Requirement title.
- Business objective.
- Functional description.
- Expected functional behavior.
- Business rules and constraints, where applicable.
- Acceptance criteria.
- Assumptions and open questions.

#### Documentation Rules

1. Describe the functionality from the business or user perspective.
2. Use clear language understandable to nontechnical stakeholders.
3. Avoid unnecessary technical terminology.
4. Do not prescribe implementation technologies unless explicitly required.
5. Define acceptance criteria that describe observable, testable outcomes.
6. Preserve the business intent of the original requirement.
7. Keep implementation architecture, libraries, frameworks, and configuration details primarily in `plan.md`.

#### Technical Constraints in requirement.md

Technical requirements should not be added to `requirement.md` merely because they are relevant to implementation.

However, technical or nonfunctional constraints must remain visible when they represent explicit business obligations.

Examples include:

- Regulatory compliance requirements.
- Security requirements mandated by the business.
- Data retention requirements.
- Availability requirements.
- Performance requirements.
- Privacy requirements.
- Auditability requirements.

For example:

```text
The application must retain audit records for seven years.
```

This belongs in `requirement.md` because it represents a business or compliance obligation.

The technical architecture for implementing the retention mechanism belongs in `plan.md`.

### Stage 3: Technical Implementation Plan

**Document:** `plan.md`

This document defines **HOW** the requirements will be implemented.

The primary audience includes:

- Software architects.
- Technical leads.
- Software engineers.
- AI coding agents.
- DevOps and platform engineers.

Each functional requirement should have a corresponding technical implementation section.

The plan may include:

- Technical requirements, when applicable.
- Implementation approach.
- Application architecture.
- Components and modules.
- Technology choices.
- Frameworks and libraries.
- Configuration changes.
- Integration requirements.
- Security considerations.
- Performance considerations.
- Dependencies.
- Testing strategy.
- Technical validation criteria.
- Technical risks.
- Decisions requiring approval.

#### Optional Technical Requirements

Technical requirements are optional.

When technical requirements are necessary, they should generally be documented in `plan.md` under their corresponding functional requirement.

Each technical requirement must reference its parent functional requirement.

Example:

```text
FR-02: Execute Python Code

    TR-FR-02-01: Execution Isolation

    TR-FR-02-02: Execution Timeout

    TR-FR-02-03: Execution Result Capture
```

Technical requirements define technical capabilities or constraints that the implementation must satisfy.

They should not be confused with technical implementation decisions.

For example:

| Statement | Classification |
|---|---|
| The coding agent must execute generated Python code. | Functional requirement |
| Generated code must execute in an isolated environment. | Technical requirement |
| Execution must enforce a configurable timeout. | Technical requirement |
| Use Docker to implement the sandbox. | Technical implementation decision |
| Configure Docker resource limits. | Implementation task |
| Verify that execution terminates after the timeout. | Technical validation |

If the project owner explicitly mandates a particular technology, that technology becomes a requirement or constraint rather than an optional implementation decision.

Technical recommendations must be distinguished from approved technical decisions.

### Stage 4: Implementation Tasks

**Document:** `tasks.md`

This document defines the actionable work required to implement each functional requirement.

Tasks must be organized hierarchically under their corresponding functional requirement.

Each task should include:

- Task identifier.
- Task description.
- Parent functional requirement.
- Relevant acceptance criteria.
- Relevant technical requirements, when applicable.
- Dependencies.
- Completion conditions.
- Execution status.
- Verification evidence.

Tasks should be sufficiently detailed that an AI coding agent can execute them without making significant unapproved architectural decisions.

### Stage 5: Implementation

The AI coding agent implements approved tasks.

Implementation must follow:

1. Approved functional requirements.
2. Approved technical requirements, when applicable.
3. Approved technical implementation plans.
4. Defined implementation tasks.
5. Project coding standards.
6. Security and operational constraints.

The agent must not implement unrelated functionality.

### Stage 6: Validation and Testing

The agent validates the implementation against the corresponding acceptance criteria and applicable technical requirements.

Validation may include:

- Business acceptance testing.
- Unit tests.
- Integration tests.
- Configuration validation.
- Functional testing.
- Security validation.
- Performance testing.
- Execution results.
- Manual verification, where appropriate.

#### Business Validation

Business validation determines whether the application behaves as requested.

Business acceptance criteria are defined in `requirement.md`.

They should be understandable and verifiable by business analysts, product managers, and QA engineers.

#### Technical Validation

Technical validation determines whether the implementation satisfies the required technical constraints and architecture.

Technical validation criteria and strategies are documented in `plan.md`.

Examples include:

- Verifying sandbox isolation.
- Verifying execution timeout enforcement.
- Verifying resource limits.
- Verifying API error handling.
- Verifying configuration correctness.

Tasks must not be marked complete until their applicable business and technical completion conditions have been satisfied and verified.

---

## 3. Functional Requirement Identification

### 3.1 Common Traceability Identifier

Every functional requirement must have a unique identifier.

Format:

`FR-XX`

Examples:

- `FR-01`
- `FR-02`
- `FR-03`
- `FR-04`

The functional requirement identifier is the primary traceability key throughout the development lifecycle.

**The same identifier must appear in all four documentation files.**

For example:

```text
FR-02
  |
  +-- requirement-draft.md
  |      FR-02: Original requirement
  |
  +-- requirement.md
  |      FR-02: Formal functional requirement
  |
  +-- plan.md
  |      FR-02: Technical implementation plan
  |
  +-- tasks.md
         FR-02: Implementation tasks
```

Searching for `FR-02` should identify all related requirements, implementation plans, tasks, and validation references.

### 3.2 Ownership of Functional Requirement IDs

Only the project owner introduces new top-level functional requirements.

For example, if `requirement-draft.md` contains:

```markdown
## FR-01: Initialize CrewAI Project

## FR-02: Configure Coder Agent
```

The AI agent must not independently introduce:

```markdown
## FR-03: Configure Agent Memory
```

unless FR-03 has been introduced or explicitly approved by the project owner.

However, the agent may elaborate FR-02 into detailed subrequirements, acceptance criteria, technical requirements, and implementation tasks.

### 3.3 Functional Requirement Subsections

A functional requirement may contain subrequirements.

Format:

`FR-XX.N`

Example:

```text
FR-02: Execute Python Code

    FR-02.1: Generate Python Code

    FR-02.2: Execute Generated Code

    FR-02.3: Return Execution Results
```

These are subdivisions of FR-02.

They are not independent top-level functional requirements.

Subrequirements must remain consistent with the business intent of their parent requirement.

Functional subrequirements should describe business behavior rather than technical implementation activities.

### 3.4 Technical Requirement Identifiers

Technical requirements are optional.

When defined, they must be associated with an existing functional requirement.

Format:

`TR-FR-XX-NN`

Example:

```text
FR-02: Execute Python Code
|
+-- TR-FR-02-01: Execution Isolation
|
+-- TR-FR-02-02: Execution Timeout
|
+-- TR-FR-02-03: Execution Result Capture
```

These technical requirements belong to FR-02.

They must not be treated as independent functional requirements.

Technical requirement identifiers must remain stable once assigned.

### 3.5 Identifier Stability

Once assigned, functional requirement identifiers must remain stable.

The same principle applies to:

- Functional subrequirements.
- Technical requirements.
- Acceptance criteria.
- Implementation tasks.
- Implementation subtasks.

Identifiers must not be reused for unrelated requirements or tasks.

If a requirement or task is cancelled or superseded, preserve its identifier and record the corresponding status.

---

## 4. Acceptance Criteria Identification

Each functional requirement must contain measurable acceptance criteria.

Format:

`AC-FR-XX-NN`

### 4.1 Business-Verifiable Acceptance Criteria

Acceptance criteria must primarily describe observable system behavior.

They should be understandable and verifiable by business analysts, product managers, and QA engineers without requiring detailed knowledge of the underlying implementation.

Example:

```markdown
## FR-02: Execute Python Code

### Acceptance Criteria

- AC-FR-02-01: Given a coding assignment, the agent
  generates Python code corresponding to the assignment.

- AC-FR-02-02: The agent executes the generated code.

- AC-FR-02-03: The agent returns the execution results.

- AC-FR-02-04: If execution fails, the agent reports
  the failure with an understandable error message.
```

These acceptance criteria describe expected functionality.

They do not prescribe how the application must implement that functionality.

### 4.2 Acceptance Criteria vs. Implementation Activities

Acceptance criteria must not be limited to implementation activities.

For example:

**Implementation activity:**

```text
Update agents.yaml.
```

**Business acceptance criterion:**

```text
Given a coding assignment, the configured agent
generates a Python solution.
```

The first describes work to perform.

The second describes a condition that must be satisfied.

### 4.3 Business Acceptance vs. Technical Validation

Business acceptance criteria belong in `requirement.md`.

Technical validation criteria should generally be documented in `plan.md`.

Example:

| Business Acceptance Criterion | Technical Validation |
|---|---|
| The agent executes generated Python code successfully. | Verify the execution process returns exit code 0. |
| The agent reports execution failures. | Verify stderr and nonzero exit-code handling. |
| The agent returns generated code and execution results. | Verify output artifact creation and contents. |
| The agent does not continue indefinitely when execution stalls. | Verify configured timeout enforcement. |

Both forms of validation are important.

However, they serve different audiences and purposes.

### 4.4 Acceptance Criteria Rules

1. Acceptance criteria must be observable and testable.
2. Acceptance criteria must primarily describe expected behavior.
3. Avoid implementation-specific terminology unless required by the business.
4. Acceptance criteria must remain traceable to their parent functional requirement.
5. Technical validation must not replace business acceptance testing.
6. Acceptance criteria must not introduce functionality that is absent from the approved business requirement.

---

## 5. Technical Plan Traceability

Each functional requirement must have a corresponding section in `plan.md`.

The technical plan must use the same functional requirement identifier.

### 5.1 Recommended Structure

Example:

```markdown
## FR-02: Technical Implementation Plan

### Objective

Implement the ability to generate and execute Python code.

### Technical Requirements (Optional)

#### TR-FR-02-01: Execution Isolation

Generated Python code must execute in an isolated environment.

#### TR-FR-02-02: Execution Timeout

The execution environment must enforce a configurable timeout.

### Technical Approach

Describe the proposed implementation approach.

### Architecture

Describe the architecture supporting the requirement.

### Components

Identify the components and modules involved.

### Dependencies

Identify required libraries and configuration dependencies.

### Technical Validation Strategy

Describe how the implementation will be technically validated.

### Decisions Requiring Approval

Document unresolved technical decisions.
```

### 5.2 Technical Requirements vs. Technical Decisions

A technical requirement defines a condition the implementation must satisfy.

A technical decision describes the chosen implementation approach.

Example:

```text
Technical Requirement:
    Generated code must execute in isolation.

Technical Decision:
    Use Docker containers to provide isolation.

Implementation Task:
    Configure the Docker execution environment.

Technical Validation:
    Verify that generated code cannot access
    unauthorized host resources.
```

This distinction allows implementation technologies to change without unnecessarily changing the underlying requirements.

### 5.3 Technical Requirement Traceability

When technical requirements are defined:

1. Each technical requirement must reference its parent functional requirement.
2. Each technical requirement must have a unique identifier.
3. Each technical requirement must be addressed by the implementation plan.
4. Relevant implementation tasks must reference the technical requirements they satisfy.
5. Technical validation must demonstrate that applicable technical requirements are satisfied.

### 5.4 Implementation Phases

Implementation phases may be used for scheduling or organizing work.

However, phase identifiers such as `P-01` or `P-02` must not be treated as functional requirement identifiers.

A phase may contain tasks associated with multiple functional requirements.

**Functional requirement IDs remain the authoritative traceability mechanism.**

---

## 6. Hierarchical Implementation Task Identification

Implementation tasks must be organized under their corresponding functional requirement.

### 6.1 Parent Task Identifier

Format:

`T-FR-XX-NN`

Example:

```text
FR-02
  |
  +-- T-FR-02-01: Configure Agent
  |
  +-- T-FR-02-02: Configure Task
  |
  +-- T-FR-02-03: Configure Crew
```

The task identifier explicitly identifies its parent functional requirement.

### 6.2 Subtask Identifier

Format:

`T-FR-XX-NN.N`

Example:

```text
FR-02: Configure Coder Agent
|
+-- T-FR-02-01: Configure agents.yaml
|     |
|     +-- T-FR-02-01.1: Define agent role
|     |
|     +-- T-FR-02-01.2: Define agent goal
|     |
|     +-- T-FR-02-01.3: Configure LLM
|     |
|     +-- T-FR-02-01.4: Validate configuration
|
+-- T-FR-02-02: Configure tasks.yaml
      |
      +-- T-FR-02-02.1: Define coding task
      |
      +-- T-FR-02-02.2: Define expected output
      |
      +-- T-FR-02-02.3: Configure output file
      |
      +-- T-FR-02-02.4: Validate task configuration
```

### 6.3 Example tasks.md Structure

```markdown
## FR-02: Configure Coder Agent

### T-FR-02-01: Configure agents.yaml

- [ ] T-FR-02-01.1: Define the coder agent role.
- [ ] T-FR-02-01.2: Define the coder agent goal.
- [ ] T-FR-02-01.3: Configure the LLM.
- [ ] T-FR-02-01.4: Validate the agent configuration.

Functional Requirement:
- FR-02

Technical Requirements:
- TR-FR-02-01 (if applicable)

Acceptance Criteria:
- AC-FR-02-01

Dependencies:
- Required framework configuration must be available.

Completion Conditions:
- The agent configuration is valid.
- The application can load the agent configuration.

Verification Evidence:
- Pending.

### T-FR-02-02: Configure tasks.yaml

- [ ] T-FR-02-02.1: Define the coding task.
- [ ] T-FR-02-02.2: Define expected output.
- [ ] T-FR-02-02.3: Configure the output file.
- [ ] T-FR-02-02.4: Validate the task configuration.

Functional Requirement:
- FR-02

Acceptance Criteria:
- AC-FR-02-02
- AC-FR-02-03

Dependencies:
- T-FR-02-01

Completion Conditions:
- The task configuration is valid.
- The task references the intended agent.

Verification Evidence:
- Pending.
```

### 6.4 Task Completion Rules

A parent task may be marked complete only when:

1. All required subtasks are complete.
2. Relevant acceptance criteria are satisfied.
3. Applicable technical requirements are satisfied.
4. Required verification has succeeded.
5. Any required approvals have been obtained.

A completed task must contain appropriate verification evidence.

A failed or blocked task must remain incomplete.

### 6.5 Cross-Requirement Dependencies

A task may depend on work associated with another functional requirement.

For example:

```text
T-FR-03-01 depends on T-FR-02-02
```

The task retains its primary requirement identifier.

If a task supports multiple functional requirements, it must explicitly reference the additional requirements.

Do not duplicate the same implementation work under multiple requirements.

---

## 7. Incremental Requirements Development

The workflow must support introducing new functional requirements throughout the project lifecycle.

### Example

Initially:

```text
FR-01
FR-02
```

Later, the owner adds:

```text
FR-03
FR-04
```

The AI agent must process only the newly introduced or explicitly modified requirements.

The agent must not regenerate all existing documentation.

### Incremental Processing Rules

When a new functional requirement is introduced:

1. Read the new requirement from `requirement-draft.md`.
2. Review existing formal requirements and dependencies.
3. Add the corresponding section to `requirement.md`.
4. Add the corresponding technical implementation section to `plan.md`.
5. Add the corresponding hierarchical tasks to `tasks.md`.
6. Validate traceability across all documents.
7. Identify unresolved decisions.
8. Request approval before implementation.

Previously completed requirements and tasks must remain unchanged unless the new requirement creates a documented dependency or conflict.

### Example

If FR-03 is introduced:

```text
requirement-draft.md
    FR-03

requirement.md
    FR-03
    AC-FR-03-01
    AC-FR-03-02

plan.md
    FR-03
    TR-FR-03-01 (optional)

tasks.md
    FR-03
    T-FR-03-01
    T-FR-03-01.1
    T-FR-03-01.2
    T-FR-03-02
```

The agent must preserve FR-01 and FR-02.

---

## 8. Requirements Traceability Validation

Before completing a documentation update, the AI agent must validate traceability.

### Required Checks

1. Every formal functional requirement corresponds to an owner-approved draft requirement.
2. Every functional requirement has a corresponding technical implementation plan.
3. Every functional requirement has relevant acceptance criteria.
4. Every functional requirement has associated implementation tasks.
5. Every implementation task references its parent functional requirement.
6. Relevant tasks reference applicable acceptance criteria.
7. Task dependencies reference valid task identifiers.
8. No requirement or task identifier is duplicated.
9. Previously assigned identifiers remain stable.
10. Previously completed work and verification evidence are preserved.
11. Every technical requirement, when defined, references a valid parent functional requirement.
12. Every technical requirement is addressed by the technical implementation plan and relevant implementation or verification tasks.
13. Business acceptance criteria remain understandable and verifiable without requiring detailed implementation knowledge.
14. Technical implementation decisions are not incorrectly presented as functional requirements.
15. No new top-level functional requirements have been introduced without owner approval.

### Optional Traceability Matrix

A traceability matrix may be included when useful.

Example:

| Requirement | Acceptance Criteria | Technical Requirements | Technical Plan | Implementation Tasks |
|---|---|---|---|---|
| FR-01 | AC-FR-01-01 | — | FR-01 | T-FR-01-01 |
| FR-02 | AC-FR-02-01 | TR-FR-02-01 | FR-02 | T-FR-02-01 |
| FR-02 | AC-FR-02-02 | TR-FR-02-02 | FR-02 | T-FR-02-02 |
| FR-03 | AC-FR-03-01 | — | FR-03 | T-FR-03-01 |

The traceability matrix is supplementary.

The common FR identifier must still appear directly in the corresponding document sections and task identifiers.

---

## 9. Change Management

Requirements may evolve after documentation or implementation has begun.

Changes must be controlled to avoid losing completed work.

### 9.1 Existing Requirement Changes

When an existing functional requirement changes:

1. Identify the modified requirement.
2. Compare the change against the current formal requirement.
3. Identify affected technical requirements.
4. Identify affected technical implementation plans.
5. Identify affected tasks and subtasks.
6. Identify affected acceptance criteria and tests.
7. Determine whether previously completed work remains valid.
8. Document the impact.
9. Request approval for consequential changes.

Do not silently overwrite previously approved decisions.

### 9.2 Identifier Stability

Once assigned, an identifier must not be changed or reused without an explicitly approved migration.

Examples:

- `FR-02` must continue to identify the same functional requirement.
- `TR-FR-02-01` must continue to identify the same technical requirement.
- `T-FR-02-01` must continue to identify the same implementation task.
- `AC-FR-02-01` must continue to identify the same acceptance criterion.

If an item is cancelled or superseded, preserve its identifier and record its status.

### 9.3 Change History

Consequential changes should include:

- Date.
- Affected functional requirement IDs.
- Description of the change.
- Reason for the change.
- Impacted tasks or components.
- Approval status.

---

## 10. Approval Gates

AI agents must distinguish documentation generation from implementation authorization.

### Gate 1: Requirements Approval

The owner reviews the formalized business requirements.

Unresolved business questions must be identified.

### Gate 2: Technical Plan Approval

The owner reviews consequential technical decisions.

Examples include:

- Architecture choices.
- Framework or library changes.
- Sandbox configuration.
- Security boundaries.
- External service dependencies.
- Infrastructure changes.
- Cost-related decisions.

### Gate 3: Implementation Authorization

Implementation begins only after the owner authorizes the relevant tasks or scope of work.

### Gate 4: Verification

Tasks are marked complete only after the required business and technical validation succeeds.

Approval for one task does not automatically authorize unrelated tasks.

---

## 11. AI Agent Execution Rules

These rules apply to Claude Code CLI, Codex CLI, and other AI development agents.

### 11.1 Documentation-Only Requests

When asked to generate or update requirements, plans, or tasks:

**Allowed:**

- Read project documentation.
- Inspect existing source code.
- Analyze dependencies.
- Generate or update the requested documentation.
- Identify technical questions.
- Recommend implementation approaches.

**Not allowed without separate authorization:**

- Modify application source code.
- Install or upgrade dependencies.
- Create or modify runtime environments.
- Execute the application.
- Invoke live LLM services.
- Perform infrastructure changes.
- Commit or push changes to Git.

### 11.2 Implementation Requests

When implementation is explicitly authorized:

1. Read the relevant functional requirement.
2. Read the approved implementation plan.
3. Identify applicable technical requirements.
4. Identify the authorized task IDs.
5. Check dependencies and approval prerequisites.
6. Implement only the authorized work.
7. Perform appropriate business and technical validation.
8. Record verification evidence.
9. Update task status.
10. Summarize changes and results.

### 11.3 Handling Ambiguity

When requirements are incomplete or ambiguous:

- Identify the ambiguity.
- Explain the available interpretations.
- Recommend an approach when appropriate.
- Request clarification for decisions that materially affect business behavior, architecture, security, or cost.

Do not silently invent business requirements.

---

## 12. Migration of Existing Documentation

Some projects may already contain requirements, plans, and tasks created before adoption of this workflow.

For example, the current Coder Crew project contains:

- Existing functional requirement identifiers.
- Acceptance criteria using an earlier numbering convention.
- Implementation phases such as `P-01`.
- Flat task identifiers such as `T-001` through `T-029`.
- Previously completed and verified tasks.

These identifiers must not be automatically renumbered.

### Migration Procedure

Before converting existing documentation:

1. Review the current `requirement-draft.md`.
2. Review the current `requirement.md`.
3. Review the current `plan.md`.
4. Review the current `tasks.md`.
5. Identify differences between owner-defined requirements and agent-generated requirements.
6. Propose a mapping between existing and new identifiers.
7. Identify impacts on task dependencies and completed work.
8. Present the proposed migration to the owner.
9. Obtain approval before modifying existing identifiers.
10. Preserve a searchable mapping between old and new identifiers.

### Migration Example

| Existing Identifier | Proposed Identifier | Description |
|---|---|---|
| T-007 | T-FR-02-01 | Configure agent |
| T-008 | T-FR-02-02 | Configure LLM |
| T-009 | T-FR-02-03 | Configure task |

**This table is illustrative, not an approved migration mapping.**

The actual mapping must be based on reviewing the existing documents.

Previously completed work and verification evidence must be preserved.

---

## 13. Workflow Integration with Claude Code CLI and Codex CLI

This document is the authoritative definition of the development workflow.

It must remain independent of the AI coding tool.

### Claude Code CLI

The project's `CLAUDE.md` may reference this document and instruct Claude to follow it when processing requirements or implementation tasks.

### Codex CLI

The project's `AGENTS.md` may reference this document and instruct Codex to follow the same process.

### Prompt Files

Prompt files such as `prompts/prompt-1.md` should invoke this workflow rather than independently redefining it.

For example:

```text
Read REQUIREMENTS_DRIVEN_DEVELOPMENT_WORKFLOW.md.

Process FR-02 from requirement-draft.md.

Update requirement.md, plan.md, and tasks.md according
to the workflow.

Preserve all unrelated requirements and completed work.

Do not implement application code.

Summarize the documentation changes and identify
any decisions requiring approval.
```

### Instruction Precedence

The documents serve different purposes:

| Document | Authority |
|---|---|
| `REQUIREMENTS_DRIVEN_DEVELOPMENT_WORKFLOW.md` | Development process and traceability rules |
| `requirement-draft.md` | Owner-provided business intent |
| `requirement.md` | Approved functional requirements |
| `plan.md` | Approved technical implementation approach |
| `tasks.md` | Implementation tasks, status, and verification evidence |
| `AGENTS.md` | Codex-specific project guidance |
| `CLAUDE.md` | Claude-specific project guidance |
| `prompts/prompt-1.md` | Instructions for a specific workflow operation |

If these documents contain conflicting instructions, the agent must identify the conflict and request clarification rather than silently overriding approved requirements.

---

## 14. Completion and Reporting

After processing a functional requirement, the AI agent must provide a concise report.

The report should include:

1. Functional requirement IDs processed.
2. Documents updated.
3. Functional requirements and acceptance criteria created or modified.
4. Technical requirements created or modified, when applicable.
5. Technical plan sections updated.
6. Tasks and subtasks created or modified.
7. Existing work preserved.
8. Traceability validation results.
9. Outstanding questions and approval requirements.
10. Implementation status.

Documentation generation must not be reported as completed implementation.

A requirement is considered implemented only when its approved implementation tasks and required acceptance criteria have been successfully verified.

---

## 15. Fundamental Workflow Rule

**Every functional requirement must remain traceable from its original business intent through formal requirements, technical planning, implementation tasks, and verification.**

The functional requirement ID is the common identifier connecting these artifacts.

Functional requirements and business acceptance criteria must remain understandable and verifiable by business stakeholders.

Technical requirements are optional and should generally be documented in the technical implementation plan under their corresponding functional requirement.

New requirements must be incorporated incrementally without unnecessarily modifying existing requirements or losing completed work.

AI coding agents must follow this process consistently, regardless of the development tool used.
