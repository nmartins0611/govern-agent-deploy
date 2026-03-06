# Deploy with Commit Skill
# Combines git operations with AAP job template execution
# For use with Claude Code + AAP MCP server

## Purpose
This skill automates the complete deployment workflow: commit code changes to git, push to dev branch, trigger an AAP deployment job template, monitor execution, and report server details from the deployment results.

**Key Behavior**: All deployments automatically push commits to the `dev` branch (or create it if it doesn't exist) to ensure development deployments are isolated from the main branch.

## Skill Activation

This skill activates when the developer:
- Says "deploy [app/code/changes]"
- Asks to "commit and deploy"
- Requests "push and run deployment"
- Mentions "deploy to [environment]" with uncommitted changes
- Specifically asks to deploy with a job template

## Workflow

When activated, follow this 6-step process:

### Step 1 — Check Git Status
**Actions**:
1. Run `git status --short` to check for uncommitted changes
2. Run `git diff` to see what changed
3. If there are uncommitted changes:
   - Show a summary of changed files
   - Proceed to Step 2
4. If working tree is clean:
   - Skip to Step 3 (no commit needed)
   - Inform: "Working tree clean, proceeding to deployment"

### Step 2 — Commit Changes (if needed)
**Actions**:
1. Display changed files to developer
2. Ask: "Commit these changes before deployment? (yes/no)"
3. If yes:
   - Stage all changes with `git add .` (or specific files if developer specifies)
   - Generate a concise commit message based on changes
   - Show proposed commit message
   - Ask for confirmation or allow developer to modify
   - Execute: `git commit -m "message" -m "Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"`
   - Confirm commit succeeded with `git log -1 --oneline`
4. If no:
   - Warn: "Deploying without committing. Changes are not version controlled."
   - Ask: "Continue anyway? (yes/no)"
   - If no, abort workflow

**Important**:
- Never skip git hooks or force operations
- Use heredoc format for multi-line commit messages
- Always confirm commit before pushing

### Step 3 — Push to Dev Branch
**Actions**:
1. Check current branch: `git branch --show-current`
2. If not on `dev` branch:
   - Check if dev branch exists: `git rev-parse --verify dev 2>/dev/null`
   - If dev branch exists:
     - Create new branch from current commit: `git checkout -b dev-deploy-[timestamp]`
     - Inform: "Created branch dev-deploy-[timestamp] from current commit"
   - If dev branch does not exist:
     - Create dev branch: `git checkout -b dev`
     - Inform: "Created new dev branch"
   - If already on dev branch:
     - Continue with current branch
3. Check if origin remote exists: `git remote -v | grep origin`
4. Push to dev branch:
   - If dev branch tracks remote: `git push`
   - If dev branch doesn't track remote: `git push -u origin dev`
   - Display: "✓ Pushed commit [sha] to origin/dev"
5. Confirm push succeeded with: `git log origin/dev -1 --oneline`
6. Save branch info for deployment context:
   - Branch: dev (or dev-deploy-[timestamp])
   - Commit SHA: [sha]
   - Remote: origin/dev

### Step 4 — Discover AAP Job Template
**Trigger**: Commit complete (or skipped)

**Actions**:
1. Load AAP job management tools using ToolSearch: query "aap job"
2. Call `mcp__aap-job-mgmt__job_templates_list` to list available templates
3. If developer specified template name:
   - Search for exact or fuzzy match in template list
   - If found, proceed to Step 5
   - If not found, show available templates and ask developer to select
4. If no template specified:
   - Filter templates for deployment-related ones (name contains "deploy", "environment", etc.)
   - Show filtered list with IDs and descriptions
   - Ask: "Which deployment template should I use?"
   - Wait for developer selection

### Step 5 — Pre-flight and Launch Job
**Trigger**: Job template identified

**Actions**:
1. Retrieve full template details: `mcp__aap-job-mgmt__job_templates_retrieve` with template ID
2. Load inventory tools if needed using ToolSearch: query "aap inventory"
3. Call `mcp__aap-inventory__inventories_list` to get inventory details
4. Present pre-flight summary:
   ```
   Ready to deploy:
   - Template: [template name]
   - Inventory: [inventory name] ([host count] hosts)
   - Environment: [dev/staging/prod if detectable]
   - Branch: dev (pushed to origin/dev)
   - Latest commit: [git log -1 --oneline]
   - Extra vars: [if any]

   Proceed with deployment? (yes/no)
   ```

5. Apply safety guardrails:
   - **Production confirmation**: If inventory name contains "production", "prod", or "prd", require exact phrase "yes, target production"
   - **Version/tag confirmation**: If extra_vars contain `version`, `tag`, `sha`, `release`, repeat the value and require confirmation
   - **Inventory requirement**: If template has no inventory set, list available inventories and require developer to specify one

6. On confirmation, launch job:
   - Call `mcp__aap-job-mgmt__job_templates_launch_create`
   - Extract job ID and URL from response
   - Report:
     ```
     ✓ Deployment job launched
     Job ID: [id]
     URL: [AAP UI link - construct as https://[aap-host]/#/jobs/playbook/[job-id]/output]
     Status: Pending

     Monitoring deployment...
     ```

### Step 6 — Monitor and Report Results
**Trigger**: Job launched successfully

**Actions**:
1. Poll job status every 30 seconds using `mcp__aap-job-mgmt__jobs_retrieve`
2. Display real-time updates:
   ```
   [12:34:56] Running... (1m 15s)
              Current: Installing application on web-01
   ```

3. While job is running:
   - Show elapsed time on each poll
   - Use `mcp__aap-job-mgmt__jobs_job_events_list` to get recent task events
   - Display current task name if available

4. On job completion (successful or failed):
   - Call `mcp__aap-job-mgmt__jobs_job_host_summaries_list` for host results
   - Call `mcp__aap-job-mgmt__jobs_stdout_retrieve` to get full output
   - Parse output for server details (IP addresses, URLs, ports, etc.)

5. Present deployment summary:
   ```
   ✓ Deployment completed successfully
   Duration: 3m 45s

   📊 Deployment Results:
   - Hosts changed: [count]
   - Hosts failed: [count]

   🖥️ Server Details:
   - Server: web-01.example.com (192.168.1.10)
   - Application URL: http://192.168.1.10/app
   - Apache status: Running
   - Application path: /var/www/html/app

   [If available from job output:]
   - Load balancer: lb-01.example.com
   - Health check: PASSED
   ```

6. Extract server details by:
   - Searching job stdout for patterns like:
     - IP addresses (regex: `\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b`)
     - URLs (regex: `https?://[^\s]+`)
     - Hostnames (from ansible facts or output)
     - Service ports
     - Application paths
   - Parsing ansible facts from job events if available
   - Looking for registered variables in playbook output

7. If deployment failed:
   - Show last 50 lines of output
   - Highlight error messages
   - Call `mcp__aap-job-mgmt__jobs_job_events_list` with filter for failed events
   - Suggest fixes based on error context
   - Ask: "Revert commit [sha]? (yes/no)"

8. Ask follow-up:
   ```
   Next steps:
   - Run smoke tests?
   - Check application health?
   - Deploy to another environment?
   ```

## Server Details Extraction Strategy

To extract server details from job output, search for these patterns in stdout:

1. **Ansible Facts** (if gather_facts is enabled):
   ```
   Look for: "ansible_default_ipv4": {"address": "IP"}
   Look for: "ansible_fqdn": "hostname"
   ```

2. **Playbook Output**:
   ```
   Look for: "Application deployed to: http://..."
   Look for: "Server: [hostname]"
   Look for: "Listening on port: [port]"
   ```

3. **Registered Variables**:
   ```
   Look for: "PLAY RECAP" section for host names
   Look for: debug/msg outputs with server info
   ```

4. **Common Patterns**:
   ```
   - "Web server available at: http://..."
   - "Application URL: ..."
   - "Deployed to: /var/www/..."
   - "Service running on: ..."
   ```

5. **Use Job Events for Structured Data**:
   - Call `mcp__aap-job-mgmt__jobs_job_events_list`
   - Filter for events with type "runner_on_ok"
   - Look for events with names like "Display server info", "Show deployment URL"
   - Parse event data for structured output

## Safety Guardrails

1. **Commit Confirmation**:
   - Always show what will be committed
   - Allow developer to review and modify commit message
   - Never skip git hooks

2. **Dev Branch Push**:
   - Automatically switches to or creates dev branch for deployments
   - Never pushes development deployments to main/master branch
   - Pushes to origin/dev before triggering deployment
   - Confirms push succeeded before deployment
   - Displays branch and commit SHA in pre-flight summary

3. **Deployment Confirmation**:
   - Always show pre-flight summary with all deployment details
   - Require explicit confirmation before launching jobs
   - Extra confirmation for production deployments (exact phrase "yes, target production")
   - Show host count before confirming
   - If host count > 20 for production, add extra warning

4. **Rollback Awareness**:
   - Track the commit SHA that was deployed
   - If deployment fails, suggest: "Revert commit [sha]? (yes/no)"
   - Keep deployment history in conversation context

## MCP Tool Reference

**Required tools** (load with ToolSearch before use):

Job Management:
- `mcp__aap-job-mgmt__job_templates_list` - List all templates
- `mcp__aap-job-mgmt__job_templates_retrieve` - Get template details
- `mcp__aap-job-mgmt__job_templates_launch_create` - Launch a job
- `mcp__aap-job-mgmt__jobs_retrieve` - Get job status
- `mcp__aap-job-mgmt__jobs_stdout_retrieve` - Get job output/logs
- `mcp__aap-job-mgmt__jobs_job_events_list` - Get task-level events
- `mcp__aap-job-mgmt__jobs_job_host_summaries_list` - Get per-host results

Inventory Management:
- `mcp__aap-inventory__inventories_list` - List inventories
- `mcp__aap-inventory__hosts_list` - List hosts in inventory

## Success Criteria

The skill works correctly when:
- Developer can deploy with a single command
- All changes are committed before deployment (or explicitly skipped)
- Commits are automatically pushed to dev branch (not main/master)
- Job templates are discovered and launched automatically
- Deployment is monitored in real-time
- Server details are extracted and displayed clearly
- Failed deployments show errors and suggest fixes
- No manual AAP UI access is needed for standard deployments
- Dev branch isolation prevents accidental main branch deployments

## Customization

You can customize this skill for your environment:

**Change commit co-author** (Step 2):
```markdown
-m "Co-Authored-By: Your Name <your@email.com>"
```

**Change branch strategy** (Step 3):
- Modify to use different branch names (e.g., `deploy`, `staging`)
- Add merge logic for production deployments

**Add custom server detail patterns** (Step 6):
- Add regex patterns specific to your playbook output
- Customize what details are extracted and displayed

**Adjust safety thresholds** (Step 5):
- Change host count warning threshold (default: 20)
- Add custom confirmation requirements
- Modify production detection patterns
