---
name: deploy-to-aap
description: Commits code, pushes to dev branch, and triggers Ansible Automation Platform deployment jobs
---

# Deploy to AAP Skill

This skill automates the deployment workflow by:

1. Checking git repository status
2. Committing any pending changes
3. Pushing to the 'dev' branch
4. Triggering AAP job templates for infrastructure, application deployment, and tests

## Usage

Simply invoke the skill:

```
/deploy-to-aap
```

## What it does

The skill will execute the deployment script which:

1. **Git Operations**
   - Verifies you're in a git repository
   - Checks for uncommitted changes
   - Creates/switches to 'dev' branch
   - Commits changes with a deployment message
   - Pushes to remote origin

2. **AAP Integration**
   - Loads configuration from `aap_config.json`
   - Triggers three job templates in sequence:
     - Infrastructure deployment (VMs, networking, load balancers)
     - Application deployment (pulls dev branch, deploys Flask app)
     - Test execution (runs pytest against deployed environment)
   - Returns job IDs for monitoring

## Configuration

The skill reads from `.claude/skills/deploy-to-aap/scripts/aap_config.json`.

Copy the example file and configure:

```bash
cp .claude/skills/deploy-to-aap/scripts/aap_config.json.example .claude/skills/deploy-to-aap/scripts/aap_config.json
```

## Mock vs Real Mode

By default, the skill runs in **mock mode** to demonstrate the workflow without requiring a real AAP instance.

To use with a real AAP instance:
1. Set `"mock_mode": false` in `aap_config.json`
2. Set the `AAP_TOKEN` environment variable
3. Configure your AAP URL and job template IDs

See `docs/AAP_INTEGRATION.md` for detailed setup instructions.

## Output

The skill will display:
- Git operations performed
- AAP job IDs (or mock IDs in demo mode)
- Links to monitor job execution in AAP dashboard
- Any errors encountered

## Requirements

- Git repository initialized
- Remote origin configured
- AAP configuration file present
- (For real mode) AAP_TOKEN environment variable set

Execute the deployment script:

```bash
bash .claude/skills/deploy-to-aap/scripts/deploy.sh
```
