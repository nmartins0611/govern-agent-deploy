# Troubleshooting Guide

Solutions to common issues when using the AAP Deployment Skill.

## Installation Issues

### Problem: Skill Not Activating

**Symptoms**: Claude doesn't respond to "deploy this" or deployment requests.

**Solution**:
1. Verify CLAUDE.md file is in your project root:
   ```bash
   ls -la CLAUDE.md
   ```

2. Check that the file contains the AAP Deployment Skill instructions:
   ```bash
   head -20 CLAUDE.md
   # Should show "# Deploy with Commit Skill" or similar
   ```

3. Restart Claude Code conversation (start a new conversation)

4. Try an explicit trigger phrase:
   ```
   "Deploy this application using AAP"
   ```

---

### Problem: MCP Server Not Found

**Symptoms**: Error like "AAP MCP server not configured" or "Cannot find mcp__aap-job-mgmt tools"

**Solution**:
1. This skill requires an AAP MCP server connection. Verify it's configured:
   ```
   You: "List available MCP servers"
   ```

2. Test the connection:
   ```
   You: "List AAP job templates"
   ```

3. If no MCP server exists, you'll need to set one up first. The skill won't work without it.

---

## Git Issues

### Problem: Permission Denied on Push

**Symptoms**: Error when pushing to origin/dev

**Solution**:
1. Check git remote configuration:
   ```bash
   git remote -v
   ```

2. Verify SSH keys or credentials:
   ```bash
   ssh -T git@github.com  # For GitHub
   # or your git server
   ```

3. Configure git credentials if using HTTPS:
   ```bash
   git config credential.helper store
   ```

4. If using SSH, ensure key is added:
   ```bash
   ssh-add ~/.ssh/id_rsa
   ```

---

### Problem: Dev Branch Already Exists with Different History

**Symptoms**: Error "cannot push to dev, branches have diverged"

**Solution**:
1. Check branch status:
   ```bash
   git branch -a
   git log --oneline --graph dev origin/dev
   ```

2. If you want to force push (BE CAREFUL):
   ```
   You: "Force push to dev branch"
   ```
   Claude will warn you about this operation.

3. Or create a new branch:
   ```
   You: "Create a new deployment branch instead of using dev"
   ```

---

### Problem: Commit Fails Due to Hooks

**Symptoms**: Pre-commit hooks fail (linting, tests, etc.)

**Solution**:
1. Fix the hook errors first:
   ```bash
   # Check what failed
   git commit  # Shows hook output
   ```

2. The skill will NOT skip hooks (by design for safety). You must:
   - Fix linting errors
   - Fix failing tests
   - Or temporarily disable the hook (not recommended)

3. If you need to bypass hooks (emergency only):
   ```
   You: "Commit with --no-verify flag"
   ```
   Claude will warn you about this.

---

## AAP Template Issues

### Problem: No Deployment Templates Found

**Symptoms**: Claude says "No deployment templates found" or shows unrelated templates

**Solution**:
1. Verify templates exist in AAP:
   ```
   You: "List all AAP job templates"
   ```

2. Check template naming - deployment templates should have names like:
   - "Deploy to dev"
   - "Deploy environment"
   - "Application deployment"

3. The skill uses fuzzy matching. Try being more specific:
   ```
   You: "Deploy using template 'exact-template-name'"
   ```

4. If templates have unusual names, specify the ID:
   ```
   You: "Deploy using AAP template ID 42"
   ```

---

### Problem: Template Launch Fails

**Symptoms**: Error when launching job: "Permission denied" or "Template requires variables"

**Solution**:
1. Check RBAC permissions in AAP:
   - Your AAP user needs "Execute" permission on the template
   - Verify in AAP UI: Templates → [template] → Access

2. If template requires extra_vars:
   ```
   You: "Deploy to dev with extra_vars: {version: '1.2.0', env: 'development'}"
   ```

3. If template requires inventory and none is set:
   ```
   You: "Deploy using template X with inventory Y"
   ```

---

### Problem: Cannot Find Recent Jobs

**Symptoms**: "Why did deployment fail?" returns no results

**Solution**:
1. Check job history scope:
   ```
   You: "List all recent AAP jobs"
   ```

2. If jobs exist but aren't found, try being specific:
   ```
   You: "Show details for AAP job ID 1523"
   ```

3. Verify RBAC permissions - you might not have access to view job results

---

## Deployment Monitoring Issues

### Problem: Job Monitoring Times Out

**Symptoms**: Claude stops monitoring after 1 hour or connection drops

**Solution**:
1. For long-running jobs, check status manually:
   ```
   You: "What's the status of AAP job 1589?"
   ```

2. Increase monitoring patience (skill default is 1 hour):
   ```
   You: "Continue monitoring job 1589"
   ```

3. Check job in AAP UI if needed - URL is provided when job launches

---

### Problem: Server Details Not Extracted

**Symptoms**: Deployment succeeds but "Server Details" section is empty or minimal

**Solution**:
1. Add debug tasks to your Ansible playbooks:
   ```yaml
   - name: Display deployment info
     debug:
       msg: |
         Application URL: http://{{ ansible_fqdn }}/{{ app_name }}
         Server IP: {{ ansible_default_ipv4.address }}
         App Path: {{ deploy_path }}
   ```

2. Enable fact gathering in your playbook:
   ```yaml
   - hosts: all
     gather_facts: yes  # Make sure this is enabled
   ```

3. Check job output manually:
   ```
   You: "Show me the full output from job 1523"
   ```

4. The skill looks for patterns like IPs, URLs, hostnames. Structure your output clearly.

---

### Problem: Failed Deployment Doesn't Show Logs

**Symptoms**: Deployment fails but no error details shown

**Solution**:
1. Request logs explicitly:
   ```
   You: "Show me the logs for failed job 1602"
   ```

2. Check if you have permission to view job stdout:
   ```
   You: "Retrieve stdout for AAP job 1602"
   ```

3. Look at job events for task-level failures:
   ```
   You: "Show job events for job 1602"
   ```

---

## Inventory Issues

### Problem: Wrong Hosts Targeted

**Symptoms**: Deployment runs on unexpected servers

**Solution**:
1. Verify inventory before deployment:
   ```
   You: "What hosts are in the dev-webservers inventory?"
   ```

2. Use inventory limit patterns:
   ```
   You: "Deploy to staging but limit to webservers group"
   ```

3. Check the pre-flight summary carefully - it shows host count

4. For production, double-check inventory name in pre-flight

---

### Problem: Inventory Not Found

**Symptoms**: Template requires inventory but none selected

**Solution**:
1. List available inventories:
   ```
   You: "List AAP inventories"
   ```

2. Specify inventory explicitly:
   ```
   You: "Deploy to dev using inventory dev-servers"
   ```

3. Check if template has a default inventory set in AAP UI

---

## Production Safety Issues

### Problem: Production Confirmation Not Working

**Symptoms**: Can't deploy to production even with confirmation

**Solution**:
1. Use the EXACT phrase required:
   ```
   You: "yes, target production"
   ```
   (not "yes", not "confirm", not "yes target prod")

2. If inventory name doesn't contain "prod/production/prd", Claude won't trigger the extra check. Update inventory name or:
   ```
   You: "This is a production deployment, require explicit confirmation"
   ```

---

### Problem: Deployed to Production by Accident

**Symptoms**: Oh no.

**Solution**:
1. Check what was deployed:
   ```
   You: "Show details of last deployment job"
   ```

2. If rollback is possible:
   ```
   You: "Revert the last commit and redeploy to production"
   ```

3. If you need emergency rollback:
   ```
   You: "Run the rollback job template immediately"
   ```

4. **Prevention**: Always review the pre-flight summary carefully. Production deployments show:
   - ⚠ Production Target Detected
   - Host count warning
   - Explicit confirmation requirement

---

## General Debugging

### Problem: Skill Behaves Unexpectedly

**Symptoms**: Workflow doesn't follow expected steps

**Solution**:
1. Check which skill file is loaded:
   ```bash
   cat CLAUDE.md | head -5
   ```

2. Verify no conflicting instructions in project

3. Start a fresh conversation (skills are loaded per conversation)

4. Be explicit about what you want:
   ```
   You: "Follow the AAP deployment skill workflow to deploy this app"
   ```

---

### Problem: Need to Debug AAP API Calls

**Symptoms**: Want to see raw MCP tool calls and responses

**Solution**:
1. Ask Claude to show tool calls:
   ```
   You: "Show me the exact MCP tool calls you're making"
   ```

2. Test tools directly:
   ```
   You: "Call mcp__aap-job-mgmt__job_templates_list and show raw response"
   ```

3. Check MCP server logs (location depends on your MCP server setup)

---

## Getting Help

### Still Stuck?

1. **Check EXAMPLES.md** - See if your scenario matches a working example

2. **Review README.md** - Verify prerequisites are met

3. **Test components individually**:
   - Git: Can you commit and push manually?
   - AAP MCP: Can you list templates?
   - AAP permissions: Can you launch jobs in AAP UI?

4. **Simplify**:
   - Try deploying without commit (to isolate git issues)
   - Try launching AAP job directly (to isolate deployment issues)
   - Break down the workflow into steps

5. **Ask Claude**:
   ```
   You: "Debug why deployment isn't working. Show me each step."
   ```

### Common Combinations

**Git works, AAP doesn't**:
- MCP connection issue or RBAC permissions

**AAP works, git doesn't**:
- Remote authentication or branch permissions

**Both work separately, fail together**:
- Likely timing issue or state problem - start fresh conversation

**Nothing works**:
- Verify CLAUDE.md file is present and valid
- Confirm MCP server is connected
- Check Claude Code is up to date

---

## Pro Tips

### Avoid Common Mistakes

1. **Don't skip pre-flight review** - That's your safety net
2. **Watch for production warnings** - They're there for a reason
3. **Check host count** - Especially before production deploys
4. **Read error messages** - Claude extracts the relevant parts
5. **Keep playbooks verbose** - More output = better details extraction

### Make Debugging Easier

1. Add debug tasks to playbooks:
   ```yaml
   - debug: var=hostvars[inventory_hostname]
   ```

2. Use consistent template naming in AAP

3. Enable verbose job output in AAP templates

4. Test deployments in dev first, always

5. Keep commit messages clear - helps with deployment tracking

### Speed Up Workflow

1. Use template names in requests:
   ```
   "Deploy with template X"  # Faster than letting Claude search
   ```

2. Pre-answer commit confirmation:
   ```
   "Deploy this - auto-commit with default message"
   ```

3. Skip monitoring for quick deploys:
   ```
   "Launch deployment job but don't wait for completion"
   ```

4. Batch operations:
   ```
   "Commit everything in /app directory and deploy to dev"
   ```
