# Ansible Automation Platform Integration

## Overview

This document explains how to integrate the `/deploy-to-aap` skill with a real Ansible Automation Platform (AAP) instance.

By default, the skill runs in **mock mode** for demonstration purposes. This guide shows how to configure it for production use.

## Architecture

### Deployment Workflow

1. **Developer invokes skill** → `/deploy-to-aap`
2. **Git operations** → Code committed and pushed to dev branch
3. **AAP job triggers** → Three job templates launched:
   - Infrastructure provisioning
   - Application deployment
   - Test execution

### AAP Job Templates

The integration expects three job templates configured in AAP:

#### 1. Deploy Infrastructure
- **Purpose:** Provision cloud resources (VMs, networks, load balancers)
- **Playbook:** `ansible/playbooks/deploy-infrastructure.yml`
- **Inventory:** Dynamic cloud inventory
- **Variables:**
  - `git_branch`: Branch to deploy from
  - `environment`: Target environment (dev/staging/prod)

#### 2. Deploy Application
- **Purpose:** Deploy the Flask banking application
- **Playbook:** `ansible/playbooks/deploy-application.yml`
- **Steps:**
  - Clone repository from specified branch
  - Install Python dependencies
  - Configure application
  - Start/restart Flask service
- **Variables:**
  - `git_branch`: Branch to deploy
  - `app_port`: Application port (default: 5000)

#### 3. Run Tests
- **Purpose:** Execute pytest suite against deployed application
- **Playbook:** `ansible/playbooks/run-tests.yml`
- **Steps:**
  - Install test dependencies
  - Run pytest with coverage
  - Report results
- **Variables:**
  - `git_branch`: Branch to test

## Configuration

### 1. AAP Setup

#### Create Job Templates

In your AAP instance:

1. Navigate to **Templates** → **Add** → **Job Template**
2. Create three templates with these settings:

**Infrastructure Template:**
- Name: Deploy Infrastructure
- Job Type: Run
- Inventory: Your cloud inventory
- Project: Your banking-app project
- Playbook: `ansible/playbooks/deploy-infrastructure.yml`
- Credentials: Cloud credentials
- Variables: `git_branch: dev`

**Application Template:**
- Name: Deploy Application
- Job Type: Run
- Inventory: Application servers
- Project: Your banking-app project
- Playbook: `ansible/playbooks/deploy-application.yml`
- Credentials: SSH credentials
- Variables: `git_branch: dev`, `app_port: 5000`

**Tests Template:**
- Name: Run Tests
- Job Type: Run
- Inventory: Application servers
- Project: Your banking-app project
- Playbook: `ansible/playbooks/run-tests.yml`
- Credentials: SSH credentials

#### Get Template IDs

Find the template IDs from AAP API:

```bash
curl -H "Authorization: Bearer $AAP_TOKEN" \
  https://your-aap-instance.com/api/v2/job_templates/
```

Note the `id` field for each template.

### 2. Authentication

#### Generate API Token

1. Log into AAP web interface
2. Navigate to **Users** → Your user → **Tokens**
3. Click **Add**
4. Set scope to **Write**
5. Copy the generated token

#### Set Environment Variable

```bash
export AAP_TOKEN="your-aap-token-here"
```

For persistent configuration, add to your shell profile:

```bash
echo 'export AAP_TOKEN="your-token"' >> ~/.bashrc
source ~/.bashrc
```

### 3. Configure Skill

Edit `.claude/skills/deploy-to-aap/scripts/aap_config.json`:

```json
{
  "aap_url": "https://your-aap-instance.com",
  "job_templates": {
    "infrastructure": {
      "id": 10,
      "name": "Deploy Infrastructure"
    },
    "application": {
      "id": 15,
      "name": "Deploy Application"
    },
    "tests": {
      "id": 20,
      "name": "Run Tests"
    }
  },
  "mock_mode": false,
  "github": {
    "repo_url": "git@github.com:your-org/govern-agent-deploy.git",
    "dev_branch": "dev"
  }
}
```

**Important:** Set `"mock_mode": false` to enable real AAP integration.

## AAP API Reference

### Launch Job Template

**Endpoint:** `POST /api/v2/job_templates/{id}/launch/`

**Headers:**
```
Authorization: Bearer {token}
Content-Type: application/json
```

**Body:**
```json
{
  "extra_vars": {
    "git_branch": "dev",
    "environment": "development"
  }
}
```

**Response:**
```json
{
  "id": 1234,
  "name": "Deploy Application",
  "status": "pending",
  "url": "/api/v2/jobs/1234/",
  "related": {
    "stdout": "/api/v2/jobs/1234/stdout/"
  }
}
```

### Monitor Job Status

**Endpoint:** `GET /api/v2/jobs/{id}/`

**Response:**
```json
{
  "id": 1234,
  "status": "successful",
  "started": "2026-02-28T10:00:00Z",
  "finished": "2026-02-28T10:05:00Z",
  "failed": false
}
```

## Troubleshooting

### Common Issues

#### "AAP_TOKEN not set"

**Cause:** Environment variable missing

**Solution:**
```bash
export AAP_TOKEN="your-token-here"
```

#### "Job template not found"

**Cause:** Incorrect template ID in config

**Solution:** Verify template IDs via AAP API:
```bash
curl -H "Authorization: Bearer $AAP_TOKEN" \
  https://your-aap.com/api/v2/job_templates/
```

#### "Unauthorized"

**Cause:** Invalid or expired token

**Solution:** Generate new token in AAP web interface

#### "Network timeout"

**Cause:** Cannot reach AAP instance

**Solution:**
- Verify AAP URL is correct
- Check network connectivity
- Verify firewall rules allow access

### Debug Mode

Enable verbose output in the deployment script:

```bash
bash -x .claude/skills/deploy-to-aap/scripts/deploy.sh
```

## Security Considerations

### Production Recommendations

1. **Never commit tokens:** Keep `AAP_TOKEN` in environment, not in files
2. **Use HTTPS:** Ensure AAP URL uses HTTPS
3. **Token rotation:** Regularly rotate API tokens
4. **Least privilege:** Grant tokens minimum required permissions
5. **Audit logs:** Monitor AAP job execution logs
6. **Branch protection:** Require PR reviews for production branches

### Network Security

- Run AAP behind VPN or private network
- Use IP allowlisting for API access
- Enable rate limiting on AAP API endpoints
- Use mutual TLS for enhanced security

## Advanced Configuration

### Custom Playbooks

To use different playbooks, update the job templates in AAP to point to your custom playbooks.

### Environment Variables

Pass additional variables to AAP jobs by modifying the deployment script:

```bash
--data "{\"extra_vars\": {
  \"git_branch\": \"$DEV_BRANCH\",
  \"custom_var\": \"value\"
}}"
```

### Webhook Integration

For automated deployments on git push:

1. Configure webhook in GitHub/GitLab
2. Point to AAP webhook endpoint
3. AAP automatically triggers on push to dev branch

### Notifications

Configure AAP notifications:
- Email on job completion/failure
- Slack integration
- Custom webhooks

## Monitoring

### AAP Dashboard

Monitor jobs in AAP web interface:
```
https://your-aap.com/#/jobs
```

### Job Logs

View job output:
```
https://your-aap.com/#/jobs/playbook/{job_id}
```

### Prometheus Metrics

AAP exposes metrics for Prometheus monitoring:
- Job success/failure rates
- Job duration
- Queue depth

## References

- [AAP API Documentation](https://docs.ansible.com/automation-controller/latest/html/controllerapi/index.html)
- [Job Templates Guide](https://docs.ansible.com/automation-controller/latest/html/userguide/job_templates.html)
- [API Authentication](https://docs.ansible.com/automation-controller/latest/html/administration/oauth2_token_auth.html)
