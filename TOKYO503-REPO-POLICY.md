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
```
