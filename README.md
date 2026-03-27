# govern-agent-deploy

AI-governed deployment workflows for Ansible Automation Platform (AAP). This repository demonstrates how AI coding agents (Claude Code) can safely commit, push, and deploy application content through AAP job templates using conversational interfaces.

## Overview

This project combines three components into a governed deployment pipeline:

| Component | Purpose |
|-----------|---------|
| **AI Agent Skills** | Instruction sets that teach Claude Code how to interact with AAP safely |
| **Sample Application** | A static web app (Cheeseburger Consumption Map) used as deployment content |
| **Ansible Playbooks** | Automation content that deploys, verifies, rolls back, and cleans up the application on RHEL servers |

The result is a conversational deployment workflow where a developer says _"deploy this app"_ and the AI agent handles the full lifecycle: git commit, branch management, AAP job template discovery, launch, monitoring, and result extraction.

## Repository Structure

```
govern-agent-deploy/
├── CLAUDE.md                          # Base AAP Job Execution Skill (agent instructions)
├── DEPLOY_SKILL.md                    # Deploy with Commit Skill (git + AAP workflow)
├── README.md                          # This file
│
├── cheeseburger-map-app/              # Sample web application content
│   ├── index.html                     #   Leaflet.js interactive world map
│   ├── app.js                         #   Map initialization and interactivity
│   ├── data.js                        #   Country consumption data + color scheme
│   ├── style.css                      #   Layout and responsive styling
│   ├── .htaccess                      #   Apache rewrite rules
│   └── README.md                      #   Application-specific documentation
│
├── ansible-playbooks/                 # Ansible automation content
│   ├── deploy.yml                     #   Main deployment playbook
│   ├── verify.yml                     #   Post-deployment verification
│   ├── rollback.yml                   #   Application removal (keeps Apache)
│   ├── cleanup.yml                    #   Full teardown (removes Apache too)
│   ├── requirements.yml               #   Galaxy collection dependencies
│   ├── ansible.cfg                    #   Ansible configuration
│   ├── inventory/hosts                #   Target host inventory
│   ├── group_vars/webservers.yml      #   Webserver group variables
│   ├── templates/
│   │   └── cheeseburger-map.conf.j2   #   Apache vhost Jinja2 template
│   ├── README.md                      #   Playbook documentation
│   └── QUICK_START.md                 #   Playbook quick start guide
│
└── SKILL_PACKAGE/                     # Distributable skill package
    ├── README.md                      #   Package overview and installation
    ├── QUICK_START.md                 #   5-minute getting started guide
    ├── AAP_DEPLOY_SKILL.md            #   Portable deployment skill
    ├── AAP_BASE_SKILL.md              #   Portable base AAP skill
    ├── EXAMPLES.md                    #   Real-world usage scenarios
    ├── TROUBLESHOOTING.md             #   Common issues and solutions
    ├── CHANGELOG.md                   #   Version history and roadmap
    ├── PACKAGE_CONTENTS.md            #   Package file descriptions
    └── LICENSE                        #   MIT License
```

## How It Works

### The Governed Deployment Flow

```
Developer: "Deploy this app"
        │
        ▼
┌─────────────────────────────────────────────────┐
│  AI Agent (Claude Code)                         │
│                                                 │
│  1. Check git status → show uncommitted changes │
│  2. Commit changes → AI-generated message       │
│  3. Push to dev branch → branch isolation       │
│  4. Discover AAP template → fuzzy matching      │
│  5. Pre-flight check → confirmation required    │
│  6. Launch AAP job → via MCP server             │
│  7. Monitor execution → real-time updates       │
│  8. Extract results → server IPs, URLs, status  │
│                                                 │
│  Safety Guardrails:                             │
│  • Production requires "yes, target production" │
│  • Version/tag values require confirmation      │
│  • Duplicate run detection within 2 minutes     │
│  • Automatic log retrieval on failure           │
│  • Dev branch isolation (never pushes to main)  │
└─────────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────────┐
│  Ansible Automation Platform                    │
│                                                 │
│  Job Template → Inventory → Playbook Execution  │
│  • Install Apache on RHEL targets               │
│  • Configure firewall (HTTP/HTTPS)              │
│  • Deploy application files                     │
│  • Set SELinux contexts                         │
│  • Create Apache vhost                          │
│  • Verify deployment                            │
└─────────────────────────────────────────────────┘
        │
        ▼
Developer sees: server URLs, host summaries, next steps
```

### Two Skills, One Pipeline

| Skill | File | Use Case |
|-------|------|----------|
| **Base AAP Skill** | `CLAUDE.md` | General AAP job execution: patching, restarts, provisioning, any job template |
| **Deploy with Commit Skill** | `DEPLOY_SKILL.md` | Code deployment: git commit + push to dev + AAP job launch + result extraction |

The base skill provides a 5-step workflow (discover, pre-flight, launch, monitor, summarize) for any AAP job template. The deploy skill extends it with git operations and server detail extraction.

## Prerequisites

- **Claude Code** with MCP support
- **AAP MCP Server** configured and connected (provides `aap-job-mgmt` and `aap-inventory` tool namespaces)
- **Ansible Automation Platform 2.4+** with job templates and RBAC permissions
- **Git** repository with remote configured
- **RHEL 8/9** target servers (for the included playbooks)

## Quick Start

### 1. Clone the Repository

```bash
git clone <repository-url>
cd govern-agent-deploy
```

### 2. Configure Target Hosts

```bash
# Edit inventory with your RHEL server addresses
vi ansible-playbooks/inventory/hosts
```

### 3. Install Ansible Dependencies

```bash
cd ansible-playbooks
ansible-galaxy collection install -r requirements.yml
```

### 4. Test Connectivity

```bash
ansible webservers -m ping
```

### 5. Deploy via AI Agent

In Claude Code, with the AAP MCP server connected:

```
You: "Deploy the cheeseburger map app"
```

Or deploy directly with Ansible:

```bash
ansible-playbook ansible-playbooks/deploy.yml
```

## AI Agent Skills

### Base AAP Job Execution (`CLAUDE.md`)

Enables conversational AAP job management with a mandatory 5-step workflow:

1. **Discovery** -- List templates, fuzzy-match developer intent
2. **Pre-flight** -- Show template, inventory, extra vars; require confirmation
3. **Launch** -- Trigger via MCP, extract job ID and URL
4. **Monitor** -- Poll every 30s, show task progress, auto-retrieve logs on failure
5. **Summary** -- Host-level results, suggested next steps

Safety guardrails enforce production confirmation phrases, version verification, inventory requirements, duplicate run detection, and long-running job alerts.

**Alternative integration methods** are documented (commented out) in the skill for environments that use direct REST API calls or Event Driven Ansible webhooks instead of MCP.

### Deploy with Commit (`DEPLOY_SKILL.md`)

Extends the base skill with git-integrated deployment:

1. **Git status** -- Detect uncommitted changes
2. **Commit** -- Stage, generate message, confirm, commit with co-author
3. **Push to dev** -- Create/switch to dev branch, push to origin
4. **Template discovery** -- Find deployment-related AAP templates
5. **Pre-flight + launch** -- Full confirmation flow with branch/commit context
6. **Monitor + extract** -- Real-time status, parse server IPs/URLs/paths from output

Dev branch isolation ensures deployment commits never land on main/master.

## Ansible Playbooks

### `deploy.yml` -- Main Deployment

Deploys the web application to RHEL servers:
- Installs and configures Apache (httpd)
- Opens HTTP/HTTPS through firewalld
- Copies application files with correct ownership
- Sets SELinux contexts for web content
- Creates Apache virtual host from Jinja2 template
- Waits for Apache readiness on port 80

### `verify.yml` -- Post-Deployment Verification

Validates the deployment succeeded:
- Apache installed, running, and enabled
- Application files present
- Firewall rules active
- HTTP response returns 200
- SELinux contexts correct

### `rollback.yml` -- Application Rollback

Removes the application while preserving Apache:
- Removes app directory and vhost config
- Cleans up application logs
- Restarts Apache with default config
- Interactive confirmation prompt

### `cleanup.yml` -- Full Teardown

Completely removes everything:
- Uninstalls Apache
- Removes application files, configs, and logs
- Disables firewall rules for HTTP/HTTPS
- Returns server to pre-deployment state
- Interactive confirmation prompt

## Sample Application

The **Global Cheeseburger Consumption Map** is a static web application that serves as deployment content:

- Interactive world map built with **Leaflet.js**
- Color-coded markers for 35+ countries
- Click-to-view consumption statistics
- Top 5 countries ranking
- Responsive design, no build step required
- Runs on any static file server (Apache, Nginx, Python HTTP server)

## Distributing the Skills

The `SKILL_PACKAGE/` directory contains portable versions of both skills with full documentation. To share with your team:

```bash
# Option 1: Share the package directory
cp -r SKILL_PACKAGE/ /path/to/share/

# Option 2: Archive it
tar -czf aap-deployment-skill-v1.0.0.tar.gz SKILL_PACKAGE/
```

Recipients copy the skill files into their project:

```bash
cp AAP_DEPLOY_SKILL.md /path/to/project/CLAUDE.md
```

See `SKILL_PACKAGE/README.md` for detailed installation paths and customization options.

## Customization

### Adapt for Your Application

Replace the cheeseburger-map-app with your own content:

1. Put your application files in a directory at the repo root
2. Update `app_source_dir` in `deploy.yml`
3. Adjust the Apache vhost template for your app's needs
4. Update `group_vars/webservers.yml` with your app name and server details

### Modify Safety Thresholds

Edit the skill files to adjust:
- Production host count warning threshold (default: 20)
- Polling interval (default: 30 seconds)
- Max monitoring duration (default: 1 hour)
- Production inventory name patterns (`*prod*`, `*production*`, `*prd*`)
- Required confirmation phrases

### Add Integration Methods

The base skill includes commented-out sections for:
- **Direct AAP REST API** -- Use `curl`/`WebFetch` instead of MCP tools
- **Event Driven Ansible** -- Trigger via EDA webhooks with HMAC signing

Uncomment the relevant section in `CLAUDE.md` to enable.

## License

MIT License. See `SKILL_PACKAGE/LICENSE`.
