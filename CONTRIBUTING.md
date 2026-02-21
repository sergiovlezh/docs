# Contributing

## Branching Strategy

This project uses **GitHub Flow** with release tags.

### Permanent branches

- `main` -> Stable code only, tagged releases

### Short-lived branches

- `feat/*` -> New features, branch off `main`, merge back into `main`
- `fix/*` -> Bug fixes, branch off `main`, merge back into `main`
- `hotfix/*` -> Urgent fixes on a specific release, branch off the release tag

### Releases

Releases are marked with tags on `main`:

```bash
git tag v0.1.0
git push origin main --tags
```

### Versioning

This project follows [Semantic Versioning](https://semver.org/):

- `MAJOR` -> Breaking changes
- `MINOR` -> New features, backwards compatible (active major version only)
- `PATCH` -> Bug and security fixes (can be applied to any supported major version)

Once a new major version is released, previous major versions only receive `PATCH` updates for security reasons.

### Hotfixing a previous release

```bash
# Start from the tag you want to fix (Always the latest patch of that version)
git checkout v1.0.1
git checkout -b hotfix/description

# Apply fix and commit

# Tag from the hotfix branch (Tags are permanent and not tied to the branch)
git tag v1.0.2
git push origin --tags

# Cleanup (The tag survives the branch deletion)
git checkout main
git branch -d hotfix/description
```

### Staging

When you need to test multiple features together before merging to `main`, create a temporary staging branch:

```bash
# Create a new branch
git checkout -b staging

# Merge the feature branches into the staging branch
git merge feat/something
git merge feat/something-else

# Test, then discard

# Cleanup
git branch -D staging
```
