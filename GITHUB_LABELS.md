# GitHub Labels Configuration for pyHWM14

This document suggests labels to configure in GitHub for efficient issue tracking.

## Recommended Labels

### Issue Type (Use one per issue)
- **bug** (color: `#d73a4a`) - Something isn't working
- **feature** (color: `#a2eeef`) - New functionality request
- **enhancement** (color: `#84b6eb`) - Improvement to existing feature
- **documentation** (color: `#0075ca`) - Documentation only
- **maintenance** (color: `#fbca04`) - Code maintenance, refactoring

### Priority
- **priority: critical** (color: `#ff0000`) - Urgent, blocking release
- **priority: high** (color: `#ff6600`) - Important, target next release
- **priority: medium** (color: `#ffcc00`) - Standard priority
- **priority: low** (color: `#cccccc`) - Nice to have, no rush

### Status
- **status: needs-review** (color: `#fbca04`) - Awaiting maintainer review
- **status: in-progress** (color: `#1d76db`) - Currently being worked on
- **status: blocked** (color: `#ff6600`) - Waiting for something else
- **status: won't-fix** (color: `#cccccc`) - Intentionally closed
- **status: duplicate** (color: `#cfd3d7`) - Already covered elsewhere
- **status: stale** (color: `#cfd3d7`) - No activity for 90 days

### Community
- **good-first-issue** (color: `#7057ff`) - Good for new contributors
- **help-wanted** (color: `#33aa3f`) - We need community help
- **discussion** (color: `#d4c5f9`) - Discussion needed, not ready for implementation

### Technical
- **type: bug** (color: `#d73a4a`) - Confirmed bugfix needed
- **type: question** (color: `#d4af37`) - User support question
- **security** (color: `#d73a4a`) - Security vulnerability
- **performance** (color: `#117ab5`) - Performance improvement
- **windows** (color: `#117ab5`) - Windows-specific issue
- **macos** (color: `#117ab5`) - macOS-specific issue
- **linux** (color: `#117ab5`) - Linux-specific issue

### Size/Effort (Estimate)
- **size: small** (color: `#90ee90`) - < 1 hour
- **size: medium** (color: `#ffff99`) - 1-4 hours
- **size: large** (color: `#ff9999`) - > 4 hours

## How to Create Labels

1. Go to: https://github.com/rilma/pyHWM14/labels
2. Click "New label"
3. Fill in:
   - **Label name**: (e.g., "priority: critical")
   - **Description**: (e.g., "Urgent, blocking release")
   - **Color**: (see hex codes above)
4. Click "Create label"

## Label Usage Examples

### New Bug Report
```
- bug
- priority: medium
- status: needs-review
- type: bug
```

### Feature Request
```
- feature
- priority: low
- status: needs-review
- good-first-issue (if appropriate)
```

### Performance Issue
```
- enhancement
- performance
- priority: high
- status: needs-review
```

### Platform-Specific Bug
```
- bug
- windows (or macos/linux)
- priority: medium
```

### Help Wanted
```
- help-wanted
- good-first-issue
- size: medium
- (type: feature or bug as appropriate)
```

## Triaging Workflow

**When issue is created:**
1. Add appropriate type label (bug/feature/documentation/maintenance)
2. Note any affected platforms (windows/macos/linux)
3. Add initial priority estimate
4. If appropriate for new contributors, add `good-first-issue`

**When reviewing:**
1. Update `status:` label (needs-review → in-progress)
2. Adjust priority if needed
3. Set size estimate if not already done

**When closing:**
1. Use appropriate status if applicable (duplicate/won't-fix/stale)
2. Archive in appropriate GitHub Project milestone

---

**Note**: This is a suggestion. You can customize labels based on your needs. The key is consistency!
