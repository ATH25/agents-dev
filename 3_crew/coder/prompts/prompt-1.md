
# Prompt 1: Requirements, Technical Planning, and Task Generation

## 1. Intent and Objective

We are establishing a structured, requirements-driven software
development process for the CrewAI Coding Agent project.

The objective is to progressively transform business requirements
into formal specifications, technical implementation plans, and
actionable development tasks.

The development process consists of six stages:

1. Business Requirements
2. Refined Functional Requirements
3. Technical Planning
4. Task Breakdown
5. Implementation
6. Validation and Testing

The first four stages are documentation and planning activities.

Implementation will be performed later using agentic coding tools
such as Codex, Claude Code, or Antigravity.

Validation and testing will be performed after implementation.

IMPORTANT:
For this assignment, perform ONLY stages 2, 3, and 4.
Do not implement or modify application source code.

---

## 2. Source of Requirements

The primary source of business requirements is:

`../requirement-draft.md`

This document contains business requirements provided by the
project owner.

Business requirements will be introduced incrementally, potentially
one requirement at a time.

Your responsibility is to refine these requirements without
changing their original intent.

You may identify ambiguities, missing details, dependencies,
or potential improvements.

However:

- Do not introduce new business requirements without approval.
- Do not assume unspecified functionality is required.
- Do not change the original business intent.
- Clearly identify assumptions and open questions.
- Preserve previously approved requirements.
- Maintain consistent requirement identifiers.

The generated documents must remain synchronized as new
requirements are introduced.

---

## 3. Documentation Workflow

The documentation workflow is:

requirement-draft.md → requirement.md → plan.md → tasks.md → Implementation → Validation & Testing

Each document serves a distinct purpose.


### requirement-draft.md

Contains the original business requirements.

Focuses primarily on WHAT the application should accomplish.

This file is maintained by the project owner.

Do not modify this file.

### requirement.md

Contains refined, structured, and testable requirements.

Defines WHAT must be delivered.

Includes functional requirements, supporting details,
constraints, and acceptance criteria.

Avoid unnecessary implementation details.

### plan.md

Contains the technical implementation strategy.

Defines HOW the requirements will be implemented.

Includes architecture, technical approach, dependencies,
implementation phases, and validation strategy.

### tasks.md

Contains the actionable implementation checklist.

Defines the specific activities required to execute the plan.

Every task should be traceable to a requirement and a
corresponding implementation phase.

---

# TASK 1: Generate requirement.md

## Objective

Read `../requirement-draft.md` and generate a formal,
well-structured `requirement.md`.

If `../requirement.md` already exists, review its contents
and update it rather than blindly overwriting it.

## Instructions

1. Read and understand the business requirements.
2. Identify the application's objective and scope.
3. Convert business requirements into formal functional requirements.
4. Assign unique identifiers such as FR-01, FR-02, etc.
5. Preserve the original intent of each requirement.
6. Group related requirements logically.
7. Define measurable acceptance criteria.
8. Identify relevant constraints and dependencies.
9. Identify ambiguities and open questions.
10. Distinguish approved requirements from recommendations.

## Required Document Structure

### 1. Project Overview

Describe:

- Project name
- Business objective
- Application purpose
- High-level scope

### 2. Functional Requirements

Create a table with the following columns:

| ID | Requirement | Description | Status |
|----|-------------|-------------|--------|

Use consistent requirement identifiers.

For the current CrewAI Coding Agent project:

FR-01 — CrewAI Framework

The project scaffold has already been generated using:

`crewai create crew coder`

Mark FR-01 as completed.

Other requirements should remain pending until their
implementation has been verified.

### 3. Detailed Requirements

Provide additional details for requirements that need
further explanation.

For example:

- Agent definitions
- Task definitions
- LLM configuration
- Input requirements
- Output requirements
- Crew configuration

Only include requirements supported by the business draft.

### 4. Acceptance Criteria

Create a table:

| AC ID | Requirement ID | Acceptance Criterion |
|-------|----------------|----------------------|

Acceptance criteria must be:

- Clear
- Specific
- Testable
- Traceable to requirements

### 5. Constraints and Dependencies

Document known constraints and dependencies.

Do not invent constraints that have not been approved.

### 6. Assumptions and Open Questions

Document ambiguities requiring clarification.

Do not silently convert assumptions into requirements.

## Deliverable

Create or update:

`../requirement.md`

---

# TASK 2: Generate plan.md

## Objective

Generate a technical implementation plan based on the
approved requirements in `../requirement.md`.

The plan must explain HOW each requirement will be implemented.

## Instructions

1. Read `../requirement.md`.
2. Review the existing project structure and relevant source files.
3. Identify functionality already implemented.
4. Identify functionality requiring implementation or modification.
5. Define the proposed technical architecture.
6. Identify components, configuration files, and dependencies.
7. Organize implementation into logical phases.
8. Define the technical approach for each phase.
9. Identify risks and technical considerations.
10. Define the validation strategy.

Do not modify application source code.

## Required Document Structure

### 1. Technical Overview

Summarize the technical objective and proposed solution.

### 2. Current State Assessment

Identify:

- Existing project scaffold
- Existing components
- Existing configuration
- Reusable functionality
- Missing functionality

Clearly distinguish between:

- Already implemented
- Partially implemented
- Not implemented
- Not yet verified

### 3. Proposed Architecture

Describe the major components and their interactions.

Use Mermaid diagrams when they improve clarity.

### 4. Technical Approach

Describe how the approved requirements will be implemented.

Include relevant:

- Frameworks
- Configuration files
- Components
- Integration points
- Execution workflows
- Dependencies

### 5. Implementation Phases

Organize the implementation into logical phases.

For each phase, document:

- Phase identifier
- Objective
- Related requirement IDs
- Technical activities
- Dependencies
- Expected deliverables

### 6. Technical Dependencies

Identify required libraries, frameworks, services,
runtime environments, and configuration dependencies.

### 7. Risks and Considerations

Identify relevant implementation risks.

Recommendations must be clearly distinguished from
approved requirements.

### 8. Validation Strategy

Describe how the implementation will be validated
against the acceptance criteria in `../requirement.md`.

## Deliverable

Create or update:

`plan.md`

---

# TASK 3: Generate tasks.md

## Objective

Generate an actionable implementation checklist based on
`plan.md` and `../requirement.md`.

The task list will be used by AI coding agents during
the implementation phase.

## Instructions

1. Read `../requirement.md`.
2. Read `plan.md`.
3. Identify all implementation phases.
4. Break each phase into actionable development tasks.
5. Assign unique task identifiers.
6. Associate tasks with requirement IDs.
7. Preserve dependencies and implementation order.
8. Include validation tasks where appropriate.
9. Use Markdown checkboxes.
10. Do not mark tasks complete unless completion is verified.

## Required Document Structure

Organize tasks by implementation phase.

Example:

### Phase 1 — Project Setup

- [x] T-001: Generate CrewAI project scaffold.
      Requirement: FR-01

### Phase 2 — Agent Configuration

- [ ] T-002: Configure coding agent.
      Requirement: FR-02

- [ ] T-003: Configure LLM.
      Requirement: FR-04

### Phase 3 — Task Configuration

- [ ] T-004: Configure coding task.
      Requirement: FR-03

The examples above illustrate the required format.
Generate the actual tasks from the approved requirements
and technical plan.

## Task Requirements

Each task must be:

- Specific
- Actionable
- Independently verifiable
- Appropriately scoped for an AI coding agent
- Traceable to one or more functional requirements
- Associated with an implementation phase

Avoid vague tasks such as:

"Implement the application."

Instead, define the specific implementation activity.

## Task Completion Rules

Use:

- [ ] Not completed
- [x] Completed and verified

IMPORTANT:

The CrewAI project scaffold has already been generated.

Therefore, the corresponding scaffold-generation task
may be marked complete.

Do not mark agent configuration, task configuration,
LLM configuration, or other implementation activities
complete without verifying their actual implementation.

## Deliverable

Create or update:

`tasks.md`

---

## 4. Traceability Requirements

Maintain traceability across all documents.

The relationship must be:

Business Requirement
        |
        v
Functional Requirement (FR)
        |
        v
Acceptance Criterion (AC)
        |
        v
Technical Implementation Phase
        |
        v
Implementation Task (T)
        |
        v
Validation

Every functional requirement should have:

1. A unique identifier.
2. One or more acceptance criteria.
3. A corresponding implementation approach.
4. One or more implementation or verification tasks.

If a requirement is already implemented, create
verification tasks where appropriate.

Do not generate unnecessary implementation tasks
for functionality already confirmed complete.

---

## 5. Documentation Standards

Follow these standards:

1. Use Markdown formatting.
2. Use consistent headings.
3. Use tables where they improve readability.
4. Use stable requirement and task identifiers.
5. Maintain traceability between documents.
6. Avoid duplicating requirements unnecessarily.
7. Keep business requirements separate from technical design.
8. Clearly identify assumptions and recommendations.
9. Preserve previously approved requirements.
10. Do not modify `../requirement-draft.md`.

If example requirement, plan, or task documents exist
elsewhere in the project, they may be used as structural
references only.

Do not copy unrelated business requirements.

---

## 6. Execution Instructions

Execute the documentation tasks sequentially:

1. Generate or update `../requirement.md`.
2. Generate or update `plan.md`.
3. Generate or update `tasks.md`.

Before generating each downstream document, read the
latest version of its upstream documents.

Do not modify application source code.

Do not install dependencies.

Do not execute the CrewAI application.

Do not perform implementation or testing at this stage.

---

## 7. Expected Final Output

At the end of this assignment, the project should contain:

1. `../requirement.md`
   - Refined functional requirements
   - Acceptance criteria
   - Constraints and dependencies
   - Assumptions and open questions

2. `plan.md`
   - Current state assessment
   - Proposed architecture
   - Technical implementation approach
   - Implementation phases
   - Dependencies
   - Validation strategy

3. `tasks.md`
   - Actionable implementation checklist
   - Requirement traceability
   - Implementation phases
   - Verified completion status

After creating the documents, provide a concise summary
of the work completed.

List any ambiguities or decisions requiring approval.

Do not begin application implementation.