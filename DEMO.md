# Banking Demo Walkthrough

This document provides a step-by-step walkthrough for demonstrating the Banking Application with Claude Code Deployment.

## Demo Scenario

**Story:** A developer uses Claude Code to build a banking REST API, then deploys it to production infrastructure with a single command.

## Prerequisites

Before the demo, ensure:

```bash
# Install dependencies
python3 -m venv venv
source venv/bin/activate
pip install -r requirements-dev.txt

# Verify tests pass
pytest tests/ -v

# Initialize git (if not already done)
git init
git config user.name "Demo User"
git config user.email "demo@example.com"
```

## Demo Flow

### Part 1: Show the Application (5 minutes)

#### 1.1 Application Structure

```bash
# Show project structure
tree -L 2 -I 'venv|__pycache__|.git|htmlcov|.pytest_cache'
```

**Explain:**
- `banking_app/` - Main application code
- `tests/` - Comprehensive test suite
- `.claude/skills/deploy-to-aap/` - Custom deployment skill
- `ansible/playbooks/` - Deployment automation
- `docs/` - Complete documentation

#### 1.2 Run the Application

```bash
# Start the API
python run.py
```

**Open another terminal and test:**

```bash
# Health check
curl http://localhost:5000/api/v1/health

# Get account balance (using seed data)
curl http://localhost:5000/api/v1/accounts/test-account-1/balance

# Transfer funds
curl -X POST http://localhost:5000/api/v1/accounts/transfer \
  -H "Content-Type: application/json" \
  -d '{
    "from_account_id": "test-account-1",
    "to_account_id": "test-account-2",
    "amount": 100.00,
    "description": "Demo transfer"
  }'

# Check transaction history
curl http://localhost:5000/api/v1/accounts/test-account-1/transactions
```

**Explain:**
- REST API with balance, transfer, and transaction endpoints
- SQLite database with seed accounts
- Proper error handling and validation

#### 1.3 Show Test Coverage

```bash
# Run tests with coverage
pytest tests/ -v --cov=banking_app --cov-report=term-missing
```

**Explain:**
- 26 comprehensive tests
- 86% code coverage (exceeds 80% target)
- Unit tests for business logic
- Integration tests for API endpoints

### Part 2: The Deployment Skill (10 minutes)

#### 2.1 Show the Skill Definition

```bash
# View skill definition
cat .claude/skills/deploy-to-aap/SKILL.md
```

**Explain:**
- Custom Claude Code skill
- Invoked with `/deploy-to-aap`
- Automates entire deployment pipeline
- Works in mock mode by default

#### 2.2 Show the Deployment Script

```bash
# Show key parts of the deployment script
cat .claude/skills/deploy-to-aap/scripts/deploy.sh | head -50
```

**Explain:**
- Bash script that orchestrates deployment
- Git operations: commit, branch, push
- AAP job template triggering
- Mock vs real mode

#### 2.3 Show Configuration

```bash
# Show AAP configuration
cat .claude/skills/deploy-to-aap/scripts/aap_config.json
```

**Explain:**
- Mock mode enabled for demo
- Three job templates configured:
  - Infrastructure deployment
  - Application deployment
  - Test execution
- Easy to switch to real AAP

### Part 3: Execute Deployment (5 minutes)

#### 3.1 Make a Code Change

**In Claude Code, demonstrate:**

```
User: "Add a new endpoint GET /api/v1/status that returns uptime information"

Claude: [Implements the feature]
```

Or manually edit a file:

```python
# Add to banking_app/routes.py
import time
start_time = time.time()

@api.route('/status', methods=['GET'])
def status():
    return jsonify({
        "uptime_seconds": int(time.time() - start_time),
        "status": "running"
    }), 200
```

#### 3.2 Run the Deployment Skill

```bash
# Execute the deployment
bash .claude/skills/deploy-to-aap/scripts/deploy.sh
```

**Or in Claude Code:**
```
/deploy-to-aap
```

**Watch the output:**

1. ✓ Prerequisites check
2. ✓ Git commit of changes
3. ✓ Switch to dev branch
4. ✓ Mock AAP job triggers:
   - Infrastructure deployment (Job ID: XXXX)
   - Application deployment (Job ID: XXXX)
   - Test execution (Job ID: XXXX)

**Explain:**
- Single command deployment
- Git workflow automated
- Three-stage deployment pipeline
- In production, these would be real AAP jobs

### Part 4: Show AAP Integration (5 minutes)

#### 4.1 Show Ansible Playbooks

```bash
# Infrastructure playbook
cat ansible/playbooks/deploy-infrastructure.yml

# Application deployment playbook
cat ansible/playbooks/deploy-application.yml

# Test execution playbook
cat ansible/playbooks/run-tests.yml
```

**Explain:**
- Infrastructure: Provision VMs, networks, load balancers
- Application: Clone repo, install deps, start service
- Tests: Run pytest, verify deployment

#### 4.2 Show Mock vs Real Mode

```bash
# Show mock mode configuration
grep "mock_mode" .claude/skills/deploy-to-aap/scripts/aap_config.json
```

**Explain:**
- Demo runs in mock mode (no AAP needed)
- To use real AAP:
  1. Set `"mock_mode": false`
  2. Configure AAP URL
  3. Set `AAP_TOKEN` environment variable
  4. Configure job template IDs

### Part 5: Documentation (3 minutes)

#### 5.1 Show Documentation Structure

```bash
# List documentation
ls -1 docs/

# Show API documentation excerpt
head -50 docs/API.md

# Show deployment guide excerpt
head -30 docs/DEPLOYMENT.md
```

**Explain:**
- Complete API reference with examples
- Deployment guide for using the skill
- AAP integration guide for production setup
- Main README with quick start

#### 5.2 Show README

```bash
# View README
cat README.md
```

**Highlight:**
- Quick start instructions
- Architecture diagrams (in markdown)
- Demo workflow
- Production considerations

## Demo Talking Points

### Problem Being Solved

**Traditional workflow:**
1. Developer writes code
2. Manually creates git commits
3. Manually pushes to remote
4. Logs into AAP web interface
5. Manually triggers jobs
6. Monitors multiple dashboards
7. **Total time: 15-30 minutes**

**With /deploy-to-aap skill:**
1. Developer writes code
2. Runs `/deploy-to-aap`
3. **Total time: 30 seconds**

### Key Benefits

1. **Speed** - One command replaces 10+ manual steps
2. **Consistency** - Same process every time
3. **Integration** - Git and AAP workflow automated
4. **Flexibility** - Mock mode for demos, real mode for production
5. **Extensibility** - Easy to add more deployment stages

### Technical Highlights

1. **Clean Architecture** - Separation of concerns (models, services, routes)
2. **Comprehensive Testing** - 86% coverage with meaningful tests
3. **Production-Ready** - Proper error handling, validation, logging
4. **DevOps Integration** - Ansible playbooks for real deployments
5. **Documentation** - Complete docs for all aspects

### Real-World Applications

**This pattern applies to:**
- Any web application deployment
- Microservices deployment
- Database migrations
- Infrastructure as Code workflows
- CI/CD pipeline integration
- Multi-environment deployments (dev/staging/prod)

### Customization Examples

**Extend the skill to:**
- Run database migrations before deployment
- Trigger smoke tests after deployment
- Send Slack notifications on completion
- Deploy to multiple environments
- Integrate with monitoring tools
- Generate deployment reports

## Demo Script

### Opening (1 minute)

> "Today I'll show you a complete development-to-deployment workflow using Claude Code. We've built a banking REST API and created a custom skill that deploys it to production infrastructure with a single command."

### Application Demo (5 minutes)

> "Here's the banking application - it's a Flask REST API with three core operations: checking balances, transferring funds, and viewing transaction history. Let me show you it in action..."

[Run curl commands]

> "Notice the comprehensive error handling, input validation, and clean JSON responses. This is production-quality code with 86% test coverage."

### Deployment Demo (10 minutes)

> "Now here's where it gets interesting. Instead of manually committing code, pushing to git, logging into AAP, and triggering jobs - we've automated all of that with a custom Claude Code skill."

> "Let me make a change to the code..."

[Make change]

> "Now, watch what happens when I run the deployment command..."

[Execute /deploy-to-aap]

> "In seconds, it's committed the code, pushed to our dev branch, and triggered three AAP jobs: infrastructure provisioning, application deployment, and test execution. In a real environment, these jobs would spin up VMs, deploy the app, and verify everything works."

### AAP Integration (5 minutes)

> "Behind the scenes, we're using Ansible Automation Platform. Here are the actual playbooks that would run..."

[Show playbooks]

> "These handle everything from provisioning cloud resources to deploying the application and running tests. The beauty is that developers don't need to know Ansible - they just run /deploy-to-aap."

### Wrap-up (2 minutes)

> "This demonstrates how Claude Code can accelerate not just development, but your entire deployment pipeline. Custom skills bridge the gap between code and infrastructure, letting developers deploy with confidence in seconds instead of minutes."

> "And this same pattern works for any deployment target - AWS, Azure, GCP, on-prem - whatever automation platform you use."

## Q&A Preparation

**Q: Does this work without AAP?**
A: Yes! Mock mode demonstrates the workflow without requiring AAP. It's perfect for development and testing.

**Q: Can we use this with other automation platforms?**
A: Absolutely. The script can be adapted to trigger Jenkins, GitLab CI, GitHub Actions, or any other platform with an API.

**Q: Is this secure for production?**
A: The demo shows the pattern. For production, you'd add authentication to the API, use HTTPS, store secrets securely, and follow your organization's security policies.

**Q: How do we handle rollbacks?**
A: The git workflow makes this easy - revert the commit and re-run the skill, or trigger AAP to deploy a previous version.

**Q: Can we deploy to multiple environments?**
A: Yes! You could create `/deploy-to-staging`, `/deploy-to-prod`, etc., or modify the skill to accept an environment parameter.

## Post-Demo

**Follow-up resources:**
- Share the repository
- Point to documentation
- Discuss customization for their use case
- Offer to help with implementation

**Next steps for adopters:**
1. Clone this repository
2. Adapt for their application
3. Configure their automation platform
4. Test in development
5. Roll out to teams
