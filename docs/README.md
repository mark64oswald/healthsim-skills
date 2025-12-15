# HealthSim Documentation

**Shared documentation for all HealthSim products (PatientSim, MemberSim, RxMemberSim)**

---

## Getting Started

If you're new to HealthSim, start here:

| Resource | Description |
|----------|-------------|
| **[hello-healthsim/](../hello-healthsim/)** | 5-minute quick start guide |
| **[SKILL.md](../SKILL.md)** | Master skill file reference |

---

## Documentation Index

### MCP Integration

How to integrate with Claude Desktop and Claude Code via MCP (Model Context Protocol):

| Document | Description |
|----------|-------------|
| [integration-guide.md](mcp/integration-guide.md) | Complete MCP integration guide |
| [development-guide.md](mcp/development-guide.md) | Developing MCP servers |
| [configuration.md](mcp/configuration.md) | MCP server configuration |

### State Management

Save, load, and manage scenarios and sessions:

| Document | Description |
|----------|-------------|
| [user-guide.md](state-management/user-guide.md) | User guide for state management |
| [specification.md](state-management/specification.md) | Technical specification |

### Skills Framework

How to create and use skills - structured knowledge documents:

| Document | Description |
|----------|-------------|
| [format-specification.md](skills/format-specification.md) | Skills format v1.0 specification |
| [format-specification-v2.md](skills/format-specification-v2.md) | Skills format v2.0 (Claude-optimized) |
| [migration-guide.md](skills/migration-guide.md) | Migrating from v1.0 to v2.0 |
| [creating-skills.md](skills/creating-skills.md) | Guide to creating new skills |

### Extension Framework

How to add new capabilities to HealthSim:

| Document | Description |
|----------|-------------|
| [philosophy.md](extensions/philosophy.md) | Conversation-first extension philosophy |
| [mcp-tools.md](extensions/mcp-tools.md) | Adding MCP tools (actions) |
| [skills.md](extensions/skills.md) | Adding skills (knowledge) |
| [slash-commands.md](extensions/slash-commands.md) | Adding slash commands (shortcuts) |
| [quick-reference.md](extensions/quick-reference.md) | Single-page quick reference |

### Architecture

System design and technical specifications:

| Document | Description |
|----------|-------------|
| [layered-pattern.md](architecture/layered-pattern.md) | Layered architecture overview |
| [healthsim-core-spec.md](architecture/healthsim-core-spec.md) | Shared infrastructure specification |

### Contributing

Development guidelines and standards:

| Document | Description |
|----------|-------------|
| [contributing.md](contributing.md) | Contribution guidelines for all products |

---

## Product-Specific Documentation

For documentation specific to each product, see the respective repositories:

| Product | Repository | Documentation |
|---------|------------|---------------|
| **PatientSim** | [patientsim](https://github.com/mark64oswald/patientsim) | `patientsim/docs/` |
| **MemberSim** | [membersim](https://github.com/mark64oswald/membersim) | `membersim/docs/` |
| **RxMemberSim** | [rxmembersim](https://github.com/mark64oswald/rxmembersim) | `rxmembersim/docs/` |

### What's Shared vs. Product-Specific?

| Shared (in healthsim-workspace/docs/) | Product-Specific (in product repos) |
|------------------------------------|-------------------------------------|
| MCP integration | User guides (generating entities) |
| State management | API reference |
| Skills format | Product tutorials |
| Extension framework | Use case guides |
| Architecture | Product-specific formats |
| Contributing guidelines | Product-specific validation |

---

## Scenario & Format Reference

For scenarios, formats, and reference data:

| Resource | Location | Description |
|----------|----------|-------------|
| **Scenarios** | [scenarios/](../scenarios/) | Clinical scenarios by product |
| **Formats** | [formats/](../formats/) | Output format transformations |
| **References** | [references/](../references/) | Code systems, clinical rules, terminology |

---

## Quick Links

### By Task

| I want to... | Go to... |
|--------------|----------|
| Get started quickly | [hello-healthsim/](../hello-healthsim/) |
| Configure MCP | [mcp/configuration.md](mcp/configuration.md) |
| Save/load scenarios | [state-management/user-guide.md](state-management/user-guide.md) |
| Add a new MCP tool | [extensions/mcp-tools.md](extensions/mcp-tools.md) |
| Create a new skill | [skills/creating-skills.md](skills/creating-skills.md) |
| Add a slash command | [extensions/slash-commands.md](extensions/slash-commands.md) |
| Understand architecture | [architecture/layered-pattern.md](architecture/layered-pattern.md) |
| Contribute code | [contributing.md](contributing.md) |

### By Role

| Role | Start with... |
|------|---------------|
| **User** | [hello-healthsim/](../hello-healthsim/) |
| **Developer** | [extensions/philosophy.md](extensions/philosophy.md) |
| **Architect** | [architecture/layered-pattern.md](architecture/layered-pattern.md) |
| **Contributor** | [contributing.md](contributing.md) |

---

## Document Conventions

Throughout this documentation:

- **User requests** are shown in conversational form: `"Generate a diabetic patient"`
- **Code examples** use Python and markdown code blocks
- **File paths** are relative to repository root
- **Cross-references** link to other relevant documents

---

## Getting Help

- **GitHub Discussions**: Ask questions about HealthSim
- **GitHub Issues**: Report bugs or request features
- **Pull Requests**: Contribute improvements

---

*HealthSim generates synthetic test data only. Never use for actual patient care or real PHI.*
