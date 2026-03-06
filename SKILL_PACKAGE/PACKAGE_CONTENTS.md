# Package Contents

This directory contains everything needed to distribute and use the AAP Deployment Skill for Claude Code.

## Files Overview

```
SKILL_PACKAGE/
├── README.md                    # Start here - Overview and installation
├── QUICK_START.md               # 5-minute getting started guide
├── AAP_DEPLOY_SKILL.md          # Main skill: Git + Deployment workflow
├── AAP_BASE_SKILL.md            # Base skill: General AAP job execution
├── EXAMPLES.md                  # Real-world usage scenarios
├── TROUBLESHOOTING.md           # Common issues and solutions
├── CHANGELOG.md                 # Version history and roadmap
├── LICENSE                      # MIT License
└── PACKAGE_CONTENTS.md          # This file
```

## File Purposes

### README.md (Start Here)
- **Purpose**: Package overview and installation instructions
- **Audience**: Anyone evaluating or installing the skill
- **Contains**:
  - What the skill does (elevator pitch)
  - Prerequisites
  - Installation steps
  - Basic usage
  - Links to other documentation

**Read this first** to understand what you're getting and if it fits your needs.

---

### QUICK_START.md (Get Running Fast)
- **Purpose**: Get from zero to first deployment in 5 minutes
- **Audience**: Developers ready to install and test
- **Contains**:
  - Prerequisites checklist
  - Copy-paste installation commands
  - First deployment walkthrough
  - Common commands reference
  - Troubleshooting first deploy

**Use this** when you want to try it immediately without reading everything.

---

### AAP_DEPLOY_SKILL.md (Core Deployment Skill)
- **Purpose**: Complete deployment workflow instructions for Claude Code
- **Audience**: Claude Code (this is the skill instruction file)
- **Contains**:
  - 6-step deployment workflow
  - Git commit and push automation
  - AAP job template discovery
  - Job monitoring and result extraction
  - Safety guardrails

**Installation**: Copy this file to your project as `CLAUDE.md`

**When to use**:
- You want to deploy code changes to AAP
- Need git commit + push + deployment in one workflow
- Want server details extracted automatically
- Require dev branch isolation

---

### AAP_BASE_SKILL.md (General AAP Automation)
- **Purpose**: General-purpose AAP job execution instructions
- **Audience**: Claude Code (skill instruction file)
- **Contains**:
  - 5-step job execution workflow
  - Job template discovery and launch
  - Monitoring and result reporting
  - No git integration

**Installation**: Copy to your project as `AAP_SKILL.md` (alongside CLAUDE.md) or merge with AAP_DEPLOY_SKILL.md

**When to use**:
- Patching jobs
- Service restarts
- Provisioning
- Any AAP automation that doesn't involve code deployment

---

### EXAMPLES.md (Real-World Scenarios)
- **Purpose**: Detailed usage examples showing the skill in action
- **Audience**: Developers learning the skill
- **Contains**:
  - First-time deployment
  - Update existing app
  - Production deployment with version tagging
  - Deployment failure and rollback
  - Multi-environment deployments
  - Deployment with smoke tests
  - Skip commit scenarios

**Use this** to see how the skill handles different situations and learn best practices.

---

### TROUBLESHOOTING.md (Fix Issues)
- **Purpose**: Solutions to common problems
- **Audience**: Developers encountering issues
- **Contains**:
  - Installation issues
  - Git problems (auth, push, hooks)
  - AAP template discovery failures
  - Monitoring and extraction issues
  - Production safety problems
  - Debugging techniques

**Use this** when something doesn't work as expected.

---

### CHANGELOG.md (Version History)
- **Purpose**: Track changes, versions, and roadmap
- **Audience**: Users tracking updates and contributors
- **Contains**:
  - Version 1.0.0 release notes
  - Feature list
  - Known limitations
  - Future enhancements roadmap
  - Contributing guidelines

**Use this** to see what's new, what's planned, and how to contribute.

---

### LICENSE (MIT)
- **Purpose**: Legal terms for use and distribution
- **Audience**: Legal/compliance review
- **Contains**: MIT License text

**Summary**: You can freely use, modify, and distribute this skill.

---

## Distribution Methods

### Method 1: Share the Entire Package

**Best for**: Distributing to a team or publishing publicly

```bash
# Zip the package
zip -r aap-deployment-skill-v1.0.0.zip SKILL_PACKAGE/

# Or tar.gz
tar -czf aap-deployment-skill-v1.0.0.tar.gz SKILL_PACKAGE/
```

**Recipients do**:
1. Extract the archive
2. Read README.md
3. Follow QUICK_START.md
4. Copy AAP_DEPLOY_SKILL.md to their project

---

### Method 2: Share Core Files Only

**Best for**: Quick sharing with developers who know Claude Code

```bash
# Create minimal distribution
mkdir aap-deploy-skill
cp README.md QUICK_START.md AAP_DEPLOY_SKILL.md aap-deploy-skill/
```

**Recipients do**:
1. Read README.md
2. Copy AAP_DEPLOY_SKILL.md to project as CLAUDE.md
3. Start deploying

---

### Method 3: Git Repository

**Best for**: Version control and collaboration

```bash
# Initialize git repo in SKILL_PACKAGE
cd SKILL_PACKAGE
git init
git add .
git commit -m "Initial release: AAP Deployment Skill v1.0.0"
git remote add origin <your-repo-url>
git push -u origin main
```

**Recipients do**:
```bash
git clone <your-repo-url>
cd aap-deployment-skill
cp AAP_DEPLOY_SKILL.md /path/to/their/project/CLAUDE.md
```

---

### Method 4: Internal Package Repository

**Best for**: Enterprise distribution

Structure for internal package managers:
```
name: aap-deployment-skill
version: 1.0.0
description: Automate AAP deployments with Claude Code
files:
  - AAP_DEPLOY_SKILL.md
  - AAP_BASE_SKILL.md
  - README.md
  - QUICK_START.md
install_command: |
  cp AAP_DEPLOY_SKILL.md $PROJECT_ROOT/CLAUDE.md
```

---

## Installation Paths

Users can install the skill in different ways depending on their needs:

### Path A: Deployment Only (Most Common)
```bash
cp AAP_DEPLOY_SKILL.md /path/to/project/CLAUDE.md
```

**Result**: Deploy workflow available, no general AAP automation

---

### Path B: Both Deployment + General AAP
```bash
cp AAP_DEPLOY_SKILL.md /path/to/project/CLAUDE.md
cp AAP_BASE_SKILL.md /path/to/project/AAP_SKILL.md
```

**Result**: Both deployment and general AAP automation available

---

### Path C: General AAP Only
```bash
cp AAP_BASE_SKILL.md /path/to/project/CLAUDE.md
```

**Result**: General AAP automation, no deployment workflow

---

### Path D: Merged Skills (Advanced)
```bash
# Manually merge AAP_DEPLOY_SKILL.md and AAP_BASE_SKILL.md
# into a single CLAUDE.md file
```

**Result**: Single skill file with both workflows

---

## Customization Guide

Users may want to customize the skill for their environment:

### What Can Be Customized

1. **Commit message format** (AAP_DEPLOY_SKILL.md, Step 2)
   - Change co-author tag
   - Modify message structure

2. **Branch strategy** (AAP_DEPLOY_SKILL.md, Step 3)
   - Change target branch from `dev` to another name
   - Add merge logic for production

3. **Server detail extraction** (AAP_DEPLOY_SKILL.md, Step 6)
   - Add custom regex patterns
   - Change what details are displayed

4. **Safety thresholds** (Both skills)
   - Adjust host count warnings
   - Modify production detection patterns
   - Add custom confirmation requirements

5. **Monitoring behavior** (Both skills)
   - Change polling interval (default: 30s)
   - Adjust max monitoring duration (default: 1 hour)

### How to Customize

1. Copy the skill file to your project
2. Edit the relevant section
3. Document your changes (add comments)
4. Test thoroughly
5. Optional: Share customizations back to the community

---

## Support and Contributions

### Getting Help

1. **Check documentation first**:
   - README.md for overview
   - QUICK_START.md for installation
   - TROUBLESHOOTING.md for common issues
   - EXAMPLES.md for usage patterns

2. **Test components**:
   - MCP connection: "List AAP job templates"
   - Git setup: `git push` manually
   - Skill loading: Start new conversation

3. **Debug mode**:
   - Ask Claude: "Debug why deployment isn't working"
   - Request: "Show me the exact MCP tool calls"

### Contributing Improvements

If you enhance the skill:

1. **Document the change**:
   - What problem it solves
   - How to use the new feature
   - Any breaking changes

2. **Test thoroughly**:
   - Verify existing workflows still work
   - Test edge cases
   - Check safety guardrails

3. **Share back** (optional):
   - Create patch file
   - Submit to original maintainer
   - Share in community forums

---

## Package Metadata

**Name**: AAP Deployment Skill for Claude Code
**Version**: 1.0.0
**Release Date**: 2026-03-06
**License**: MIT
**Compatibility**: Claude Code with AAP MCP server

**Requirements**:
- Claude Code (any version with MCP support)
- AAP MCP server connection
- Git repository
- AAP 2.4+ (recommended)

**Size**: ~150 KB (all files)
**Format**: Markdown + text files
**Dependencies**: None (pure skill instructions)

---

## Quality Checklist for Distributors

Before sharing this package, verify:

- [ ] All files present and readable
- [ ] README.md opens and renders correctly
- [ ] Installation paths in docs are accurate
- [ ] Examples reflect your AAP environment (or are generic)
- [ ] License is acceptable for your use case
- [ ] Version number is correct in CHANGELOG.md
- [ ] No sensitive information in files (hostnames, tokens, etc.)
- [ ] Links to external resources work (if any)

---

## Quick Reference

**To install**: Copy `AAP_DEPLOY_SKILL.md` to project as `CLAUDE.md`
**To test**: Say "Deploy this app" in Claude Code
**To customize**: Edit the copied CLAUDE.md file
**To upgrade**: Replace CLAUDE.md with new version
**To uninstall**: Remove CLAUDE.md file

**Support**: See TROUBLESHOOTING.md
**Examples**: See EXAMPLES.md
**Changes**: See CHANGELOG.md
**License**: See LICENSE

---

## Distribution Best Practices

1. **Version your distribution**:
   - Include version in filename: `aap-deployment-skill-v1.0.0.zip`
   - Update CHANGELOG.md with each release

2. **Include all documentation**:
   - Don't distribute just the skill files
   - Include README, QUICK_START, TROUBLESHOOTING

3. **Test before distributing**:
   - Extract and install in a fresh project
   - Run through QUICK_START.md
   - Verify examples work

4. **Communicate requirements clearly**:
   - MCP server must be pre-configured
   - Git repository required
   - AAP permissions needed

5. **Provide support channel**:
   - Email, Slack, GitHub issues, etc.
   - Point users to TROUBLESHOOTING.md first

---

**Ready to distribute?** Zip this entire SKILL_PACKAGE directory and share!
