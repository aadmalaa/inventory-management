"""
Tests for purchase order API endpoints.
"""
import pytest

# Imported so tests can clean up in-memory purchase orders (no delete endpoint exists)
from mock_data import purchase_orders


@pytest.fixture
def po_cleanup():
    """Remove purchase orders created during a test from the in-memory store."""
    created_before = list(purchase_orders)
    yield
    purchase_orders[:] = created_before


class TestPurchaseOrderEndpoints:
    """Test suite for purchase-order-related endpoints."""

    def _valid_payload(self, client):
        """Build a valid create payload from a real backlog item without a PO."""
        backlog = client.get("/api/backlog").json()
        item = next(b for b in backlog if not b["has_purchase_order"])
        return {
            "backlog_item_id": item["id"],
            "supplier_name": "Pytest Supplier Co",
            "quantity": item["quantity_needed"] - item["quantity_available"],
            "unit_cost": 15.75,
            "expected_delivery_date": "2025-11-15",
            "notes": "Created by automated test"
        }

    def test_create_purchase_order(self, client, po_cleanup):
        """Test creating a purchase order for a backlog item."""
        payload = self._valid_payload(client)
        response = client.post("/api/purchase-orders", json=payload)
        assert response.status_code == 201

        po = response.json()
        assert po["backlog_item_id"] == payload["backlog_item_id"]
        assert po["supplier_name"] == payload["supplier_name"]
        assert po["quantity"] == payload["quantity"]
        assert abs(po["unit_cost"] - payload["unit_cost"]) < 0.01
        assert po["expected_delivery_date"] == payload["expected_delivery_date"]
        assert po["status"] == "Pending"
        assert po["id"].startswith("PO-")
        assert "created_date" in po

    def test_create_purchase_order_updates_backlog(self, client, po_cleanup):
        """Test that the backlog reflects a newly created purchase order."""
        payload = self._valid_payload(client)
        po = client.post("/api/purchase-orders", json=payload).json()

        backlog = client.get("/api/backlog").json()
        item = next(b for b in backlog if b["id"] == payload["backlog_item_id"])
        assert item["has_purchase_order"] is True
        assert item["purchase_order_id"] == po["id"]

    def test_create_duplicate_purchase_order(self, client, po_cleanup):
        """Test that a backlog item cannot get a second purchase order."""
        payload = self._valid_payload(client)
        first = client.post("/api/purchase-orders", json=payload)
        assert first.status_code == 201

        second = client.post("/api/purchase-orders", json=payload)
        assert second.status_code == 400
        assert "already has" in second.json()["detail"].lower()

    def test_create_purchase_order_invalid_backlog_item(self, client):
        """Test creating a purchase order for a nonexistent backlog item."""
        response = client.post("/api/purchase-orders", json={
            "backlog_item_id": "nonexistent-999",
            "supplier_name": "Nobody Inc",
            "quantity": 10,
            "unit_cost": 1.0,
            "expected_delivery_date": "2025-11-15"
        })
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    def test_create_purchase_order_missing_fields(self, client):
        """Test that creating a purchase order without required fields fails validation."""
        response = client.post("/api/purchase-orders", json={
            "backlog_item_id": "1"
        })
        assert response.status_code == 422

    def test_get_purchase_order_by_backlog_item(self, client, po_cleanup):
        """Test fetching a purchase order by its backlog item ID."""
        payload = self._valid_payload(client)
        created = client.post("/api/purchase-orders", json=payload).json()

        response = client.get(f"/api/purchase-orders/{payload['backlog_item_id']}")
        assert response.status_code == 200

        po = response.json()
        assert po["id"] == created["id"]
        assert po["backlog_item_id"] == payload["backlog_item_id"]

    def test_get_purchase_order_nonexistent_backlog_item(self, client):
        """Test fetching a purchase order for a backlog item that has none."""
        response = client.get("/api/purchase-orders/nonexistent-999")
        assert response.status_code == 404

        data = response.json()
        assert "detail" in data
        assert "no purchase order" in data["detail"].lower()
