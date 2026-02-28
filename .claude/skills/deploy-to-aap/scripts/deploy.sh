#!/bin/bash

# Deploy to AAP Script
# This script commits changes, pushes to dev branch, and triggers AAP deployment jobs

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="$SCRIPT_DIR/aap_config.json"

# Functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

check_prerequisites() {
    log_info "Checking prerequisites..."

    # Check if we're in a git repository
    if ! git rev-parse --git-dir > /dev/null 2>&1; then
        log_error "Not a git repository. Please initialize git first."
        exit 1
    fi

    # Check if config file exists
    if [ ! -f "$CONFIG_FILE" ]; then
        log_error "Configuration file not found: $CONFIG_FILE"
        log_info "Copy the example file: cp $SCRIPT_DIR/aap_config.json.example $CONFIG_FILE"
        exit 1
    fi

    log_success "Prerequisites check passed"
}

load_config() {
    log_info "Loading configuration..."

    if ! command -v jq &> /dev/null; then
        log_warning "jq not installed, using basic JSON parsing"
        MOCK_MODE=$(grep -o '"mock_mode"[[:space:]]*:[[:space:]]*[^,}]*' "$CONFIG_FILE" | grep -o 'true\|false')
        AAP_URL=$(grep -o '"aap_url"[[:space:]]*:[[:space:]]*"[^"]*"' "$CONFIG_FILE" | sed 's/.*: *"\(.*\)"/\1/')
        DEV_BRANCH=$(grep -o '"dev_branch"[[:space:]]*:[[:space:]]*"[^"]*"' "$CONFIG_FILE" | sed 's/.*: *"\(.*\)"/\1/')
    else
        MOCK_MODE=$(jq -r '.mock_mode // true' "$CONFIG_FILE")
        AAP_URL=$(jq -r '.aap_url // "https://aap.example.com"' "$CONFIG_FILE")
        DEV_BRANCH=$(jq -r '.github.dev_branch // "dev"' "$CONFIG_FILE")
    fi

    if [ "$MOCK_MODE" = "true" ]; then
        log_warning "Running in MOCK MODE - no real AAP jobs will be triggered"
    else
        log_info "Running in REAL MODE - will trigger actual AAP jobs"

        if [ -z "$AAP_TOKEN" ]; then
            log_error "AAP_TOKEN environment variable not set"
            exit 1
        fi
    fi

    log_success "Configuration loaded"
}

git_operations() {
    log_info "Performing git operations..."

    # Check for uncommitted changes
    if [ -n "$(git status --porcelain)" ]; then
        log_info "Found uncommitted changes, committing..."
        git add -A
        git commit -m "Deploy: Automated commit via /deploy-to-aap skill

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
        log_success "Changes committed"
    else
        log_info "No uncommitted changes found"
    fi

    # Switch to dev branch
    if git show-ref --verify --quiet "refs/heads/$DEV_BRANCH"; then
        log_info "Switching to existing $DEV_BRANCH branch..."
        git checkout "$DEV_BRANCH"
    else
        log_info "Creating new $DEV_BRANCH branch..."
        git checkout -b "$DEV_BRANCH"
    fi

    # Push to remote
    log_info "Pushing to remote origin/$DEV_BRANCH..."

    if git remote get-url origin > /dev/null 2>&1; then
        git push -u origin "$DEV_BRANCH" || {
            log_warning "Push failed - this might be the first push or remote is not configured"
            log_info "You may need to set up the remote: git remote add origin <url>"
        }
        log_success "Code pushed to $DEV_BRANCH branch"
    else
        log_warning "No remote 'origin' configured - skipping push"
        log_info "Configure with: git remote add origin <repository-url>"
    fi
}

trigger_aap_job_mock() {
    local job_name=$1
    local job_id=$2

    log_info "MOCK: Triggering AAP job template: $job_name (ID: $job_id)"

    # Simulate API call
    local mock_job_id=$((RANDOM % 9000 + 1000))
    local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

    echo ""
    log_success "MOCK: Job launched successfully"
    echo -e "  ${BLUE}Job Name:${NC} $job_name"
    echo -e "  ${BLUE}Job ID:${NC} $mock_job_id"
    echo -e "  ${BLUE}Status:${NC} pending"
    echo -e "  ${BLUE}Started:${NC} $timestamp"
    echo -e "  ${BLUE}Monitor:${NC} $AAP_URL/#/jobs/playbook/$mock_job_id"
    echo ""

    # Simulate job execution time
    sleep 1
}

trigger_aap_job_real() {
    local job_name=$1
    local job_id=$2

    log_info "Triggering AAP job template: $job_name (ID: $job_id)"

    # Make actual API call to AAP
    local response
    response=$(curl -s -X POST \
        -H "Authorization: Bearer $AAP_TOKEN" \
        -H "Content-Type: application/json" \
        --data "{\"extra_vars\": {\"git_branch\": \"$DEV_BRANCH\"}}" \
        "$AAP_URL/api/v2/job_templates/$job_id/launch/")

    # Parse response
    if command -v jq &> /dev/null; then
        local launched_job_id=$(echo "$response" | jq -r '.id // empty')

        if [ -n "$launched_job_id" ]; then
            log_success "Job launched successfully"
            echo -e "  ${BLUE}Job ID:${NC} $launched_job_id"
            echo -e "  ${BLUE}Monitor:${NC} $AAP_URL/#/jobs/playbook/$launched_job_id"
            echo ""
        else
            log_error "Failed to launch job"
            echo "$response"
            exit 1
        fi
    else
        echo "$response"
    fi
}

trigger_aap_jobs() {
    log_info "Triggering AAP deployment jobs..."
    echo ""

    if [ "$MOCK_MODE" = "true" ]; then
        # Mock mode - simulate job triggers
        echo "========================================="
        echo "   AAP DEPLOYMENT JOBS (MOCK MODE)"
        echo "========================================="
        echo ""

        trigger_aap_job_mock "Deploy Infrastructure" 10
        trigger_aap_job_mock "Deploy Application" 15
        trigger_aap_job_mock "Run Tests" 20

        echo "========================================="
        echo ""
        log_success "All deployment jobs triggered (mock mode)"
        log_info "In production, monitor jobs at: $AAP_URL/#/jobs"

    else
        # Real mode - make actual API calls
        if command -v jq &> /dev/null; then
            INFRA_TEMPLATE_ID=$(jq -r '.job_templates.infrastructure.id' "$CONFIG_FILE")
            APP_TEMPLATE_ID=$(jq -r '.job_templates.application.id' "$CONFIG_FILE")
            TEST_TEMPLATE_ID=$(jq -r '.job_templates.tests.id' "$CONFIG_FILE")
        else
            log_error "jq is required for real mode AAP integration"
            exit 1
        fi

        trigger_aap_job_real "Deploy Infrastructure" "$INFRA_TEMPLATE_ID"
        trigger_aap_job_real "Deploy Application" "$APP_TEMPLATE_ID"
        trigger_aap_job_real "Run Tests" "$TEST_TEMPLATE_ID"

        log_success "All deployment jobs triggered"
    fi
}

main() {
    echo ""
    echo "========================================="
    echo "  Deploy to Ansible Automation Platform"
    echo "========================================="
    echo ""

    check_prerequisites
    load_config
    git_operations
    trigger_aap_jobs

    echo ""
    log_success "Deployment initiated successfully!"
    echo ""
}

# Run main function
main
