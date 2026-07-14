"""
Tests for tasks API endpoints.
"""
import pytest


class TestTasksEndpoints:
    """Test suite for task-related endpoints."""

    def test_get_all_tasks(self, client):
        """Test getting all tasks."""
        response = client.get("/api/tasks")
        assert response.status_code == 200

        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0

        first_task = data[0]
        assert "id" in first_task
        assert "title" in first_task
        assert "priority" in first_task
        assert "dueDate" in first_task
        assert "status" in first_task

    def test_task_field_types(self, client):
        """Test that task fields have proper types and values."""
        response = client.get("/api/tasks")
        data = response.json()

        valid_priorities = ["high", "medium", "low"]
        valid_statuses = ["pending", "completed"]

        for task in data:
            assert isinstance(task["id"], int)
            assert isinstance(task["title"], str)
            assert task["priority"].lower() in valid_priorities
            assert task["status"].lower() in valid_statuses
            # Due dates are ISO format (YYYY-MM-DD)
            assert "-" in task["dueDate"]

    def test_create_task(self, client):
        """Test creating a new task."""
        payload = {
            "title": "Test task from pytest",
            "priority": "high",
            "dueDate": "2025-11-01"
        }
        response = client.post("/api/tasks", json=payload)
        assert response.status_code == 201

        task = response.json()
        try:
            assert task["title"] == payload["title"]
            assert task["priority"] == payload["priority"]
            assert task["dueDate"] == payload["dueDate"]
            assert task["status"] == "pending"
            # API task IDs stay above 100 to avoid colliding with client-side mock tasks
            assert task["id"] > 100

            # Task should now appear in the list
            all_tasks = client.get("/api/tasks").json()
            assert any(t["id"] == task["id"] for t in all_tasks)
        finally:
            # Clean up so other tests see the original state
            client.delete(f"/api/tasks/{task['id']}")

    def test_create_task_default_priority(self, client):
        """Test that priority defaults to medium when omitted."""
        payload = {"title": "Task without priority", "dueDate": "2025-11-02"}
        response = client.post("/api/tasks", json=payload)
        assert response.status_code == 201

        task = response.json()
        try:
            assert task["priority"] == "medium"
        finally:
            client.delete(f"/api/tasks/{task['id']}")

    def test_create_task_missing_fields(self, client):
        """Test that creating a task without required fields fails validation."""
        response = client.post("/api/tasks", json={"priority": "high"})
        assert response.status_code == 422

    def test_toggle_task(self, client):
        """Test toggling a task between pending and completed."""
        created = client.post("/api/tasks", json={
            "title": "Toggle me",
            "priority": "low",
            "dueDate": "2025-11-03"
        }).json()
        task_id = created["id"]

        try:
            # pending -> completed
            response = client.patch(f"/api/tasks/{task_id}")
            assert response.status_code == 200
            assert response.json()["status"] == "completed"

            # completed -> pending
            response = client.patch(f"/api/tasks/{task_id}")
            assert response.status_code == 200
            assert response.json()["status"] == "pending"
        finally:
            client.delete(f"/api/tasks/{task_id}")

    def test_toggle_nonexistent_task(self, client):
        """Test toggling a task that doesn't exist."""
        response = client.patch("/api/tasks/999999")
        assert response.status_code == 404

        data = response.json()
        assert "detail" in data
        assert "not found" in data["detail"].lower()

    def test_delete_task(self, client):
        """Test deleting a task."""
        created = client.post("/api/tasks", json={
            "title": "Delete me",
            "priority": "medium",
            "dueDate": "2025-11-04"
        }).json()
        task_id = created["id"]

        response = client.delete(f"/api/tasks/{task_id}")
        assert response.status_code == 200
        assert response.json()["id"] == task_id

        # Task should no longer appear in the list
        all_tasks = client.get("/api/tasks").json()
        assert not any(t["id"] == task_id for t in all_tasks)

    def test_delete_nonexistent_task(self, client):
        """Test deleting a task that doesn't exist."""
        response = client.delete("/api/tasks/999999")
        assert response.status_code == 404

        data = response.json()
        assert "detail" in data
        assert "not found" in data["detail"].lower()
