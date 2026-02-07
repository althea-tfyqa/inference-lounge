# Git Branches & Workflow: Inference Lounge Project

**Created:** February 6, 2026
**Purpose:** Educational guide for understanding git branches in the context of the Inference Lounge project

---

## Table of Contents
1. [What Are Git Branches? (The Concept)](#what-are-git-branches-the-concept)
2. [Why We're Using Branches for This Project](#why-were-using-branches-for-this-project)
3. [Your Current Setup](#your-current-setup)
4. [Git Worktree Explained](#git-worktree-explained)
5. [Daily Workflow Commands](#daily-workflow-commands)
6. [Common Scenarios](#common-scenarios)
7. [Visual Mental Model](#visual-mental-model)
8. [Glossary](#glossary)

---

## What Are Git Branches? (The Concept)

### The Metaphor
Imagine your project's history as a tree:
- The **trunk** is your main branch (stable, production-ready code)
- **Branches** grow off the trunk for experiments, new features, or redesigns
- Branches can merge back into the trunk when ready
- Or branches can stay separate indefinitely

### Why Branches Exist
Branches let you:
1. **Experiment safely** - Try things without breaking working code
2. **Work in parallel** - Multiple features can develop simultaneously
3. **Preserve history** - Keep different versions of your project
4. **Collaborate** - Team members work on separate branches
5. **Release management** - Maintain stable vs. development versions

### The Technical Reality
A branch is just a **pointer** to a specific commit in your git history. That's it. When you "create a branch," you're just creating a new pointer. All the commits still exist in one shared history.

```
Commit history (simplified):
A ← B ← C ← D ← E
        ↑       ↑
      main    comic-theme
```

Both `main` and `comic-theme` point to commits in the same history. When you switch branches, git just moves your working directory to show the files at that commit.

---

## Why We're Using Branches for This Project

### The Problem
You wanted to redesign Inference Lounge with a 1950s comic book aesthetic:
- Speech bubbles instead of message boxes
- Character portrait column
- Retro styling and fonts
- Completely different visual structure

But you also wanted to **keep using** the current working version for:
- Actual AI conversations (research, teaching prep)
- Testing existing features
- Daily work that can't wait for the redesign

### The Solution: Two Branches
Instead of replacing the working app or trying to maintain two themes in one codebase, we created two branches:

**`main` branch:**
- Stable, working version
- The app as it existed before the comic redesign
- Your "daily driver" for actual use
- Won't change unless you explicitly update it

**`comic-theme` branch:**
- Creative development playground
- Where all the comic book UI work happens
- Can break, experiment, iterate freely
- Started as a copy of `main`, then diverges

### Why This Beats Alternatives

**vs. Theme Switcher:**
- Comic UI is structurally different (not just CSS)
- Would require `if comic_mode:` everywhere in code
- Messy to maintain two UIs in one codebase

**vs. Separate Repo/Fork:**
- Hard to keep features in sync
- Duplication of effort
- Overkill for single-user app

**Git branches give you:**
- Clean separation
- Both versions available instantly
- Easy to merge features between them if needed
- Standard developer workflow

---

## Your Current Setup

### What Was Created

You now have **two working directories** on your computer:

```
/Users/adelwich/Projects/tools/
├── inference_lounge/          ← Comic theme development (comic-theme branch)
└── inference_lounge-stable/   ← Daily use stable version (main branch)
```

### How They're Connected

Both directories are linked to the **same git repository**. They share:
- Commit history
- Branches
- Remote (GitHub)
- Git configuration

Changes committed in one directory are visible to the other (after pushing/pulling).

### Git Worktree (What Just Happened)

We used `git worktree add ../inference_lounge-stable main` which:
1. Created a new directory (`inference_lounge-stable`)
2. Checked out the `main` branch there
3. Linked it to the main repository's git database
4. Allows both directories to coexist without conflicts

This is different from cloning twice:
- **Clone twice:** Two completely separate repositories (copy everything)
- **Worktree:** Two working directories, one repository (share git history)

---

## Daily Workflow Commands

### Starting Your Day

**To use the stable app (actual work):**
```bash
cd /Users/adelwich/Projects/tools/inference_lounge-stable
poetry run python main.py
```

**To work on comic theme development:**
```bash
cd /Users/adelwich/Projects/tools/inference_lounge
poetry run python main.py
```

You can run both simultaneously in different terminal windows!

### Making Changes to Comic Theme

```bash
cd /Users/adelwich/Projects/tools/inference_lounge

# Verify you're on comic-theme branch
git branch
# Should show: * comic-theme

# Make your changes to code (add speech bubbles, portraits, etc.)
# Test the app

# Stage and commit changes
git add .
git commit -m "Add speech bubble tail styling"

# Push to GitHub
git push
```

### Checking What Branch You're On

```bash
git branch
# Shows all branches, * marks current one

git status
# First line shows: "On branch comic-theme"
```

### If You Accidentally Edit in the Wrong Directory

**Scenario:** You meant to edit comic theme but accidentally changed something in `inference_lounge-stable`

```bash
# See what changed
git status

# Option 1: Discard changes
git restore .

# Option 2: Move changes to comic-theme
git stash                    # Save changes temporarily
cd ../inference_lounge       # Go to comic theme directory
git stash pop                # Apply saved changes here
```

---

## Common Scenarios

### Scenario 1: "I want to add a feature to BOTH branches"

**Example:** You fix a bug or add a useful feature to main, and want it in comic-theme too.

```bash
# Make the change in main branch
cd inference_lounge-stable
# Edit code, test, commit
git add .
git commit -m "Fix image loading bug"
git push

# Bring that change into comic-theme
cd ../inference_lounge
git merge main
# This pulls commits from main into comic-theme

# If there are conflicts, git will tell you
# Edit conflicting files, then:
git add .
git commit -m "Merge bug fix from main"
git push
```

### Scenario 2: "I want to bring comic theme changes into main"

**When:** You're happy with the comic theme and want to replace main with it.

```bash
cd inference_lounge-stable
git merge comic-theme
# This brings comic-theme changes into main

# Or, if you want to REPLACE main entirely:
git checkout comic-theme
git branch -D main           # Delete old main
git checkout -b main         # Create new main from comic-theme
git push --force origin main # Update GitHub (careful!)
```

⚠️ **Warning:** Force pushing rewrites history. Only do this on personal projects.

### Scenario 3: "I want to see what's different between branches"

```bash
# See list of changed files
git diff main comic-theme --name-only

# See actual code differences
git diff main comic-theme

# See differences for specific file
git diff main comic-theme gui.py
```

### Scenario 4: "I want to switch branches in the same directory"

**Why you might do this:** Check something quickly in main without opening the other directory.

```bash
cd inference_lounge

# Save your current work
git commit -am "WIP: speech bubble styling"

# Switch to main
git checkout main
# Your files now show main branch version

# Do whatever you need, then switch back
git checkout comic-theme
# Back to your comic theme work
```

⚠️ **Important:** Commit or stash changes before switching branches!

### Scenario 5: "I broke everything and want to start over"

```bash
# Discard ALL uncommitted changes
git restore .

# Go back to last commit
git reset --hard HEAD

# Go back to specific earlier commit
git log                    # Find commit hash
git reset --hard abc123    # Replace abc123 with actual hash
```

---

## Visual Mental Model

### How Git Sees Your Project

```
GitHub (Remote Repository)
         ↓
    origin/main
    origin/comic-theme
         ↓
Your Computer (Local Repository)
    ├── main (branch pointer)
    └── comic-theme (branch pointer)
         ↓
Two Working Directories:
    ├── inference_lounge-stable/  (checked out to: main)
    └── inference_lounge/         (checked out to: comic-theme)
```

### Commit History Timeline

```
Initial commits:
A ← B ← C ← D ← E ← F ← G
                        ↑
                    (both branches start here)

After working on both branches:

                  ┌─ H ← I ← J  (main: bug fixes, small tweaks)
                  │
A ← B ← C ← D ← E ← F ← G
                  │
                  └─ K ← L ← M ← N  (comic-theme: UI redesign)
                                 ↑
                              (you are here)

Legend:
├─ = branch split
← = parent commit relationship
Letters = individual commits
```

### What "Merging" Does

**Merging `main` into `comic-theme`:**

```
Before merge:
                  ┌─ H ← I ← J  (main)
                  │
A ← B ← C ← D ← E ← F ← G
                  │
                  └─ K ← L ← M  (comic-theme)

After: git merge main (from comic-theme branch):

                  ┌─ H ← I ← J ←┐
                  │              ↓
A ← B ← C ← D ← E ← F ← G        │
                  │              │
                  └─ K ← L ← M ← MERGE (comic-theme now)
                                   ↑
                        (contains both H,I,J and K,L,M)
```

---

## Git Worktree Explained

### What Is a Worktree?

A worktree is an **additional working directory** linked to the same git repository.

**Normal git:**
- One working directory per repository
- To see different branches, you switch (`git checkout`)
- Files change in-place

**With worktrees:**
- Multiple working directories, same repository
- Each directory shows a different branch
- No switching needed - just `cd` between directories

### Why It's Useful Here

You want to:
- **Use** the stable app (main branch) for actual work
- **Develop** the comic theme (comic-theme branch) in parallel

Without worktrees, you'd have to:
1. Commit current work
2. Switch branches
3. Restart app
4. Do your thing
5. Switch back
6. Restart app again

With worktrees, you just open two terminal windows!

### Technical Details

**What `git worktree add ../inference_lounge-stable main` did:**

1. Created directory: `/Users/adelwich/Projects/tools/inference_lounge-stable/`
2. Created file: `/Users/adelwich/Projects/tools/inference_lounge/.git/worktrees/inference_lounge-stable/`
3. Made `inference_lounge-stable/.git` a file (not directory) that points to main repo
4. Checked out `main` branch in that directory

**Both directories share:**
- `.git/objects/` (all commits, blobs, trees)
- `.git/refs/` (all branches)
- `.git/config` (repository configuration)

**Each directory has its own:**
- Working files (actual code)
- Index/staging area
- Currently checked-out branch

### Worktree Commands

```bash
# List all worktrees
git worktree list

# Add a new worktree
git worktree add <path> <branch>

# Remove a worktree (when done with it)
git worktree remove <path>

# Prune deleted worktrees from git's tracking
git worktree prune
```

---

## Glossary

**Branch:** A pointer to a specific commit. Represents a line of development.

**Commit:** A snapshot of your project at a specific point in time. Contains all files, metadata, and a pointer to parent commit(s).

**Working Directory:** The folder on your computer where you edit files. What you see in Finder/Explorer.

**Staging Area (Index):** A preview of your next commit. `git add` puts files here. `git commit` saves the staged files.

**HEAD:** A pointer to your current position in the git history. Usually points to the latest commit on your current branch.

**Origin:** The default name for the remote repository (on GitHub).

**Remote:** A version of your repository hosted elsewhere (e.g., GitHub, GitLab).

**Merge:** Combining changes from two branches into one.

**Checkout:** Switch to a different branch or commit. Changes what files appear in your working directory.

**Worktree:** An additional working directory linked to the same repository.

**main (formerly master):** The default branch name. Conventionally the "stable" or "production" branch.

**Stash:** Temporarily save uncommitted changes without committing them. Like a clipboard for git.

**Fast-forward:** A merge where one branch is directly ahead of another (no divergence). Git just moves the pointer forward.

**Merge Conflict:** When the same lines of code were changed differently in two branches. Git can't auto-merge; you must resolve manually.

**Pull:** Fetch changes from remote and merge them into your current branch (`git pull` = `git fetch` + `git merge`).

**Push:** Upload your local commits to the remote repository.

**Clone:** Create a complete copy of a repository on your computer.

**Fork:** Create a copy of someone else's repository under your own account (GitHub-specific term).

---

## Quick Reference Card

### Where Am I?
```bash
pwd                    # Show current directory
git branch             # Show current branch (* marks active)
git status             # Show branch, changes, staging area
```

### Daily Use Workflow
```bash
# Use stable version
cd inference_lounge-stable && poetry run python main.py

# Develop comic theme
cd inference_lounge && poetry run python main.py
```

### Making Changes (Comic Theme)
```bash
cd inference_lounge
# Edit files
git add .
git commit -m "Descriptive message"
git push
```

### Switching Branches (Same Directory)
```bash
git status                # Check for uncommitted changes
git commit -am "Save"     # Or git stash
git checkout main         # Switch to main
git checkout comic-theme  # Switch back
```

### Syncing Changes Between Branches
```bash
# Bring main's changes into comic-theme
cd inference_lounge
git merge main

# Bring comic-theme's changes into main
cd inference_lounge-stable
git merge comic-theme
```

### Viewing Differences
```bash
git diff main comic-theme              # All differences
git diff main comic-theme --name-only  # Just file names
git log --oneline --graph --all        # Visual commit history
```

### Emergency Commands
```bash
git restore .              # Discard all uncommitted changes
git reset --hard HEAD      # Reset to last commit
git stash                  # Save changes temporarily
git stash pop              # Restore stashed changes
```

---

## Learning Resources

### Want to Go Deeper?

**Interactive tutorials:**
- [Learn Git Branching](https://learngitbranching.js.org/) - Visual, interactive
- [Git Immersion](https://gitimmersion.com/) - Step-by-step tutorial

**Visualization tools:**
- `git log --oneline --graph --all` - Terminal visualization
- [GitKraken](https://www.gitkraken.com/) - GUI with visual commit graph
- [GitHub Desktop](https://desktop.github.com/) - Simplified GUI

**Cheat sheets:**
- [GitHub Git Cheat Sheet](https://education.github.com/git-cheat-sheet-education.pdf)
- [Atlassian Git Tutorial](https://www.atlassian.com/git/tutorials)

---

## Project-Specific Notes

### Your Inference Lounge Setup

**`inference_lounge-stable/` (main branch):**
- Purpose: Daily driver for actual AI conversations
- Rule: Don't edit code here (just use the app)
- Updates: Only when you explicitly merge from comic-theme or make fixes

**`inference_lounge/` (comic-theme branch):**
- Purpose: Creative development of comic book UI
- Active work: Speech bubbles, portraits, retro styling
- Freedom: Break things, experiment, iterate
- When ready: Can merge back into main or replace it entirely

### Files to Notice

**In `inference_lounge/` (comic-theme branch):**
- `COMIC_THEME_README.md` - Implementation guide
- `comic_preview.html` - HTML mockup
- `speech_bubble_widget.py` - Custom PyQt widgets
- `comic_styles_preview.py` - QSS styling examples

**These files exist in both branches** (created before branch split).

Once you start modifying the UI in comic-theme, the branches will diverge:
- `main`: Original UI (message widgets, current styling)
- `comic-theme`: New UI (speech bubbles, portraits, retro theme)

### Commit Messages for This Project

Good commit messages help you understand history:

**Good:**
- "Add speech bubble tail styling to message widgets"
- "Implement circular portrait column layout"
- "Fix banner gradient on comic theme"

**Less helpful:**
- "Update files"
- "WIP"
- "Changes"

**Best practice:**
- Start with verb (Add, Fix, Update, Remove)
- Be specific about what changed
- Reference issue/feature if applicable

---

## Questions for Reflection

As you work with this setup, think about:

1. **When should I merge `main` into `comic-theme`?**
   - When you've added features to main that comic-theme needs
   - Regularly (weekly?) to avoid massive merge conflicts later

2. **When should I merge `comic-theme` into `main`?**
   - When the comic theme is stable and you're ready to make it your default
   - Or maybe never - keep both branches indefinitely!

3. **What if I want a third branch for another experiment?**
   - `git checkout -b experimental-feature` creates a new branch
   - `git worktree add ../inference_lounge-experiment experimental-feature` gives it a directory

4. **How do I know if I've broken something?**
   - Run the app frequently while developing
   - Commit small changes so you can revert easily
   - Use `git diff` before committing to review changes

---

## Final Thoughts

Git branches are one of the most powerful features of version control. They enable you to:
- Experiment safely
- Maintain multiple versions
- Collaborate effectively
- Preserve working code while exploring new ideas

For Inference Lounge, branches give you the freedom to completely redesign the UI without losing your working daily-use version. As you get comfortable with this workflow, you'll find branches become second nature.

**Remember:** Git is a safety net. Almost nothing you do is irreversible. If you break something, you can always go back to a previous commit.

---

**Questions? Confused about something?** Add notes here or ask Claude to clarify specific concepts.

**NotebookLM prompt ideas:**
- "Create a visual cheat sheet for git branch workflow"
- "Explain git worktree in simple terms with diagrams"
- "Generate a quick reference card for daily commands"

---

*This document is version-controlled in your repository. As you learn more, feel free to edit and expand it!*
