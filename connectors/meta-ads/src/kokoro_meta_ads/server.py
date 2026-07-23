# pyright: reportMissingImports=false, reportUnknownArgumentType=false, reportUnknownMemberType=false, reportUnknownParameterType=false, reportUnknownVariableType=false

"""Read-only Meta Ads MCP server with an explicit credential boundary."""

from __future__ import annotations

import json
import logging
import os
import re
from contextlib import asynccontextmanager
from datetime import date
from typing import Any

from facebook_business.adobjects.ad import Ad
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.user import User
from facebook_business.api import FacebookAdsApi
from facebook_business.exceptions import FacebookRequestError
from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

from kokoro_meta_ads.doctor import REQUIRED_ENVIRONMENT, diagnose

LOGGER = logging.getLogger("kokoro_meta_ads")
ACCOUNT_ID_PATTERN = re.compile(r"^act_[0-9]+$")
OBJECT_ID_PATTERN = re.compile(r"^[0-9]+$")
ALLOWED_DATE_PRESETS = {
    "today",
    "yesterday",
    "last_7d",
    "last_14d",
    "last_30d",
    "last_90d",
    "this_month",
    "last_month",
    "lifetime",
}
ALLOWED_LEVELS = {"account", "campaign", "adset", "ad"}
ALLOWED_STATUSES = {"ACTIVE", "ARCHIVED", "DELETED", "PAUSED"}
ALLOWED_BREAKDOWNS = {
    "age",
    "country",
    "device_platform",
    "gender",
    "impression_device",
    "placement",
    "publisher_platform",
    "region",
}
READ_ONLY_TOOL = ToolAnnotations(
    readOnlyHint=True,
    destructiveHint=False,
    idempotentHint=True,
    openWorldHint=True,
)


@asynccontextmanager
async def app_lifespan(_server: FastMCP):
    """Initialize the provider SDK only after credentials are present."""
    readiness = diagnose()
    if readiness["status"] != "ready":
        missing = ", ".join(str(name) for name in readiness["missing"])
        raise RuntimeError(
            "Meta Ads connector is unconfigured. "
            f"Missing environment variables: {missing}"
        )

    FacebookAdsApi.init(
        os.environ["FACEBOOK_APP_ID"],
        os.environ["FACEBOOK_APP_SECRET"],
        os.environ["FACEBOOK_ACCESS_TOKEN"],
    )
    LOGGER.info("Meta Ads read-only connector initialized")
    yield {"credential_names": REQUIRED_ENVIRONMENT}


mcp = FastMCP(name="Kokoro Meta Ads Read Only", lifespan=app_lifespan)


def _json_safe(value: Any) -> Any:
    """Normalize SDK objects into MCP-serializable values."""
    if not isinstance(value, (dict, list, tuple, str, int, float, bool, type(None))):
        try:
            value = dict(value)
        except (TypeError, ValueError):
            value = str(value)
    return json.loads(json.dumps(value, default=str))


def _pick(record: Any, fields: list[str]) -> dict[str, Any]:
    """Return an allowlisted dictionary from a provider SDK object."""
    return {field: _json_safe(record.get(field)) for field in fields}


def _provider_error(error: FacebookRequestError) -> dict[str, Any]:
    """Return provider diagnostics without request headers or credentials."""
    return {
        "code": error.api_error_code(),
        "error": True,
        "message": error.api_error_message() or "Meta Ads API request failed",
    }


def _unexpected_error(error: Exception) -> dict[str, Any]:
    LOGGER.exception("Meta Ads connector request failed")
    return {
        "error": True,
        "message": "Unexpected connector error",
        "type": type(error).__name__,
    }


def _require_account_id(account_id: str) -> None:
    if not ACCOUNT_ID_PATTERN.fullmatch(account_id):
        raise ValueError("account_id must use the act_<digits> format")


def _require_object_id(object_id: str, field_name: str) -> None:
    if not OBJECT_ID_PATTERN.fullmatch(object_id):
        raise ValueError(f"{field_name} must contain digits only")


def _insight_params(
    *,
    date_preset: str,
    level: str,
    time_range_since: str | None,
    time_range_until: str | None,
) -> dict[str, Any]:
    if level not in ALLOWED_LEVELS:
        allowed = ", ".join(sorted(ALLOWED_LEVELS))
        raise ValueError(f"level must be one of: {allowed}")

    params: dict[str, Any] = {"level": level}
    if time_range_since is not None or time_range_until is not None:
        if time_range_since is None or time_range_until is None:
            raise ValueError("custom time range requires both since and until")
        since = date.fromisoformat(time_range_since)
        until = date.fromisoformat(time_range_until)
        if since > until:
            raise ValueError("custom time range since must not be after until")
        params["time_range"] = {
            "since": time_range_since,
            "until": time_range_until,
        }
        return params

    if date_preset not in ALLOWED_DATE_PRESETS:
        allowed = ", ".join(sorted(ALLOWED_DATE_PRESETS))
        raise ValueError(f"date_preset must be one of: {allowed}")
    params["date_preset"] = date_preset
    return params


def _list_ad_accounts() -> list[dict[str, Any]]:
    fields = [
        "account_id",
        "account_status",
        "amount_spent",
        "balance",
        "currency",
        "id",
        "name",
        "spend_cap",
        "timezone_name",
    ]
    accounts = User(fbid="me").get_ad_accounts(fields=fields)
    return [_pick(account, fields) for account in accounts]


def _account_summary(
    account_id: str,
    *,
    date_preset: str,
    time_range_since: str | None,
    time_range_until: str | None,
) -> dict[str, Any]:
    _require_account_id(account_id)
    params = _insight_params(
        date_preset=date_preset,
        level="account",
        time_range_since=time_range_since,
        time_range_until=time_range_until,
    )
    account = AdAccount(account_id)
    account.api_get(fields=["account_status", "currency", "name", "timezone_name"])
    insight_fields = [
        "clicks",
        "cpc",
        "cpm",
        "ctr",
        "frequency",
        "impressions",
        "reach",
        "spend",
    ]
    insights = list(account.get_insights(fields=insight_fields, params=params))
    return {
        "account": _pick(
            account,
            ["account_status", "currency", "id", "name", "timezone_name"],
        ),
        "insights": _pick(insights[0], insight_fields) if insights else {},
    }


@mcp.tool(annotations=READ_ONLY_TOOL)
def list_ad_accounts() -> list[dict[str, Any]]:
    """List every Meta advertising account available to the user token."""
    try:
        return _list_ad_accounts()
    except FacebookRequestError as error:
        return [_provider_error(error)]
    except Exception as error:  # pragma: no cover - provider/runtime boundary
        return [_unexpected_error(error)]


@mcp.tool(annotations=READ_ONLY_TOOL)
def get_campaigns(
    account_id: str,
    status_filter: str | None = None,
) -> list[dict[str, Any]]:
    """Read campaign configuration for one advertising account."""
    try:
        _require_account_id(account_id)
        params: dict[str, Any] = {}
        if status_filter is not None:
            normalized_status = status_filter.upper()
            if normalized_status not in ALLOWED_STATUSES:
                allowed = ", ".join(sorted(ALLOWED_STATUSES))
                raise ValueError(f"status_filter must be one of: {allowed}")
            params["effective_status"] = [normalized_status]

        fields = [
            "buying_type",
            "created_time",
            "daily_budget",
            "effective_status",
            "id",
            "lifetime_budget",
            "name",
            "objective",
            "start_time",
            "status",
            "stop_time",
            "updated_time",
        ]
        campaigns = AdAccount(account_id).get_campaigns(fields=fields, params=params)
        return [_pick(campaign, fields) for campaign in campaigns]
    except ValueError as error:
        return [{"error": True, "message": str(error)}]
    except FacebookRequestError as error:
        return [_provider_error(error)]
    except Exception as error:  # pragma: no cover - provider/runtime boundary
        return [_unexpected_error(error)]


@mcp.tool(annotations=READ_ONLY_TOOL)
def get_campaign_performance(
    account_id: str,
    date_preset: str = "last_30d",
    level: str = "campaign",
    time_range_since: str | None = None,
    time_range_until: str | None = None,
) -> list[dict[str, Any]]:
    """Read performance metrics at account, campaign, ad-set or ad level."""
    try:
        _require_account_id(account_id)
        params = _insight_params(
            date_preset=date_preset,
            level=level,
            time_range_since=time_range_since,
            time_range_until=time_range_until,
        )
        fields = [
            "actions",
            "campaign_id",
            "campaign_name",
            "clicks",
            "cost_per_action_type",
            "cpc",
            "cpm",
            "ctr",
            "date_start",
            "date_stop",
            "frequency",
            "impressions",
            "reach",
            "spend",
        ]
        insights = AdAccount(account_id).get_insights(fields=fields, params=params)
        return [_pick(insight, fields) for insight in insights]
    except ValueError as error:
        return [{"error": True, "message": str(error)}]
    except FacebookRequestError as error:
        return [_provider_error(error)]
    except Exception as error:  # pragma: no cover - provider/runtime boundary
        return [_unexpected_error(error)]


@mcp.tool(annotations=READ_ONLY_TOOL)
def get_campaign_status_and_budget(account_id: str) -> list[dict[str, Any]]:
    """Read campaign status, configured budget and lifetime spend."""
    try:
        _require_account_id(account_id)
        fields = [
            "budget_remaining",
            "daily_budget",
            "effective_status",
            "id",
            "lifetime_budget",
            "name",
            "status",
        ]
        campaigns = AdAccount(account_id).get_campaigns(fields=fields)
        results: list[dict[str, Any]] = []
        for campaign in campaigns:
            record = _pick(campaign, fields)
            insights = list(
                campaign.get_insights(
                    fields=["spend"],
                    params={"date_preset": "lifetime", "level": "campaign"},
                )
            )
            record["lifetime_spend"] = (
                _json_safe(insights[0].get("spend")) if insights else "0"
            )
            results.append(record)
        return results
    except ValueError as error:
        return [{"error": True, "message": str(error)}]
    except FacebookRequestError as error:
        return [_provider_error(error)]
    except Exception as error:  # pragma: no cover - provider/runtime boundary
        return [_unexpected_error(error)]


@mcp.tool(annotations=READ_ONLY_TOOL)
def get_demographic_breakdown(
    account_id: str,
    date_preset: str = "last_30d",
    level: str = "campaign",
    breakdowns: str = "age,gender",
    time_range_since: str | None = None,
    time_range_until: str | None = None,
) -> list[dict[str, Any]]:
    """Read performance segmented by allowlisted demographic dimensions."""
    try:
        _require_account_id(account_id)
        selected = [item.strip() for item in breakdowns.split(",") if item.strip()]
        if not selected or any(item not in ALLOWED_BREAKDOWNS for item in selected):
            allowed = ", ".join(sorted(ALLOWED_BREAKDOWNS))
            raise ValueError(f"breakdowns must use one or more of: {allowed}")
        params = _insight_params(
            date_preset=date_preset,
            level=level,
            time_range_since=time_range_since,
            time_range_until=time_range_until,
        )
        params["breakdowns"] = selected
        fields = [
            "campaign_id",
            "campaign_name",
            "clicks",
            "cpc",
            "cpm",
            "ctr",
            "impressions",
            "reach",
            "spend",
            *selected,
        ]
        insights = AdAccount(account_id).get_insights(fields=fields, params=params)
        return [_pick(insight, fields) for insight in insights]
    except ValueError as error:
        return [{"error": True, "message": str(error)}]
    except FacebookRequestError as error:
        return [_provider_error(error)]
    except Exception as error:  # pragma: no cover - provider/runtime boundary
        return [_unexpected_error(error)]


@mcp.tool(annotations=READ_ONLY_TOOL)
def get_ad_creative_details(ad_id: str) -> dict[str, Any]:
    """Read the allowlisted creative payload associated with one ad."""
    try:
        _require_object_id(ad_id, "ad_id")
        fields = [
            "creative",
            "effective_status",
            "id",
            "name",
            "preview_shareable_link",
            "status",
        ]
        ad = Ad(ad_id)
        ad.api_get(fields=fields)
        return _pick(ad, fields)
    except ValueError as error:
        return {"error": True, "message": str(error)}
    except FacebookRequestError as error:
        return _provider_error(error)
    except Exception as error:  # pragma: no cover - provider/runtime boundary
        return _unexpected_error(error)


@mcp.tool(annotations=READ_ONLY_TOOL)
def get_account_insights_summary(
    account_id: str,
    date_preset: str = "last_30d",
    time_range_since: str | None = None,
    time_range_until: str | None = None,
) -> dict[str, Any]:
    """Read account metadata and an aggregated performance summary."""
    try:
        return _account_summary(
            account_id,
            date_preset=date_preset,
            time_range_since=time_range_since,
            time_range_until=time_range_until,
        )
    except ValueError as error:
        return {"error": True, "message": str(error)}
    except FacebookRequestError as error:
        return _provider_error(error)
    except Exception as error:  # pragma: no cover - provider/runtime boundary
        return _unexpected_error(error)


@mcp.tool(annotations=READ_ONLY_TOOL)
def get_all_accounts_overview(
    date_preset: str = "last_30d",
    time_range_since: str | None = None,
    time_range_until: str | None = None,
) -> list[dict[str, Any]]:
    """Read a performance overview for every accessible ad account."""
    try:
        accounts = _list_ad_accounts()
        results: list[dict[str, Any]] = []
        for account in accounts:
            account_id = str(account.get("id") or "")
            if not ACCOUNT_ID_PATTERN.fullmatch(account_id):
                continue
            try:
                results.append(
                    _account_summary(
                        account_id,
                        date_preset=date_preset,
                        time_range_since=time_range_since,
                        time_range_until=time_range_until,
                    )
                )
            except FacebookRequestError as error:
                results.append({"account_id": account_id, **_provider_error(error)})
        return results
    except ValueError as error:
        return [{"error": True, "message": str(error)}]
    except FacebookRequestError as error:
        return [_provider_error(error)]
    except Exception as error:  # pragma: no cover - provider/runtime boundary
        return [_unexpected_error(error)]


def main() -> None:
    """Run the connector over STDIO."""
    logging.basicConfig(level=logging.INFO)
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
