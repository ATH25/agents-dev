
Read @requirement.md and @plan.md completely.

Create @tasks.md from plan.md, using requirement.md as the authoritative reference whenever you need additional detail or need to verify that nothing was dropped.

Requirements for tasks.md:

- Use checklist format for every executable task: `- [ ]`
- Organize the checklist by the implementation phases in plan.md.
- Make every task execution-ready and specific enough that another coding agent can implement it without guessing.
- Preserve all relevant implementation details from plan.md and requirement.md, including file names, class/function names, YAML keys, environment variables, tools, APIs, inputs, outputs, configuration values, validation rules, constraints, and acceptance criteria where applicable.
- Do not duplicate large sections of requirement.md or plan.md unnecessarily; reference them where appropriate while still giving each task enough detail to execute.
- Do not invent new requirements or architecture.
- If plan.md and requirement.md conflict, requirement.md is authoritative.
- If you discover a material gap or contradiction that prevents producing accurate tasks.md, stop and report it instead of guessing.
- Include implementation tasks, validation tasks, and a final checklist covering the acceptance criteria.
- Do not modify requirement.md or plan.md.
- Do not implement any code yet.

Only create tasks.md.