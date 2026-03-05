# Quick Start Guide

## 1. Prerequisites Check

```bash
# Verify Ansible is installed
ansible --version

# Install Ansible if needed (on Fedora/RHEL)
sudo dnf install ansible-core

# Install required collections
ansible-galaxy collection install -r requirements.yml
```

## 2. Configure Your Environment

### Edit inventory file
```bash
vi inventory/hosts
```

Add your RHEL server(s):
```ini
[webservers]
192.168.1.100
```

### Edit variables
```bash
vi group_vars/webservers.yml
```

Update `server_name` and `server_admin_email`.

## 3. Test Connectivity

```bash
# Ping all servers
ansible webservers -m ping

# Check if servers are reachable
ansible webservers -m shell -a "hostname"
```

## 4. Deploy Application

```bash
# Deploy to all webservers
ansible-playbook deploy.yml

# Deploy to specific host
ansible-playbook deploy.yml --limit 192.168.1.100

# Dry run first
ansible-playbook deploy.yml --check
```

## 5. Verify Deployment

```bash
# Run verification playbook
ansible-playbook verify.yml

# Or manually test
curl http://your-server-ip/
```

## 6. Common Operations

### Update application files
```bash
# After modifying files in ../cheeseburger-map-app/
ansible-playbook deploy.yml
```

### View logs
```bash
ansible webservers -m shell -a "tail -f /var/log/httpd/cheeseburger-map-access.log"
```

### Restart Apache
```bash
ansible webservers -m systemd -a "name=httpd state=restarted" --become
```

### Rollback application
```bash
ansible-playbook rollback.yml
```

### Complete cleanup
```bash
ansible-playbook cleanup.yml
```

## Troubleshooting

### Can't connect to servers
```bash
# Test SSH
ssh ansible@your-server-ip

# Check SSH keys
ssh-copy-id ansible@your-server-ip
```

### Permission denied
```bash
# Verify sudo access
ansible webservers -m shell -a "whoami" --become
```

### SELinux blocking access
```bash
# Check SELinux denials
ansible webservers -m shell -a "ausearch -m avc -ts recent" --become
```

## Quick Reference

| Task | Command |
|------|---------|
| Deploy | `ansible-playbook deploy.yml` |
| Verify | `ansible-playbook verify.yml` |
| Rollback | `ansible-playbook rollback.yml` |
| Cleanup | `ansible-playbook cleanup.yml` |
| Ping hosts | `ansible webservers -m ping` |
| Check syntax | `ansible-playbook deploy.yml --syntax-check` |
| Dry run | `ansible-playbook deploy.yml --check` |
| Verbose | `ansible-playbook deploy.yml -vvv` |
