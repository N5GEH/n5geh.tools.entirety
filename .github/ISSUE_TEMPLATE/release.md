---
name: Release
about: Prepare for a release
title: Release vx.x.x
labels: release
assignees: ''

---

**Release Version**
Specify the version number for the release (e.g., v2.2.1):

**What is changed?**
TODO: please at least copy the release note here, afterwards

**Checklist**
- [ ] Create a branch under this issue
- [ ] Update roadmap
- [ ] Merge this brach to development
- [ ] Delete main branch protection rule
- [ ] Merge development to main with the type "merge commit", with the commit message **"new release"** ONLY
- [ ] Semantic Release Action will create a new tag, generate release note and publish the release automatically
- [ ] After verification recreate main branch protection rule (require PR and at least one reviewer)
