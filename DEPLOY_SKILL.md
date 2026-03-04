# Deploy with Commit Skill
# Combines git operations with AAP job template execution
# Last updated: 2026-03-04 (updated for dev branch deployment)

## Purpose
This skill automates the complete deployment workflow: commit code changes to git, push to dev branch, trigger an AAP deployment job template, monitor execution, and report server details from the deployment results.

**Key Behavior**: All deployments automatically push commits to the `dev` branch (or create it if it doesn't exist) to ensure development deployments are isolated from the main branch.

## Skill Activation

This skill activates when the developer:
- Says "deploy [app/code/changes]"
- Asks to "commit and deploy"
- Requests "push and run deployment"
- Mentions "deploy to [environment]" with uncommitted changes
- Specifically asks to deploy with a job template like "Deploy environment for dev"

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
   - Generate a concise commit message based on changes (e.g., "Deploy cheeseburger-map-app v1.0")
   - Show proposed commit message
   - Ask for confirmation or allow developer to modify
   - Execute: `git commit -m "message" -m "Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"`
   - Confirm commit succeeded with `git log -1 --oneline`
4. If no:
   - Warn: "Deploying without committing. Changes are not version controlled."
   - Ask: "Continue anyway? (yes/no)"
   - If no, abort workflow

**Important**:
- Follow all git safety protocols from CLAUDE.md
- Never skip hooks or force operations
- Use heredoc format for commit messages

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
1. Load AAP job management tools: `ToolSearch` with query "aap job"
2. Call `mcp__aap-job-mgmt__job_templates_list` to list available templates
3. If developer specified template name (e.g., "Deploy environment for dev"):
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
2. Load inventory tools if needed: `ToolSearch` with query "aap inventory"
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

5. Apply safety guardrails from CLAUDE.md:
   - Production confirmation if needed
   - Version/tag confirmation if extra_vars contains version info
   - Inventory requirement validation

6. On confirmation, launch job:
   - Call `mcp__aap-job-mgmt__job_templates_launch_create`
   - Extract job ID and URL
   - Report:
     ```
     ✓ Deployment job launched
     Job ID: [id]
     URL: [AAP UI link]
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

3. On job completion (successful or failed):
   - Call `mcp__aap-job-mgmt__jobs_job_host_summaries_list` for host results
   - Call `mcp__aap-job-mgmt__jobs_stdout_retrieve` to get full output
   - Parse output for server details (IP addresses, URLs, ports, etc.)

4. Present deployment summary:
   ```
   ✓ Deployment completed successfully
   Duration: 3m 45s

   📊 Deployment Results:
   - Hosts changed: [count]
   - Hosts failed: [count]

   🖥️ Server Details:
   - Server: web-01.example.com (192.168.1.10)
   - Application URL: http://192.168.1.10/cheeseburger-map-app
   - Apache status: Running
   - Application path: /var/www/html/cheeseburger-map-app

   [If available from job output:]
   - Load balancer: lb-01.example.com
   - Health check: PASSED
   ```

5. Extract server details by:
   - Searching job stdout for patterns like:
     - IP addresses (regex: `\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b`)
     - URLs (regex: `https?://[^\s]+`)
     - Hostnames (from ansible facts or output)
     - Service ports
     - Application paths
   - Parsing ansible facts from job events if available
   - Looking for registered variables in playbook output

6. If deployment failed:
   - Show last 50 lines of output
   - Highlight error messages
   - Call `mcp__aap-job-mgmt__jobs_job_events_list` for failed events
   - Suggest fixes: "Check application logs on [failed host]?"

7. Ask follow-up:
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

## Example Interaction

```
Developer: "Deploy this but first commit the code to git, then trigger 'Deploy environment for dev'"

Claude:
Step 1: Checking git status...

Found uncommitted changes:
  M cheeseburger-map-app/index.html
  A cheeseburger-map-app/style.css
  A cheeseburger-map-app/app.js
  A cheeseburger-map-app/data.js

Commit these changes before deployment? (yes/no)

Developer: "yes"

Claude:
Proposed commit message:
"Add cheeseburger consumption map application

- Interactive world map showing consumption data
- 35+ countries with sample data
- Responsive design for Apache deployment"

Proceed with this commit message? (yes/no)

Developer: "yes"

Claude:
✓ Changes committed successfully
Commit: a1b2c3d Add cheeseburger consumption map application

Switching to dev branch for deployment...
Created new dev branch
✓ Pushed commit a1b2c3d to origin/dev

Loading AAP job templates...
Found template: "Deploy environment for dev" (ID: 42)

Ready to deploy:
- Template: Deploy environment for dev
- Inventory: dev-webservers (3 hosts)
- Environment: dev
- Branch: dev (pushed to origin/dev)
- Latest commit: a1b2c3d Add cheeseburger consumption map application
- Extra vars: none

Proceed with deployment? (yes/no)

Developer: "yes"

Claude:
✓ Deployment job launched
Job ID: 1523
URL: https://aap.example.com/#/jobs/playbook/1523/output
Status: Pending

Monitoring deployment...

[12:34:56] Running... (45s)
           Current: Copying application files to web-01

[12:35:26] Running... (1m 15s)
           Current: Restarting Apache on web-01

[12:35:56] ✓ Deployment completed successfully
Duration: 2m 30s

📊 Deployment Results:
- Hosts changed: 3
- Hosts failed: 0

🖥️ Server Details:
- Server: dev-web-01.example.com (10.0.1.10)
- Application URL: http://dev-web-01.example.com/cheeseburger-map-app
- Apache status: Running
- Application path: /var/www/html/cheeseburger-map-app
- DocumentRoot: /var/www/html

Additional servers:
- dev-web-02.example.com (10.0.1.11)
- dev-web-03.example.com (10.0.1.12)

Next steps:
- Test application: http://dev-web-01.example.com/cheeseburger-map-app
- Run smoke tests?
- Deploy to staging?
```

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
   - Apply all AAP safety guardrails from CLAUDE.md
   - Extra confirmation for production deployments
   - Show inventory host count

4. **Rollback Awareness**:
   - Track the commit SHA that was deployed
   - If deployment fails, suggest: "Revert commit a1b2c3d? (yes/no)"
   - Keep deployment history in conversation context

## Integration with Existing AAP Skill

This skill extends the AAP Job Execution Skill from CLAUDE.md by:
- Adding git operations before job launch
- Focusing on deployment workflows specifically
- Enhancing server details extraction from job output
- Providing deployment-specific follow-up suggestions

Both skills can coexist:
- Use this skill for: code deployments requiring git commits
- Use base AAP skill for: general job template execution (patching, restarts, provisioning)

## Success Criteria

The skill works correctly when:
- Developer can deploy with a single command
- All changes are committed before deployment
- Commits are automatically pushed to dev branch (not main/master)
- Job templates are discovered and launched automatically
- Deployment is monitored in real-time
- Server details are extracted and displayed clearly
- Failed deployments show errors and suggest fixes
- No manual AAP UI access is needed for standard deployments
- Dev branch isolation prevents accidental main branch deployments
