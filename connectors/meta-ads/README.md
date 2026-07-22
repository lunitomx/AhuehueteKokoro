# Kokoro Meta Ads MCP

Portable, owned and read-only MCP server for Meta Ads reporting. It uses the
official `facebook-business` Python SDK and exposes exactly eight query tools:

1. `list_ad_accounts`
2. `get_campaigns`
3. `get_campaign_performance`
4. `get_campaign_status_and_budget`
5. `get_demographic_breakdown`
6. `get_ad_creative_details`
7. `get_account_insights_summary`
8. `get_all_accounts_overview`

It cannot create, update, pause, activate, or delete advertising resources.

## Credentials

The server reads these names from its process environment:

- `FACEBOOK_ACCESS_TOKEN`
- `FACEBOOK_APP_ID`
- `FACEBOOK_APP_SECRET`

The public template contains empty values. Never place real values in this
checkout or in a tracked MCP configuration file.

Check readiness without contacting Meta or revealing values:

```bash
uv run --project connectors/meta-ads kokoro-meta-ads-doctor
```

An installation without credentials reports `unconfigured` and remains a valid
Kokoro installation. Agent-specific registration is documented by Kokoro's MCP
reference and uses the installed `run.sh` launcher.
