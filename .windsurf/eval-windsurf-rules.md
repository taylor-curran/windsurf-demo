# Eval Windsurf Rules

CI/CD Guidelines Assessment Playbook

## Overview
Evaluate code changes in CI/CD against .windsurf/rules/ guidelines. Analyzes diff only, not entire repo.

## Process
1. Get changed files: `git diff --name-only HEAD~1`
2. Load rules: Parse all .windsurf/rules/*.md files
3. Check diff: Analyze only changed lines against rules
4. Report violations: Ordered by priority

## Assessment Template
❌ Violations Found (Priority Order)

1. [Violation Title]
   - File: path/to/file.py:line
   - Rule: "[guideline text]"
   - Issue: [description]

2. [Next Violation]
   - File: path/to/file.js:line  
   - Rule: "[guideline text]"
   - Issue: [description]

## CI Commands
```bash
# Get rules
find .windsurf/rules/ -name "*.md" -exec cat {} \;

# Get diff (works with fetch-depth: 0 in GitHub Actions)
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

## GitHub Actions Integration
This playbook is designed to work with GitHub Actions that use:
- `fetch-depth: 0` for full git history
- Devin API calls with the playbook prompt
- Analysis of only changed files in the current PR/push

### Example GitHub Action Usage
```yaml
name: Code Review CI

on: 
  push:
  pull_request:

jobs:
  code-review:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        with:
          fetch-depth: 0  # Get full history for diff analysis
      
      - name: Run code review
        run: |
          curl --request POST \
            --url https://api.devin.ai/v1/sessions \
            --header 'Authorization: Bearer <token>' \
            --header 'Content-Type: application/json' \
            --data '{
              "prompt": "Review the code diff against rules using this playbook",
              "idempotent": true
            }'
```

## Implementation Notes
- The playbook analyzes only changed files to be efficient in CI/CD workflows
- Git commands are optimized for GitHub Actions environment with full history
- Rules are loaded from all .md files in .windsurf/rules/ directory
- Assessment focuses on violations ordered by business impact priority
