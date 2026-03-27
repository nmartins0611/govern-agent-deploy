# Content Skill Architecture Guide

This document explains how the AI agent skills, Ansible automation content, and application content work together in `govern-agent-deploy` to create a governed deployment pipeline.

## What Is a "Content Skill"?

In this project, a content skill is an instruction set that teaches an AI coding agent how to safely manage and deploy automation content through Ansible Automation Platform. The skill defines:

- **What the agent can do** -- trigger AAP jobs, monitor execution, extract results
- **How it must behave** -- mandatory confirmation steps, production safeguards, log retrieval
- **What it cannot do** -- skip pre-flight checks, bypass production confirmation, ignore failures

The content itself (playbooks, applications, templates) is what gets deployed. The skill governs _how_ the agent interacts with that content through AAP.

## Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                        Developer                                 │
│               (natural language requests)                        │
└────────────────────────┬─────────────────────────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────────────────┐
│                   AI Agent Layer                                 │
│                                                                  │
│  ┌────────────────────┐    ┌─────────────────────────────────┐  │
│  │  CLAUDE.md          │    │  DEPLOY_SKILL.md                │  │
│  │  Base AAP Skill     │    │  Deploy with Commit Skill       │  │
│  │                     │    │                                  │  │
│  │  • Job discovery    │    │  • Git commit/push              │  │
│  │  • Pre-flight check │    │  • Dev branch management        │  │
│  │  • Job launch       │    │  • Template discovery           │  │
│  │  • Status monitoring│    │  • Server detail extraction     │  │
│  │  • Result summary   │    │  • Rollback suggestions         │  │
│  │                     │    │                                  │  │
│  │  Use for:           │    │  Use for:                       │  │
│  │  Patching, restarts │    │  Code deployments               │  │
│  │  provisioning, any  │    │  with version control           │  │
│  │  AAP job template   │    │  integration                    │  │
│  └────────────────────┘    └─────────────────────────────────┘  │
│                                                                  │
│  Safety Guardrails (enforced by both skills):                   │
│  ├── Production confirmation phrases                            │
│  ├── Version/tag verification                                   │
│  ├── Inventory validation                                       │
│  ├── Duplicate run detection                                    │
│  ├── Long-running job alerts                                    │
│  └── Automatic failure log retrieval                            │
└────────────────────────┬─────────────────────────────────────────┘
                         │ MCP Server Tools
                         │ (aap-job-mgmt, aap-inventory)
                         ▼
┌──────────────────────────────────────────────────────────────────┐
│               Ansible Automation Platform                        │
│                                                                  │
│  Job Templates ──► Inventories ──► Playbook Execution           │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Automation Content (ansible-playbooks/)                  │   │
│  │                                                           │   │
│  │  deploy.yml    ─── Install Apache, copy app, configure   │   │
│  │  verify.yml    ─── Validate deployment succeeded         │   │
│  │  rollback.yml  ─── Remove app, keep infrastructure       │   │
│  │  cleanup.yml   ─── Full teardown to pre-deploy state     │   │
│  └──────────────────────────────────────────────────────────┘   │
│                         │                                        │
│                         ▼                                        │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Target RHEL Servers                                      │   │
│  │                                                           │   │
│  │  Apache (httpd) + firewalld + SELinux                    │   │
│  │  └── /var/www/html/cheeseburger-map/                     │   │
│  │      ├── index.html                                       │   │
│  │      ├── app.js                                           │   │
│  │      ├── data.js                                          │   │
│  │      └── style.css                                        │   │
│  └──────────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────────┘
```

## Skill Design Principles

### 1. Mandatory Human Confirmation

Every destructive or impactful action requires explicit developer approval. The agent never auto-launches jobs.

```
Agent: Ready to deploy:
       - Template: Deploy to dev
       - Inventory: dev-webservers (3 hosts)
       Proceed? (yes/no)

Developer: yes                          ← Required before launch
```

For production targets, a specific phrase is required:

```
Agent: ⚠ This will affect 47 production hosts
       Type: "yes, target production"

Developer: yes, target production       ← Exact phrase required
```

### 2. Progressive Disclosure

The workflow reveals information step by step, giving the developer control at each stage:

| Step | What the agent shows | What the developer decides |
|------|---------------------|---------------------------|
| Git status | Changed files | Whether to commit |
| Commit message | AI-generated summary | Accept, modify, or reject |
| Branch push | Target branch and SHA | Whether to proceed |
| Pre-flight | Template, inventory, host count | Whether to launch |
| Monitoring | Real-time task progress | Whether to continue or cancel |
| Results | Server details, host summaries | Next action (test, promote, rollback) |

### 3. Fail-Safe Defaults

- Dev branch isolation: deployments never push to main/master
- Automatic log retrieval: failures surface error context immediately
- Git hook compliance: the agent never bypasses pre-commit hooks
- Inventory validation: missing inventories halt the workflow
- Duplicate detection: re-launching the same template within 2 minutes triggers a warning

### 4. Transparent State

The agent always shows what it's about to do and what it did:

- Pre-flight summaries before every launch
- Real-time monitoring with task names and elapsed time
- Post-job summaries with per-host results
- Server detail extraction (IPs, URLs, paths) from playbook output

## Content Lifecycle

### Deployment Content

The Ansible playbooks manage the full application lifecycle:

```
deploy.yml ──────► Application running on RHEL servers
                   Apache configured, firewall open, SELinux set

verify.yml ──────► Confirmation that deployment succeeded
                   All assertions pass: httpd running, files present,
                   HTTP 200, firewall rules active, SELinux correct

rollback.yml ────► Application removed, Apache reset to defaults
                   Infrastructure (Apache, firewall) remains installed

cleanup.yml ─────► Complete teardown to pre-deployment state
                   Apache uninstalled, firewall rules removed
```

### Playbook Design for Agent Extraction

The playbooks are structured to produce output that the AI agent can parse for server details. Key patterns:

```yaml
# The agent looks for debug messages containing URLs, IPs, paths
- name: Display deployment info
  ansible.builtin.debug:
    msg: "Application URL: http://{{ ansible_fqdn }}/{{ app_name }}"

# PLAY RECAP gives the agent host-level success/failure counts
# Job events give task-level granularity
# Host summaries give per-host ok/changed/failed/unreachable counts
```

The `verify.yml` playbook produces structured assertions that map directly to the agent's result extraction:

| Verification | What the agent reports |
|-------------|----------------------|
| httpd running | "Apache status: Running" |
| HTTP 200 response | "Health check: PASSED" |
| Files present | "Application files deployed" |
| SELinux context | "SELinux: correctly configured" |

## MCP Integration

The skills interact with AAP exclusively through MCP server tools. No direct API calls are made.

### Tool Namespaces

| Namespace | Tools | Purpose |
|-----------|-------|---------|
| `aap-job-mgmt` | `job_templates_list`, `job_templates_retrieve`, `job_templates_launch_create`, `jobs_retrieve`, `jobs_stdout_retrieve`, `jobs_job_events_list`, `jobs_job_host_summaries_list`, `jobs_list` | Job template management, launch, monitoring |
| `aap-inventory` | `inventories_list`, `hosts_list` | Inventory and host discovery |

### Typical MCP Call Sequence

```
1. job_templates_list           → Find matching template
2. job_templates_retrieve       → Get template details (inventory, vars)
3. inventories_list             → Validate inventory and host count
4. job_templates_launch_create  → Launch the job
5. jobs_retrieve (polling)      → Monitor status every 30s
6. jobs_job_events_list         → Get current task names while running
7. jobs_retrieve (final)        → Get terminal status
8. jobs_job_host_summaries_list → Per-host results
9. jobs_stdout_retrieve         → Full output for detail extraction
```

## Alternative Integration Methods

The base skill (`CLAUDE.md`) documents two alternative approaches for environments without MCP:

### Direct REST API

Uses `curl` or HTTP tools to call the AAP Controller API directly. Requires managing authentication tokens, SSL certificates, pagination, and rate limits. Better for environments without MCP server support.

### Event Driven Ansible (EDA)

Sends webhook payloads to an EDA Controller, which routes events through rulebooks to trigger AAP jobs. Better for complex event-driven workflows, multi-step automations, and environments that aggregate events from multiple sources.

Both alternatives are documented as commented-out sections in `CLAUDE.md` and can be enabled by uncommenting the relevant block.

## Extending the Skills

### Adding a New Deployment Target

1. Create a new playbook (e.g., `deploy-staging.yml`)
2. Add a corresponding AAP job template
3. The AI agent will discover it automatically via `job_templates_list`

### Adding Pre/Post Deployment Steps

Chain operations in conversation:

```
Developer: "Deploy to dev, run verify, then deploy to staging if it passes"
```

The agent executes each step sequentially, confirming before each launch.

### Customizing Server Detail Extraction

Add structured debug output to your playbooks:

```yaml
- name: Show deployment details
  debug:
    msg:
      - "Application URL: http://{{ ansible_fqdn }}/{{ app_name }}"
      - "Version: {{ app_version }}"
      - "Database: {{ db_host }}:{{ db_port }}"
```

The agent's extraction patterns look for:
- IP addresses (`\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b`)
- URLs (`https?://[^\s]+`)
- Hostnames from Ansible facts
- Key-value patterns in debug messages

### Adding Custom Safety Rules

Edit the skill files to add environment-specific guardrails:

```markdown
## Additional Safety Rules

- Require approval ticket number for production deployments
- Block deployments during maintenance windows (Friday 5pm - Monday 8am)
- Require minimum test coverage before staging promotion
```

## File Reference

| File | Type | Consumed By | Purpose |
|------|------|-------------|---------|
| `CLAUDE.md` | AI Skill | Claude Code agent | Base AAP job execution instructions |
| `DEPLOY_SKILL.md` | AI Skill | Claude Code agent | Git + deployment workflow instructions |
| `ansible-playbooks/deploy.yml` | Playbook | AAP / Ansible | Install and deploy the application |
| `ansible-playbooks/verify.yml` | Playbook | AAP / Ansible | Post-deployment health checks |
| `ansible-playbooks/rollback.yml` | Playbook | AAP / Ansible | Remove application, keep infrastructure |
| `ansible-playbooks/cleanup.yml` | Playbook | AAP / Ansible | Full teardown |
| `ansible-playbooks/requirements.yml` | Dependencies | ansible-galaxy | Collection requirements (ansible.posix) |
| `ansible-playbooks/ansible.cfg` | Config | Ansible | SSH, privilege escalation, caching |
| `ansible-playbooks/group_vars/webservers.yml` | Variables | Ansible | App name, version, server settings |
| `ansible-playbooks/inventory/hosts` | Inventory | Ansible | Target RHEL server addresses |
| `ansible-playbooks/templates/cheeseburger-map.conf.j2` | Template | Ansible | Apache vhost with security headers |
| `cheeseburger-map-app/*` | Application | Apache / Browser | Static web app (HTML/CSS/JS) |
| `SKILL_PACKAGE/*` | Documentation | Humans | Distributable skill package with guides |
