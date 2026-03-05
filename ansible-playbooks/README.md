# Ansible Playbooks for Cheeseburger Map Application

This directory contains Ansible playbooks to deploy the Cheeseburger Map web application to RHEL webservers.

## Directory Structure

```
ansible-playbooks/
├── deploy.yml                      # Main deployment playbook
├── ansible.cfg                     # Ansible configuration
├── inventory/
│   └── hosts                       # Inventory file (define your servers here)
├── group_vars/
│   └── webservers.yml             # Variables for webserver group
└── templates/
    └── cheeseburger-map.conf.j2   # Apache virtual host template
```

## Prerequisites

### On Control Node (where you run Ansible)
- Ansible 2.9 or higher installed
- SSH access to target RHEL servers
- Python 3.6+ installed

### On Target RHEL Servers
- RHEL 8 or RHEL 9
- Python 3 installed
- Sudo access for the Ansible user
- SSH key-based authentication configured

## Setup Instructions

### 1. Configure Inventory

Edit `inventory/hosts` and add your RHEL webserver hostnames or IP addresses:

```ini
[webservers]
web01.example.com
web02.example.com
192.168.1.10
```

### 2. Configure Variables

Edit `group_vars/webservers.yml` to customize:
- `server_name`: Your domain name
- `server_admin_email`: Admin contact email
- Other application-specific settings

### 3. Configure SSH Access

Ensure you can SSH to your servers:

```bash
# Test SSH connection
ssh ansible@web01.example.com

# Or copy your SSH key
ssh-copy-id ansible@web01.example.com
```

### 4. Test Connectivity

```bash
cd ansible-playbooks
ansible webservers -m ping
```

## Deployment

### Deploy to All Webservers

```bash
cd ansible-playbooks
ansible-playbook deploy.yml
```

### Deploy to Specific Host

```bash
ansible-playbook deploy.yml --limit web01.example.com
```

### Check Mode (Dry Run)

```bash
ansible-playbook deploy.yml --check
```

### Verbose Output

```bash
ansible-playbook deploy.yml -v
# or -vv, -vvv for more verbosity
```

## What the Playbook Does

The `deploy.yml` playbook performs the following tasks:

1. **Install Apache (httpd)** - Installs the Apache web server
2. **Install and configure firewalld** - Sets up the firewall
3. **Open firewall ports** - Allows HTTP (80) and HTTPS (443) traffic
4. **Create application directory** - Creates `/var/www/html/cheeseburger-map/`
5. **Copy application files** - Deploys HTML, CSS, and JS files
6. **Set permissions** - Configures proper file ownership (apache:apache)
7. **Configure SELinux** - Sets correct SELinux context for web content
8. **Create virtual host** - Deploys Apache configuration
9. **Start Apache** - Ensures httpd service is running and enabled
10. **Verify deployment** - Waits for Apache to be ready on port 80

## Post-Deployment

After successful deployment, the application will be available at:

```
http://your-server-ip/
http://your-server-name/
```

### Verify Deployment

```bash
# Check Apache status
ansible webservers -m shell -a "systemctl status httpd"

# Check firewall rules
ansible webservers -m shell -a "firewall-cmd --list-services"

# Test HTTP access
curl http://your-server-ip/
```

### View Logs

```bash
# Apache access logs
ansible webservers -m shell -a "tail -n 50 /var/log/httpd/cheeseburger-map-access.log"

# Apache error logs
ansible webservers -m shell -a "tail -n 50 /var/log/httpd/cheeseburger-map-error.log"
```

## Troubleshooting

### SELinux Issues

If you encounter permission denied errors, check SELinux:

```bash
# Check SELinux status
ansible webservers -m shell -a "getenforce"

# View SELinux denials
ansible webservers -m shell -a "ausearch -m avc -ts recent"

# Temporarily set to permissive (for testing only)
ansible webservers -m shell -a "setenforce 0"
```

### Firewall Issues

```bash
# Check firewall status
ansible webservers -m shell -a "firewall-cmd --state"

# List allowed services
ansible webservers -m shell -a "firewall-cmd --list-all"

# Reload firewall
ansible webservers -m shell -a "firewall-cmd --reload"
```

### Apache Issues

```bash
# Test Apache configuration
ansible webservers -m shell -a "httpd -t"

# Restart Apache
ansible webservers -m shell -a "systemctl restart httpd"

# View Apache status
ansible webservers -m shell -a "systemctl status httpd"
```

## Updating the Application

To update the application files:

1. Update files in `../cheeseburger-map-app/`
2. Run the deployment playbook again:

```bash
ansible-playbook deploy.yml
```

The playbook is idempotent and safe to run multiple times.

## Security Considerations

- The playbook configures basic security headers in Apache
- SELinux is properly configured for web content
- Firewall rules restrict access to HTTP/HTTPS only
- Directory listing is disabled
- Consider adding HTTPS/SSL certificates for production use

## Advanced Usage

### Using Ansible Vault for Sensitive Data

```bash
# Create encrypted variables file
ansible-vault create group_vars/webservers_vault.yml

# Edit encrypted file
ansible-vault edit group_vars/webservers_vault.yml

# Run playbook with vault
ansible-playbook deploy.yml --ask-vault-pass
```

### Tags for Selective Execution

Add tags to tasks in deploy.yml and run:

```bash
ansible-playbook deploy.yml --tags "apache,firewall"
```

## Support

For issues or questions, refer to:
- Ansible Documentation: https://docs.ansible.com/
- RHEL Documentation: https://access.redhat.com/documentation/
