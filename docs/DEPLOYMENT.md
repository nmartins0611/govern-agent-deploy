# Deployment Guide

## Overview

This guide explains how to use the `/deploy-to-aap` skill to deploy the banking application through Ansible Automation Platform.

## Quick Start

### Prerequisites

1. **Git repository initialized:**
   ```bash
   git init
   git remote add origin <your-repo-url>
   ```

2. **AAP configuration:**
   - Configuration file exists: `.claude/skills/deploy-to-aap/scripts/aap_config.json`
   - For real AAP: `AAP_TOKEN` environment variable set

3. **Code ready to deploy:**
   - All changes committed or ready to commit
   - Tests passing locally

### Using the Skill

Simply invoke:
```
/deploy-to-aap
```

The skill will:
1. Commit any pending changes
2. Switch to/create `dev` branch
3. Push to remote
4. Trigger AAP deployment jobs

## Workflow Details

### Step 1: Git Operations

The skill performs these git operations:

```bash
# Add all changes
git add -A

# Commit with deployment message
git commit -m "Deploy: Automated commit via /deploy-to-aap skill"

# Create or switch to dev branch
git checkout -b dev  # or git checkout dev

# Push to remote
git push -u origin dev
```

### Step 2: AAP Job Triggers

Three job templates are triggered in sequence:

#### 1. Infrastructure Deployment
**Duration:** ~5-10 minutes
**What it does:**
- Provisions cloud VMs
- Configures networks
- Sets up load balancers
- Configures firewalls

**AAP Playbook:** `ansible/playbooks/deploy-infrastructure.yml`

#### 2. Application Deployment
**Duration:** ~3-5 minutes
**What it does:**
- Clones dev branch from GitHub
- Installs Python dependencies
- Configures Flask application
- Starts/restarts service
- Configures Nginx/Apache

**AAP Playbook:** `ansible/playbooks/deploy-application.yml`

#### 3. Test Execution
**Duration:** ~2-3 minutes
**What it does:**
- Installs test dependencies
- Runs pytest suite
- Generates coverage report
- Reports results

**AAP Playbook:** `ansible/playbooks/run-tests.yml`

## Mock vs Real Mode

### Mock Mode (Default)

**Use when:**
- Demonstrating the workflow
- No AAP instance available
- Testing the skill itself

**Behavior:**
- Git operations are real
- AAP jobs are simulated
- Mock job IDs displayed
- No actual infrastructure changes

**Configuration:**
```json
{
  "mock_mode": true
}
```

### Real Mode

**Use when:**
- AAP instance configured
- Ready for actual deployment
- AAP_TOKEN set

**Behavior:**
- All operations are real
- Actual AAP jobs launched
- Real infrastructure provisioned
- Returns actual job IDs

**Configuration:**
```json
{
  "mock_mode": false
}
```

Set `AAP_TOKEN`:
```bash
export AAP_TOKEN="your-aap-token"
```

## Manual Deployment

If you prefer manual control, run the deployment script directly:

```bash
bash .claude/skills/deploy-to-aap/scripts/deploy.sh
```

## Monitoring Deployment

### During Deployment

The skill displays:
- Git operation status
- AAP job IDs
- Links to AAP dashboard

### After Deployment

Monitor in AAP web interface:
```
https://your-aap-instance.com/#/jobs
```

View specific job:
```
https://your-aap-instance.com/#/jobs/playbook/{job_id}
```

## Troubleshooting

### "Not a git repository"

**Problem:** Git not initialized

**Solution:**
```bash
git init
git remote add origin <your-repo-url>
```

### "Configuration file not found"

**Problem:** `aap_config.json` missing

**Solution:**
```bash
cp .claude/skills/deploy-to-aap/scripts/aap_config.json.example \
   .claude/skills/deploy-to-aap/scripts/aap_config.json
```

### "Push failed"

**Problem:** Remote not configured or authentication failed

**Solution:**
```bash
# Configure remote
git remote add origin git@github.com:username/repo.git

# Or update existing
git remote set-url origin git@github.com:username/repo.git

# Verify SSH key
ssh -T git@github.com
```

### "AAP_TOKEN not set" (Real Mode)

**Problem:** Environment variable missing

**Solution:**
```bash
export AAP_TOKEN="your-token-here"

# Make permanent
echo 'export AAP_TOKEN="your-token"' >> ~/.bashrc
source ~/.bashrc
```

### AAP Job Failed

**Problem:** AAP job template execution failed

**Debug steps:**
1. Check job logs in AAP dashboard
2. Verify inventory and credentials
3. Check playbook syntax
4. Ensure target hosts are reachable

## Best Practices

### Before Deploying

1. **Run tests locally:**
   ```bash
   pytest tests/ -v
   ```

2. **Check code quality:**
   ```bash
   black banking_app/
   ```

3. **Review changes:**
   ```bash
   git diff
   git status
   ```

### Git Workflow

**Recommended branch strategy:**
```
main (production)
├── staging
│   └── dev (feature development)
└── hotfix-*
```

**Workflow:**
1. Develop on feature branches
2. Merge to `dev` for testing
3. Use `/deploy-to-aap` to deploy dev to test environment
4. After testing, merge `dev` → `staging`
5. Deploy staging to staging environment
6. After approval, merge `staging` → `main`
7. Deploy main to production

### Environment Strategy

**Separate configurations:**
- Development: Deploy from `dev` branch
- Staging: Deploy from `staging` branch
- Production: Deploy from `main` branch

**Configure per environment:**
```json
{
  "github": {
    "dev_branch": "dev"
  },
  "deployment": {
    "environment": "development"
  }
}
```

## Advanced Usage

### Custom Commit Message

Edit deployment script to customize commit message:

```bash
git commit -m "Deploy: Your custom message here"
```

### Deploy Specific Branch

Modify `aap_config.json`:
```json
{
  "github": {
    "dev_branch": "feature/new-feature"
  }
}
```

### Additional AAP Variables

Pass extra variables in deployment script:

```bash
--data "{\"extra_vars\": {
  \"git_branch\": \"$DEV_BRANCH\",
  \"app_port\": 8000,
  \"workers\": 4
}}"
```

## Rollback

If deployment fails:

### Option 1: Revert Commit
```bash
git revert HEAD
git push origin dev
/deploy-to-aap  # Deploy previous version
```

### Option 2: Deploy Previous Tag
```bash
git checkout v1.0.0
/deploy-to-aap
```

### Option 3: Manual AAP Rollback
1. Navigate to AAP dashboard
2. Find successful previous job
3. Click "Relaunch"

## Security Notes

### Never Commit:
- API tokens
- Passwords
- Private keys
- `aap_config.json` with sensitive data

### Use Environment Variables:
```bash
export AAP_TOKEN="..."
export DATABASE_PASSWORD="..."
```

### Verify Before Deploy:
- No secrets in code
- `.gitignore` configured correctly
- Environment-specific configs separated

## Next Steps

After successful deployment:

1. **Verify application:**
   ```bash
   curl https://your-deployed-app.com/api/v1/health
   ```

2. **Check logs:**
   - AAP job output
   - Application logs on servers

3. **Run smoke tests:**
   ```bash
   pytest tests/smoke/ -v
   ```

4. **Monitor metrics:**
   - Application performance
   - Error rates
   - Response times

## Additional Resources

- [AAP Integration Guide](AAP_INTEGRATION.md)
- [API Documentation](API.md)
- [Ansible Automation Platform Docs](https://docs.ansible.com/automation-controller/)
