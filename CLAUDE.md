# AAP Job Execution Skill
# MCP Server: ansible-aap (already configured)
# Access: read-write
# Scope: job triggering, monitoring, and results via AAP API
# Last updated: 2026-03-04

## Related Skills

- **DEPLOY_SKILL.md** - Deploy with Commit Skill: Combines git operations with AAP deployment jobs. Use this when the developer wants to commit code changes and deploy in one workflow.
- **This file (CLAUDE.md)** - Base AAP Job Execution Skill: Use for general AAP job template execution (patching, restarts, provisioning, etc.)

## Purpose
This skill enables Claude Code to trigger and manage Ansible Automation Platform (AAP) job templates conversationally through the existing ansible-aap MCP server connection. All AAP interactions must go through the MCP server tools - never make direct API calls.

## Core Workflow

When a developer asks to run any automation, deployment, or AAP-related task, follow this mandatory 5-step workflow:

### Step 1 — Discovery
**Trigger**: Any request to run automation, trigger a job, deploy, patch, restart, provision, etc.

**Actions**:
1. Load the AAP job management tools using ToolSearch if not already loaded
2. Call `mcp__aap-job-mgmt__job_templates_list` to list all available job templates
3. If the developer's request is ambiguous or doesn't match a specific template name:
   - Present the available templates clearly with their names and descriptions
   - Ask the developer to clarify which template they want to run
4. If the request clearly matches a template, proceed to Step 2
5. Match the developer's intent using fuzzy matching (e.g., "restart apache" → "Apache Restart" template)

### Step 2 — Pre-flight Check
**Trigger**: After identifying the target job template

**Actions**:
1. Retrieve full template details using `mcp__aap-job-mgmt__job_templates_retrieve` with the template ID
2. Load inventory management tools if needed and call `mcp__aap-inventory__inventories_list` to get available inventories
3. Present a clear pre-flight summary to the developer:
   ```
   Ready to launch:
   - Template: [template name]
   - Inventory: [inventory name] ([host count] hosts)
   - Extra vars: [any extra_vars that will be passed, or "none"]
   - Estimated duration: [if available from recent runs]

   Proceed? (yes/no)
   ```
4. NEVER skip this confirmation step
5. Wait for explicit developer confirmation before proceeding

**Special confirmation requirements**:
- If inventory name contains "production", "prod", or "prd": require the exact phrase "yes, target production"
- If extra_vars contain `version`, `tag`, `sha`, or `release`: repeat the exact value and require confirmation
- If the template has no inventory set: stop and require the developer to specify an inventory

### Step 3 — Launch
**Trigger**: Developer confirms pre-flight check

**Actions**:
1. Call `mcp__aap-job-mgmt__job_templates_launch_create` with:
   - Template ID
   - Any extra_vars specified by the developer
   - Inventory if needed
2. Immediately extract from the response:
   - Job ID
   - Job URL (construct as: https://[aap-hostname]/#/jobs/playbook/[job-id]/output)
3. Report to developer:
   ```
   ✓ Job launched successfully
   Job ID: [id]
   URL: [direct link to AAP UI]
   Status: Pending

   Monitoring job...
   ```
4. Confirm the launch was successful before proceeding to monitoring
5. If launch fails, report the error immediately and do not proceed

### Step 4 — Monitor
**Trigger**: Successful job launch

**Actions**:
1. Poll job status using `mcp__aap-job-mgmt__jobs_retrieve` every 30 seconds
2. Track the current status and report updates inline:
   - `pending` → "Job queued, waiting to start..."
   - `waiting` → "Job waiting for resources..."
   - `running` → "Running... (elapsed: [time])"
   - `successful` → Proceed to Step 5
   - `failed` → Immediately retrieve logs and display them
   - `canceled` → Report cancellation and stop monitoring
3. While `running`:
   - Show elapsed time on each poll
   - Use `mcp__aap-job-mgmt__jobs_job_events_list` to get recent task events
   - Display current task name if available
4. If `failed`:
   - Call `mcp__aap-job-mgmt__jobs_stdout_retrieve` to get full job output
   - Display the last 50 lines of output
   - Highlight the failure reason
   - Call `mcp__aap-job-mgmt__jobs_job_events_list` with failed events
   - Do NOT make the developer ask for logs - provide them automatically
5. If a job runs longer than expected:
   - Query recent job history for this template to establish baseline duration
   - If current job exceeds 2x typical duration, warn: "This job is taking longer than usual. Typical duration: [baseline], current: [elapsed]"

**Monitoring format**:
```
[12:34:56] Running... (2m 15s)
           Current: Installing packages on web-server-01

[12:35:26] Running... (2m 45s)
           Current: Restarting apache service

[12:35:56] ✓ Successful (3m 10s)
```

### Step 5 — Post-job Summary
**Trigger**: Job reaches terminal state (successful, failed, canceled)

**Actions**:
1. Retrieve final job details using `mcp__aap-job-mgmt__jobs_retrieve`
2. Get host summaries using `mcp__aap-job-mgmt__jobs_job_host_summaries_list`
3. Present a summary:
   ```
   Job completed: [status]
   Duration: [time]
   Hosts changed: [count]
   Hosts failed: [count]
   Hosts unreachable: [count]

   [If failed] Failed tasks:
   - [task name] on [host]

   [If unreachable hosts] Unreachable hosts:
   - [host1]
   - [host2]
   ```
4. Suggest next steps if relevant:
   - If deployment succeeded: "Run smoke tests?"
   - If patching succeeded: "Verify services are healthy?"
   - If hosts unreachable: "Check connectivity to [hosts]?"
5. Ask: "Would you like to trigger any follow-on jobs?"

## Safety Guardrails

Enforce these rules strictly:

1. **Production Protection**:
   - Any inventory matching `*prod*`, `*production*`, `*prd*` requires explicit confirmation stating "yes, target production"
   - Show host count before confirming production runs
   - If host count > 20 for production, add extra warning: "This will affect [N] production hosts"

2. **Version/Release Confirmation**:
   - If extra_vars contain `version`, `tag`, `sha`, `release`, `branch`, or similar:
     - Display the exact value clearly
     - Ask: "Confirm deployment of version [X]? (yes/no)"
     - Require exact match confirmation

3. **Inventory Requirement**:
   - If a job template has no inventory set and developer didn't specify one:
     - Stop and display: "This template requires an inventory. Available inventories:"
     - List inventories using `mcp__aap-inventory__inventories_list`
     - Ask developer to specify: "Which inventory should I use?"

4. **Duplicate Run Protection**:
   - Track job launches in conversation context
   - If same template is requested within 2 minutes of previous launch:
     - Warn: "You launched this template [X] seconds ago (Job ID: [id]). Launch again? (yes/no)"
     - Show status of the previous job

5. **Long-Running Job Detection**:
   - Query `mcp__aap-job-mgmt__jobs_list` filtered by template to get recent run history
   - Calculate median duration for the template
   - If current job exceeds 2x median: "⚠ This job is running longer than usual ([current] vs typical [median])"
   - Suggest: "Check job output or cancel?"

6. **Failed Job Immediate Logs**:
   - On any failure, automatically retrieve and display logs
   - Never make the developer ask "why did it fail?"
   - Show the failure context immediately

## Example Interactions

These examples show how developers should interact with this skill:

### Example 1 — Simple job trigger
```
Developer: "Run the apache restart job on staging"

Claude:
1. Lists job templates, finds "Apache Restart"
2. Shows pre-flight:
   Ready to launch:
   - Template: Apache Restart
   - Inventory: staging-web (3 hosts)
   - Extra vars: none

   Proceed? (yes/no)

Developer: "yes"

Claude:
✓ Job launched successfully
Job ID: 842
URL: https://aap.example.com/#/jobs/playbook/842/output
Status: Pending

Monitoring job...

[12:34:26] Running... (15s)
           Current: Restarting apache on web-01

[12:34:56] ✓ Successful (45s)

Job completed: successful
Duration: 45s
Hosts changed: 3
Hosts failed: 0

Would you like to trigger any follow-on jobs?
```

### Example 2 — Job with extra vars
```
Developer: "Provision an environment for PR #247 using the small instance size"

Claude:
Found template: "Provision PR Environment"

Ready to launch:
- Template: Provision PR Environment
- Inventory: dynamic-aws
- Extra vars:
  pr_number: 247
  instance_size: small

Proceed? (yes/no)

Developer: "yes"

Claude: [continues with launch and monitoring]
```

### Example 3 — Debugging past failure
```
Developer: "Why did the last patching job fail?"

Claude:
1. Queries recent jobs: mcp__aap-job-mgmt__jobs_list filtered by "patching"
2. Finds most recent failed job (ID: 839)
3. Retrieves logs: mcp__aap-job-mgmt__jobs_stdout_retrieve
4. Shows:

Last patching job (ID: 839) failed 2 hours ago.

Failure reason: Task "Yum update" failed on 2/15 hosts

Failed hosts:
- db-01: Insufficient disk space in /var/cache
- db-02: Insufficient disk space in /var/cache

Last 20 lines of output:
[shows relevant log excerpt]

Suggested fix: Clear yum cache or expand /var disk on db-01, db-02
```

### Example 4 — Chained jobs
```
Developer: "Deploy version 2.1.4 of the payments service to staging, then run the smoke tests"

Claude:
Step 1: Deploy payments-service

Ready to launch:
- Template: Deploy Payments Service
- Inventory: staging-payments (2 hosts)
- Extra vars:
  version: 2.1.4

Confirm deployment of version 2.1.4? (yes/no)

Developer: "yes"

Claude:
✓ Job launched successfully
Job ID: 845
[monitors and completes]

Job completed: successful
Duration: 3m 20s
Hosts changed: 2

Step 2: Running smoke tests

Ready to launch:
- Template: Payments Smoke Tests
- Inventory: staging-payments (2 hosts)
- Extra vars: none

Proceed? (yes/no)

Developer: "yes"

Claude: [launches and monitors smoke tests]
```

### Example 5 — Production safety check
```
Developer: "Run the patching job on production"

Claude:
⚠ Production Target Detected

Ready to launch:
- Template: OS Patching
- Inventory: production-all (47 hosts)
- Extra vars: none

⚠ This will affect 47 production hosts

To proceed, type: "yes, target production"

Developer: "yes, target production"

Claude: ✓ Confirmed. Launching job...
[continues with monitoring]
```

## Technical Implementation Notes

### Loading MCP Tools
Before any AAP operation, ensure tools are loaded:
```
Use ToolSearch with query "aap job" to load job management tools
Use ToolSearch with query "aap inventory" to load inventory tools
Use ToolSearch with query "aap monitoring" to load monitoring tools if needed
```

### Common Tool Patterns

**List all job templates**:
```
mcp__aap-job-mgmt__job_templates_list
Returns: list of templates with id, name, description
```

**Get template details**:
```
mcp__aap-job-mgmt__job_templates_retrieve
Params: template_id
Returns: full template config including inventory, extra_vars
```

**Launch a job**:
```
mcp__aap-job-mgmt__job_templates_launch_create
Params: template_id, extra_vars (JSON), inventory (optional)
Returns: job id, url, status
```

**Check job status**:
```
mcp__aap-job-mgmt__jobs_retrieve
Params: job_id
Returns: status, started, finished, elapsed
```

**Get job output/logs**:
```
mcp__aap-job-mgmt__jobs_stdout_retrieve
Params: job_id
Returns: full stdout from job execution
```

**Get job events** (task-level details):
```
mcp__aap-job-mgmt__jobs_job_events_list
Params: job_id, event_type (optional)
Returns: list of events with task names, statuses, timestamps
```

**Get host summaries**:
```
mcp__aap-job-mgmt__jobs_job_host_summaries_list
Params: job_id
Returns: per-host results (ok, changed, failed, unreachable)
```

**List inventories**:
```
mcp__aap-inventory__inventories_list
Returns: list of inventories with id, name, host count
```

**List recent jobs**:
```
mcp__aap-job-mgmt__jobs_list
Params: page_size, job_template (optional filter)
Returns: recent jobs with status, duration, timestamps
```

### Polling Strategy
- Initial poll: immediately after launch
- Subsequent polls: every 30 seconds while status is pending/waiting/running
- Max polls: 120 (1 hour max monitoring)
- After max polls: warn "Job still running after 1 hour. Continue monitoring? (yes/no)"

### Status Mapping
- `pending` / `waiting` → Job not started yet, keep polling
- `running` → Job executing, show progress, keep polling
- `successful` → Terminal state, show summary
- `failed` → Terminal state, retrieve logs immediately
- `error` → Terminal state, show error details
- `canceled` → Terminal state, report cancellation

### Error Handling
- If any MCP tool call fails: display the error clearly and stop the workflow
- If job launch returns an error: explain the error and suggest fixes
- If job retrieval fails during monitoring: retry up to 3 times before reporting error
- If logs retrieval fails: report "Could not retrieve logs" but continue with summary

### Context Tracking
Maintain in conversation memory:
- Recently launched jobs (template_id, job_id, timestamp)
- Current monitoring state (job_id, start_time, last_status)
- Template duration baselines (calculate from recent job history)

## Alternative Integration Methods

**Default Method**: This skill uses MCP server tools (as documented above). However, users may choose alternative integration methods based on their environment and requirements. Uncomment and configure one of the following alternatives if preferred:

<!-- ALTERNATIVE 1: DIRECT AAP REST API INTEGRATION
## Direct API Integration (Commented Out - Enable if Not Using MCP)

If you prefer to interact directly with the AAP REST API instead of using MCP tools, uncomment this section and comment out the MCP tool patterns above.

### Configuration Requirements
- AAP API URL: https://your-aap-controller.example.com
- Authentication: Personal Access Token (PAT) or OAuth2
- API Version: v2 (Controller API)

### Environment Setup
```bash
export AAP_HOST="https://your-aap-controller.example.com"
export AAP_TOKEN="your-personal-access-token"
export AAP_VERIFY_SSL="true"  # Set to false for self-signed certs
```

### API Endpoint Patterns

**List Job Templates**:
```bash
curl -X GET "${AAP_HOST}/api/v2/job_templates/" \
  -H "Authorization: Bearer ${AAP_TOKEN}" \
  -H "Content-Type: application/json"
```

**Get Template Details**:
```bash
curl -X GET "${AAP_HOST}/api/v2/job_templates/{template_id}/" \
  -H "Authorization: Bearer ${AAP_TOKEN}"
```

**Launch Job Template**:
```bash
curl -X POST "${AAP_HOST}/api/v2/job_templates/{template_id}/launch/" \
  -H "Authorization: Bearer ${AAP_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "extra_vars": {
      "version": "2.1.4",
      "environment": "staging"
    },
    "inventory": 123,
    "limit": "webservers"
  }'
```

**Get Job Status**:
```bash
curl -X GET "${AAP_HOST}/api/v2/jobs/{job_id}/" \
  -H "Authorization: Bearer ${AAP_TOKEN}"
```

**Get Job Output/Logs**:
```bash
curl -X GET "${AAP_HOST}/api/v2/jobs/{job_id}/stdout/?format=json" \
  -H "Authorization: Bearer ${AAP_TOKEN}"
```

**Get Job Events** (task-level details):
```bash
curl -X GET "${AAP_HOST}/api/v2/jobs/{job_id}/job_events/" \
  -H "Authorization: Bearer ${AAP_TOKEN}"
```

**Cancel Running Job**:
```bash
curl -X POST "${AAP_HOST}/api/v2/jobs/{job_id}/cancel/" \
  -H "Authorization: Bearer ${AAP_TOKEN}"
```

**List Inventories**:
```bash
curl -X GET "${AAP_HOST}/api/v2/inventories/" \
  -H "Authorization: Bearer ${AAP_TOKEN}"
```

**List Recent Jobs** (with filtering):
```bash
curl -X GET "${AAP_HOST}/api/v2/jobs/?page_size=20&order_by=-created&job_template={template_id}" \
  -H "Authorization: Bearer ${AAP_TOKEN}"
```

### Implementation Notes for API Mode
- Use WebFetch tool with appropriate prompts to make API calls
- Store AAP credentials securely (use environment variables or secret management)
- Handle pagination for large result sets (check 'next' field in responses)
- Implement exponential backoff for rate limiting
- Validate SSL certificates in production (set AAP_VERIFY_SSL=true)
- Parse JSON responses to extract relevant fields
- All endpoints return JSON; use `format=json` query param for stdout endpoint

### Response Structures

**Job Launch Response**:
```json
{
  "id": 845,
  "url": "/api/v2/jobs/845/",
  "type": "job",
  "status": "pending",
  "job_template": 42,
  "inventory": 123,
  "created": "2026-03-05T12:34:56.789Z",
  "modified": "2026-03-05T12:34:56.789Z"
}
```

**Job Status Response**:
```json
{
  "id": 845,
  "status": "running",
  "started": "2026-03-05T12:35:00.000Z",
  "finished": null,
  "elapsed": 45.23,
  "job_template_name": "Deploy Application",
  "playbook": "deploy.yml",
  "inventory_name": "staging-web"
}
```

### Error Handling for API Mode
- HTTP 401: Token expired or invalid - refresh authentication
- HTTP 403: Permission denied - check RBAC settings
- HTTP 404: Resource not found - verify template/job ID
- HTTP 500: Server error - retry with exponential backoff
- Connection timeout: Check network connectivity to AAP controller

### Trade-offs of Direct API
**Pros**:
- No MCP server dependency
- Direct control over API interactions
- Can work in environments without MCP support
- Easier to debug API calls

**Cons**:
- Requires credential management
- More verbose tool calls (WebFetch + parsing)
- Manual handling of pagination and rate limits
- SSL/TLS configuration required
- Less abstraction from API changes

END ALTERNATIVE 1 -->

<!-- ALTERNATIVE 2: EVENT DRIVEN ANSIBLE WEBHOOK INTEGRATION
## Event Driven Ansible Integration (Commented Out - Enable if Using EDA)

If you prefer to trigger automations via Event Driven Ansible (EDA) webhooks instead of direct job template launches, uncomment this section. This approach is ideal for event-driven workflows and asynchronous operations.

### Configuration Requirements
- Event Driven Ansible Controller URL
- Webhook endpoint configured in EDA rulebook
- Webhook authentication token or HMAC secret
- Rulebook activated in EDA Controller

### Environment Setup
```bash
export EDA_WEBHOOK_URL="https://your-eda-controller.example.com/api/eda/v1/webhook/{webhook_id}/"
export EDA_WEBHOOK_TOKEN="your-webhook-auth-token"
export EDA_WEBHOOK_SECRET="your-hmac-secret"  # Optional, for HMAC signing
```

### Webhook Payload Patterns

**Trigger Deployment via Webhook**:
```bash
curl -X POST "${EDA_WEBHOOK_URL}" \
  -H "Authorization: Bearer ${EDA_WEBHOOK_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "event_type": "deployment_request",
    "source": "claude-code",
    "metadata": {
      "requested_by": "developer@example.com",
      "timestamp": "2026-03-05T12:34:56Z",
      "conversation_id": "conv-abc123"
    },
    "payload": {
      "template_name": "Deploy Application",
      "inventory": "staging-web",
      "extra_vars": {
        "version": "2.1.4",
        "environment": "staging",
        "rollback_enabled": true
      }
    }
  }'
```

**Trigger via Generic Event**:
```bash
curl -X POST "${EDA_WEBHOOK_URL}" \
  -H "Authorization: Bearer ${EDA_WEBHOOK_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "event_type": "automation_trigger",
    "action": "restart_service",
    "target_inventory": "production-web",
    "service_name": "apache",
    "reason": "high memory usage detected"
  }'
```

**Trigger with HMAC Signing** (for enhanced security):
```bash
PAYLOAD='{"event_type":"deployment_request","payload":{"version":"2.1.4"}}'
SIGNATURE=$(echo -n "$PAYLOAD" | openssl dgst -sha256 -hmac "$EDA_WEBHOOK_SECRET" | awk '{print $2}')

curl -X POST "${EDA_WEBHOOK_URL}" \
  -H "Authorization: Bearer ${EDA_WEBHOOK_TOKEN}" \
  -H "Content-Type: application/json" \
  -H "X-Webhook-Signature: sha256=${SIGNATURE}" \
  -d "$PAYLOAD"
```

### EDA Rulebook Example
This rulebook receives webhook events and launches AAP job templates:

```yaml
---
- name: Handle Claude Code Automation Requests
  hosts: all
  sources:
    - name: webhook_source
      ansible.eda.webhook:
        host: 0.0.0.0
        port: 5000
        token: "{{ eda_webhook_token }}"

  rules:
    - name: Process deployment request
      condition: event.event_type == "deployment_request"
      action:
        run_job_template:
          name: "{{ event.payload.template_name }}"
          organization: Default
          inventory: "{{ event.payload.inventory }}"
          extra_vars: "{{ event.payload.extra_vars }}"
          wait: false

    - name: Process restart request
      condition: event.event_type == "automation_trigger" and event.action == "restart_service"
      action:
        run_job_template:
          name: "Service Restart"
          organization: Default
          inventory: "{{ event.target_inventory }}"
          extra_vars:
            service_name: "{{ event.service_name }}"
            reason: "{{ event.reason }}"
          wait: false

    - name: Log all webhook events
      condition: true
      action:
        debug:
          msg: "Received webhook event: {{ event }}"
```

### Workflow Changes for EDA Mode

**Step 1 — Discovery** (Modified):
- Instead of listing job templates, list available webhook event types
- Present to developer: "Available automation triggers: deployment_request, restart_service, patching_workflow"
- Map developer intent to event_type

**Step 2 — Pre-flight Check** (Modified):
- Show webhook payload preview instead of job template details
- Display: event type, target inventory, payload parameters
- Same confirmation workflow applies

**Step 3 — Trigger** (Modified):
- POST webhook payload instead of launching job template
- Response is typically HTTP 202 Accepted (async)
- Extract webhook request ID if provided

**Step 4 — Monitor** (Modified):
- EDA webhooks are async - monitoring depends on EDA rulebook actions
- If rulebook launches AAP job, query AAP jobs API to find triggered job
- Match by metadata (timestamp, source=claude-code, conversation_id)
- Poll job status as normal once job identified
- If rulebook doesn't provide job ID, inform developer: "Webhook triggered successfully. Job monitoring not available in webhook mode."

**Step 5 — Post-trigger Summary** (Modified):
- If job was found and monitored, show normal summary
- If fire-and-forget: "Webhook triggered successfully. Event: {event_type}, Target: {inventory}"

### Implementation Notes for EDA Mode
- Use Bash tool with curl for webhook POST requests
- Generate HMAC signatures if webhook requires signing
- Include metadata for traceability (conversation_id, timestamp, requested_by)
- Handle HTTP 202 Accepted as success
- Implement retry logic for network failures (3 retries with exponential backoff)
- If EDA provides callback URL in response, optionally poll it for status
- Consider webhook delivery failures as non-blocking (fire-and-forget)

### Event Type Patterns

**Standard Event Types**:
```json
{
  "event_type": "deployment_request",      // Application deployment
  "event_type": "patching_request",        // OS/package patching
  "event_type": "restart_request",         // Service restart
  "event_type": "scaling_request",         // Infrastructure scaling
  "event_type": "backup_request",          // Backup operations
  "event_type": "provisioning_request"     // New resource provisioning
}
```

**Event Payload Structure**:
```json
{
  "event_type": "deployment_request",
  "source": "claude-code",
  "priority": "normal",                    // normal|high|critical
  "metadata": {
    "requested_by": "user@example.com",
    "conversation_id": "conv-xyz789",
    "timestamp": "2026-03-05T12:34:56Z",
    "approval_id": "approval-123"          // If pre-approved
  },
  "payload": {
    "template_name": "Deploy Application",
    "inventory": "staging-web",
    "extra_vars": {},
    "limit": "webservers",                 // Ansible limit pattern
    "tags": ["deploy", "migrate"],         // Ansible tags
    "skip_tags": ["backup"]                // Ansible skip tags
  },
  "callbacks": {
    "success_webhook": "https://...",      // Optional callback URLs
    "failure_webhook": "https://..."
  }
}
```

### Error Handling for EDA Mode
- HTTP 401/403: Check webhook token validity
- HTTP 404: Verify webhook endpoint URL and activation ID
- HTTP 400: Validate webhook payload schema
- HTTP 500: EDA Controller error - check EDA logs
- Timeout: Webhook endpoint not responding - verify EDA service health
- Signature mismatch: HMAC secret incorrect or payload modified

### Trade-offs of EDA Webhook Mode
**Pros**:
- Decouples trigger from execution (event-driven)
- Rulebooks can add complex logic and filtering
- Can trigger multiple actions from single webhook
- Better for asynchronous workflows
- Centralized event handling and routing
- Can integrate with other event sources (monitoring, CI/CD)

**Cons**:
- Requires EDA Controller deployment and configuration
- Less direct feedback (async by nature)
- Harder to monitor specific job outcomes
- Requires maintaining rulebooks alongside playbooks
- Additional layer of abstraction
- Webhook delivery not guaranteed (no built-in retry)
- Debugging requires checking both EDA and AAP logs

### When to Use EDA Mode
- Complex event-driven workflows (e.g., "deploy after CI passes AND approval received")
- Integration with monitoring systems (trigger remediation on alerts)
- Multi-step automations with branching logic
- Need to aggregate events before acting
- Compliance requirements for event audit trails
- Coordinating actions across multiple AAP instances

END ALTERNATIVE 2 -->

## Skill Activation

This skill activates automatically when the developer:
- Asks to "run", "trigger", "launch", "execute" any job, playbook, or automation
- Mentions specific job template names
- Asks about job status, failures, or history
- Requests deployments, patches, restarts, provisioning, or other operations typically handled by AAP
- Says "check AAP", "what jobs are running", "cancel job", etc.

Do not wait for a special command - interpret natural language requests and map them to this workflow.

## Skill Constraints

1. All AAP interactions MUST use the MCP server tools - never make direct API calls
2. Never skip the pre-flight confirmation (Step 2)
3. Never launch production jobs without explicit production confirmation
4. Always retrieve logs automatically on failure
5. Always poll job status until terminal state (unless developer cancels)
6. Work with any job template in AAP - do not hardcode template names
7. Keep developer informed with real-time status updates during monitoring
8. Treat this skill as read-write - launching jobs is permitted and expected

## Success Criteria

The skill is working correctly when:
- Developers can trigger any AAP job using natural language
- All jobs require explicit confirmation before launch
- Production jobs have extra safety checks
- Failed jobs automatically show logs and error context
- Job monitoring happens automatically without developer asking
- Chained job workflows are supported
- Developers never have to leave the conversation to check AAP UI (though the URL is always provided)
