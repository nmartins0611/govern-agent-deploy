# Banking Demo with Claude Code Deployment

A demonstration project showcasing development-to-deployment automation using Claude Code and Ansible Automation Platform (AAP).

## Overview

This project demonstrates:

1. **Banking REST API** - A sample Flask application with realistic banking operations
2. **Automated Deployment** - Custom Claude Code skill (`/deploy-to-aap`) that automates the deployment pipeline
3. **AAP Integration** - Integration with Ansible Automation Platform for infrastructure provisioning and application deployment

### Why This Demo?

This addresses the common challenge of moving from development to deployed infrastructure quickly and reliably. It demonstrates how Claude Code can accelerate not just development, but the entire deployment workflow through custom skills.

## Features

### Banking Application

- **Balance Checking** - Query account balances
- **Fund Transfers** - Transfer money between accounts with transaction safety
- **Transaction History** - View paginated transaction logs
- **RESTful API** - Clean REST endpoints with JSON responses
- **Data Persistence** - SQLite database with seed data
- **Comprehensive Tests** - pytest suite with >80% coverage

### Deployment Automation

- **One Command Deploy** - `/deploy-to-aap` triggers entire deployment
- **Git Integration** - Automatic commit, branch management, and push
- **AAP Orchestration** - Triggers infrastructure, app deployment, and test jobs
- **Mock Mode** - Demo mode without requiring real AAP instance
- **Production Ready** - Switch to real mode with simple configuration

## Quick Start

### 1. Install Dependencies

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install application dependencies
pip install -r requirements.txt

# Install development dependencies (for testing)
pip install -r requirements-dev.txt
```

### 2. Run the Application

```bash
python run.py
```

The API will start on `http://localhost:5000`

### 3. Test the API

```bash
# Check health
curl http://localhost:5000/api/v1/health

# Get list of available endpoints
curl http://localhost:5000/

# Check balance (using seed account)
curl http://localhost:5000/api/v1/accounts/test-account-1/balance
```

### 4. Run Tests

```bash
pytest tests/ -v
```

With coverage:
```bash
pytest tests/ -v --cov=banking_app --cov-report=html
```

View coverage report: `open htmlcov/index.html`

## API Endpoints

### Health Check
```bash
GET /api/v1/health
```

### Get Balance
```bash
GET /api/v1/accounts/<account_id>/balance
```

Example:
```bash
curl http://localhost:5000/api/v1/accounts/test-account-1/balance
```

### Transfer Funds
```bash
POST /api/v1/accounts/transfer
Content-Type: application/json

{
  "from_account_id": "test-account-1",
  "to_account_id": "test-account-2",
  "amount": 100.00,
  "description": "Payment for services"
}
```

Example:
```bash
curl -X POST http://localhost:5000/api/v1/accounts/transfer \
  -H "Content-Type: application/json" \
  -d '{
    "from_account_id": "test-account-1",
    "to_account_id": "test-account-2",
    "amount": 50.00,
    "description": "Test transfer"
  }'
```

### Get Transaction History
```bash
GET /api/v1/accounts/<account_id>/transactions?page=1&per_page=10
```

Example:
```bash
curl http://localhost:5000/api/v1/accounts/test-account-1/transactions
```

## Deployment with /deploy-to-aap

### Setup

1. **Initialize Git repository:**
   ```bash
   git init
   git remote add origin <your-repo-url>
   ```

2. **Verify deployment configuration exists:**
   ```bash
   ls .claude/skills/deploy-to-aap/scripts/aap_config.json
   ```

   If missing:
   ```bash
   cp .claude/skills/deploy-to-aap/scripts/aap_config.json.example \
      .claude/skills/deploy-to-aap/scripts/aap_config.json
   ```

### Deploy

Simply invoke the skill in Claude Code:

```
/deploy-to-aap
```

The skill will:
1. ✅ Commit any pending changes
2. ✅ Switch to `dev` branch
3. ✅ Push to GitHub
4. ✅ Trigger AAP infrastructure deployment
5. ✅ Trigger AAP application deployment
6. ✅ Trigger AAP test execution

### Mock Mode (Default)

By default, the skill runs in **mock mode** for demonstration:
- Git operations are real
- AAP job triggers are simulated
- No actual infrastructure changes
- Perfect for demos without AAP instance

### Real Mode

To use with actual AAP:

1. Set `"mock_mode": false` in `aap_config.json`
2. Configure AAP URL and job template IDs
3. Set AAP token:
   ```bash
   export AAP_TOKEN="your-aap-token"
   ```
4. Run `/deploy-to-aap`

See [docs/AAP_INTEGRATION.md](docs/AAP_INTEGRATION.md) for detailed setup.

## Project Structure

```
govern-agent-deploy/
├── banking_app/           # Main application package
│   ├── __init__.py
│   ├── app.py            # Flask application factory
│   ├── database.py       # Database initialization and seeding
│   ├── exceptions.py     # Custom exception classes
│   ├── models.py         # SQLAlchemy models
│   ├── routes.py         # API route definitions
│   ├── services.py       # Business logic layer
│   └── validators.py     # Input validation utilities
├── tests/                # Test suite
│   ├── conftest.py       # pytest fixtures
│   ├── test_services.py  # Business logic tests
│   └── test_routes.py    # API integration tests
├── .claude/skills/       # Claude Code custom skills
│   └── deploy-to-aap/
│       ├── SKILL.md      # Skill definition
│       └── scripts/
│           ├── deploy.sh         # Deployment automation script
│           └── aap_config.json   # AAP configuration
├── docs/                 # Documentation
│   ├── API.md           # API documentation
│   ├── AAP_INTEGRATION.md  # AAP setup guide
│   └── DEPLOYMENT.md    # Deployment guide
├── ansible/             # Ansible playbooks (for AAP)
│   └── playbooks/
├── run.py              # Application entry point
├── requirements.txt    # Application dependencies
├── requirements-dev.txt  # Development dependencies
├── pytest.ini         # pytest configuration
└── README.md          # This file
```

## Demo Workflow

### Complete Development to Deployment Flow

1. **Develop with Claude Code:**
   ```
   User: "Add a new endpoint for account statements"
   Claude: [Implements feature with tests]
   ```

2. **Verify locally:**
   ```bash
   pytest tests/ -v
   python run.py
   # Test manually or with curl
   ```

3. **Deploy with one command:**
   ```
   /deploy-to-aap
   ```

4. **Monitor deployment:**
   - View git operations in terminal
   - Monitor AAP jobs in dashboard
   - Verify deployment with API calls

### Sample Seed Data

The application seeds five demo accounts:

| Account Number | Holder Name    | Balance   |
|---------------|----------------|-----------|
| ACC001        | Alice Johnson  | $5,000.00 |
| ACC002        | Bob Smith      | $3,500.50 |
| ACC003        | Charlie Davis  | $10,000.75|
| ACC004        | Diana Prince   | $7,200.25 |
| ACC005        | Eve Martinez   | $1,500.00 |

## Configuration

### Environment Variables

```bash
# Flask Configuration
export FLASK_HOST="0.0.0.0"
export FLASK_PORT="5000"
export FLASK_DEBUG="False"

# Database
export DATABASE_URL="sqlite:///banking.db"

# AAP (for real mode)
export AAP_TOKEN="your-aap-token"
```

### AAP Configuration

Edit `.claude/skills/deploy-to-aap/scripts/aap_config.json`:

```json
{
  "aap_url": "https://your-aap-instance.com",
  "job_templates": {
    "infrastructure": {"id": 10},
    "application": {"id": 15},
    "tests": {"id": 20}
  },
  "mock_mode": true,
  "github": {
    "repo_url": "git@github.com:username/govern-agent-deploy.git",
    "dev_branch": "dev"
  }
}
```

## Documentation

- **[API Documentation](docs/API.md)** - Complete API reference with examples
- **[Deployment Guide](docs/DEPLOYMENT.md)** - How to use `/deploy-to-aap` skill
- **[AAP Integration](docs/AAP_INTEGRATION.md)** - Setting up real AAP integration

## Architecture

### Application Architecture

```
┌─────────────┐
│   Client    │
└──────┬──────┘
       │ HTTP/JSON
┌──────▼──────┐
│   Routes    │  (Flask endpoints)
└──────┬──────┘
       │
┌──────▼──────┐
│  Services   │  (Business logic)
└──────┬──────┘
       │
┌──────▼──────┐
│   Models    │  (SQLAlchemy)
└──────┬──────┘
       │
┌──────▼──────┐
│  Database   │  (SQLite)
└─────────────┘
```

### Deployment Architecture

```
┌──────────────┐
│ Claude Code  │
│ /deploy-to-aap│
└──────┬───────┘
       │
       ├─────────────────┐
       │                 │
┌──────▼──────┐   ┌──────▼──────┐
│     Git     │   │     AAP     │
│ commit/push │   │ API Trigger │
└─────────────┘   └──────┬──────┘
                         │
                   ┌─────┴─────┐
                   │           │
           ┌───────▼────┐ ┌───▼────────┐
           │Infrastructure│ │Application│
           │  Provision  │ │  Deploy   │
           └─────────────┘ └───┬───────┘
                               │
                         ┌─────▼─────┐
                         │   Tests   │
                         └───────────┘
```

## Testing

### Run All Tests
```bash
pytest tests/ -v
```

### Run Specific Test File
```bash
pytest tests/test_services.py -v
```

### Run with Coverage
```bash
pytest tests/ -v --cov=banking_app --cov-report=term-missing
```

### Test Categories

- **Unit Tests** (`test_services.py`) - Business logic validation
- **Integration Tests** (`test_routes.py`) - API endpoint testing
- **Fixtures** (`conftest.py`) - Reusable test data and setup

## Production Considerations

This is a demo application. For production use, consider:

### Security
- [ ] Add authentication (JWT, OAuth2)
- [ ] Implement authorization and role-based access
- [ ] Use HTTPS/TLS
- [ ] Add request rate limiting
- [ ] Validate and sanitize all inputs
- [ ] Use production-grade database (PostgreSQL, MySQL)
- [ ] Never commit secrets or tokens

### Reliability
- [ ] Add database migrations (Alembic)
- [ ] Implement proper error logging
- [ ] Add monitoring and alerting
- [ ] Configure database backups
- [ ] Use connection pooling
- [ ] Add health checks and readiness probes

### Performance
- [ ] Cache frequently accessed data (Redis)
- [ ] Add database indexes
- [ ] Implement async processing for heavy operations
- [ ] Use a production WSGI server (Gunicorn, uWSGI)
- [ ] Add load balancing

### Deployment
- [ ] Use environment-specific configurations
- [ ] Implement CI/CD pipelines
- [ ] Add automated rollback capability
- [ ] Use container orchestration (Kubernetes)
- [ ] Implement blue-green or canary deployments

## Troubleshooting

### Application won't start
```bash
# Check if port 5000 is in use
lsof -i :5000

# Use different port
export FLASK_PORT=8000
python run.py
```

### Tests failing
```bash
# Ensure test dependencies installed
pip install -r requirements-dev.txt

# Clear pytest cache
pytest --cache-clear

# Run single test for debugging
pytest tests/test_services.py::TestGetBalance::test_get_balance_success -v
```

### Deployment skill errors
```bash
# Verify config exists
cat .claude/skills/deploy-to-aap/scripts/aap_config.json

# Run deployment script manually for debugging
bash -x .claude/skills/deploy-to-aap/scripts/deploy.sh
```

## Contributing

This is a demo project. Feel free to:
- Use it as a template for your own projects
- Modify the banking logic for your use case
- Extend the AAP integration
- Add new deployment targets

## License

MIT License - Feel free to use this for learning and development.

## Support

For issues or questions:
- Check the documentation in `docs/`
- Review test cases for usage examples
- Examine the deployment script for troubleshooting

## Acknowledgments

Built to demonstrate:
- Claude Code's development capabilities
- Custom skills for deployment automation
- Integration with enterprise automation platforms (AAP)
- Modern Python/Flask API development patterns
