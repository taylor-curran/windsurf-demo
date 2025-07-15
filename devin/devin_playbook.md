# CI/CD Guidelines Assessment Playbook

## Overview
Evaluate code changes in CI/CD against `.windsurf/rules/` guidelines. Analyzes diff only, not entire repo.

## Process

1. **Get changed files**: `git diff --name-only HEAD~1`
2. **Load rules**: Parse all `.windsurf/rules/*.md` files
3. **Check diff**: Analyze only changed lines against rules
4. **Report violations**: Ordered by priority

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

## CI Commands

```bash
# Get rules
find .windsurf/rules/ -name "*.md" -exec cat {} \;

# Get diff
git diff HEAD~1 --unified=0

# Check changed files only
git diff --name-only HEAD~1 | xargs grep -n "pattern"
```

## Priority Order
1. Security vulnerabilities
2. Production stability risks  
3. Data integrity issues
4. Performance impacts
5. Maintainability concerns
6. Code consistency