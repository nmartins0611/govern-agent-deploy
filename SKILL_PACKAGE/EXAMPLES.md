# Usage Examples

Real-world scenarios showing how to use the AAP Deployment Skill.

## Example 1: First-Time Deployment

**Scenario**: You've built a new web application and want to deploy it to dev.

```
You: "I just finished the cheeseburger map app. Deploy it to dev."

Claude:
Checking git status...

Found uncommitted changes:
  A cheeseburger-map-app/index.html
  A cheeseburger-map-app/style.css
  A cheeseburger-map-app/app.js
  A cheeseburger-map-app/data.js

Commit these changes before deployment? (yes/no)

You: "yes"

Claude:
Proposed commit message:
"Add cheeseburger consumption map application

- Interactive world map with D3.js visualization
- 35+ countries with consumption data
- Responsive design for web deployment"

Proceed with this commit message? (yes/no)

You: "yes"

Claude:
✓ Changes committed successfully
Commit: f8a9c2e Add cheeseburger consumption map application

Creating dev branch...
✓ Pushed commit f8a9c2e to origin/dev

Loading AAP deployment templates...
Found 3 deployment templates:
1. Deploy environment for dev
2. Deploy to staging
3. Deploy to production

Which template should I use?

You: "1"

Claude:
Ready to deploy:
- Template: Deploy environment for dev
- Inventory: dev-webservers (3 hosts)
- Environment: dev
- Branch: dev (pushed to origin/dev)
- Latest commit: f8a9c2e Add cheeseburger consumption map application
- Extra vars: none

Proceed with deployment? (yes/no)

You: "yes"

Claude:
✓ Deployment job launched
Job ID: 1523
URL: https://aap.example.com/#/jobs/playbook/1523/output
Status: Pending

Monitoring deployment...

[14:23:15] Running... (30s)
           Current: Copying application files to dev-web-01

[14:23:45] Running... (1m 0s)
           Current: Configuring Apache vhost

[14:24:15] Running... (1m 30s)
           Current: Restarting Apache service

[14:24:35] ✓ Deployment completed successfully
Duration: 2m 20s

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

---

## Example 2: Update Existing App

**Scenario**: You've fixed a bug and want to redeploy.

```
You: "Fixed the data rendering bug. Redeploy to dev."

Claude:
Checking git status...

Found uncommitted changes:
  M cheeseburger-map-app/app.js

Commit these changes before deployment? (yes/no)

You: "yes"

Claude:
Proposed commit message:
"Fix data rendering bug in cheeseburger map

- Resolve undefined country data handling
- Add null checks for consumption values"

Proceed with this commit message? (yes/no)

You: "yes"

Claude:
✓ Changes committed successfully
Commit: 3b7d1f2 Fix data rendering bug in cheeseburger map

Already on dev branch
✓ Pushed commit 3b7d1f2 to origin/dev

Found template: "Deploy environment for dev"

Ready to deploy:
- Template: Deploy environment for dev
- Inventory: dev-webservers (3 hosts)
- Environment: dev
- Branch: dev
- Latest commit: 3b7d1f2 Fix data rendering bug
- Extra vars: none

Proceed with deployment? (yes/no)

You: "yes"

Claude:
✓ Deployment job launched
Job ID: 1547

[14:45:20] Running... (25s)
[14:45:45] ✓ Deployment completed successfully
Duration: 1m 5s

📊 Deployment Results:
- Hosts changed: 3
- Hosts failed: 0

🖥️ Server Details:
- Application URL: http://dev-web-01.example.com/cheeseburger-map-app
- 3 hosts updated successfully

Test the fix: http://dev-web-01.example.com/cheeseburger-map-app
```

---

## Example 3: Production Deployment with Version Tag

**Scenario**: Ready to deploy version 1.2.0 to production.

```
You: "Deploy version 1.2.0 to production"

Claude:
Checking git status...
Working tree clean, proceeding to deployment

Loading AAP templates...
Found template: "Deploy to production"

⚠ Production Target Detected

Ready to deploy:
- Template: Deploy to production
- Inventory: production-webservers (24 hosts)
- Environment: production
- Branch: master
- Latest commit: a4f8e3c Release version 1.2.0
- Extra vars:
  version: 1.2.0

⚠ This will affect 24 production hosts

Confirm deployment of version 1.2.0 to production

To proceed, type: "yes, target production"

You: "yes, target production"

Claude:
✓ Confirmed. Launching deployment...

✓ Deployment job launched
Job ID: 1589
URL: https://aap.example.com/#/jobs/playbook/1589/output

Monitoring deployment...

[15:30:10] Running... (1m 30s)
           Current: Rolling restart web servers (batch 1/4)

[15:31:40] Running... (3m 0s)
           Current: Rolling restart web servers (batch 2/4)

[15:33:10] Running... (4m 30s)
           Current: Health check verification

[15:34:20] ✓ Deployment completed successfully
Duration: 6m 10s

📊 Deployment Results:
- Hosts changed: 24
- Hosts failed: 0
- Hosts unreachable: 0

🖥️ Production Servers:
- Load balancer: lb-prod.example.com
- Application URL: https://app.example.com
- Version deployed: 1.2.0
- Health check: PASSED (24/24 hosts healthy)
- Rolling restart: Completed successfully

Next steps:
- Monitor application metrics
- Check error logs
- Verify user traffic distribution
```

---

## Example 4: Deployment Failure and Rollback

**Scenario**: Deployment fails due to configuration error.

```
You: "Deploy to staging"

Claude:
[Commit and push steps...]

✓ Deployment job launched
Job ID: 1602

Monitoring deployment...

[16:15:30] Running... (45s)
           Current: Applying configuration changes

[16:16:15] ✗ Deployment failed
Duration: 1m 30s

📊 Deployment Results:
- Hosts changed: 0
- Hosts failed: 3
- Hosts unreachable: 0

❌ Failure Details:

Failed task: "Configure application settings"
Failed hosts:
- staging-web-01: Invalid JSON in config file
- staging-web-02: Invalid JSON in config file
- staging-web-03: Invalid JSON in config file

Last 20 lines of output:
---
TASK [Configure application settings] *****************************************
fatal: [staging-web-01]: FAILED! => {
    "msg": "Error parsing config.json: Expecting property name enclosed in double quotes"
}
---

Suggested fix: Check config.json syntax on line 15

Would you like to:
1. Fix the config and retry?
2. Revert commit 7c4f8a2?
3. Check detailed logs?

You: "2"

Claude:
Reverting commit 7c4f8a2...
✓ Commit reverted with new commit: 9d2e5b1 Revert "Update staging config"

The config error has been removed. Fix the JSON syntax and try again when ready.
```

---

## Example 5: Multi-Environment Deployment

**Scenario**: Deploy to dev, then staging, then production in sequence.

```
You: "Deploy to dev, then staging, then if both succeed deploy to prod"

Claude:
Step 1: Deploying to dev environment

[Commit + dev deployment...]

✓ Dev deployment completed successfully (2m 15s)
- Application URL: http://dev-web-01.example.com/app

Step 2: Deploying to staging environment

Ready to deploy:
- Template: Deploy to staging
- Inventory: staging-webservers (6 hosts)
- Branch: dev
- Latest commit: f3a7c1e Feature update

Proceed with staging deployment? (yes/no)

You: "yes"

Claude:
✓ Staging deployment completed successfully (3m 40s)
- Application URL: http://staging.example.com/app
- 6 hosts changed successfully

Both dev and staging deployments succeeded.

Step 3: Deploying to production

⚠ Production Target Detected

Ready to deploy:
- Template: Deploy to production
- Inventory: production-webservers (24 hosts)
- Branch: master (will merge dev → master first)
- Latest commit: f3a7c1e Feature update

⚠ This will affect 24 production hosts

To proceed, type: "yes, target production"

You: "yes, target production"

Claude:
Merging dev → master...
✓ Merged and pushed to origin/master

✓ Production deployment completed successfully (6m 50s)
- Application URL: https://app.example.com
- 24 hosts changed successfully
- Health check: PASSED

All environments deployed successfully:
✓ Dev (2m 15s)
✓ Staging (3m 40s)
✓ Production (6m 50s)
```

---

## Example 6: Deployment with Smoke Tests

**Scenario**: Deploy and automatically run smoke tests.

```
You: "Deploy to staging and run smoke tests"

Claude:
Step 1: Deploying application

[Commit + deployment...]

✓ Deployment completed successfully (2m 45s)
- Application URL: http://staging.example.com/app

Step 2: Running smoke tests

Loading test templates...
Found template: "Run application smoke tests"

Ready to launch:
- Template: Run application smoke tests
- Inventory: staging-webservers (6 hosts)
- Extra vars:
  app_url: http://staging.example.com/app

Proceed with smoke tests? (yes/no)

You: "yes"

Claude:
✓ Smoke test job launched
Job ID: 1635

Monitoring tests...

[17:30:15] Running... (30s)
           Current: HTTP endpoint tests

[17:30:45] Running... (1m 0s)
           Current: Database connectivity tests

[17:31:15] Running... (1m 30s)
           Current: API response time tests

[17:31:35] ✓ Smoke tests passed
Duration: 1m 50s

📊 Test Results:
✓ HTTP endpoints: 15/15 passed
✓ Database connections: 6/6 passed
✓ API response times: All < 200ms
✓ Health check: All hosts healthy

Deployment validated successfully!

Next step: Deploy to production?
```

---

## Example 7: Skip Commit (Deploy Uncommitted)

**Scenario**: Quick test deployment without committing.

```
You: "Just deploy this to my test server, don't commit yet"

Claude:
Checking git status...

Found uncommitted changes:
  M app.js
  M style.css

Commit these changes before deployment? (yes/no)

You: "no"

Claude:
⚠ Warning: Deploying without committing. Changes are not version controlled.

Continue anyway? (yes/no)

You: "yes"

Claude:
Proceeding with deployment (uncommitted changes)...

Ready to deploy:
- Template: Deploy to test
- Inventory: test-server (1 host)
- Branch: dev (current state)
- Status: ⚠ Uncommitted changes present
- Extra vars: none

Proceed with deployment? (yes/no)

You: "yes"

Claude:
✓ Deployment completed successfully (1m 15s)
- Application URL: http://test.example.com/app

⚠ Reminder: Changes are not committed. Don't forget to commit when ready.
```

---

## Tips for Best Results

### Commit Messages
Let Claude generate them - they're based on actual code changes:
```
You: "yes" (to commit prompt)
```

Or provide your own:
```
You: "yes but use this message: Hotfix for login bug"
```

### Template Discovery
Be specific to save time:
```
You: "Deploy using template 'Deploy environment for dev'"
```

Or let Claude find it:
```
You: "Deploy to dev"  # Claude will search for dev-related templates
```

### Server Details
Make sure your playbooks output useful info:
```yaml
- name: Display deployment info
  debug:
    msg: |
      Application deployed to: http://{{ ansible_fqdn }}/{{ app_name }}
      Version: {{ app_version }}
      Port: {{ app_port }}
```

Claude will extract and display this automatically.

### Chained Operations
You can request multi-step workflows:
```
You: "Deploy to dev, run tests, and if tests pass deploy to staging"
```

Claude will execute each step and confirm before proceeding.
