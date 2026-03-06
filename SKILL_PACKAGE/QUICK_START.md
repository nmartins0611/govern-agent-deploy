# Quick Start Guide

Get up and running with the AAP Deployment Skill in 5 minutes.

## Prerequisites Check

Before starting, verify you have:

- [ ] Claude Code installed and working
- [ ] AAP MCP server configured (test with: "List AAP job templates")
- [ ] Git repository initialized in your project
- [ ] At least one AAP deployment job template

## Installation (30 seconds)

### Option 1: Deployment Skill Only
```bash
cp AAP_DEPLOY_SKILL.md /path/to/your/project/CLAUDE.md
```

### Option 2: Both Deployment + General AAP Skills
```bash
cp AAP_DEPLOY_SKILL.md /path/to/your/project/CLAUDE.md
cp AAP_BASE_SKILL.md /path/to/your/project/AAP_SKILL.md
```

**Note**: The skill instructions must be in your project directory to be loaded by Claude Code.

## Verify Installation (30 seconds)

1. Start Claude Code in your project directory
2. Start a new conversation
3. Ask: "List AAP job templates"

If you see templates listed, you're ready to deploy.

## First Deployment (2 minutes)

Make a small change to your code, then:

```
You: "Deploy this app to dev"
```

Claude will:
1. ✓ Show uncommitted changes
2. ✓ Offer to commit them
3. ✓ Generate commit message
4. ✓ Push to dev branch
5. ✓ Find deployment template
6. ✓ Show pre-flight summary
7. ✓ Launch and monitor job
8. ✓ Report server details

Just follow the prompts and confirm each step.

## Common Commands

### Deploy with default settings
```
"Deploy this"
"Deploy to dev"
"Commit and deploy"
```

### Deploy to specific template
```
"Deploy using template 'Deploy environment for dev'"
```

### Check deployment status
```
"What's the status of the last deployment?"
"Show me the latest job"
```

### Debug failures
```
"Why did the deployment fail?"
"Show logs for job 1523"
```

### Production deployment
```
"Deploy to production"
# Claude will require: "yes, target production"
```

## Understanding the Workflow

### What Happens When You Say "Deploy"

```
You: "Deploy this app"
  ↓
Claude: Shows uncommitted changes
  ↓
You: "yes" (to commit)
  ↓
Claude: Shows proposed commit message
  ↓
You: "yes" (to proceed)
  ↓
Claude: Commits, pushes to dev, finds template
  ↓
Claude: Shows pre-flight summary
  ↓
You: "yes" (to deploy)
  ↓
Claude: Launches job, monitors in real-time
  ↓
Claude: Shows server details when complete
```

**Key Points**:
- You confirm at each major step
- Claude handles git, AAP, and monitoring
- No context switching to AAP UI needed
- All deployments go to dev branch automatically

## Safety Features You'll See

### 1. Pre-flight Summary
Before every deployment:
```
Ready to deploy:
- Template: Deploy to dev
- Inventory: dev-servers (3 hosts)
- Branch: dev
- Latest commit: abc123f Add new feature

Proceed? (yes/no)
```

**Always review this carefully.**

### 2. Production Protection
For production:
```
⚠ Production Target Detected
⚠ This will affect 47 production hosts

To proceed, type: "yes, target production"
```

You MUST type the exact phrase.

### 3. Auto Logs on Failure
If deployment fails:
```
❌ Deployment failed

Failed task: "Install packages"
Failed hosts: web-01

Last 20 lines of output:
[error details automatically shown]

Suggested fix: Check package repository
```

No need to ask "why did it fail" - Claude shows you immediately.

## Customization

### Change Commit Message Format
Edit `AAP_DEPLOY_SKILL.md` Step 2:
```markdown
git commit -m "message" -m "Co-Authored-By: Your Name <your@email.com>"
```

### Change Branch Strategy
Edit `AAP_DEPLOY_SKILL.md` Step 3:
```markdown
# Default: push to 'dev' branch
# Change to: push to 'staging' branch
```

### Add Custom Server Details
Edit `AAP_DEPLOY_SKILL.md` Step 6, add regex patterns:
```markdown
- Custom pattern: "MyApp URL: ..."
```

## Troubleshooting First Deploy

### Problem: Skill doesn't activate
**Solution**:
- Verify CLAUDE.md is in project root
- Start a new conversation
- Try: "Deploy this application using AAP"

### Problem: No templates found
**Solution**:
- Test MCP: "List all AAP job templates"
- Check template names contain "deploy" or "environment"
- Specify exact name: "Deploy using template 'exact-name'"

### Problem: Git push fails
**Solution**:
- Check git credentials: `git push` (manually)
- Verify SSH keys or HTTPS token
- Check remote exists: `git remote -v`

### Problem: No server details shown
**Solution**:
- Add debug tasks to your playbook:
  ```yaml
  - name: Show deployment info
    debug:
      msg: "App URL: http://{{ ansible_fqdn }}/app"
  ```

## Next Steps

Once your first deployment works:

1. **Read EXAMPLES.md** - See advanced scenarios
2. **Review TROUBLESHOOTING.md** - For any issues
3. **Customize the skill** - Adjust to your workflow
4. **Share with your team** - Copy the SKILL_PACKAGE

## Getting Help

**Quick checks**:
```
"List AAP job templates"           # Test MCP connection
"Show git status"                  # Check repository state
"What's my current branch?"        # Verify git setup
```

**Debug mode**:
```
"Debug why deployment isn't working. Show me each step."
```

**Still stuck?**
- See TROUBLESHOOTING.md
- Test each component separately (git, AAP, MCP)
- Ask Claude: "Help me debug the AAP deployment skill"

## Tips for Success

1. **Review pre-flight summaries** - They're your safety net
2. **Start with dev** - Test there before production
3. **Watch host counts** - Especially for production
4. **Let Claude generate commit messages** - They're based on actual changes
5. **Read the error logs** - Claude extracts the important parts

## Example Session

Here's what a successful first deployment looks like:

```
You: "I've updated the homepage. Deploy to dev."

Claude:
Found uncommitted changes:
  M index.html
  M style.css

Commit these changes? (yes/no)

You: "yes"

Claude:
Proposed commit message:
"Update homepage design

- Modernize layout
- Update color scheme"

Proceed? (yes/no)

You: "yes"

Claude:
✓ Committed and pushed to dev
✓ Found template: Deploy to dev
✓ Job launched (ID: 123)

[14:30:15] Running... (30s)
[14:30:45] ✓ Successful (1m 15s)

Server Details:
- URL: http://dev.example.com
- 3 hosts updated

Test: http://dev.example.com
```

**That's it!** You just deployed with conversation.

---

**Ready?** Try: `"Deploy this app"` and follow the prompts.
