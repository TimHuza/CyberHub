# Create Git Commit & Push Agent and Skill

I want you to create a dedicated Claude Code agent and skill for managing Git commits and pushing changes to GitHub.

The functionality will be triggered through the following custom command:

`/gt-msg`

## 1. Main Purpose

When I execute `/gt-msg`, the workflow should:

1. Analyze the changes made in the current Git repository.
2. Generate a clear, professional commit message based on the actual changes.
3. Present the proposed commit message to me.
4. Show a short summary of the files and changes being committed.
5. Ask for my explicit approval.
6. After approval, create the Git commit and push it to the appropriate GitHub remote and branch.

## 2. Git Repository Awareness

The agent must understand the current Git environment before generating a commit.

It should identify:

- Current repository name.
- GitHub repository URL.
- Current branch.
- Configured remote (usually `origin`).
- Current commit hash.
- Latest Git tag/version.
- Uncommitted changes.
- Staged and unstaged files.

It must never assume which repository or branch I am working on.

Always inspect the actual Git information.

### Branch Awareness

- Detect the currently checked-out branch.
- Push to the corresponding remote branch.
- Never switch branches automatically.
- Never push to a different branch without my permission.
- If the branch has no upstream, explain the situation and ask how to proceed.

### Version and Tag Awareness

- Identify the latest existing version tag.
- Understand the relationship between the current branch, commits, and tags.
- Include relevant version information in the commit summary.
- Never create, modify, or delete tags automatically.
- Do not assume that every commit requires a new version.

If a release or version tag might be appropriate, suggest it separately.

## 3. Commit Message Generation

Generate commit messages based on the actual changes.

Follow conventional commit formatting where appropriate.

Examples:

- `feat: add Markdown preview to note editor`
- `fix: correct quiz scoring calculation`
- `docs: update CyberHub architecture documentation`
- `refactor: improve Django app structure`
- `chore: update project dependencies`

The message must accurately describe the changes.

Do not invent functionality or include changes that are not present.

## 4. Approval Workflow

**My approval is mandatory before committing and pushing.**

Before asking for approval, show:

- Repository name.
- Current branch.
- GitHub remote.
- Latest version tag.
- Files that will be committed.
- Short description of the changes.
- Proposed commit message.

Then ask:

"Do you approve creating this commit and pushing it to GitHub?"

### If I approve:

1. Commit the approved changes.
2. Push the commit to the detected remote and current branch.
3. Verify that the push succeeded.
4. Report the resulting commit hash and destination.

### If I reject:

- Do not commit.
- Do not push.
- Wait for my next instructions.

If the repository state changes after approval, inspect it again and request approval for the updated changes.

## 5. Important Safety Rules

- Never use `git add .` blindly.
- Never automatically include unrelated files.
- Never commit secrets, credentials, API keys, `.env` files, or sensitive data.
- Inspect staged and unstaged changes before committing.
- Never amend previous commits automatically.
- Never force push.
- Never delete branches or tags.
- Never change branches automatically.
- Never overwrite Git history.
- Never push without explicit approval.
- If there are merge conflicts or unexpected Git states, stop and explain the problem.

If there are no changes to commit, inform me instead of creating an empty commit.

## 6. Token Efficiency

- Keep Git inspection focused.
- Avoid reading unrelated project files.
- Use Git commands to inspect changes rather than loading entire files unnecessarily.
- Generate concise commit messages.
- Avoid unnecessary agent invocations.
- Do not repeat repository information unnecessarily.

## 7. Agent and Skill Design

Create:

**Agent:** A specialized Git Commit & Push Agent.

Responsibilities:
- Git repository inspection.
- Change analysis.
- Commit message generation.
- Branch and remote awareness.
- Version/tag awareness.
- Safe commit and push workflow.

**Skill:** A reusable Git workflow skill.

Responsibilities:
- Define the `/gt-msg` workflow.
- Explain commit message conventions.
- Define Git inspection procedures.
- Enforce approval requirements.
- Document safe commit and push practices.

The `/gt-msg` command should activate the appropriate workflow and agent.

Use the current official Claude Code documentation to determine the correct configuration format and locations.

Avoid duplicating unnecessary instructions between the agent, skill, and `CLAUDE.md`.

## 8. Final Instruction

First inspect the existing Claude Code configuration and determine the appropriate locations for the new agent and skill.

Present your proposed files and their responsibilities.

**Do not create or modify anything until I explicitly approve.**

After approval, create only the specifically authorized agent and skill files.