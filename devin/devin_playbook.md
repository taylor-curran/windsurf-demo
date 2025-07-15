# CI/CD Guidelines Assessment Playbook

## Overview
Evaluate code changes in CI/CD against `.windsurf/rules/` guidelines. Analyzes diff only, not entire repo.

## Trigger Command
This playbook is triggered by the `!eval_rules` command in GitHub Actions workflow.

## Process

1. **Get changed files**: `git diff --name-only HEAD~1`
2. **Load rules**: Parse all `.windsurf/rules/*.md` files
3. **Check diff**: Analyze only changed lines against rules
4. **Report violations**: Ordered by priority

## Execution Steps

### Step 1: Load Windsurf Rules
```bash
find .windsurf/rules/ -name "*.md" -exec cat {} \;
```
Parse each rule file and extract guidelines. Look for:
- Security requirements
- Performance standards  
- Code quality rules
- Best practices

### Step 2: Get Code Changes
```bash
git diff HEAD~1 --unified=0
```
Focus only on added/modified lines (lines starting with `+`).

### Step 3: Analyze Against Rules
For each changed line, check against all loaded rules:
- Match patterns and keywords
- Identify potential violations
- Categorize by severity/priority

### Step 4: Generate Report
Use the assessment template below to report findings.

## Assessment Template

```
❌ Violations Found (Priority Order)

1. [Violation Title]
   - File: path/to/file.py:line
   - Rule: "[guideline text]"
   - Issue: [description]

2. [Next Violation]
   - File: path/to/file.js:line  
   - Rule: "[guideline text]"
   - Issue: [description]
```

## Success Criteria

✅ **Complete Assessment When:**
- All `.windsurf/rules/*.md` files have been loaded and parsed
- Code diff has been analyzed line by line
- All violations have been categorized by priority
- Report follows the assessment template format
- No false positives (only report actual rule violations)

## CI Commands Reference

```bash
# Load all rules from .windsurf/rules/
find .windsurf/rules/ -name "*.md" -exec cat {} \;

# Get diff with context
git diff HEAD~1 --unified=3

# Get only changed files
git diff --name-only HEAD~1

# Get diff without context (focus on changes only)
git diff HEAD~1 --unified=0

# Check specific patterns in changed files
git diff --name-only HEAD~1 | xargs grep -n "pattern"

# Show file changes with line numbers
git diff HEAD~1 --no-index --word-diff=color
```

## Priority Order
1. Security vulnerabilities
2. Production stability risks  
3. Data integrity issues
4. Performance impacts
5. Maintainability concerns
6. Code consistency
