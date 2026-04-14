---
name: smart-git
version: 1.0.0
description: |
  Perform intelligent Git operations including commits, branch management, history viewing, and conflict resolution with auto-generated conventional commit messages.
  Use when user mentions /git, /commit, /push, /pull, or any version control related operations.
---

# Smart Git

Intelligent Git assistant that analyzes changes and generates standardized commit messages.

## Behavioral Flow

Follow this flow for every Git operation:

1. **Analyze** → Check repository status and working directory changes
2. **Validate** → Ensure operation is appropriate for current context
3. **Execute** → Run Git commands
4. **Optimize** → Apply standardized messages and workflow patterns
5. **Report** → Provide status summary and next steps

## Tool Coordination

| Tool     | Purpose                                      |
| -------- | -------------------------------------------- |
| **Bash** | Git command execution, repository operations |
| **Read** | Config file review, conflict file analysis   |
| **Grep** | Log search, status parsing                   |
| **Edit** | Conflict resolution, config modification     |

## Commit Message Convention

Use Conventional Commits format:

```
<type>(<scope>): <subject>

[body]
```

**Types:**
| Type       | Description                       |
| ---------- | --------------------------------- |
| `feat`     | New feature                       |
| `fix`      | Bug fix                           |
| `docs`     | Documentation changes             |
| `style`    | Code formatting (no logic change) |
| `refactor` | Code refactoring                  |
| `perf`     | Performance improvement           |
| `test`     | Test related                      |
| `chore`    | Build/tool/dependency changes     |
| `ci`       | CI configuration                  |

**DO:**
- Use imperative mood ("Add feature" not "Added feature")
- Keep subject under 50 characters, capitalize first letter, no period
- Explain "why" not "what" in body
- One commit per logical change (atomic commits)

**DON'T:**
- Vague messages like "update", "fix", "misc changes"
- Implementation details in subject line
- Mix unrelated changes
- Use past tense
- Add any Co-Authored-By, Signed-off-by, or similar trailer tags — commits are authored solely by the user

**Examples:**

Feature:
```
feat(auth): add OAuth2 login support

Integrate OAuth2 flow with Google and GitHub providers
```

Fix:
```
fix(api): handle null pointer in user profile

Add null checks before accessing nested properties
```

Refactor:
```
refactor(db): simplify query builder

Extract common query patterns into reusable functions
```

**Pre-commit Checklist:**
- [ ] Type is accurate (feat/fix/refactor...)
- [ ] Scope is clear and specific
- [ ] Subject is under 50 characters
- [ ] Uses imperative mood
- [ ] Body explains the reason
- [ ] Atomic commit (one logical change)
- [ ] No Co-Authored-By or other trailer tags
- [ ] Files staged by specific name (not git add . / -A)

## Key Patterns

### Smart Commit
```
Analyze changes → Identify change type → Extract scope → Generate subject → Compose message
```

Steps:
```bash
git status                    # 1. Check status
git diff HEAD                 # 2. Analyze changes
git log --oneline -5          # 3. Reference history style
git add <specific-files>      # 4. Stage by name (NEVER use git add . or git add -A)
git commit -m "<message>"     # 5. Commit (NO --no-verify, NO trailer tags)
```

### Atomic Commit Strategy

One logical change per commit.

**Split decision:**
| Scenario                     | Decision       |
| ---------------------------- | -------------- |
| Different features/types     | Split          |
| Different modules            | Consider split |
| Same feature, multiple files | Don't split    |

**User override:**
- `atomic` / `split` → Force split
- `single` / `together` → Force merge
- No instruction → Auto-split (default)

### Status Analysis
```
Repository state → Categorize changes → Actionable recommendations
```

Output format:
- Untracked file count
- Modified file count
- Staged file count
- Suggested next action

### Branch Strategy

Naming convention:
- `feature/xxx` - New feature
- `fix/xxx` - Bug fix
- `hotfix/xxx` - Urgent fix
- `release/xxx` - Release

Merge strategy:
```bash
git merge --no-ff <branch>    # Preserve merge history
```

### Conflict Resolution

Flow:
1. `git status` to identify conflicted files
2. Read and analyze conflict content
3. Edit to resolve (remove conflict markers)
4. `git add <file>` to mark resolved
5. `git merge --continue` or `git rebase --continue`

### Safe Rollback

| Scenario                          | Command                       |
| --------------------------------- | ----------------------------- |
| Discard working directory changes | `git checkout -- <file>`      |
| Unstage files                     | `git reset HEAD <file>`       |
| Reset keeping changes             | `git reset --soft <commit>`   |
| Reset discarding changes          | `git reset --hard <commit>` ⚠️ |
| Safe revert pushed commit         | `git revert <commit>`         |

## Boundaries

**Will do:**
- Execute all regular Git operations
- Intelligently generate commit messages from change analysis
- Provide workflow optimization and best practice guidance
- Guided conflict resolution
- Clear status summaries and next step recommendations

**Will NOT do (unless explicitly requested):**
- Modify Git global config
- Execute `push --force` (use `--force-with-lease` instead)
- Execute `reset --hard` on uncommitted changes
- Modify pushed history
- Delete remote branches
- Handle complex merges requiring manual judgment

**Must confirm before executing:**
- Any `--force` operation
- `reset --hard`
- Delete branches
- Rebase pushed commits
