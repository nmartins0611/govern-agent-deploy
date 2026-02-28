# Quick Start Guide

Get the banking demo running in 5 minutes.

## Installation

```bash
# 1. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements-dev.txt
```

## Run Tests

```bash
# Run all tests
pytest tests/ -v

# With coverage report
pytest tests/ -v --cov=banking_app --cov-report=html
open htmlcov/index.html  # View coverage report
```

## Run Application

```bash
# Start the server
python run.py

# In another terminal, test the API:
curl http://localhost:5000/api/v1/health
```

## API Examples

### Check Balance
```bash
curl http://localhost:5000/api/v1/accounts/test-account-1/balance
```

### Transfer Funds
```bash
curl -X POST http://localhost:5000/api/v1/accounts/transfer \
  -H "Content-Type: application/json" \
  -d '{
    "from_account_id": "test-account-1",
    "to_account_id": "test-account-2",
    "amount": 100.00,
    "description": "Payment"
  }'
```

### Transaction History
```bash
curl http://localhost:5000/api/v1/accounts/test-account-1/transactions
```

## Deploy with Skill

```bash
# Initialize git (first time only)
git init
git config user.name "Your Name"
git config user.email "your@email.com"

# Run deployment
bash .claude/skills/deploy-to-aap/scripts/deploy.sh

# Or in Claude Code:
# /deploy-to-aap
```

## Seed Accounts

The application comes with 5 pre-seeded accounts:

| Account | Name           | Balance    |
|---------|----------------|------------|
| ACC001  | Alice Johnson  | $5,000.00  |
| ACC002  | Bob Smith      | $3,500.50  |
| ACC003  | Charlie Davis  | $10,000.75 |
| ACC004  | Diana Prince   | $7,200.25  |
| ACC005  | Eve Martinez   | $1,500.00  |

Account IDs are generated dynamically. Use `/balance` endpoint to find IDs.

## Project Structure

```
govern-agent-deploy/
├── banking_app/              # Application code
│   ├── app.py               # Flask app factory
│   ├── routes.py            # API endpoints
│   ├── services.py          # Business logic
│   ├── models.py            # Database models
│   └── database.py          # DB initialization
├── tests/                   # Test suite
│   ├── test_services.py     # Unit tests
│   └── test_routes.py       # API tests
├── .claude/skills/          # Deployment skill
│   └── deploy-to-aap/
│       ├── SKILL.md         # Skill definition
│       └── scripts/
│           └── deploy.sh    # Deployment script
├── docs/                    # Documentation
│   ├── API.md              # API reference
│   ├── DEPLOYMENT.md       # Deployment guide
│   └── AAP_INTEGRATION.md  # AAP setup
└── ansible/playbooks/       # Ansible playbooks
```

## Common Commands

```bash
# Run specific test file
pytest tests/test_services.py -v

# Run single test
pytest tests/test_services.py::TestGetBalance::test_get_balance_success -v

# Format code
black banking_app/

# Check git status
git status

# View logs
tail -f *.log

# Clean up
rm -rf __pycache__ .pytest_cache htmlcov *.db
```

## Troubleshooting

### Port 5000 in use
```bash
# Find process using port 5000
lsof -i :5000

# Use different port
export FLASK_PORT=8000
python run.py
```

### Import errors
```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements-dev.txt
```

### Tests failing
```bash
# Clear pytest cache
pytest --cache-clear

# Run with verbose output
pytest tests/ -vv
```

### Deployment script errors
```bash
# Ensure git is initialized
git init

# Check config file exists
ls .claude/skills/deploy-to-aap/scripts/aap_config.json

# Run with debug output
bash -x .claude/skills/deploy-to-aap/scripts/deploy.sh
```

## Next Steps

- Read [README.md](README.md) for complete overview
- Check [DEMO.md](DEMO.md) for demo walkthrough
- See [docs/API.md](docs/API.md) for API reference
- Review [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) for deployment details

## Support

- **Documentation:** See `docs/` directory
- **Examples:** Check test files in `tests/`
- **Issues:** Review code and error messages
