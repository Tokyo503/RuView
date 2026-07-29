# Tokyo503 Repository Safety Policy

This repository is linked to the Tokyo503 account, but it is not the main Tokyo503 automation vault.

## Safety defaults

```yaml
no_secrets_in_repo: true
no_webhook_urls_in_docs: true
no_authorization_headers_in_logs: true
auto_delete: false
auto_publish_without_review: false
make_api_write_mode: blocked
```

## RuView-specific rule

Because this repository contains a separate project, Tokyo503 automation must not modify runtime code, architecture, permissions, or public-facing behavior automatically.

## v7 Claude Playbooks Policy

v7 Claude playbooks may be used only for read-only review, documentation suggestions, and proposal/report generation.

Allowed v7 use:

```text
read-only Claude stack review
agent pattern readiness report
safe documentation proposal
non-destructive repository notes
```

Blocked v7 use:

```yaml
auto_code_change: false
auto_install_tools: false
auto_connect_mcp: false
auto_create_agents: false
auto_publish: false
auto_delete: false
make_api_write_mode: blocked
orchestration_live_mode: blocked
```

## v7.2 ChatGPT Claude Bridge Policy

ChatGPT/Claude bridge may be used only for read-only review, comparison notes, and documentation proposals for RuView.

Allowed bridge use:

```text
read-only dual-model review
safe documentation comparison
non-destructive recommendation report
conflict-resolution summary without code changes
```

Blocked bridge use:

```yaml
auto_code_change: false
live_api_call_from_ruview: false
openai_key_in_repo: false
anthropic_key_in_repo: false
raw_payload_logging: false
auto_connect_mcp: false
auto_publish: false
auto_delete: false
make_api_write_mode: blocked
orchestration_live_mode: blocked
```

Any bridge output that recommends code or architecture changes must become a proposal/report only; it must not modify RuView runtime files automatically.

## Allowed from Tokyo503 automation

```text
read-only review
safe documentation
policy note
non-destructive reports
```

## Blocked without explicit review

```text
code changes
architecture changes
secret changes
GitHub permission changes
delete or rename files
auto publishing
Make API write mode
v7 tool installation
v7 MCP connection
v7 live orchestration
ChatGPT Claude bridge live call
OpenAI or Anthropic key storage
```
