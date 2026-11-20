# CyberHub — Software Architecture Planning

We are now moving to the architecture planning stage of CyberHub.

Your task is to help me design the overall software architecture before we begin implementation.

You have already created the initial Claude Code configuration, including:
- `CLAUDE.md`
- Custom agents.
- Custom skills.

Use these resources when appropriate. In particular, use the architecture agent and relevant CyberHub component skills when they provide value.

Do not unnecessarily load every skill or invoke every agent.

# 1. Your Objective

I want to establish a complete architectural foundation for CyberHub.

We need to understand how the application will work internally, how its components will communicate, how information will be stored, and how the different technologies will fit together.

I do not want to start coding before we understand the architecture.

# 2. Project Requirements

Use the following five components as the foundation:

**AIM — AI Mentor**
- AI-powered educational assistant.
- Uses Ollama for local AI.
- Accesses educational PDFs, transcripts, NTT folders and notes.
- Can retrieve PTM information through `/ptm`.
- Supports `/exlit` and future custom commands.

**QEF — Quiz Exam Forge**
- Generates quizzes from selected NTT folders and notes.
- Supports different question types and difficulty levels.
- Records quiz results.
- Sends relevant progress information to PTM.

**NTT — Note Taker**
- Markdown-only note storage.
- Folder-based organization.
- Code and Preview editor tabs.
- Preview mode when opening existing notes.
- Creation dates displayed under note names.
- Accessible by AIM and QEF.

**CLV — Command Library Vault**
- Main tabs for Python, Linux, Networking, Windows, Cybersecurity, etc.
- Nested categories.
- Searchable commands with explanations and examples.

**PTM — Progress Tracking Manager**
- Records created notes.
- Records completed quizzes.
- Tracks total questions, correct answers and incorrect answers.
- Maintains educational progress and statistics.
- Provides information to AIM when `/ptm` is requested.

# 3. Preferred Technology Stack

My current preferences:

- Python
- Django
- HTML
- CSS
- Bootstrap
- SQLite initially
- PostgreSQL potentially later
- Ollama (llama3.1:8b)
- LangChain if necessary
- Docker
- Git and GitHub

Evaluate these technologies and explain whether they are appropriate.

Do not introduce additional frameworks or technologies without explaining why they are necessary.

# 4. Architecture Areas to Investigate

I want you to investigate and propose an architecture covering the following areas.

## A. Overall Application Architecture

- What architectural approach should CyberHub use?
- How should Django be organized?
- Should each component have its own Django app?
- How should shared functionality be organized?
- How should components communicate?
- How can we avoid tightly coupling the components?

Consider whether a modular monolith is appropriate initially.

## B. Project Structure

Propose a logical directory structure.

Consider:
- Django applications.
- Templates.
- Static files.
- Media and uploaded educational files.
- Markdown notes.
- AI-related functionality.
- Shared utilities.
- Tests.
- Configuration.
- Documentation.

Explain the responsibility of each major directory.

Do not create the directories or files yet.

## C. Database Architecture

Design the initial database structure.

Consider the data required by all five components.

Explain:
- Main database entities.
- Relationships between entities.
- Foreign keys.
- How notes and folders are represented.
- How quizzes and questions are represented.
- How quiz attempts and answers are recorded.
- How progress statistics are maintained.
- How command categories and commands are represented.

Provide an ER diagram using Mermaid if useful.

Explain the database design in beginner-friendly language.

## D. Component Integration

Design how the five components communicate.

Pay particular attention to:

- NTT → QEF
- NTT → AIM
- QEF → PTM
- NTT → PTM
- PTM → AIM

Explain how information should be accessed without unnecessarily duplicating data.

Consider whether shared services, APIs, Django models, or another approach would be appropriate.

## E. AIM and Local AI Architecture

This is an important part of CyberHub.

Investigate how Django should communicate with Ollama.

Consider:
- Local LLM integration.
- Conversation history.
- Educational document processing.
- PDF extraction.
- Accessing NTT Markdown notes.
- Retrieving relevant information from selected folders.
- RAG, embeddings and vector databases if necessary.
- How AIM retrieves PTM statistics through `/ptm`.
- How secret commands such as `/exlit` should be processed.

Do not automatically introduce LangChain or a vector database. Explain when they would actually become useful.

## F. NTT Architecture

Explain how to implement the Markdown note system.

Consider:
- Markdown file storage versus database storage.
- Folder representation.
- Code editor and Preview functionality.
- Markdown rendering.
- Image and attachment handling.
- Creation dates.
- How AIM and QEF can access note content.

Discuss the advantages and disadvantages of the available approaches.

## G. Security Architecture

Consider:
- Authentication.
- Authorization.
- File upload security.
- PDF processing security.
- Markdown rendering and XSS prevention.
- Local AI security.
- Database protection.
- Secrets and environment variables.
- Backup and recovery.

Recommend appropriate beginner-friendly security practices.

## H. Testing and Maintenance

Explain how we should approach:
- Unit testing.
- Integration testing.
- Component testing.
- Database migrations.
- Error handling.
- Logging.
- Code quality.
- Future maintenance.

# 5. Development Roadmap

After proposing the architecture, recommend a gradual implementation roadmap.

I want to develop CyberHub throughout my education, so the application should grow as my knowledge improves.

Organize development into logical phases.

For each phase, explain:
- What we will build.
- Which components are involved.
- What technologies we will learn.
- What functionality will become available.
- What must be completed before moving forward.

Identify a reasonable MVP.

Do not assume all five components need to be implemented immediately.

# 6. How to Present Your Work

I want a structured architecture proposal.

Use the following order:

1. Architecture overview.
2. Recommended architectural approach.
3. Technology stack evaluation.
4. Proposed project structure.
5. Database design.
6. Component integration.
7. AI architecture.
8. Security architecture.
9. Testing strategy.
10. Development roadmap.
11. Important architectural decisions.
12. Open questions and decisions requiring my input.

For every major recommendation:
- Explain what it is.
- Explain why you recommend it.
- Mention relevant alternatives.
- Explain advantages and disadvantages.
- Use beginner-friendly language.

Use diagrams where they genuinely improve understanding.

Do not overcomplicate the architecture.

# 7. Important Rules

**This is an architecture planning task, NOT an implementation task.**

You are allowed to:
- Read project files.
- Inspect existing configurations.
- Analyze existing documentation.
- Research current official technical documentation.
- Use relevant agents and skills.
- Produce architectural proposals in your response.

You are NOT allowed to:
- Create project files.
- Create directories.
- Write or edit documentation.
- Modify configurations.
- Install packages.
- Run commands that modify the environment.
- Create database migrations.
- Start implementation.

You must ask for my explicit permission before any modification.

If you believe additional information is necessary, ask me focused questions.

Do not silently make important architectural decisions on my behalf.

# 8. Final Instruction

Start by reviewing the existing CyberHub configuration and project context.

Then begin the architecture analysis.

I want you to act as a software architect and technical advisor, but remember that I am a beginner and want to understand the decisions being made.

**Your objective is to help me establish a solid, understandable architecture that we can approve before writing the first line of application code.**