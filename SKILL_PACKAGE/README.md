# AAP Deployment Skill for Claude Code

**Automate your deployment workflow**: Commit code, push to git, trigger AAP deployment jobs, and monitor results - all conversationally with Claude Code.

## What This Skill Does

This skill enables Claude Code to execute complete deployment workflows through natural conversation:

1. **Commit changes** to git with AI-generated messages
2. **Push to dev branch** automatically (safe isolation from main)
3. **Trigger AAP deployment jobs** via your existing MCP connection
4. **Monitor deployment** in real-time with status updates
5. **Extract server details** from playbook output (IPs, URLs, paths)
6. **Report results** with deployment summary and next steps

### Example Workflow

```
You: "Deploy this app"

Claude:
✓ Committed changes to dev branch
✓ Pushed to origin/dev
✓ Deployment job launched (ID: 1523)

[12:34:56] Running... (1m 15s)
           Current: Copying files to web-01

✓ Deployment completed successfully (2m 30s)

Server Details:
- Application URL: http://dev-web-01.example.com/myapp
- Apache status: Running
- 3 hosts changed, 0 failed

Test application: http://dev-web-01.example.com/myapp
```

No context switching. No manual AAP UI. Just conversation.

## Prerequisites

You must have:
- ✅ Claude Code installed
- ✅ AAP MCP server configured and working
- ✅ Git repository initialized in your project
- ✅ AAP job templates for deployment

**Important**: This skill assumes you already have the AAP MCP server connection configured. If you don't, set that up first.

## Installation

### 1. Copy Skill Files

Copy these files to your project directory:

```bash
cp AAP_DEPLOY_SKILL.md /path/to/your/project/CLAUDE.md
```

Or if you want both deployment and general AAP skills:

```bash
cp AAP_BASE_SKILL.md /path/to/your/project/CLAUDE.md
cp AAP_DEPLOY_SKILL.md /path/to/your/project/DEPLOY_SKILL.md
```

### 2. Verify MCP Connection

Make sure your AAP MCP server is working:

```bash
# In Claude Code, ask:
"List AAP job templates"

# You should see your templates listed
```

### 3. Test the Skill

Make a small change to your code and try:

```
"Deploy this to dev"
```

Claude should guide you through the commit → push → deploy workflow.

## Usage

### Simple Deployment

```
You: "Deploy this app"
You: "Commit and deploy to dev"
You: "Push to dev and run deployment"
```

Claude will:
- Detect uncommitted changes
- Offer to commit them
- Push to dev branch
- Find appropriate deployment template
- Show pre-flight summary
- Launch and monitor job
- Report results with server details

### Specify Template

```
You: "Deploy using the 'Deploy environment for dev' template"
```

### Production Deployment

```
You: "Deploy to production"
```

Claude will apply extra safety checks:
- Require explicit "yes, target production" confirmation
- Show host count warning
- Confirm version/tag if specified

### Check Deployment Status

```
You: "What's the status of the last deployment?"
You: "Why did the deployment fail?"
```

Claude will retrieve job details and logs automatically.

## What's Included

### Files in This Package

```
SKILL_PACKAGE/
├── README.md                    # This file
├── AAP_DEPLOY_SKILL.md          # Deployment workflow instructions
├── AAP_BASE_SKILL.md            # Base AAP job execution skill
├── EXAMPLES.md                  # Detailed usage examples
└── TROUBLESHOOTING.md           # Common issues and solutions
```

### Main Skill: AAP_DEPLOY_SKILL.md

The deployment skill follows this workflow:

1. **Check Git Status** - Detect uncommitted changes
2. **Commit Changes** - Stage and commit with AI-generated message
3. **Push to Dev Branch** - Automatically push to origin/dev
4. **Discover Job Template** - Find or let you select deployment template
5. **Pre-flight Check** - Confirm deployment details
6. **Monitor & Report** - Real-time status + server details extraction

### Base Skill: AAP_BASE_SKILL.md

General AAP automation skill for:
- Patching jobs
- Service restarts
- Provisioning
- Any non-deployment AAP job template

Use deployment skill for code deployments, base skill for everything else.

## Safety Features

### Git Safety
- Always shows what will be committed
- Never skips git hooks
- Allows commit message review/modification
- Tracks deployment commit SHAs for rollback

### Dev Branch Isolation
- **All deployments automatically target dev branch**
- Creates dev branch if it doesn't exist
- Never pushes development work to main/master
- Shows branch and commit SHA in pre-flight

### Production Protection
- Explicit confirmation required for production inventories
- Host count warning for large deployments
- Version/tag confirmation for releases
- Duplicate run detection (prevents double-deploys)

### Deployment Monitoring
- Real-time job status updates
- Automatic log retrieval on failure
- Long-running job warnings
- Server detail extraction from output

## Configuration

### Customizing the Skill

Edit `AAP_DEPLOY_SKILL.md` to adjust:

**Commit Message Format** (Step 2):
```markdown
- Change co-author tag
- Modify message template
```

**Branch Strategy** (Step 3):
```markdown
# Default: push to 'dev' branch
# To change: modify Step 3 branch logic
```

**Server Detail Extraction** (Step 6):
```markdown
# Add custom regex patterns for your playbook output
# Customize what gets extracted and displayed
```

### AAP Job Template Requirements

Your AAP job templates should:
- Include descriptive names (helps with fuzzy matching)
- Output server details via debug tasks
- Use consistent naming for deployment templates
- Set appropriate timeouts

**Helpful**: Add debug tasks to your playbooks:
```yaml
- name: Display deployment URL
  debug:
    msg: "Application URL: http://{{ ansible_fqdn }}/{{ app_name }}"
```

Claude will extract these details automatically.

## Examples

See [EXAMPLES.md](EXAMPLES.md) for detailed scenarios including:
- First-time deployment
- Update existing app
- Production deployment with version tagging
- Multi-environment deployment
- Rollback on failure
- Chained deployment + smoke tests

## Troubleshooting

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for solutions to:
- MCP connection issues
- Git authentication problems
- Template discovery failures
- Deployment monitoring timeouts
- Server detail extraction

## Contributing

Found an issue or want to improve the skill? This package is designed to be:
- **Forkable** - Copy and customize for your environment
- **Extensible** - Add custom workflows to the skill files
- **Shareable** - Distribute your improvements to your team

## License

MIT License - Use freely, modify as needed, share improvements.

## Support

For issues related to:
- **Claude Code**: https://github.com/anthropics/claude-code/issues
- **This skill**: Open an issue in your fork or distribution point
- **AAP MCP server**: Check your MCP server documentation

---

**Quick Start**: Copy `AAP_DEPLOY_SKILL.md` to your project as `CLAUDE.md`, verify MCP connection, and say "deploy this app" in Claude Code.
