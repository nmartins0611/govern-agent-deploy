# Changelog

All notable changes to the AAP Deployment Skill will be documented in this file.

## [1.0.0] - 2026-03-06

### Initial Release

**Features**:
- Complete deployment workflow (commit → push → deploy → monitor)
- Automatic dev branch isolation for deployments
- Real-time job monitoring with status updates
- Server detail extraction from playbook output
- Production safety guardrails
- Automatic log retrieval on failures
- Support for chained deployments
- Integration with AAP MCP server

**Skills Included**:
- AAP_DEPLOY_SKILL.md - Deployment workflow with git integration
- AAP_BASE_SKILL.md - General AAP job execution

**Documentation**:
- README.md - Overview and installation
- QUICK_START.md - 5-minute getting started guide
- EXAMPLES.md - Real-world usage scenarios
- TROUBLESHOOTING.md - Common issues and solutions

**Safety Features**:
- Pre-flight confirmation for all deployments
- Production confirmation requirement ("yes, target production")
- Version/tag confirmation for releases
- Host count warnings for large deployments
- Duplicate run detection
- Long-running job warnings
- Automatic rollback suggestions on failure

**Extraction Capabilities**:
- IP addresses from job output
- URLs and hostnames
- Service ports and application paths
- Ansible facts (if gather_facts enabled)
- Custom debug task output

**Git Integration**:
- Automatic commit message generation
- Dev branch creation and management
- Push verification before deployment
- Commit SHA tracking for rollback
- Git hook respect (never skips hooks)

### Known Limitations

- Requires AAP MCP server pre-configured
- Limited to MCP tool-based AAP interaction (no direct API)
- Server detail extraction depends on playbook output format
- Maximum monitoring duration: 1 hour (configurable)

### Requirements

- Claude Code (compatible version)
- AAP MCP server connection
- Git repository
- AAP job templates with execute permissions

## Future Enhancements (Roadmap)

### Planned for 1.1.0
- [ ] Support for workflow job templates
- [ ] Enhanced multi-environment deployment chains
- [ ] Deployment rollback automation
- [ ] Custom pre-flight validation hooks
- [ ] Configurable branch strategies

### Under Consideration
- [ ] Integration with Event Driven Ansible (EDA)
- [ ] Support for approval workflows
- [ ] Deployment metrics and analytics
- [ ] Custom server detail extraction patterns (user-configurable)
- [ ] Parallel multi-inventory deployments
- [ ] Deployment templates (save common workflows)

## Contributing

Found a bug or have a feature request?

1. Check TROUBLESHOOTING.md first
2. Review existing issues/discussions
3. Submit detailed issue with:
   - Claude Code version
   - AAP version
   - Steps to reproduce
   - Expected vs actual behavior
   - Relevant logs or screenshots

For feature requests:
- Describe the use case
- Explain the benefit
- Provide example workflow

## Version History

| Version | Date       | Highlights                              |
|---------|------------|-----------------------------------------|
| 1.0.0   | 2026-03-06 | Initial release with core features      |

---

**Versioning**: This project follows [Semantic Versioning](https://semver.org/).
- MAJOR: Breaking changes to skill behavior
- MINOR: New features, backward compatible
- PATCH: Bug fixes, documentation updates
