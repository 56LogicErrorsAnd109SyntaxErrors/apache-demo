from django.http import Http404, JsonResponse
from django.shortcuts import render


def graph_page(request):
    """Render the base HTML page shell for the governance map."""
    return render(request, "my_app/graph.html")


def graph_data_api(request):
    """API endpoint providing nodes and directional edges."""
    data = {
        "nodes": [
            {"id": "producer_1", "name": "Producer 1", "category": 0, "symbolSize": 50},
            {"id": "producer_2", "name": "Producer 2", "category": 0, "symbolSize": 50},
            {"id": "endpoint_1", "name": "/api/v1/users", "category": 1, "symbolSize": 40},
            {"id": "endpoint_2", "name": "/api/v1/billing", "category": 1, "symbolSize": 40},
            {"id": "endpoint_3", "name": "/api/v1/status", "category": 1, "symbolSize": 40},
            {"id": "consumer_1", "name": "Consumer 1", "category": 2, "symbolSize": 45},
            {"id": "consumer_2", "name": "Consumer 2", "category": 2, "symbolSize": 45},
        ],
        "edges": [
            {"source": "producer_1", "target": "endpoint_1", "label": {"show": True, "formatter": "owner"}},
            {"source": "producer_2", "target": "endpoint_2", "label": {"show": True, "formatter": "owner"}},
            {"source": "producer_2", "target": "endpoint_3", "label": {"show": True, "formatter": "owner"}},
            {"source": "consumer_1", "target": "endpoint_1", "label": {"show": True, "formatter": "api-key-1"}},
            {"source": "consumer_2", "target": "endpoint_1", "label": {"show": True, "formatter": "api-key-2"}},
            {"source": "consumer_2", "target": "endpoint_2", "label": {"show": True, "formatter": "api-key-3"}},
        ],
    }
    return JsonResponse(data)


def entity_detail_page(request, entity_type, entity_id):
    """Render a simple detail page for a producer, consumer, or endpoint."""
    sample_data = {
        "producer": {
            "title": "Producer Detail",
            "subtitle": "Overview of a team or service that owns endpoints.",
            "badge": "Producer",
            "entity_name": "Payments Platform",
            "entity_id": entity_id,
            "summary": [
                {"label": "Owned endpoints", "value": "3"},
                {"label": "Pending approvals", "value": "2"},
                {"label": "Approval SLA", "value": "24 hours"},
            ],
            "primary_panel_title": "Endpoints owned",
            "primary_panel_items": [
                {"title": "/api/v1/billing", "detail": "Risk level: Medium • Serving 14 consumers"},
                {"title": "/api/v1/invoices", "detail": "Risk level: High • Serving 6 consumers"},
                {"title": "/api/v1/payments", "detail": "Risk level: Low • Serving 21 consumers"},
            ],
            "secondary_panel_title": "Approval requests",
            "secondary_panel_items": [
                {"title": "Request from Consumer Analytics", "detail": "Status: Pending • Expires in 6 days"},
                {"title": "Request from Partner Reporting", "detail": "Status: Approved • Approved on Jun 10, 2026"},
            ],
            "detail_sections": [
                {
                    "title": "Current configuration",
                    "rows": [
                        ("Owner", "Payments Platform Team"),
                        ("Primary contact", "payments-ops@company.com"),
                        ("Review cycle", "Monthly"),
                    ],
                },
                {
                    "title": "Recent updates",
                    "rows": [
                        ("Jun 12, 2026", "Updated auth policy for billing API"),
                        ("Jun 04, 2026", "Adjusted endpoint timeout settings"),
                    ],
                },
            ],
        },
        "consumer": {
            "title": "Consumer Detail",
            "subtitle": "Overview of who is using approved API access.",
            "badge": "Consumer",
            "entity_name": "Marketing Analytics",
            "entity_id": entity_id,
            "summary": [
                {"label": "API keys", "value": "4"},
                {"label": "Open requests", "value": "1"},
                {"label": "Last API call", "value": "15 minutes ago"},
            ],
            "primary_panel_title": "API keys",
            "primary_panel_items": [
                {"title": "Key for /api/v1/users", "detail": "TTL: 30 days • Issued Jun 01, 2026"},
                {"title": "Key for /api/v1/billing", "detail": "TTL: 14 days • Issued Jun 08, 2026"},
                {"title": "Key for /api/v1/status", "detail": "TTL: 90 days • Issued May 21, 2026"},
            ],
            "secondary_panel_title": "Requests to producers",
            "secondary_panel_items": [
                {"title": "Access to billing API", "detail": "Reason: Monthly reporting • Status: Pending"},
                {"title": "Access to payments API", "detail": "Reason: Customer dashboards • Status: Approved"},
            ],
            "detail_sections": [
                {
                    "title": "Recent API activity",
                    "rows": [
                        ("Jun 15, 2026 09:30", "Called /api/v1/users from 10.18.2.44"),
                        ("Jun 15, 2026 09:18", "Called /api/v1/billing from 10.18.2.44"),
                        ("Jun 15, 2026 08:54", "Called /api/v1/status from 10.18.2.44"),
                    ],
                },
                {
                    "title": "Traffic notes",
                    "rows": [
                        ("Anomaly watch", "Traffic is within normal range"),
                        ("Payload size", "Average request size: 24 KB"),
                    ],
                },
            ],
        },
        "endpoint": {
            "title": "Endpoint Detail",
            "subtitle": "Overview of a published API endpoint and how it is used.",
            "badge": "Endpoint",
            "entity_name": "/api/v1/billing",
            "entity_id": entity_id,
            "summary": [
                {"label": "Consumers served", "value": "14"},
                {"label": "Health status", "value": "Healthy"},
                {"label": "Risk level", "value": "Medium"},
            ],
            "primary_panel_title": "Endpoint owner",
            "primary_panel_items": [
                {"title": "Payments Platform", "detail": "Owner of this endpoint"},
                {"title": "Service description", "detail": "Provides billing data for approved consumers"},
                {"title": "Current health", "detail": "Healthy with no active incidents"},
            ],
            "secondary_panel_title": "Configuration history",
            "secondary_panel_items": [
                {"title": "Jun 12, 2026", "detail": "Added response header logging"},
                {"title": "Jun 05, 2026", "detail": "Updated rate limit settings"},
            ],
            "detail_sections": [
                {
                    "title": "Usage summary",
                    "rows": [
                        ("Consumers", "14 active consumers"),
                        ("Last update", "Jun 12, 2026 at 14:20"),
                        ("Data risk", "Medium due to financial identifiers"),
                    ],
                },
                {
                    "title": "Recent API calls",
                    "rows": [
                        ("Jun 15, 2026 09:32", "Consumer Analytics called from 10.18.2.44"),
                        ("Jun 15, 2026 09:14", "Partner Reporting called from 10.18.2.58"),
                    ],
                },
            ],
        },
    }

    page_data = sample_data.get(entity_type)
    if not page_data:
        raise Http404("Unknown entity type")

    return render(
        request,
        "my_app/entity_detail.html",
        {
            "entity_type": entity_type,
            **page_data,
        },
    )
