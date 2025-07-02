# Release Process for Space Conquer

This document outlines the process for creating and publishing releases of Space Conquer.

## 1. Update Version Numbers

1. Update version in `setup.py`
2. Update version in `src/version.py` (if exists)
3. Update version in README badges

## 2. Update CHANGELOG.md

Add a new section for the new version at the top of the file:

```markdown
## [X.Y.Z] - YYYY-MM-DD

### Added
- New feature 1
- New feature 2

### Changed
- Change 1
- Change 2

### Fixed
- Bug fix 1
- Bug fix 2
```

## 3. Commit Changes and Create a Tag

```bash
git add .
git commit -m "Bump version to X.Y.Z"
git tag -a vX.Y.Z -m "Version X.Y.Z"
git push origin main
git push origin vX.Y.Z
```

## 4. Automated Release Process

After pushing the tag, GitHub Actions will automatically:

1. Build executables for Windows, macOS, and Linux
2. Create ZIP packages for each platform
3. Create a GitHub Release with the tag name
4. Upload the ZIP packages to the release

## 5. Verify the Release

1. Go to your repository on GitHub
2. Click on "Actions" to monitor the build progress
3. Once completed, check the "Releases" page to verify:
   - The release was created
   - All ZIP packages were uploaded
   - The release description is correct

## 6. Announce the Release

Announce the new release on relevant channels:
- Project website
- Social media
- Relevant forums or communities
