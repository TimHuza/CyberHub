# CyberHub — Claude Code Project Configuration Setup

You are responsible for designing the Claude Code configuration system for my project, **CyberHub**.

Your task is to analyze the project, understand its purpose, and independently design a suitable configuration consisting of:

- `CLAUDE.md`
- Custom Agents
- Custom Skills

You should make thoughtful decisions about what agents and skills are necessary. I do not want unnecessary configurations or excessive complexity.

**IMPORTANT: You must follow all instructions below.**

---

# 1. Project Context

CyberHub is my personal web application designed to support my 1.5-year Cybersecurity + AI education at IT Step Academy.

Its purpose is to help me:
- Understand difficult technical concepts.
- Organize educational materials.
- Prepare for examinations.
- Document what I learn.
- Store useful commands and technical references.
- Track my educational progress.

CyberHub is a long-term project that will evolve alongside my education.

## Initial Components

| Abbreviation | Component | Purpose |
|---|---|---|
| AIM | AI Mentor | AI-powered learning assistant. |
| QEF | Quiz Exam Forge | Quiz and examination preparation. |
| NTT | Note Taker | Markdown-based note management. |
| CLV | Command Library Vault | Searchable technical command library. |
| PTM | Progress Tracking Manager | Educational progress tracking. |

These components will be developed gradually.

## Preferred Technology Stack

- Programming Language: Python
- Backend: Django
- Frontend: HTML, CSS, Bootstrap
- Database: SQLite initially, potentially PostgreSQL later.
- AI: Ollama (local LLMs).
- AI Framework: LangChain (optional).
- Containerization: Docker.
- Version Control: Git and GitHub.

These are preferences, not final architectural decisions. Do not assume every technology must be implemented immediately.

## ADDITIONAL PROJECT REQUIREMENTS — COMPONENT FUNCTIONALITY

The following requirements describe the intended functionality and relationships between CyberHub components.

Use this information when designing `CLAUDE.md`, custom agents, and custom skills.

These are current project requirements and design intentions, not permission to begin implementation. Some technical details remain open for architectural discussion.

---

## 1. NTT — Note Taker

NTT is a Markdown-based note management system.

### Markdown Editor

The note editor must have two tabs:

- **Code:** Write and edit notes using Markdown (`.md`).
- **Preview:** See the rendered Markdown.

Similar how you make Pull Requests or Issues on GitHub.

### Notes and Folders

- Notes must be organized into folders.
- Users can create and manage folders.
- Opening an existing note should display it in Preview mode by default.
- An Edit button should open the editing interface with Code and Preview tabs.
- Notes should display their creation date underneath their names.
- Notes should support technical content, code blocks, tables, images, and other standard Markdown elements.

### Integration with Other Components

NTT is an important source of educational information for other CyberHub components.

- QEF should be able to access NTT folders and their notes to generate quizzes.
- AIM should be able to access NTT folders and individual notes to answer questions and explain educational material.

---

## 2. QEF — Quiz Exam Forge

QEF generates quizzes to help prepare for examinations and test my knowledge.

### Educational Sources

QEF should be able to generate quizzes using:

- Educational materials stored in NTT.
- Individual Markdown notes.
- Entire NTT folders.
- Other supported educational files when appropriate.

### Important Integration

QEF must be able to use NTT folders and notes as a source of information.

For example:

1. I open QEF.
2. I select an NTT folder containing networking notes (Optional because QEF can generate quizes without NTT notes).
3. QEF analyzes the selected notes.
4. QEF generates a quiz based on that material.

The architecture should account for selecting individual notes or entire folders.

QEF should also track quiz results and provide information that PTM can record.

---

## 3. CLV — Command Library Vault

CLV is a searchable library for technical commands and references.

### Main Tabs

Commands should be organized into separate main tabs, such as:

- Python
- Linux
- Networking
- Windows
- Cybersecurity
- Other categories as needed.

These are initial examples, not a fixed list.

### Nested Categories

Each main tab should contain smaller categories to organize commands.

Example:

```text
Networking
├── Connectivity & Path Testing
│   ├── Command 1
│   ├── Command 2
│   └── ...
│
└── Interface
    ├── Command 1
    ├── Command 2
    └── ...

Python
├── File Handling
├── Lists
├── Dictionaries
└── ...
```

Each command should support relevant information such as:

- Command name.
- Description.
- Explanation of parameters.
- Usage examples.
- Additional personal notes.

The structure should be flexible enough to support additional main tabs and nested categories in the future.

---

## 4. AIM — AI Mentor

AIM is the central AI-powered learning assistant in CyberHub.

It should be able to retrieve and use information from multiple educational sources.

### Knowledge Sources

AIM should have access to:

**1. Educational Files**
- School transcripts.
- PDF documents.
- Other supported educational materials.

**2. NTT**
- NTT folders.
- Individual Markdown notes.

**3. PTM**
- Educational progress information.
- Quiz statistics.
- Learning activity and other recorded progress.

### PTM Access Restriction

AIM should not automatically retrieve PTM statistics during every conversation.

Instead, the user must explicitly request progress information through the `/ptm` command.

For example:

```text
/ptm How is my networking progress?
```

AIM should then retrieve the relevant PTM information and answer the question.

### Secret Chat Commands

AIM should support special commands that change how it processes a request.

Initial commands:

**1. `/exlit [prompt]`**

Explains a subject as if explaining it to a 12-year-old beginner.

Requirements:
- Very simple language.
- Avoid unnecessary technical terminology.
- Use relatable analogies.
- Explain difficult concepts step by step.
- Assume little or no previous knowledge.

Example:

```text
/exlit What is Active Directory?
```

**2. `/ptm [prompt]`**

Retrieves educational progress information from PTM.

Examples:

```text
/ptm Show my overall progress.
```

```text
/ptm How many quizzes have I completed?
```

```text
/ptm What topics should I revise?
```

More secret commands will be introduced later.

Design the command system so additional commands can be added without unnecessarily modifying the entire AIM architecture.

---

## 5. PTM — Progress Tracking Manager

PTM is responsible for recording and managing educational progress throughout my education.

It should collect activity information from other CyberHub components.

### Progress Information

Initially, PTM should track:

**NTT**
- Number of notes created.
- Other relevant note activity when appropriate.

**QEF**
- Number of total quizes.
- Number of quizzes completed.
- Total questions answered.
- Number of correct answers.
- Number of incorrect answers.
- Quiz results and performance history.

**General Learning Progress**
- Overall educational activity.
- Progress over time.
- Learning statistics.
- Areas that require additional studying.

PTM should maintain structured records so that information can be retrieved by AIM when requested.

The system should be designed to accommodate additional progress metrics in the future.

---

# 6. COMPONENT RELATIONSHIPS AND INTEGRATIONS

An important architectural requirement is that CyberHub's components must be able to communicate and exchange relevant information.

The following relationships should be considered when designing the architecture:

| Source | Destination | Purpose |
|---|---|---|
| NTT | QEF | Generate quizzes using notes and folders. |
| NTT | AIM | Answer questions using personal notes. |
| Educational Files | AIM | Answer questions using school materials. |
| QEF | PTM | Record quiz results and statistics. |
| NTT | PTM | Record note creation and related activity. |
| PTM | AIM | Provide progress information when `/ptm` is used. |

### Architectural Considerations

- Avoid unnecessary duplication of educational data.
- Establish clear responsibilities for each component.
- Design appropriate interfaces between components.
- Consider how components can access shared information securely.
- Avoid tightly coupling components together.
- Consider how future components and integrations can be introduced.
- AIM should only retrieve PTM information when explicitly requested through `/ptm`.

These relationships should influence architecture planning, agent responsibilities, and relevant skills.

Do not assume a particular implementation approach before evaluating the architecture.

---

# 7. Instructions for Designing Agents and Skills

When designing the Claude Code configuration:

1. Consider the responsibilities of all five components.
2. Identify which agents need specialized knowledge of particular components.
3. Identify which skills should contain reusable component-specific development guidelines.
4. Ensure agents understand relevant component integrations.
5. Avoid duplicating the entire project description in every agent.
6. Keep component-specific knowledge in the most appropriate locations.
7. Ensure future functionality can be introduced without redesigning the entire configuration system.

**Important:** These requirements describe the intended application. They do not authorize implementation or modification of project files.

You must still follow the permission and approval requirements defined in the main prompt.

---

# 2. Your Responsibilities

You must independently determine how Claude Code should be organized to support CyberHub development.

I want you to design three configuration layers.

## A. CLAUDE.md

Create a concise project-level instruction file.

It should explain:

- What CyberHub is.
- Project goals and philosophy.
- Preferred technology stack.
- Development principles.
- Code quality expectations.
- Security expectations.
- Architectural principles.
- How to work with me.
- Permission and approval requirements.
- Token efficiency requirements.

Keep this file relatively short.

Do not duplicate extensive documentation that belongs in individual skills.

## B. Custom Agents

Determine which specialized agents would genuinely benefit CyberHub.

Potential responsibilities could include:

- Software architecture.
- Django development.
- Python code review.
- Security reviews.
- Database design.
- AI and local LLM integration.
- Testing and debugging.

These are examples, not mandatory agents.

You should decide:
- Which agents are actually necessary.
- What each agent is responsible for.
- When each agent should be used.
- What tools and permissions each agent needs.
- How agents should communicate their findings.

Avoid creating multiple agents with overlapping responsibilities.

Prefer focused agents over agents that attempt to do everything.

## C. Custom Skills

Determine which reusable skills would help Claude work effectively on CyberHub.

Potential responsibilities could include:

- Django development conventions.
- Python coding standards.
- Database design guidelines.
- Security best practices.
- Code review procedures.
- Testing procedures.
- Project documentation standards.
- Architecture planning.

Again, these are examples, not mandatory skills.

Each skill should have a clear purpose and should be loaded only when relevant.

Avoid creating skills that simply repeat the contents of `CLAUDE.md` or duplicate other skills.

---

# 3. CRITICAL: Permission and Approval System

This is one of the most important requirements.

**You MUST ask for my explicit permission before making any changes to the project.**

This includes:

- Creating files.
- Writing content into files.
- Editing existing files.
- Deleting files.
- Renaming files.
- Moving files.
- Overwriting existing content.
- Modifying configurations.
- Installing packages or dependencies.
- Running commands that modify the project or its environment.

Reading files, listing directories, and inspecting the project are allowed without permission, provided these actions do not modify anything.

## Permission Rules

Before performing any modification:

1. Explain exactly what you want to change.
2. Identify the affected files.
3. Explain why the modification is necessary.
4. Ask for my permission.
5. Wait for my explicit approval.

Do not interpret silence, previous approval, or general project instructions as permission.

### Important distinctions

- Approval to create a file does not automatically authorize editing other files.
- Approval to edit one file does not authorize editing another.
- Approval to create a directory does not authorize creating all files inside it.
- Approval to edit does not authorize deleting.
- Approval to delete requires separate, explicit permission.
- Never silently overwrite existing content.

**Deletion requires especially careful handling.**

Before deleting anything, explain what will be deleted and why. Wait for my explicit approval for that specific deletion.

If you are uncertain whether an action modifies something, ask first.

These rules apply even when you believe a change is necessary or would improve the project.

---

# 4. Token Efficiency

I want you to be intelligent and economical with token usage.

Do not waste tokens unnecessarily.

Follow these principles:

### Context Management

- Read only files relevant to the current task.
- Do not repeatedly read the same files unless necessary.
- Avoid loading the entire repository when a smaller inspection is sufficient.
- Do not repeatedly summarize information already available in context.
- Use existing project documentation instead of rediscovering information.

### Agent Usage

- Do not invoke agents for simple tasks that you can handle yourself.
- Use specialized agents only when their expertise provides meaningful value.
- Avoid running multiple agents on the same task.
- Do not use agents just to make the workflow look sophisticated.

### Skill Usage

- Load skills only when relevant.
- Avoid unnecessary skill activation.
- Keep skill instructions focused and concise.
- Avoid repeating instructions across multiple configuration files.

### Responses

- Be direct and concise.
- Avoid unnecessary introductions and conclusions.
- Do not provide lengthy explanations when a short one is sufficient.
- Explain technical decisions when they matter.
- Ask focused questions rather than producing long lists of questions.

### General Principle

Use the smallest amount of context, tools, and tokens necessary to complete a task properly.

However, **token efficiency must never come at the expense of correctness, security, or my approval requirements.**

---

# 5. How I Want You to Work With Me

I am still learning software development.

I want to understand the technologies, architecture, and code used in CyberHub.

Therefore:

- Explain important technical decisions in beginner-friendly language.
- Do not unnecessarily introduce advanced technologies.
- Prefer straightforward and maintainable solutions.
- Explain why a particular approach is recommended.
- Do not assume I understand advanced programming concepts.
- Help me learn rather than simply producing finished implementations.

I want you to act as a technical partner, not an autonomous developer who makes every decision without consulting me.

---

# 6. Initial Task — Analyze and Design the Configuration

For now, your task is ONLY to analyze and plan.

Follow these phases:

## Phase 1 — Project Inspection

Inspect the existing CyberHub repository.

Understand:
- Existing directory structure.
- Existing documentation.
- Existing Claude Code configurations.
- Existing development decisions.
- Any conventions already established.

Do not modify anything.

If the repository is empty or some information is unavailable, work with the information provided in this prompt.

Do not invent existing project decisions.

## Phase 2 — Configuration Design

Design the proposed configuration system.

Determine:

1. What should go into `CLAUDE.md`.
2. Which custom agents should be created.
3. Which custom skills should be created.
4. How agents and skills should work together.
5. How to avoid duplicated instructions.
6. How to keep token consumption low.
7. How to enforce the permission system.

Follow Claude Code's current official documentation and supported configuration conventions when determining file formats and locations.

Do not assume outdated configuration formats.

## Phase 3 — Present Your Proposal

Before creating anything, present your proposed configuration.

Include:

- Proposed `CLAUDE.md` contents or outline.
- Proposed agents and their responsibilities.
- Proposed skills and their responsibilities.
- Proposed directory locations.
- How the configurations will interact.
- How token efficiency will be maintained.
- How the permission system will work.

Explain the reasoning behind your decisions.

Keep the proposal understandable and avoid unnecessary complexity.

## Phase 4 — Request Permission

After presenting your proposal, STOP.

Ask me whether I approve the proposed configuration.

**Do not create, write, edit, or delete any files until I explicitly approve.**

After I approve, proceed only with the specific changes I authorized.

If additional changes become necessary, ask for permission again.

---

# 7. Final Principles

Remember these priorities:

1. My approval and control over project modifications.
2. Security and correctness.
3. Simplicity and maintainability.
4. Token efficiency.
5. Learning and understanding.
6. Avoiding unnecessary complexity.

I want a carefully designed Claude Code environment that will support CyberHub throughout its development.

Do not overengineer it.

**Start with Phase 1: inspect the project and then present your proposed configuration. Do not implement anything yet.**