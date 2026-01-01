# Git Complete Guide - Version Control Concepts

## 📚 Table of Contents

1. [Version Control Concepts](#version-control-concepts)
2. [Git Architecture](#git-architecture)
3. [Git Installation & Configuration](#git-installation--configuration)
4. [Repositories](#repositories)
5. [Working Directory, Staging Area, Repository](#working-directory-staging-area-repository)
6. [Git Basic Commands](#git-basic-commands)
7. [Branching](#branching)
8. [Merging](#merging)
9. [Rebasing](#rebasing)
10. [Cherry-Pick](#cherry-pick)
11. [Reset](#reset)
12. [Revert](#revert)
13. [Stash](#stash)
14. [Commit Management](#commit-management)
15. [Tags](#tags)
16. [Diff & Log](#diff--log)
17. [Remote Repositories](#remote-repositories)
18. [Fetch, Pull, Push](#fetch-pull-push)
19. [Conflict Resolution](#conflict-resolution)
20. [Forking Workflow](#forking-workflow)
21. [Git Workflow Strategies](#git-workflow-strategies)
22. [Git Hooks](#git-hooks)
23. [Git Submodules](#git-submodules)
24. [Git Subtrees](#git-subtrees)
25. [Git Ignore](#git-ignore)
26. [Git Config](#git-config)
27. [Git Aliases](#git-aliases)
28. [Git Clean](#git-clean)
29. [Git Bisect](#git-bisect)
30. [Git Reflog](#git-reflog)
31. [Git Security](#git-security)
32. [Access Control](#access-control)
33. [CI/CD Integration with Git](#cicd-integration-with-git)
34. [Git Best Practices](#git-best-practices)

---

## 🔄 Version Control Concepts

### What is Version Control?

**Definition:** Version Control System (VCS) is a system that tracks changes to files over time, allowing you to recall specific versions later.

**Real-life example:**
Like a time machine for your code - you can go back to any point in time to see what changed and who changed it.

**Key Concepts:**
1. **Snapshot** - A saved state of your project at a specific point in time
2. **Repository** - A database storing all versions and history
3. **Commit** - A saved snapshot with a message describing changes
4. **Branch** - An independent line of development
5. **Merge** - Combining changes from different branches

**Why Version Control?**
- **Backup & Recovery** - Never lose your work
- **Collaboration** - Multiple developers can work together
- **History Tracking** - See who changed what and when
- **Experimentation** - Try new features without breaking existing code
- **Rollback** - Revert to previous versions if something breaks

**Types of Version Control:**

1. **Local VCS** - Stores changes locally (e.g., RCS)
   - **Pros:** Simple, fast
   - **Cons:** No collaboration, single point of failure

2. **Centralized VCS (CVCS)** - Single server stores all versions (e.g., SVN, CVS)
   - **Pros:** Better collaboration, easier administration
   - **Cons:** Single point of failure, requires network

3. **Distributed VCS (DVCS)** - Every user has full repository copy (e.g., Git, Mercurial)
   - **Pros:** No single point of failure, fast, offline work
   - **Cons:** More complex, larger repository size

**Git vs Other VCS:**

| Feature | Git | SVN | Mercurial |
|---------|-----|-----|-----------|
| Architecture | Distributed | Centralized | Distributed |
| Branching | Fast & cheap | Slow | Fast |
| Speed | Very fast | Moderate | Fast |
| Learning curve | Steep | Easy | Moderate |
| Community | Largest | Large | Smaller |

---

## 🏗️ Git Architecture

### Git Object Model

**Definition:** Git uses a content-addressable file system where everything is stored as objects with SHA-1 hash identifiers.

**Four Object Types:**

1. **Blob (Binary Large Object)**
   - Stores file content
   - **Example:** `blob 123abc` → file content
   - **Use case:** Every file version is stored as a blob

2. **Tree**
   - Directory structure (maps filenames to blobs)
   - **Example:** `tree 456def` → directory with files
   - **Use case:** Represents a snapshot of directory structure

3. **Commit**
   - Snapshot with metadata (author, date, message, parent commit)
   - **Example:** `commit 789ghi` → commit object
   - **Use case:** Links tree objects together in history

4. **Tag**
   - Pointer to a specific commit (usually for releases)
   - **Example:** `tag v1.0.0` → points to commit
   - **Use case:** Mark important milestones

**Visual Representation:**
```
Commit Object
├── Tree (root directory)
│   ├── Blob (file1.txt)
│   ├── Blob (file2.txt)
│   └── Tree (subdirectory/)
│       └── Blob (file3.txt)
├── Parent Commit (SHA-1)
├── Author
├── Committer
└── Commit Message
```

**Understanding SHA-1 Hashes:**
```bash
# SHA-1 hash is 40-character hexadecimal string
# Example: a1b2c3d4e5f6...

# Short form (first 7 characters usually unique)
git log --oneline
# Output: a1b2c3d Add feature
```

### Git Repository Structure

**Definition:** A Git repository consists of several key directories and files.

**Structure:**
```
.git/
├── HEAD                    # Points to current branch
├── config                  # Repository configuration
├── objects/                # All Git objects (blobs, trees, commits)
│   ├── [0-9a-f][0-9a-f]/  # Objects stored by hash prefix
│   └── pack/               # Packed objects for efficiency
├── refs/                   # References (branches, tags)
│   ├── heads/              # Branch references
│   ├── tags/               # Tag references
│   └── remotes/            # Remote branch references
├── index                   # Staging area (binary file)
├── hooks/                  # Git hooks (scripts)
├── logs/                   # Reference logs (reflog)
└── info/                   # Additional info (excludes, etc.)
```

**Key Files Explained:**

1. **HEAD** - Points to current branch/commit
   ```bash
   # View HEAD
   cat .git/HEAD
   # Output: ref: refs/heads/main
   ```

2. **index** - Staging area (binary file, use `git status` to view)
   ```bash
   # View staged files
   git ls-files --stage
   ```

3. **config** - Repository configuration
   ```bash
   # View config
   git config --list --local
   ```

### Git's Three-Tree Architecture

**Definition:** Git maintains three "trees" representing different states of your project.

**Three Trees:**

1. **Working Directory** (Working Tree)
   - Your current files on disk
   - **Location:** Your project folder
   - **State:** Modified, untracked, or clean
   - **Command to view:** `git status`

2. **Staging Area** (Index)
   - Prepared changes ready to commit
   - **Location:** `.git/index` (binary file)
   - **State:** Staged changes
   - **Command to view:** `git diff --cached` or `git status`

3. **Repository** (HEAD)
   - Committed snapshots
   - **Location:** `.git/objects/`
   - **State:** Saved commits
   - **Command to view:** `git log`

**Visual Flow:**
```
Working Directory  →  Staging Area  →  Repository
    (Modified)      (git add)      (git commit)
```

**Example Workflow:**
```bash
# 1. Modify file in working directory
echo "new content" > file.txt

# 2. Stage changes (working directory → staging area)
git add file.txt

# 3. Commit (staging area → repository)
git commit -m "Update file.txt"
```

**State Transitions:**
```bash
# Untracked → Staged
git add newfile.txt

# Modified → Staged
git add modifiedfile.txt

# Staged → Committed
git commit -m "Changes"

# Modify again (Committed → Modified)
echo "more changes" >> modifiedfile.txt
```

---

## ⚙️ Git Installation & Configuration

### Installation

**Windows:**
```bash
# Download from: https://git-scm.com/download/win
# Or use package manager:
# Chocolatey: choco install git
# Scoop: scoop install git
```

**macOS:**
```bash
# Using Homebrew
brew install git

# Using Xcode Command Line Tools
xcode-select --install
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install git
```

**Linux (RHEL/CentOS):**
```bash
sudo yum install git
# or
sudo dnf install git
```

**Verify Installation:**
```bash
git --version
# Output: git version 2.x.x
```

### Configuration Levels

**Definition:** Git has three configuration levels (system, global, local) that override each other.

**Configuration Hierarchy (from highest to lowest priority):**
1. **Local** (Repository-specific) - `.git/config`
2. **Global** (User-specific) - `~/.gitconfig` or `~/.config/git/config`
3. **System** (System-wide) - `/etc/gitconfig`

**Local Configuration:**
```bash
# Set local config (only for current repository)
git config user.name "John Doe"
git config user.email "john@example.com"

# View local config
git config --list --local
git config user.name  # Get specific value
```

**Global Configuration:**
```bash
# Set global config (all repositories for this user)
git config --global user.name "John Doe"
git config --global user.email "john@example.com"

# View global config
git config --list --global
git config --global user.name
```

**System Configuration:**
```bash
# Set system config (all users on this system)
sudo git config --system user.name "Default User"
sudo git config --system user.email "admin@example.com"

# View system config
git config --list --system
```

**Important: Local overrides Global, Global overrides System**

### Essential Configuration

**User Identity (REQUIRED for commits):**
```bash
# Set your name and email (use --global for all repos)
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# For multiple identities (work vs personal), use local config
cd ~/work-project
git config user.email "work@company.com"

cd ~/personal-project
git config user.email "personal@gmail.com"
```

**Default Editor:**
```bash
# Set default editor for commit messages
git config --global core.editor "code --wait"        # VS Code
git config --global core.editor "nano"               # Nano
git config --global core.editor "vim"                # Vim
git config --global core.editor "'C:/Program Files/Notepad++/notepad++.exe' -multiInst -notabbar -nosession -noPlugin"  # Notepad++

# On Windows, for VS Code:
git config --global core.editor "code --wait"
```

**Default Branch Name:**
```bash
# Set default branch name (Git 2.28+)
git config --global init.defaultBranch main

# For older Git versions, rename after init:
git branch -M main
```

**Line Ending Configuration (CRITICAL for cross-platform):**
```bash
# Windows: Checkout Windows-style, commit Unix-style
git config --global core.autocrlf true

# macOS/Linux: Don't convert line endings
git config --global core.autocrlf input

# Disable conversion (not recommended)
git config --global core.autocrlf false

# Alternative: Use .gitattributes (recommended)
# .gitattributes:
# * text=auto
```

**Pager Configuration:**
```bash
# Disable pager (show all output at once)
git config --global core.pager ""

# Use less with specific options
git config --global core.pager "less -FRX"
```

**Credential Storage:**
```bash
# Cache credentials for 15 minutes
git config --global credential.helper cache

# Cache for 1 hour (3600 seconds)
git config --global credential.helper "cache --timeout=3600"

# Store credentials permanently (encrypted)
git config --global credential.helper store

# Use credential manager (Windows)
git config --global credential.helper wincred

# Use macOS Keychain
git config --global credential.helper osxkeychain
```

**View All Configuration:**
```bash
# View all config (all levels)
git config --list

# View specific level
git config --list --local
git config --list --global
git config --list --system

# View specific setting
git config user.name
git config user.email
```

**Edit Configuration Files Directly:**
```bash
# Edit global config
git config --global --edit

# Edit local config
git config --local --edit
```

---

## 📁 Repositories

### What is a Repository?

**Definition:** A Git repository is a collection of files, folders, and the complete history of changes made to those files.

**Real-life example:**
Like a filing cabinet that stores not just current documents, but every version of every document ever created.

**Types of Repositories:**

1. **Local Repository**
   - Stored on your computer
   - **Location:** `.git/` directory in project folder
   - **Use case:** Your working copy

2. **Remote Repository**
   - Stored on a server (GitHub, GitLab, etc.)
   - **Use case:** Collaboration, backup, deployment

3. **Bare Repository**
   - No working directory (only `.git/` contents)
   - **Use case:** Server-side repositories for sharing

### Initializing a Repository

**Create New Repository:**
```bash
# Initialize repository in current directory
git init

# Initialize with branch name
git init -b main
git init --initial-branch=main

# Initialize bare repository (no working directory)
git init --bare
```

**What `git init` does:**
- Creates `.git/` directory
- Creates initial branch (default: `master` or `main`)
- Sets up repository structure
- **Does NOT create initial commit**

**Clone Existing Repository:**
```bash
# Clone repository (creates new directory)
git clone https://github.com/user/repo.git

# Clone to specific directory
git clone https://github.com/user/repo.git my-project

# Clone specific branch
git clone -b branch-name https://github.com/user/repo.git

# Clone with depth (shallow clone - fewer commits)
git clone --depth 1 https://github.com/user/repo.git

# Clone bare repository
git clone --bare https://github.com/user/repo.git

# Clone with specific protocol
git clone git@github.com:user/repo.git  # SSH
git clone https://github.com/user/repo.git  # HTTPS
```

**Verify Repository:**
```bash
# Check if directory is a Git repository
git status

# View repository info
git remote -v  # Remote repositories
git branch     # Local branches
git log --oneline  # Commit history
```

---

## 📂 Working Directory, Staging Area, Repository

### Understanding the Three States

**Definition:** Git has three main areas where your files can reside, each serving a specific purpose.

**The Three States:**

1. **Working Directory (Working Tree)**
   - **Location:** Your project folder (everything except `.git/`)
   - **Purpose:** Where you edit files
   - **State:** Files can be modified, new, or deleted
   - **Not tracked by Git:** Untracked files

2. **Staging Area (Index)**
   - **Location:** `.git/index` (binary file)
   - **Purpose:** Prepares changes for next commit
   - **State:** Files marked to be included in next commit
   - **Analogy:** Like a shopping cart before checkout

3. **Repository (Git Directory)**
   - **Location:** `.git/objects/`
   - **Purpose:** Stores committed snapshots permanently
   - **State:** Immutable history of all changes
   - **Analogy:** Like a photo album of snapshots

### File States

**File States in Git:**

```
Untracked → Staged → Committed
    ↓         ↓
 Modified ← Modified (after commit)
```

**Detailed States:**

1. **Untracked**
   - File exists in working directory but Git doesn't track it
   - **Command:** `git status` shows in red
   - **Action:** `git add` to start tracking

2. **Modified (Unstaged)**
   - File is tracked but changed in working directory
   - **Command:** `git status` shows in red
   - **Action:** `git add` to stage changes

3. **Staged**
   - Changes added to staging area, ready to commit
   - **Command:** `git status` shows in green
   - **Action:** `git commit` to save

4. **Committed**
   - Changes saved in repository
   - **Command:** `git log` shows in history
   - **Action:** Files are in repository, working directory is clean

**Visual Example:**
```bash
# Initial state (file committed)
echo "version 1" > file.txt
git add file.txt
git commit -m "Initial commit"

# Modify file (now Modified, Unstaged)
echo "version 2" > file.txt
git status
# Output: modified: file.txt (in red)

# Stage changes (now Staged)
git add file.txt
git status
# Output: modified: file.txt (in green, ready to commit)

# Commit (now Committed, clean working directory)
git commit -m "Update to version 2"
git status
# Output: nothing to commit, working tree clean
```

### Working with the Three States

**View Current State:**
```bash
# Show status of all files
git status

# Short format
git status -s
git status --short

# Show branch and tracking info
git status -b
git status --branch
```

**Stage Files (Working Directory → Staging Area):**
```bash
# Stage specific file
git add filename.txt

# Stage all modified files
git add .

# Stage all files in directory
git add directory/

# Stage specific pattern
git add *.py

# Stage interactively (choose which changes to stage)
git add -i
git add --interactive

# Stage parts of a file (patch mode)
git add -p filename.txt
git add --patch filename.txt
```

**Unstage Files (Staging Area → Working Directory):**
```bash
# Unstage file (keep changes in working directory)
git reset HEAD filename.txt
git restore --staged filename.txt  # Git 2.23+

# Unstage all files
git reset HEAD
git restore --staged .  # Git 2.23+
```

**Commit Changes (Staging Area → Repository):**
```bash
# Commit staged changes
git commit -m "Commit message"

# Commit with detailed message
git commit -m "Short summary" -m "Detailed description"

# Amend last commit (modify previous commit)
git commit --amend -m "New message"

# Amend without changing message
git commit --amend --no-edit
```

**View Differences:**
```bash
# Working Directory vs Staging Area
git diff

# Staging Area vs Repository (last commit)
git diff --cached
git diff --staged

# Working Directory vs Repository
git diff HEAD

# Specific file
git diff filename.txt
```

---

## 🔧 Git Basic Commands

### Essential Commands

**Initialization:**
```bash
git init                    # Initialize repository
git clone <url>             # Clone repository
```

**Status & Information:**
```bash
git status                  # Show working directory status
git status -s               # Short format
git log                     # Show commit history
git log --oneline           # Compact format
git log --graph             # Show branch graph
git log --all               # Show all branches
git branch                  # List branches
git branch -a               # List all branches (local + remote)
git remote -v               # Show remote repositories
```

**Staging:**
```bash
git add <file>              # Stage file
git add .                   # Stage all changes
git add -A                  # Stage all changes (including deletions)
git add -u                  # Stage only modified/deleted files
git add -p                  # Stage interactively (patch mode)
```

**Committing:**
```bash
git commit -m "message"     # Commit with message
git commit -a -m "message"  # Stage all tracked files and commit
git commit --amend          # Modify last commit
```

**Viewing Changes:**
```bash
git diff                    # Show unstaged changes
git diff --cached           # Show staged changes
git diff HEAD               # Show all changes vs last commit
git show <commit>           # Show specific commit
```

**Branching:**
```bash
git branch <name>           # Create branch
git checkout <branch>       # Switch to branch
git checkout -b <branch>    # Create and switch to branch
git switch <branch>         # Switch branch (Git 2.23+)
git switch -c <branch>      # Create and switch (Git 2.23+)
git branch -d <branch>      # Delete branch (safe)
git branch -D <branch>      # Force delete branch
```

**Remote Operations:**
```bash
git remote add <name> <url> # Add remote repository
git fetch <remote>          # Download changes
git pull <remote> <branch>  # Fetch and merge
git push <remote> <branch>  # Upload changes
```

### Command Categories

**Status Commands:**
```bash
# Working directory status
git status                  # Full status
git status -s               # Short status (M = modified, A = added, D = deleted, ?? = untracked)
git status -b               # Include branch info

# Check what changed
git diff                    # Unstaged changes
git diff --cached           # Staged changes
git diff HEAD               # All changes vs HEAD

# View history
git log                     # Full log
git log --oneline           # One line per commit
git log --graph --all       # Visual branch graph
git log --follow <file>     # Follow file renames
git log -p                  # Show patch (changes)
git log -S "search"         # Search for text in commits
```

**File Operations:**
```bash
# Stage files
git add <file>              # Add file
git add .                   # Add all
git add -A                  # Add all (including deletions)
git add -u                  # Add only modified/deleted
git add -p                  # Interactive staging

# Remove files
git rm <file>               # Remove and stage deletion
git rm --cached <file>      # Remove from Git but keep file
git mv <old> <new>          # Move/rename file

# Restore files
git restore <file>          # Restore from staging area (Git 2.23+)
git restore --staged <file> # Unstage file (Git 2.23+)
git restore --source=<commit> <file>  # Restore from specific commit
```

**Commit Operations:**
```bash
# Create commit
git commit -m "message"     # Commit with message
git commit -a -m "message"  # Stage all and commit
git commit --amend          # Modify last commit
git commit --amend --no-edit # Amend without changing message

# View commits
git log                     # View history
git show <commit>           # Show commit details
git show HEAD               # Show last commit
```

**Branch Operations:**
```bash
# List branches
git branch                  # Local branches
git branch -a               # All branches
git branch -r               # Remote branches only

# Create branch
git branch <name>           # Create branch
git checkout -b <name>      # Create and switch
git switch -c <name>        # Create and switch (Git 2.23+)

# Switch branch
git checkout <branch>       # Switch branch
git switch <branch>         # Switch branch (Git 2.23+)

# Delete branch
git branch -d <branch>      # Delete (safe, checks if merged)
git branch -D <branch>      # Force delete
```

---

## 🌿 Branching

### What is Branching?

**Definition:** A branch is an independent line of development. Branches allow you to work on features, fixes, or experiments without affecting the main codebase.

**Real-life example:**
Like parallel universes - you can experiment in one universe (branch) without affecting another.

**Why Branch?**
- **Isolation** - Work on features without breaking main code
- **Experimentation** - Try new ideas safely
- **Collaboration** - Multiple developers can work simultaneously
- **Organization** - Separate features, fixes, releases

### Branch Fundamentals

**What is a Branch?**
- A pointer to a specific commit
- **Location:** `.git/refs/heads/<branch-name>`
- **Content:** SHA-1 hash of a commit
- **Default:** `main` or `master` branch

**How Branches Work:**
```bash
# View current branch
git branch
# Output: * main

# View branch pointer
cat .git/refs/heads/main
# Output: a1b2c3d4e5f6... (commit SHA)

# Create new branch (creates pointer)
git branch feature-branch

# Switch branch (moves HEAD pointer)
git checkout feature-branch
# or (Git 2.23+)
git switch feature-branch
```

**Branch Creation:**
```bash
# Create branch (doesn't switch)
git branch feature-login

# Create and switch
git checkout -b feature-login
git switch -c feature-login  # Git 2.23+

# Create from specific commit
git branch feature-branch <commit-hash>

# Create from remote branch
git branch feature-branch origin/feature-branch

# Create tracking branch
git branch --track feature-branch origin/feature-branch
```

**Switching Branches:**
```bash
# Switch branch (old way)
git checkout feature-branch

# Switch branch (new way, Git 2.23+)
git switch feature-branch

# Create and switch
git switch -c new-branch

# Switch to previous branch
git switch -

# Switch and create if doesn't exist
git switch -c new-branch
```

**Branch Operations:**
```bash
# List branches
git branch                  # Local branches
git branch -a               # All branches (local + remote)
git branch -r               # Remote branches only
git branch -v               # With last commit info
git branch -vv              # With tracking info

# Rename branch
git branch -m old-name new-name          # Rename current branch
git branch -m old-branch new-branch      # Rename specific branch

# Delete branch
git branch -d branch-name   # Safe delete (checks if merged)
git branch -D branch-name   # Force delete

# Delete remote branch
git push origin --delete branch-name
git push origin :branch-name  # Old syntax
```

### Branch Strategies

**Common Branch Naming:**
```bash
# Feature branches
feature/user-authentication
feature/payment-integration
feature/add-search

# Bug fixes
bugfix/login-error
fix/memory-leak
hotfix/security-patch

# Releases
release/v1.2.0
release/2024-01

# Experiments
experiment/new-algorithm
test/performance-improvement
```

**Branch Workflow Example:**
```bash
# Start from main
git checkout main
git pull origin main

# Create feature branch
git checkout -b feature/add-user-profile

# Work on feature
echo "new feature" > profile.py
git add profile.py
git commit -m "Add user profile feature"

# Continue working...
git add .
git commit -m "Update profile styling"

# Switch back to main if needed
git checkout main

# Switch back to feature
git checkout feature/add-user-profile

# When done, merge back (covered in Merging section)
```

### Tracking Branches

**Definition:** A tracking branch is a local branch that has a direct relationship with a remote branch.

**Set Up Tracking:**
```bash
# When creating branch from remote
git checkout -b local-branch origin/remote-branch

# Set tracking for existing branch
git branch --set-upstream-to=origin/remote-branch local-branch
git branch -u origin/remote-branch local-branch

# Push and set upstream
git push -u origin branch-name
```

**Benefits of Tracking:**
- `git pull` works without specifying remote/branch
- `git status` shows ahead/behind info
- `git push` and `git pull` use tracked branch automatically

**View Tracking Info:**
```bash
# Show tracking branches
git branch -vv

# Output:
# * main      a1b2c3d [origin/main: ahead 2, behind 1] Last commit message
#   feature   d4e5f6g [origin/feature] Feature commit
```

---

## 🔀 Merging

### What is Merging?

**Definition:** Merging combines changes from different branches into a single branch, integrating development histories.

**Real-life example:**
Like merging two roads - you combine traffic from both roads into one.

**When to Merge:**
- Feature is complete and ready for main branch
- Bug fix is tested and verified
- Integrating changes from another branch

### Merge Types

**1. Fast-Forward Merge**

**Definition:** When the target branch hasn't diverged (no new commits), Git simply moves the branch pointer forward.

**Example:**
```bash
# Before merge:
# main:     A---B---C
# feature:       \
#                 D---E

# Create branch and make commits
git checkout main
git checkout -b feature-branch
git commit -m "Feature commit 1"
git commit -m "Feature commit 2"

# Switch back to main (still at C)
git checkout main

# Fast-forward merge (no merge commit needed)
git merge feature-branch
# Output: Fast-forward

# After merge:
# main:     A---B---C---D---E
# feature:  (same as main now)
```

**Force Merge Commit (even for fast-forward):**
```bash
git merge --no-ff feature-branch
# Creates merge commit even if fast-forward is possible
```

**2. Three-Way Merge**

**Definition:** When branches have diverged (both have new commits), Git creates a merge commit that combines both histories.

**Example:**
```bash
# Before merge:
# main:     A---B---C---F
# feature:      \
#                D---E

# Both branches have new commits
git checkout main
git commit -m "Main commit"  # Creates commit F

# Merge feature branch
git merge feature-branch
# Creates merge commit M

# After merge:
# main:     A---B---C---F---M
#                    \     /
# feature:           D---E
```

**Merge Commit:**
- Has two parent commits
- Combines changes from both branches
- Resolves conflicts if any

**3. Squash Merge**

**Definition:** Combines all commits from a branch into a single commit when merging.

**Example:**
```bash
# Feature branch has multiple commits
# feature: D1---D2---D3---D4

git checkout main
git merge --squash feature-branch
git commit -m "Add feature (squashed)"

# Result: All feature commits combined into one commit
# main: C---S (single commit with all changes)
```

**Use Cases:**
- Clean history (one commit per feature)
- Hide implementation details
- Simplify merge history

**Pros & Cons:**
- **Pros:** Cleaner history, easier to revert
- **Cons:** Loses individual commit history, harder to track changes

### Merge Commands

**Basic Merge:**
```bash
# Merge branch into current branch
git merge feature-branch

# Merge with message
git merge -m "Merge feature branch" feature-branch

# Abort merge (if conflicts)
git merge --abort
```

**Merge Options:**
```bash
# Fast-forward only (fail if not possible)
git merge --ff-only feature-branch

# No fast-forward (always create merge commit)
git merge --no-ff feature-branch

# Squash merge (combine commits)
git merge --squash feature-branch

# Edit merge commit message
git merge -e feature-branch
git merge --edit feature-branch
```

**Merge Strategies:**
```bash
# Recursive (default, handles most cases)
git merge -s recursive feature-branch

# Ours (keep current branch, ignore other)
git merge -s ours feature-branch

# Theirs (keep other branch, ignore current)
git merge -s theirs feature-branch

# Octopus (merge multiple branches)
git merge branch1 branch2 branch3
```

### Merge Conflicts

**Definition:** Conflicts occur when both branches modify the same part of a file differently.

**When Conflicts Happen:**
- Same line modified in both branches
- File deleted in one branch, modified in other
- File renamed differently in both branches

**Conflict Resolution Process:**
```bash
# 1. Attempt merge
git merge feature-branch
# Output: CONFLICT (content): Merge conflict in file.txt

# 2. Check status
git status
# Shows: both modified: file.txt

# 3. Open conflicted file
# File contains conflict markers:
<<<<<<< HEAD
Current branch changes
=======
Feature branch changes
>>>>>>> feature-branch

# 4. Resolve conflict (edit file, remove markers)
# Keep both, one, or create new content

# 5. Stage resolved file
git add file.txt

# 6. Complete merge
git commit
# Or: git merge --continue
```

**Conflict Markers Explained:**
```
<<<<<<< HEAD
Code from current branch (the branch you're merging INTO)
=======
Code from branch being merged (the branch you're merging FROM)
>>>>>>> branch-name
```

**Resolving Conflicts:**
```bash
# Option 1: Manual resolution (edit file)
# Remove markers, keep desired code

# Option 2: Accept current branch (ours)
git checkout --ours file.txt
git add file.txt

# Option 3: Accept incoming branch (theirs)
git checkout --theirs file.txt
git add file.txt

# Option 4: Use merge tool
git mergetool

# After resolving, complete merge
git commit
```

**View Conflicts:**
```bash
# List conflicted files
git status

# Show conflicts
git diff

# Show conflicts in staging area
git diff --cached

# Use visual merge tool
git mergetool
```

**Abort Merge:**
```bash
# Cancel merge, return to state before merge
git merge --abort

# If merge --abort doesn't work
git reset --hard HEAD
```

### Merge Best Practices

**Before Merging:**
1. Ensure working directory is clean
2. Update branches (`git pull`)
3. Run tests on feature branch
4. Review changes

**Merge Workflow:**
```bash
# 1. Update main branch
git checkout main
git pull origin main

# 2. Merge feature branch
git merge feature-branch

# 3. Resolve conflicts if any
# (edit files, git add, git commit)

# 4. Push merged changes
git push origin main

# 5. Delete feature branch (optional)
git branch -d feature-branch
git push origin --delete feature-branch
```

**Merge vs Rebase:**
- **Merge:** Preserves history, shows when branches diverged/merged
- **Rebase:** Linear history, rewrites commits
- **Rule of thumb:** Use merge for shared branches, rebase for local branches

---

## 📝 Rebasing

### What is Rebasing?

**Definition:** Rebasing moves or combines a sequence of commits to a new base commit, rewriting history to create a linear progression.

**Real-life example:**
Like replaying a movie from a different starting point - you take your changes and replay them on top of another version.

**Visual Comparison:**

**Before Rebase:**
```
main:      A---B---C
feature:      \
               D---E---F
```

**After Rebase:**
```
main:      A---B---C
feature:            \
                     D'---E'---F'
```

**Key Difference from Merge:**
- **Merge:** Creates merge commit, preserves branch structure
- **Rebase:** Rewrites commits, creates linear history

### Basic Rebase

**Rebase Command:**
```bash
# Rebase current branch onto another branch
git checkout feature-branch
git rebase main

# Rebase onto specific branch
git rebase main feature-branch
```

**Rebase Process:**
```bash
# 1. Start with feature branch
git checkout feature-branch

# 2. Rebase onto main
git rebase main

# Process:
# 1. Git finds common ancestor
# 2. Temporarily saves commits from feature-branch
# 3. Moves feature-branch to tip of main
# 4. Replays saved commits one by one
# 5. Creates new commits (different SHA-1)

# 3. If conflicts occur, resolve and continue
git add resolved-file.txt
git rebase --continue

# 4. Abort if needed
git rebase --abort
```

**Interactive Rebase:**
```bash
# Rebase last N commits interactively
git rebase -i HEAD~3        # Last 3 commits
git rebase -i HEAD~5        # Last 5 commits
git rebase -i <commit-hash> # Up to specific commit

# Interactive options:
# pick    - Use commit as-is
# reword  - Change commit message
# edit    - Stop to amend commit
# squash  - Combine with previous commit
# fixup   - Like squash, but discard message
# drop    - Remove commit
# exec    - Run shell command
```

**Interactive Rebase Example:**
```bash
# Start interactive rebase
git rebase -i HEAD~3

# Editor opens with:
pick a1b2c3d First commit
pick d4e5f6g Second commit
pick h7i8j9k Third commit

# Change to:
pick a1b2c3d First commit
squash d4e5f6g Second commit
reword h7i8j9k Third commit

# Save and close
# Git will:
# 1. Combine first and second commits
# 2. Let you edit third commit message
```

### Rebase Operations

**Rebase onto Different Base:**
```bash
# Rebase feature onto main
git checkout feature
git rebase main

# Rebase onto specific commit
git rebase <commit-hash>

# Rebase onto upstream branch
git rebase upstream/main
```

**Continue/Abort/Skip:**
```bash
# Continue rebase (after resolving conflicts)
git rebase --continue

# Abort rebase (return to state before rebase)
git rebase --abort

# Skip current commit (if conflict can't be resolved)
git rebase --skip
```

**Rebase with Merge:**
```bash
# Rebase but keep merge commits
git rebase --rebase-merges main

# Preserve merge structure
git rebase --preserve-merges main
```

### Rebase Conflicts

**Resolving Conflicts During Rebase:**
```bash
# 1. Start rebase
git rebase main
# Output: CONFLICT (content): Merge conflict in file.txt

# 2. Resolve conflict (same as merge)
# Edit file, remove conflict markers

# 3. Stage resolved file
git add file.txt

# 4. Continue rebase
git rebase --continue

# 5. Repeat for each conflicted commit

# Or abort
git rebase --abort
```

**Rebase vs Merge Conflicts:**
- **Merge:** One conflict resolution for entire merge
- **Rebase:** May need to resolve conflicts for each commit being rebased

### When to Use Rebase

**Use Rebase For:**
- ✅ Local feature branches (before merging to main)
- ✅ Cleaning up commit history
- ✅ Maintaining linear history
- ✅ Updating feature branch with latest main

**Don't Use Rebase For:**
- ❌ Shared/public branches (rewrites history others depend on)
- ❌ Branches others are working on
- ❌ Already pushed branches (unless team agrees)

**Golden Rule:**
> **Never rebase commits that have been pushed to a shared repository**

### Rebase Best Practices

**Before Rebasing:**
```bash
# 1. Ensure working directory is clean
git status

# 2. Update base branch
git checkout main
git pull origin main

# 3. Backup branch (optional but recommended)
git branch feature-backup
```

**Rebase Workflow:**
```bash
# 1. Work on feature branch
git checkout feature-branch

# 2. Rebase onto updated main
git rebase main

# 3. Resolve conflicts if any
# (edit, git add, git rebase --continue)

# 4. Force push (if already pushed)
git push --force-with-lease origin feature-branch
# --force-with-lease is safer than --force
```

**Interactive Rebase for Clean History:**
```bash
# Clean up commits before merging
git rebase -i main

# Common operations:
# - squash: Combine related commits
# - reword: Fix commit messages
# - drop: Remove unnecessary commits
# - edit: Fix bugs in commits
```

---

## 🍒 Cherry-Pick

### What is Cherry-Pick?

**Definition:** Cherry-pick applies a specific commit from one branch to another, creating a new commit with the same changes but different SHA-1.

**Real-life example:**
Like copying a specific page from one book to another - you take one piece and add it elsewhere.

**When to Use:**
- Apply a bug fix from one branch to another
- Port a feature commit to release branch
- Select specific commits without merging entire branch

### Basic Cherry-Pick

**Cherry-Pick Single Commit:**
```bash
# Switch to target branch
git checkout main

# Cherry-pick commit from another branch
git cherry-pick <commit-hash>

# Example:
git cherry-pick a1b2c3d
```

**Cherry-Pick Multiple Commands:**
```bash
# Cherry-pick range of commits
git cherry-pick <start-commit>..<end-commit>
# Note: Excludes start-commit, includes end-commit

# Cherry-pick range including start
git cherry-pick <start-commit>^..<end-commit>

# Cherry-pick multiple specific commits
git cherry-pick commit1 commit2 commit3

# Cherry-pick from another branch
git cherry-pick branch-name
# Picks the commit at tip of branch-name
```

**Cherry-Pick Options:**
```bash
# Cherry-pick without committing (just stage changes)
git cherry-pick --no-commit <commit>

# Cherry-pick without committing, don't stage
git cherry-pick --no-commit --no-stage <commit>

# Edit commit message
git cherry-pick -e <commit>
git cherry-pick --edit <commit>

# Continue after conflict resolution
git cherry-pick --continue

# Abort cherry-pick
git cherry-pick --abort

# Skip current commit (if can't resolve)
git cherry-pick --skip
```

### Cherry-Pick Workflow

**Example Scenario:**
```bash
# Bug fix made in feature branch
# main:     A---B---C
# feature:      \
#                D---E---F (F is the bug fix)

# Apply fix to main
git checkout main
git cherry-pick F

# Result:
# main:     A---B---C---F'
# feature:      \
#                D---E---F
```

**Real-World Example:**
```bash
# 1. Find commit hash in feature branch
git log feature-branch --oneline
# Output:
# a1b2c3d Add user authentication
# d4e5f6g Fix login bug
# h7i8j9k Add password reset

# 2. Switch to main
git checkout main

# 3. Cherry-pick the bug fix
git cherry-pick d4e5f6g

# 4. Resolve conflicts if any
git add resolved-file.txt
git cherry-pick --continue
```

### Cherry-Pick Conflicts

**Resolving Conflicts:**
```bash
# 1. Cherry-pick commit
git cherry-pick <commit>
# Output: CONFLICT

# 2. Resolve conflicts (same as merge)
# Edit files, remove conflict markers

# 3. Stage resolved files
git add resolved-file.txt

# 4. Continue
git cherry-pick --continue

# Or abort
git cherry-pick --abort
```

### Cherry-Pick Best Practices

**When to Use:**
- ✅ Applying hotfix to multiple branches
- ✅ Porting specific feature to release branch
- ✅ Selecting commits without merging entire branch

**When Not to Use:**
- ❌ Many commits (consider merge instead)
- ❌ Commits with dependencies (may cause issues)
- ❌ Frequently (indicates branch strategy issues)

**Tips:**
- Use `git log` to find commit hashes
- Test after cherry-picking
- Document why commit was cherry-picked
- Consider merge if many related commits

---

## ⏪ Reset

### What is Reset?

**Definition:** Reset moves the HEAD pointer (and optionally the index and working directory) to a specific commit, effectively "undoing" commits.

**Real-life example:**
Like rewinding a video tape to a previous point - you go back in time.

**⚠️ Warning:** Reset can be destructive, especially with `--hard`. Use carefully!

### Reset Modes

**Three Reset Modes:**

1. **`--soft`** - Moves HEAD only, keeps staging area and working directory unchanged
2. **`--mixed`** (default) - Moves HEAD and staging area, keeps working directory unchanged
3. **`--hard`** - Moves HEAD, staging area, and working directory (DESTRUCTIVE)

**Visual Comparison:**

**Before Reset:**
```
HEAD → C (current commit)
Index: Staged changes
Working: Modified files
```

**After `git reset --soft HEAD~1`:**
```
HEAD → B (moved back)
Index: Changes from C are staged
Working: Unchanged
```

**After `git reset --mixed HEAD~1` (or `git reset HEAD~1`):**
```
HEAD → B (moved back)
Index: Empty (unstaged)
Working: Changes from C are in working directory
```

**After `git reset --hard HEAD~1`:**
```
HEAD → B (moved back)
Index: Empty
Working: Clean (changes lost!)
```

### Reset Commands

**Reset to Previous Commit:**
```bash
# Soft reset (keep changes staged)
git reset --soft HEAD~1

# Mixed reset (default, keep changes unstaged)
git reset HEAD~1
git reset --mixed HEAD~1

# Hard reset (DESTRUCTIVE, lose changes)
git reset --hard HEAD~1
```

**Reset to Specific Commit:**
```bash
# Reset to commit hash
git reset --soft <commit-hash>
git reset --mixed <commit-hash>
git reset --hard <commit-hash>

# Reset to branch
git reset --hard origin/main
```

**Reset Specific Files:**
```bash
# Unstage file (reset from staging area)
git reset HEAD <file>
git restore --staged <file>  # Git 2.23+

# Reset file to HEAD version
git checkout HEAD -- <file>
git restore <file>  # Git 2.23+
```

### Reset Use Cases

**Undo Last Commit (Keep Changes):**
```bash
# Made a mistake in commit message or forgot to add file
git reset --soft HEAD~1
# Edit files if needed
git add forgotten-file.txt
git commit -m "Correct commit message"
```

**Unstage Files:**
```bash
# Accidentally staged too much
git reset HEAD <file>
# Or unstage all
git reset HEAD
```

**Discard Local Changes:**
```bash
# ⚠️ DESTRUCTIVE - loses all uncommitted changes
git reset --hard HEAD
# Or reset to specific commit
git reset --hard <commit-hash>
```

### Reset vs Revert

**Key Differences:**
- **Reset**: Moves HEAD pointer (rewrites history) - use for local commits
- **Revert**: Creates new commit that undoes changes (preserves history) - use for shared commits

**When to Use:**
- **Reset**: Local commits, fixing mistakes before pushing
- **Revert**: Commits already pushed to remote (safe for shared history)

---

## ↪️ Revert

### What is Revert?

**Definition:** `git revert` creates a new commit that undoes changes from a previous commit, without rewriting history.

**Real-life example:**
Like adding a correction note instead of erasing the mistake - the mistake stays in history, but you add a fix.

**Key Points:**
- Creates new commit (doesn't delete old commits)
- Safe for shared branches (doesn't rewrite history)
- Can revert multiple commits
- Can revert merge commits

### Basic Revert

**Revert Last Commit:**
```bash
# Revert the most recent commit
git revert HEAD

# Revert specific commit (by hash)
git revert <commit-hash>

# Revert commit with custom message
git revert <commit-hash> -m "Revert: Fixed bug in payment processing"
```

**Example:**
```bash
# History before revert:
# A - B - C (HEAD)

# After: git revert C
# A - B - C - C' (HEAD)
# C' undoes changes from C
```

### Revert Multiple Commands

**Revert Range of Commits:**
```bash
# Revert commits from HEAD~3 to HEAD (3 commits)
git revert HEAD~3..HEAD

# Revert commits in reverse order (oldest first)
git revert --no-commit HEAD~3..HEAD
git commit -m "Revert multiple commits"

# Revert without creating commit (manual commit)
git revert --no-commit <commit-hash>
# Make changes if needed
git commit -m "Revert and fix"
```

### Revert Merge Commands

**Revert a Merge Commit:**
```bash
# Revert merge commit (specify parent)
git revert -m 1 <merge-commit-hash>

# -m 1 means: revert to first parent (main branch)
# -m 2 means: revert to second parent (feature branch)
```

**Example:**
```bash
# Merge scenario:
#   main:  A - B - C - E (merge commit)
#              \       /
#   feature:    D --- F

# Revert merge commit E:
git revert -m 1 E

# Result: New commit that undoes the merge
```

### Revert Conflicts

**Handling Revert Conflicts:**
```bash
# Start revert (may have conflicts)
git revert <commit-hash>

# If conflicts occur:
# 1. Git shows conflicted files
# 2. Resolve conflicts manually
# 3. Stage resolved files
git add <resolved-file>

# 4. Continue revert
git revert --continue

# Or abort revert
git revert --abort
```

### Revert Use Cases

**Undo Bad Commit (Already Pushed):**
```bash
# Commit already pushed to remote
git revert <bad-commit-hash>
git push origin main
# Creates new commit that undoes the bad commit
```

**Undo Feature Merge:**
```bash
# Feature merged but causing issues
git revert -m 1 <merge-commit-hash>
git push origin main
```

**Undo Multiple Commits:**
```bash
# Revert range of commits
git revert --no-commit HEAD~5..HEAD
# Review changes
git status
# Commit all reverts together
git commit -m "Revert problematic commits"
```

### Revert Best Practices

**DO:**
- ✅ Use revert for commits already pushed
- ✅ Use revert for shared branches
- ✅ Write clear revert commit messages
- ✅ Test after reverting

**DON'T:**
- ❌ Revert commits that others are building on
- ❌ Revert without understanding impact
- ❌ Force push after revert (usually not needed)

### Reset vs Revert Comparison

| Aspect | Reset | Revert |
|--------|-------|--------|
| History | Rewrites | Preserves |
| Safe for shared commits | ❌ No | ✅ Yes |
| Creates new commit | ❌ No | ✅ Yes |
| Use case | Local commits | Shared commits |
| Can undo | Yes | Yes |
| Remote impact | Requires force push | Safe push |

---

## 📦 Stash

### What is Stash?

**Definition:** `git stash` temporarily saves uncommitted changes so you can work on something else, then reapply them later.

**Real-life example:**
Like putting work in a drawer temporarily - you save it, clear your desk, do something else, then get it back.

**Key Points:**
- Saves changes without committing
- Cleans working directory
- Can stash multiple times
- Can apply stashed changes later
- Can manage multiple stashes

### Basic Stash

**Stash Current Changes:**
```bash
# Stash all uncommitted changes (staged + unstaged)
git stash

# Stash with message
git stash save "Working on feature X"

# Stash including untracked files
git stash -u
git stash --include-untracked

# Stash including ignored files (rare)
git stash -a
git stash --all
```

**Apply Stashed Changes:**
```bash
# Apply most recent stash (keeps stash)
git stash apply

# Apply specific stash
git stash apply stash@{2}

# Apply and remove stash (pop)
git stash pop

# Apply specific stash and remove it
git stash pop stash@{1}
```

### Stash Commands

**View Stashes:**
```bash
# List all stashes
git stash list

# Show stash contents
git stash show

# Show detailed diff
git stash show -p
git stash show stash@{0} -p
```

**Manage Stashes:**
```bash
# Delete specific stash
git stash drop stash@{1}

# Delete all stashes
git stash clear

# Create stash without applying it
git stash create "message"

# Apply stash to specific branch
git stash branch new-branch stash@{1}
```

### Stash Use Cases

**Switch Branches Temporarily:**
```bash
# Working on feature, need to fix urgent bug
git stash save "WIP: feature X"
git checkout main
# Fix bug
git checkout feature
git stash pop  # Resume work
```

**Save Work Before Pulling:**
```bash
# Have uncommitted changes, need to pull
git stash
git pull
git stash pop  # Reapply changes
```

**Stash Partially:**
```bash
# Stash specific files only
git stash push -m "message" file1.txt file2.txt

# Stash all except specific files
git stash push --keep-index
# This keeps staged files, stashes unstaged
```

### Stash Advanced

**Stash with Index (Keep Staged Changes):**
```bash
# Stash unstaged changes, keep staged changes
git stash --keep-index

# Useful when you want to commit some changes
# but save others for later
```

**Interactive Stash:**
```bash
# Stash interactively (choose what to stash)
git stash -p
git stash --patch

# Git will ask for each change: stash/discard/quit
```

**Stash Multiple Times:**
```bash
# First stash
git stash save "First work"

# Continue working
git stash save "Second work"

# List stashes
git stash list
# stash@{0}: WIP on main: Second work
# stash@{1}: WIP on main: First work

# Apply in order
git stash pop  # Applies Second work
git stash pop  # Applies First work
```

### Stash Best Practices

**DO:**
- ✅ Use descriptive stash messages
- ✅ Apply stashes soon (don't forget them)
- ✅ Review stash contents before applying
- ✅ Clean up old stashes regularly

**DON'T:**
- ❌ Use stash as permanent storage
- ❌ Stash everything (consider committing instead)
- ❌ Forget to apply stashes

---

## 📝 Commit Management

### Commit Messages

**Definition:** Commit messages document what changes were made and why.

**Real-life example:**
Like a note on a package - explains what's inside and why it was sent.

**Good Commit Message Format:**
```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting
- `refactor`: Code restructuring
- `test`: Adding tests
- `chore`: Maintenance

**Examples:**
```bash
# Good commit message
git commit -m "feat(auth): add JWT token refresh endpoint

- Implement token refresh logic
- Add refresh endpoint to API
- Update authentication tests

Closes #123"

# Also good (simpler)
git commit -m "fix: resolve N+1 query in student list view"
```

### Amending Commands

**Amend Last Commit:**
```bash
# Add forgotten file to last commit
git add forgotten-file.txt
git commit --amend

# Amend commit message
git commit --amend -m "New message"

# Amend without changing message
git commit --amend --no-edit
```

**⚠️ Warning:** Don't amend commits that are already pushed (use revert instead).

### Commit History

**View Commit History:**
```bash
# View commit log
git log

# One line per commit
git log --oneline

# Graph view
git log --graph --oneline --all

# Last N commits
git log -n 5

# Since specific date
git log --since="2024-01-01"

# Author-specific
git log --author="John"
```

**Search Commit History:**
```bash
# Search in commit messages
git log --grep="bug fix"

# Search in code changes
git log -S "function_name"

# Search by file
git log -- path/to/file

# Combined search
git log --grep="auth" --author="John" --since="2024-01-01"
```

### Interactive Rebase

**Definition:** Interactive rebase lets you edit, reorder, or squash commits.

**Start Interactive Rebase:**
```bash
# Rebase last 3 commits
git rebase -i HEAD~3

# Rebase from specific commit
git rebase -i <commit-hash>

# Rebase from branch point
git rebase -i origin/main
```

**Interactive Rebase Commands:**
```
pick - use commit as is
reword - change commit message
edit - stop and edit commit
squash - combine with previous commit
fixup - like squash but discard message
drop - remove commit
```

**Example Workflow:**
```bash
# Start interactive rebase
git rebase -i HEAD~3

# Editor opens:
# pick abc123 First commit
# squash def456 Second commit
# reword ghi789 Third commit

# After editing, Git will:
# 1. Stop at commits marked 'edit'
# 2. Combine 'squash' commits
# 3. Ask for new messages for 'reword'
```

**Squash Commits:**
```bash
# Combine last 3 commits into one
git rebase -i HEAD~3
# Change 'pick' to 'squash' for commits 2 and 3
# Save and edit final commit message
```

### Commit Best Practices

**DO:**
- ✅ Write clear, descriptive messages
- ✅ Make atomic commits (one logical change)
- ✅ Use conventional commit format
- ✅ Review commits before pushing

**DON'T:**
- ❌ Commit unrelated changes together
- ❌ Write vague messages like "fix" or "update"
- ❌ Amend pushed commits
- ❌ Force push after rebase (coordinate with team)

---

## 🏷️ Tags

### What are Tags?

**Definition:** Tags mark specific points in history, typically for releases (v1.0, v2.0, etc.).

**Real-life example:**
Like a bookmark in a book - marks important pages for easy reference.

**Types:**
- **Lightweight tags**: Just a pointer to a commit
- **Annotated tags**: Full object with metadata (recommended)

### Creating Tags

**Annotated Tags (Recommended):**
```bash
# Create annotated tag
git tag -a v1.0.0 -m "Release version 1.0.0"

# Create tag for specific commit
git tag -a v1.0.0 <commit-hash> -m "Release version 1.0.0"

# Tag current commit
git tag -a v1.0.0 -m "Release version 1.0.0"
```

**Lightweight Tags:**
```bash
# Create lightweight tag (no message)
git tag v1.0.0

# Create for specific commit
git tag v1.0.0 <commit-hash>
```

### Tag Commands

**List Tags:**
```bash
# List all tags
git tag

# List tags matching pattern
git tag -l "v1.*"

# Show tag details
git show v1.0.0
```

**Delete Tags:**
```bash
# Delete local tag
git tag -d v1.0.0

# Delete remote tag
git push origin --delete v1.0.0
# Or
git push origin :refs/tags/v1.0.0
```

**Push Tags:**
```bash
# Push single tag
git push origin v1.0.0

# Push all tags
git push origin --tags

# Push annotated tags only
git push --follow-tags
```

### Tag Use Cases

**Release Tags:**
```bash
# Create release tag
git tag -a v1.2.3 -m "Release 1.2.3: Added user authentication"
git push origin v1.2.3

# Checkout specific release
git checkout v1.2.3
```

**Semantic Versioning:**
```bash
# Major version (breaking changes)
git tag -a v2.0.0 -m "Major release: API v2"

# Minor version (new features)
git tag -a v1.3.0 -m "Minor release: Added payments"

# Patch version (bug fixes)
git tag -a v1.2.1 -m "Patch: Fixed security issue"
```

### Tag Best Practices

**DO:**
- ✅ Use annotated tags for releases
- ✅ Follow semantic versioning
- ✅ Write descriptive tag messages
- ✅ Push tags with commits

**DON'T:**
- ❌ Move tags (recreate if needed)
- ❌ Tag every commit
- ❌ Forget to push tags

---

## 📊 Diff & Log

### Git Diff

**Definition:** `git diff` shows changes between commits, branches, or working directory.

**Real-life example:**
Like a before/after comparison - shows what changed.

### Diff Commands

**Working Directory Diff:**
```bash
# Show unstaged changes
git diff

# Show staged changes
git diff --staged
git diff --cached

# Show all changes (staged + unstaged)
git diff HEAD
```

**Commit Diff:**
```bash
# Compare with HEAD
git diff HEAD~1

# Compare two commits
git diff <commit1> <commit2>

# Compare with branch
git diff main..feature

# Compare specific file
git diff HEAD~1 -- path/to/file
```

**Diff Options:**
```bash
# Stat only (file list)
git diff --stat

# Word diff (highlights word changes)
git diff --word-diff

# Ignore whitespace
git diff -w

# Show only names
git diff --name-only

# Unified diff format
git diff -u
```

### Git Log

**Basic Log:**
```bash
# Full log
git log

# One line format
git log --oneline

# Graph view
git log --graph --oneline --all

# Decorate (show branch/tag names)
git log --decorate

# Combined
git log --oneline --graph --decorate --all
```

**Filtering Log:**
```bash
# Last N commits
git log -n 10

# Since date
git log --since="2 weeks ago"
git log --since="2024-01-01"
git log --since="yesterday"

# Until date
git log --until="2024-12-31"

# By author
git log --author="John Doe"

# By file
git log -- path/to/file

# Search in messages
git log --grep="bug fix"

# Search in code
git log -S "function_name"
```

**Log Formatting:**
```bash
# Custom format
git log --pretty=format:"%h - %an, %ar : %s"

# Format options:
# %h - short hash
# %H - full hash
# %an - author name
# %ae - author email
# %ar - author date (relative)
# %s - subject
# %b - body
```

**Log Examples:**
```bash
# Show commits with stats
git log --stat

# Show commits with patches
git log -p

# Show file changes only
git log --name-status

# Follow file renames
git log --follow -- path/to/file
```

### Log Best Practices

**DO:**
- ✅ Use filters to find specific commits
- ✅ Use --oneline for quick overview
- ✅ Use --graph to see branch structure
- ✅ Combine options for better views

---

## 🌐 Remote Repositories

### What are Remotes?

**Definition:** Remotes are references to other repositories (usually on GitHub, GitLab, etc.).

**Real-life example:**
Like a shortcut to a friend's house - you know where it is and can visit.

**Common Remotes:**
- `origin` - Default remote (usually where you cloned from)
- `upstream` - Original repository (for forks)
- Custom names for other remotes

### Remote Commands

**View Remotes:**
```bash
# List all remotes
git remote

# List with URLs
git remote -v

# Show remote details
git remote show origin
```

**Add Remote:**
```bash
# Add remote
git remote add <name> <url>

# Examples
git remote add origin https://github.com/user/repo.git
git remote add upstream https://github.com/original/repo.git

# Add remote with different protocol
git remote add origin git@github.com:user/repo.git  # SSH
```

**Remove Remote:**
```bash
# Remove remote
git remote remove <name>
git remote rm <name>

# Example
git remote remove origin
```

**Update Remote URL:**
```bash
# Change remote URL
git remote set-url <name> <new-url>

# Example: Switch from HTTPS to SSH
git remote set-url origin git@github.com:user/repo.git
```

**Rename Remote:**
```bash
# Rename remote
git remote rename <old-name> <new-name>

# Example
git remote rename origin upstream
```

### Remote Best Practices

**DO:**
- ✅ Use descriptive remote names
- ✅ Keep remote URLs updated
- ✅ Use SSH for authentication (more secure)

**DON'T:**
- ❌ Delete remotes without checking
- ❌ Share credentials in URLs

---

## 🔄 Fetch, Pull, Push

### Git Fetch

**Definition:** `git fetch` downloads changes from remote but doesn't merge them.

**Real-life example:**
Like checking the mailbox - you see what's new but don't bring it inside yet.

**Fetch Commands:**
```bash
# Fetch from origin (default remote)
git fetch

# Fetch from specific remote
git fetch origin

# Fetch specific branch
git fetch origin main

# Fetch all remotes
git fetch --all

# Fetch and prune (remove deleted remote branches)
git fetch --prune
git fetch -p
```

**What Fetch Does:**
- Downloads commits, branches, tags from remote
- Updates remote-tracking branches (origin/main)
- Does NOT modify your working directory
- Does NOT merge changes

**After Fetch:**
```bash
# See what changed
git log origin/main..main  # Local commits not on remote
git log main..origin/main  # Remote commits not local

# Merge fetched changes
git merge origin/main

# Or rebase on fetched changes
git rebase origin/main
```

### Git Pull

**Definition:** `git pull` fetches and merges changes from remote in one command.

**Real-life example:**
Like fetch + merge combined - gets new mail and brings it inside.

**Pull Commands:**
```bash
# Pull from origin (current branch)
git pull

# Pull from specific remote/branch
git pull origin main

# Pull with rebase (instead of merge)
git pull --rebase origin main

# Pull only (don't merge if fast-forward not possible)
git pull --ff-only
```

**Pull = Fetch + Merge:**
```bash
# These are equivalent:
git pull origin main
# Same as:
git fetch origin main
git merge origin/main
```

**Pull with Rebase:**
```bash
# Pull and rebase (linear history)
git pull --rebase origin main
# Same as:
git fetch origin main
git rebase origin/main
```

**Pull Best Practices:**
- ✅ Pull before starting work
- ✅ Use `--rebase` for cleaner history
- ✅ Resolve conflicts immediately
- ✅ Review changes before pulling

### Git Push

**Definition:** `git push` uploads local commits to remote repository.

**Real-life example:**
Like sending your work to someone - uploads your changes.

**Push Commands:**
```bash
# Push current branch to origin
git push

# Push specific branch
git push origin main

# Push to different remote
git push upstream main

# Push and set upstream
git push -u origin feature-branch
# Sets tracking, future pushes just need: git push

# Push all branches
git push --all origin

# Force push (⚠️ dangerous)
git push --force origin main
git push -f origin main

# Force push with lease (safer)
git push --force-with-lease origin main
```

**Push Tags:**
```bash
# Push single tag
git push origin v1.0.0

# Push all tags
git push origin --tags

# Push commits and tags
git push --follow-tags
```

**Force Push:**
```bash
# ⚠️ DANGEROUS: Rewrites remote history
git push --force origin main

# Safer: Only force if remote hasn't changed
git push --force-with-lease origin main

# When to use force push:
# - After rebase (coordinate with team)
# - After amending commits (before sharing)
# - NEVER on shared branches without coordination
```

### Push Best Practices

**DO:**
- ✅ Push regularly (don't accumulate commits)
- ✅ Use `--force-with-lease` instead of `--force`
- ✅ Push tags with releases
- ✅ Coordinate force pushes with team

**DON'T:**
- ❌ Force push to main/master
- ❌ Force push without team agreement
- ❌ Push broken code
- ❌ Push sensitive data

---

## ⚔️ Conflict Resolution

### What are Conflicts?

**Definition:** Conflicts occur when Git can't automatically merge changes from different branches.

**Real-life example:**
Like two people editing the same document - Git needs you to decide which version to keep.

**Conflict Scenarios:**
- Same file modified in different branches
- One branch deletes file, other modifies it
- Merge conflicts during `git merge`
- Rebase conflicts during `git rebase`

### Understanding Conflicts

**Conflict Markers:**
```
<<<<<<< HEAD (current branch)
Your changes
=======
Incoming changes
>>>>>>> branch-name (incoming branch)
```

**Conflict Resolution:**
1. Keep your changes (remove conflict markers, keep your code)
2. Keep incoming changes (remove conflict markers, keep their code)
3. Keep both (combine changes)
4. Write new code (custom resolution)

### Merge Conflicts

**During Merge:**
```bash
# Merge causes conflict
git merge feature-branch

# Git shows conflicted files
# Unmerged paths:
#   both modified: file.txt

# Resolve conflicts in files
# Edit file.txt, remove markers, keep desired code

# Stage resolved files
git add file.txt

# Complete merge
git commit
```

**Abort Merge:**
```bash
# Cancel merge (go back to before merge)
git merge --abort
```

### Rebase Conflicts

**During Rebase:**
```bash
# Rebase causes conflict
git rebase main

# Git shows conflicted files
# Resolve conflicts

# Stage resolved files
git add file.txt

# Continue rebase
git rebase --continue

# Or skip this commit
git rebase --skip

# Or abort rebase
git rebase --abort
```

### Conflict Resolution Tools

**Manual Resolution:**
```bash
# 1. Edit conflicted files
# 2. Remove conflict markers
# 3. Keep desired code
# 4. Stage files: git add
# 5. Continue: git commit or git rebase --continue
```

**Using Merge Tools:**
```bash
# Open merge tool
git mergetool

# Configure merge tool (VS Code example)
git config --global merge.tool vscode
git config --global mergetool.vscode.cmd 'code --wait $MERGED'

# List available tools
git mergetool --tool-help
```

**Common Merge Tools:**
- VS Code: `code --wait $MERGED`
- Vim: Built-in
- Beyond Compare: Commercial
- KDiff3: Cross-platform
- Meld: Linux/Windows

### Conflict Prevention

**Best Practices:**
- ✅ Pull/rebase regularly
- ✅ Keep branches short-lived
- ✅ Communicate with team
- ✅ Review changes before merging
- ✅ Use smaller, focused commits

---

## 🍴 Forking Workflow

### What is Forking?

**Definition:** Forking creates your own copy of a repository that you can modify independently.

**Real-life example:**
Like photocopying a document - you get your own copy to edit.

**Common Use Cases:**
- Contributing to open source projects
- Creating your own version of a project
- Experimenting without affecting original

### Forking Workflow

**1. Fork Repository:**
```bash
# On GitHub/GitLab: Click "Fork" button
# Creates your copy: github.com/your-username/repo
```

**2. Clone Your Fork:**
```bash
# Clone your fork
git clone https://github.com/your-username/repo.git
cd repo
```

**3. Add Upstream Remote:**
```bash
# Add original repo as upstream
git remote add upstream https://github.com/original-owner/repo.git

# Verify remotes
git remote -v
# origin    https://github.com/your-username/repo.git (your fork)
# upstream  https://github.com/original-owner/repo.git (original)
```

**4. Create Feature Branch:**
```bash
# Create branch for your changes
git checkout -b feature-branch

# Make changes
# Commit changes
git commit -m "Add new feature"
```

**5. Push to Your Fork:**
```bash
# Push to your fork
git push origin feature-branch
```

**6. Sync with Upstream:**
```bash
# Fetch upstream changes
git fetch upstream

# Merge upstream changes into your branch
git merge upstream/main

# Or rebase your branch on upstream
git rebase upstream/main
```

**7. Create Pull Request:**
```bash
# On GitHub/GitLab: Create Pull Request
# From: your-username/repo:feature-branch
# To: original-owner/repo:main
```

### Forking Best Practices

**DO:**
- ✅ Keep fork synced with upstream
- ✅ Use feature branches
- ✅ Write clear PR descriptions
- ✅ Test before submitting PR

**DON'T:**
- ❌ Work directly on main branch
- ❌ Let fork get too far behind
- ❌ Submit incomplete work

---

## 🔀 Git Workflow Strategies

### Git Flow

**Definition:** Git Flow is a branching model with specific branch types for different purposes.

**Branch Types:**
- `main/master` - Production code
- `develop` - Integration branch
- `feature/*` - New features
- `release/*` - Preparing releases
- `hotfix/*` - Urgent production fixes

**Workflow:**
```bash
# Start feature
git checkout -b feature/user-auth develop

# Work on feature
git commit -m "Add user authentication"

# Finish feature
git checkout develop
git merge --no-ff feature/user-auth
git branch -d feature/user-auth

# Create release
git checkout -b release/1.0.0 develop
# Fix bugs, don't add features
git checkout main
git merge --no-ff release/1.0.0
git tag -a v1.0.0

# Hotfix
git checkout -b hotfix/critical-bug main
# Fix bug
git checkout main
git merge --no-ff hotfix/critical-bug
git tag -a v1.0.1
```

### GitHub Flow

**Definition:** Simpler workflow with just main branch and feature branches.

**Workflow:**
```bash
# Create feature branch from main
git checkout -b feature/new-feature

# Make changes and commit
git commit -m "Add feature"

# Push and create PR
git push origin feature/new-feature

# After PR approved, merge to main
git checkout main
git pull
git merge feature/new-feature
git push
```

**Benefits:**
- Simple
- Fast
- Good for continuous deployment

### GitLab Flow

**Definition:** Similar to GitHub Flow but with environment branches.

**Branch Types:**
- `main` - Production
- `pre-production` - Staging
- `feature/*` - Features

**Workflow:**
```bash
# Create feature from main
git checkout -b feature/new-feature main

# Merge to main (auto-deploys to pre-production)
# Merge main to pre-production (test)
# Merge pre-production to production (deploy)
```

### Trunk-Based Development

**Definition:** All developers work on main branch, use short-lived branches.

**Principles:**
- Small, frequent commits
- Short-lived branches (< 1 day)
- Continuous integration
- Feature flags for incomplete features

**Workflow:**
```bash
# Create short-lived branch
git checkout -b fix-bug

# Make small change
git commit -m "Fix bug"

# Merge immediately
git checkout main
git merge fix-bug
git push
```

### Choosing Workflow

**Use Git Flow when:**
- Multiple releases in parallel
- Need strict release management
- Large team

**Use GitHub Flow when:**
- Simple project
- Continuous deployment
- Small team

**Use Trunk-Based when:**
- Rapid development
- Strong CI/CD
- Team comfortable with frequent merges

---

## 🪝 Git Hooks

### What are Git Hooks?

**Definition:** Git hooks are scripts that run automatically at certain Git events.

**Real-life example:**
Like automatic actions - when something happens, do something else.

**Hook Types:**
- **Client-side hooks** - Run on your machine
- **Server-side hooks** - Run on Git server

### Client-Side Hooks

**pre-commit:**
```bash
# .git/hooks/pre-commit
#!/bin/sh
# Run tests before commit
npm test
if [ $? -ne 0 ]; then
  echo "Tests failed, commit aborted"
  exit 1
fi
```

**commit-msg:**
```bash
# .git/hooks/commit-msg
#!/bin/sh
# Validate commit message format
if ! grep -qE "^(feat|fix|docs|style|refactor|test|chore):" "$1"; then
  echo "Commit message must start with type (feat, fix, etc.)"
  exit 1
fi
```

**post-commit:**
```bash
# .git/hooks/post-commit
#!/bin/sh
# Notify after commit
echo "Commit successful!"
```

### Server-Side Hooks

**pre-receive:**
```bash
# Runs on server before accepting pushes
# Can reject pushes that don't meet criteria
```

**update:**
```bash
# Runs for each branch being updated
# Can enforce branch protection rules
```

**post-receive:**
```bash
# Runs after accepting pushes
# Often used for deployment
```

### Installing Hooks

**Manual Installation:**
```bash
# Hooks are in .git/hooks/
ls .git/hooks/

# Make hook executable
chmod +x .git/hooks/pre-commit

# Edit hook
vim .git/hooks/pre-commit
```

**Using Hook Frameworks:**
```bash
# pre-commit framework (Python)
pip install pre-commit
pre-commit install

# husky (Node.js)
npm install husky --save-dev
npx husky install
```

### Common Hooks

**Pre-commit Checks:**
- Run linters
- Run tests
- Check code formatting
- Validate commit messages

**Post-commit Actions:**
- Send notifications
- Update documentation
- Trigger builds

---

## 📚 Git Submodules

### What are Submodules?

**Definition:** Submodules allow you to include one Git repository inside another.

**Real-life example:**
Like including a library as a separate project within your project.

**Use Cases:**
- Including shared libraries
- Including vendor code
- Including documentation from separate repo

### Submodule Commands

**Add Submodule:**
```bash
# Add submodule
git submodule add https://github.com/user/library.git libs/library

# This creates:
# - libs/library/ (the submodule)
# - .gitmodules (config file)
```

**Clone Repository with Submodules:**
```bash
# Clone with submodules
git clone --recurse-submodules <repo-url>

# Or clone then init submodules
git clone <repo-url>
git submodule init
git submodule update

# Or combine
git submodule update --init --recursive
```

**Update Submodules:**
```bash
# Update submodules to latest
git submodule update --remote

# Update specific submodule
git submodule update --remote libs/library

# Update and merge
git submodule update --remote --merge
```

**Remove Submodule:**
```bash
# Remove submodule
git submodule deinit libs/library
git rm libs/library
rm -rf .git/modules/libs/library
```

### Submodule Best Practices

**DO:**
- ✅ Document why submodules are used
- ✅ Keep submodules updated
- ✅ Use for stable dependencies

**DON'T:**
- ❌ Use for frequently changing code
- ❌ Forget to update submodules
- ❌ Modify submodule code directly (use fork)

---

## 🌳 Git Subtrees

### What are Subtrees?

**Definition:** Subtrees merge external repositories into your repository as subdirectories.

**Real-life example:**
Like copying a library into your project (not a separate repo).

### Subtree Commands

**Add Subtree:**
```bash
# Add subtree
git subtree add --prefix=libs/library \
  https://github.com/user/library.git main --squash

# --prefix: where to put it
# --squash: combine all commits into one
```

**Update Subtree:**
```bash
# Pull updates from subtree
git subtree pull --prefix=libs/library \
  https://github.com/user/library.git main --squash
```

**Push to Subtree:**
```bash
# Push changes back to subtree
git subtree push --prefix=libs/library \
  https://github.com/user/library.git main
```

### Subtree vs Submodule

| Aspect | Subtree | Submodule |
|--------|---------|-----------|
| History | Merged into main repo | Separate repo |
| Complexity | Simpler | More complex |
| Updates | Easier | More steps |
| Use case | Static dependencies | Active development |

---

## 🚫 Git Ignore

### What is .gitignore?

**Definition:** `.gitignore` tells Git which files to ignore (not track).

**Real-life example:**
Like a "do not disturb" list - files Git should leave alone.

### .gitignore Patterns

**Basic Patterns:**
```
# Ignore file
file.txt

# Ignore directory
node_modules/

# Ignore all .log files
*.log

# Ignore in specific directory
logs/*.log

# Ignore everywhere
**/*.tmp

# Don't ignore (exception)
!important.log
```

**Common Patterns:**
```
# Dependencies
node_modules/
vendor/
venv/

# Build outputs
dist/
build/
*.pyc
__pycache__/

# IDE
.vscode/
.idea/
*.swp

# OS
.DS_Store
Thumbs.db

# Environment
.env
.env.local
```

### .gitignore Best Practices

**DO:**
- ✅ Add .gitignore early
- ✅ Use patterns (not individual files)
- ✅ Document unusual patterns
- ✅ Share .gitignore with team

**DON'T:**
- ❌ Commit sensitive files (even if ignored)
- ❌ Ignore files already tracked (use git rm --cached)

---

## ⚙️ Git Config

### Configuration Levels

**System (All Users):**
```bash
git config --system user.name "Default"
# File: /etc/gitconfig (Linux) or C:\ProgramData\Git\config (Windows)
```

**Global (Current User):**
```bash
git config --global user.name "Your Name"
git config --global user.email "your@email.com"
# File: ~/.gitconfig or ~/.config/git/config
```

**Local (Current Repository):**
```bash
git config --local user.name "Project Name"
# File: .git/config
```

**Priority:** Local > Global > System

### Common Config

**User Identity:**
```bash
git config --global user.name "John Doe"
git config --global user.email "john@example.com"
```

**Editor:**
```bash
git config --global core.editor "code --wait"  # VS Code
git config --global core.editor "vim"
git config --global core.editor "nano"
```

**Merge Tool:**
```bash
git config --global merge.tool vscode
git config --global mergetool.vscode.cmd 'code --wait $MERGED'
```

**Default Branch:**
```bash
git config --global init.defaultBranch main
```

**Line Endings:**
```bash
# Windows
git config --global core.autocrlf true

# Linux/Mac
git config --global core.autocrlf input
```

**View Config:**
```bash
# List all config
git config --list

# List specific level
git config --list --local

# Get specific value
git config user.name
```

---

## 🔤 Git Aliases

### What are Aliases?

**Definition:** Aliases create shortcuts for Git commands.

**Real-life example:**
Like keyboard shortcuts - faster way to do common tasks.

### Creating Aliases

**Basic Aliases:**
```bash
# Short alias
git config --global alias.st status
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit

# Usage
git st  # instead of git status
git co main  # instead of git checkout main
```

**Complex Aliases:**
```bash
# Alias with arguments
git config --global alias.unstage 'reset HEAD --'

# Alias with multiple commands
git config --global alias.last 'log -1 HEAD'

# Alias with function
git config --global alias.visual '!gitk'
```

**Useful Aliases:**
```bash
# Log formatting
git config --global alias.lg "log --oneline --graph --decorate --all"

# Unstage
git config --global alias.unstage 'reset HEAD --'

# Last commit
git config --global alias.last 'log -1 HEAD'

# Amend
git config --global alias.amend 'commit --amend --no-edit'
```

---

## 🧹 Git Clean

### What is Git Clean?

**Definition:** `git clean` removes untracked files from working directory.

**Real-life example:**
Like cleaning up temporary files that were never saved.

### Clean Commands

**Dry Run (Preview):**
```bash
# See what would be removed
git clean -n
git clean --dry-run

# See directories too
git clean -dn
```

**Remove Files:**
```bash
# Remove untracked files
git clean -f
git clean --force

# Remove files and directories
git clean -fd

# Remove ignored files too
git clean -fX

# Remove everything (files + ignored)
git clean -fx
```

**Interactive Clean:**
```bash
# Choose what to remove
git clean -i
```

### Clean Best Practices

**DO:**
- ✅ Always use -n first (dry run)
- ✅ Be careful with -X (ignored files)
- ✅ Understand what will be removed

**DON'T:**
- ❌ Use without -n first
- ❌ Use -X without understanding
- ❌ Remove files you might need

---

## 🔍 Git Bisect

### What is Git Bisect?

**Definition:** `git bisect` uses binary search to find the commit that introduced a bug.

**Real-life example:**
Like playing "hot and cold" - Git helps you narrow down where the bug was introduced.

### Bisect Workflow

**Start Bisect:**
```bash
# Start bisect
git bisect start

# Mark current commit as bad
git bisect bad

# Mark known good commit
git bisect good <commit-hash>
# Or
git bisect good v1.0.0
```

**During Bisect:**
```bash
# Test current commit
# If bug exists:
git bisect bad

# If bug doesn't exist:
git bisect good

# Git automatically checks out next commit to test
# Repeat until bug is found
```

**Finish Bisect:**
```bash
# When bug is found, reset to original state
git bisect reset
```

**Automated Bisect:**
```bash
# Use script to test
git bisect start
git bisect bad
git bisect good v1.0.0
git bisect run npm test

# Git automatically finds the bad commit
```

### Bisect Best Practices

**DO:**
- ✅ Use when you know good and bad commits
- ✅ Use automated tests when possible
- ✅ Reset after bisect

**DON'T:**
- ❌ Use for performance issues (use other tools)
- ❌ Forget to reset

---

## 📖 Git Reflog

### What is Reflog?

**Definition:** Reflog records when branch tips are updated (commits, checkouts, resets, etc.).

**Real-life example:**
Like a history of where you've been - even if you "lost" something, reflog remembers.

### Reflog Commands

**View Reflog:**
```bash
# Show reflog for HEAD
git reflog

# Show reflog for specific branch
git reflog show main

# Show last N entries
git reflog -n 10
```

**Using Reflog:**
```bash
# Find lost commit
git reflog
# Find commit hash

# Recover using reflog
git checkout <commit-hash>
# Or create branch
git branch recovery <commit-hash>
```

**Recover Lost Branch:**
```bash
# List all reflog entries
git reflog

# Find branch deletion
# Recreate branch
git branch <branch-name> <commit-hash>
```

### Reflog Expiration

**By Default:**
- Reflog expires after 90 days
- Can be configured

**Configure Expiration:**
```bash
# Set expiration time
git config gc.reflogExpire "90 days"
git config gc.reflogExpireUnreachable "30 days"
```

---

## 🔒 Git Security

### Security Best Practices

**SSH Keys:**
```bash
# Generate SSH key
ssh-keygen -t ed25519 -C "your_email@example.com"

# Add to SSH agent
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519

# Add public key to GitHub/GitLab
cat ~/.ssh/id_ed25519.pub
```

**Credentials:**
- ❌ Don't commit passwords
- ❌ Don't commit API keys
- ❌ Don't commit tokens
- ✅ Use environment variables
- ✅ Use .gitignore for secrets
- ✅ Use credential helpers

**Credential Helper:**
```bash
# Store credentials securely
git config --global credential.helper store
# Or use cache (temporary)
git config --global credential.helper cache
```

**Signed Commits:**
```bash
# Generate GPG key
gpg --full-generate-key

# List keys
gpg --list-secret-keys --keyid-format LONG

# Configure Git to sign
git config --global user.signingkey <key-id>
git config --global commit.gpgsign true

# Sign commit
git commit -S -m "Signed commit"
```

---

## 🔐 Access Control

### Repository Access

**Public Repositories:**
- Anyone can view
- Contributors can push (with permissions)

**Private Repositories:**
- Only authorized users can access
- Can set team permissions

**Branch Protection:**
- Require PR reviews
- Require status checks
- Prevent force push
- Require linear history

### Access Control Best Practices

**DO:**
- ✅ Use branch protection
- ✅ Require PR reviews
- ✅ Use least privilege principle
- ✅ Audit access regularly

**DON'T:**
- ❌ Share credentials
- ❌ Give unnecessary access
- ❌ Skip security checks

---

## 🚀 CI/CD Integration with Git

### Continuous Integration

**Definition:** CI automatically builds and tests code when changes are pushed.

**Common CI/CD Platforms:**
- GitHub Actions
- GitLab CI
- Jenkins
- CircleCI
- Travis CI

### GitHub Actions Example

```yaml
# .github/workflows/ci.yml
name: CI
on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run tests
        run: npm test
```

### CI/CD Best Practices

**DO:**
- ✅ Run tests on every push
- ✅ Run tests on PRs
- ✅ Deploy on main branch
- ✅ Use status checks

**DON'T:**
- ❌ Skip failing tests
- ❌ Deploy untested code
- ❌ Ignore CI failures

---

## ✅ Git Best Practices

### General Best Practices

**Commits:**
- ✅ Make atomic commits (one logical change)
- ✅ Write clear commit messages
- ✅ Commit often
- ✅ Test before committing

**Branches:**
- ✅ Use descriptive branch names
- ✅ Keep branches short-lived
- ✅ Delete merged branches
- ✅ Use branches for features

**Workflow:**
- ✅ Pull before starting work
- ✅ Push regularly
- ✅ Coordinate with team
- ✅ Review before merging

**Security:**
- ✅ Don't commit secrets
- ✅ Use SSH keys
- ✅ Sign important commits
- ✅ Use branch protection

### Code Review Best Practices

**DO:**
- ✅ Review thoroughly
- ✅ Test changes locally
- ✅ Provide constructive feedback
- ✅ Approve when ready

**DON'T:**
- ❌ Approve without review
- ❌ Be harsh in comments
- ❌ Skip review process

---

## 📚 Additional Resources

**Official Documentation:**
- Git Book: https://git-scm.com/book
- Git Reference: https://git-scm.com/docs

**Learning:**
- Interactive tutorials
- GitHub Learning Lab
- Git visualization tools

**Tools:**
- GitHub Desktop (GUI)
- GitKraken (GUI)
- SourceTree (GUI)
- VS Code Git integration

---

*This guide covers essential Git concepts for version control. Practice these commands and workflows to become proficient with Git.*