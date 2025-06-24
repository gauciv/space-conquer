# Release Process for Space Impact

This document outlines the process for creating and publishing releases of Space Impact.

## 1. Update Version Numbers

1. Update version in `setup.py`
2. Update version in `space_impact/version.py`
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

## 3. Build Release Packages

Run the build script to create executable packages for your platform:

```bash
# Activate virtual environment
source venv/bin/activate  # On Linux/macOS
# or
venv\Scripts\activate     # On Windows

# Run the build script
python tools/build_executable.py
```

This will create:
- A standalone executable in the `dist` directory
- A ZIP archive in the `releases` directory

## 4. Commit Changes and Create a Tag

```bash
git add .
git commit -m "Bump version to X.Y.Z"
git tag -a vX.Y.Z -m "Version X.Y.Z"
git push origin main
git push origin vX.Y.Z
```

## 5. Create a GitHub Release

1. Go to your repository on GitHub
2. Click on "Releases" on the right sidebar
3. Click "Create a new release"
4. Tag version: vX.Y.Z (should match the tag you pushed)
5. Release title: "Space Impact vX.Y.Z"
6. Description: Copy the content from your CHANGELOG.md for this version
7. Attach the ZIP file(s) from the `releases` directory
8. Click "Publish release"

## 6. Cross-Platform Builds (Optional)

For a complete release, you may want to build packages for all platforms:

- **Windows**: Build on a Windows machine or use a CI service
- **macOS**: Build on a Mac or use a CI service
- **Linux**: Build on a Linux machine or use a CI service

Upload all platform-specific ZIP files to the GitHub release.

## 7. Announce the Release

Announce the new release on relevant channels:
- Project website
- Social media
- Relevant forums or communities
