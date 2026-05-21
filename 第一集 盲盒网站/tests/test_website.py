"""Unit tests for Blind Box Display website."""
from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path
from typing import Generator
from unittest.mock import MagicMock, patch

import pytest

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "Python" / "BlindBox"))

# Set up test database before importing app
TEST_DB_DIR = tempfile.mkdtemp()
TEST_DB_PATH = Path(TEST_DB_DIR) / "test_database.db"


def create_test_db(db_path: Path) -> None:
    """Create a test database with schema and test admin."""
    import sqlite3
    import bcrypt

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS BlindBox (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            price REAL,
            image_path TEXT,
            is_secret INTEGER DEFAULT 0,
            created_at DATETIME,
            updated_at DATETIME
        );
        CREATE TABLE IF NOT EXISTS Admin (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            created_at DATETIME
        );
    """)
    # Insert test admin (password is 'testpass' hashed with bcrypt)
    password_hash = bcrypt.hashpw("testpass".encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    cursor.execute(
        "INSERT INTO Admin (username, password, created_at) VALUES (?, ?, ?)",
        ("testadmin", password_hash, "2024-01-01T00:00:00"),
    )
    conn.commit()
    conn.close()


# Create the test database
create_test_db(TEST_DB_PATH)


@pytest.fixture
def clean_db():
    """Clean the test database before each test."""
    import sqlite3
    conn = sqlite3.connect(TEST_DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM BlindBox")
    conn.commit()
    conn.close()
    yield TEST_DB_PATH


@pytest.fixture
def app(clean_db):
    """Create Flask test application with mocked database path."""
    # Import init_db functions to patch
    import init_db

    # Save original
    original_get_connection = init_db.get_connection
    original_verify_admin = init_db.verify_admin

    # Patch DB_PATH
    with patch.object(init_db, 'DB_PATH', clean_db):
        # Reload the init_db module to pick up the patched path
        import importlib
        importlib.reload(init_db)

        # Now patch the functions in website module
        import website

        # Create a wrapper for get_connection that uses our test db
        original_conn = website.get_connection

        def mock_get_connection():
            import sqlite3
            conn = sqlite3.connect(clean_db)
            conn.execute("PRAGMA foreign_keys = 1")
            return conn

        website.get_connection = mock_get_connection

        # Store original and patch verify_admin
        original_verify = website.verify_admin

        def mock_verify_admin(username: str, password: str) -> bool:
            import sqlite3
            import bcrypt
            conn = sqlite3.connect(clean_db)
            cursor = conn.cursor()
            cursor.execute("SELECT password FROM Admin WHERE username = ?", (username,))
            row = cursor.fetchone()
            conn.close()
            if row is None:
                return False
            stored_hash = row[0]
            return bcrypt.checkpw(password.encode("utf-8"), stored_hash.encode("utf-8"))

        website.verify_admin = mock_verify_admin

        website.app.config["TESTING"] = True
        website.app.config["SECRET_KEY"] = "test-secret-key"

        yield website.app

        # Restore
        website.get_connection = original_conn
        website.verify_admin = original_verify


@pytest.fixture
def client(app):
    """Create Flask test client."""
    return app.test_client()


@pytest.fixture
def authenticated_client(client):
    """Create authenticated test client."""
    client.post(
        "/api/admin/login",
        json={"username": "testadmin", "password": "testpass"},
    )
    return client


class TestPublicAPI:
    """Test public API endpoints."""

    def test_get_boxes_empty(self, client, clean_db):
        """Test GET /api/boxes with no boxes."""
        response = client.get("/api/boxes")
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        assert len(data) == 0

    def test_get_boxes_with_data(self, authenticated_client, clean_db):
        """Test GET /api/boxes with existing boxes."""
        # Create a box first
        authenticated_client.post(
            "/api/boxes",
            json={"name": "Test Box", "price": 99.99},
        )
        response = authenticated_client.get("/api/boxes")
        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 1
        assert data[0]["name"] == "Test Box"

    def test_get_box_not_found(self, client, clean_db):
        """Test GET /api/boxes/<id> with non-existent id."""
        response = client.get("/api/boxes/9999")
        assert response.status_code == 404
        data = response.get_json()
        assert "error" in data

    def test_get_box_success(self, authenticated_client, clean_db):
        """Test GET /api/boxes/<id> with valid id."""
        # Create a box first
        create_response = authenticated_client.post(
            "/api/boxes",
            json={"name": "Test Box", "price": 50.0},
        )
        box_id = create_response.get_json()["box"]["id"]

        response = authenticated_client.get(f"/api/boxes/{box_id}")
        assert response.status_code == 200
        data = response.get_json()
        assert data["name"] == "Test Box"
        assert data["price"] == 50.0


class TestAdminAPI:
    """Test admin API endpoints."""

    def test_login_success(self, client, clean_db):
        """Test successful login."""
        response = client.post(
            "/api/admin/login",
            json={"username": "testadmin", "password": "testpass"},
        )
        assert response.status_code == 200
        data = response.get_json()
        assert data["success"] is True

    def test_login_invalid_credentials(self, client, clean_db):
        """Test login with invalid credentials."""
        response = client.post(
            "/api/admin/login",
            json={"username": "testadmin", "password": "wrongpass"},
        )
        assert response.status_code == 401
        data = response.get_json()
        assert data["success"] is False

    def test_login_missing_credentials(self, client, clean_db):
        """Test login with missing credentials."""
        response = client.post(
            "/api/admin/login",
            json={"username": "", "password": ""},
        )
        assert response.status_code == 400
        data = response.get_json()
        assert data["success"] is False

    def test_logout(self, authenticated_client, clean_db):
        """Test logout."""
        response = authenticated_client.post("/api/admin/logout")
        assert response.status_code == 200
        data = response.get_json()
        assert data["success"] is True

    def test_create_box_unauthorized(self, client, clean_db):
        """Test creating box without authentication."""
        response = client.post(
            "/api/boxes",
            json={"name": "Test Box"},
        )
        assert response.status_code == 401

    def test_create_box_success(self, authenticated_client, clean_db):
        """Test creating box with authentication."""
        response = authenticated_client.post(
            "/api/boxes",
            json={
                "name": "New Box",
                "description": "A test box",
                "price": 29.99,
                "is_secret": False,
            },
        )
        assert response.status_code == 201
        data = response.get_json()
        assert "box" in data
        assert data["box"]["name"] == "New Box"

    def test_create_box_missing_name(self, authenticated_client, clean_db):
        """Test creating box without name."""
        response = authenticated_client.post(
            "/api/boxes",
            json={"description": "No name box"},
        )
        assert response.status_code == 400

    def test_update_box_success(self, authenticated_client, clean_db):
        """Test updating a box."""
        # Create a box first
        create_response = authenticated_client.post(
            "/api/boxes",
            json={"name": "Original Name", "price": 10.0},
        )
        box_id = create_response.get_json()["box"]["id"]

        # Update the box
        response = authenticated_client.put(
            f"/api/boxes/{box_id}",
            json={"name": "Updated Name", "price": 20.0},
        )
        assert response.status_code == 200
        data = response.get_json()
        assert data["box"]["name"] == "Updated Name"
        assert data["box"]["price"] == 20.0

    def test_update_box_not_found(self, authenticated_client, clean_db):
        """Test updating non-existent box."""
        response = authenticated_client.put(
            "/api/boxes/9999",
            json={"name": "Test"},
        )
        assert response.status_code == 404

    def test_delete_box_success(self, authenticated_client, clean_db):
        """Test deleting a box."""
        # Create a box first
        create_response = authenticated_client.post(
            "/api/boxes",
            json={"name": "To Delete", "price": 5.0},
        )
        box_id = create_response.get_json()["box"]["id"]

        # Delete the box
        response = authenticated_client.delete(f"/api/boxes/{box_id}")
        assert response.status_code == 200
        data = response.get_json()
        assert data["success"] is True

    def test_delete_box_not_found(self, authenticated_client, clean_db):
        """Test deleting non-existent box."""
        response = authenticated_client.delete("/api/boxes/9999")
        assert response.status_code == 404


class TestPageRoutes:
    """Test page routes."""

    def test_index_page(self, client, clean_db):
        """Test index page renders."""
        response = client.get("/")
        assert response.status_code == 200

    def test_detail_page(self, client, clean_db):
        """Test detail page renders."""
        response = client.get("/box/1")
        assert response.status_code == 200

    def test_admin_login_page(self, client, clean_db):
        """Test admin login page renders."""
        response = client.get("/admin/login")
        assert response.status_code == 200

    def test_admin_dashboard_unauthenticated(self, client, clean_db):
        """Test admin dashboard redirects when not authenticated."""
        response = client.get("/admin")
        assert response.status_code == 302  # Redirect to login

    def test_admin_dashboard_authenticated(self, authenticated_client, clean_db):
        """Test admin dashboard renders when authenticated."""
        response = authenticated_client.get("/admin")
        assert response.status_code == 200

    def test_admin_boxes_unauthenticated(self, client, clean_db):
        """Test admin boxes page redirects when not authenticated."""
        response = client.get("/admin/boxes")
        assert response.status_code == 302

    def test_admin_boxes_authenticated(self, authenticated_client, clean_db):
        """Test admin boxes page renders when authenticated."""
        response = authenticated_client.get("/admin/boxes")
        assert response.status_code == 200

    def test_admin_boxes_new_unauthenticated(self, client, clean_db):
        """Test admin new box page redirects when not authenticated."""
        response = client.get("/admin/boxes/new")
        assert response.status_code == 302

    def test_admin_boxes_new_authenticated(self, authenticated_client, clean_db):
        """Test admin new box page renders when authenticated."""
        response = authenticated_client.get("/admin/boxes/new")
        assert response.status_code == 200

    def test_admin_boxes_edit_unauthenticated(self, client, clean_db):
        """Test admin edit box page redirects when not authenticated."""
        response = client.get("/admin/boxes/1/edit")
        assert response.status_code == 302

    def test_admin_boxes_edit_not_found(self, authenticated_client, clean_db):
        """Test admin edit page with non-existent box."""
        response = authenticated_client.get("/admin/boxes/9999/edit")
        assert response.status_code == 404

    def test_admin_boxes_edit_success(self, authenticated_client, clean_db):
        """Test admin edit page with existing box."""
        # Create a box first
        create_response = authenticated_client.post(
            "/api/boxes",
            json={"name": "Test Box", "price": 10.0},
        )
        box_id = create_response.get_json()["box"]["id"]

        response = authenticated_client.get(f"/admin/boxes/{box_id}/edit")
        assert response.status_code == 200


class TestImageUpload:
    """Test image upload functionality."""

    def test_upload_unauthorized(self, client, clean_db):
        """Test upload without authentication."""
        response = client.post("/api/upload")
        assert response.status_code == 401

    def test_upload_no_file(self, authenticated_client, clean_db):
        """Test upload without file."""
        response = authenticated_client.post("/api/upload")
        assert response.status_code == 400

    def test_upload_invalid_file_type(self, authenticated_client, clean_db):
        """Test upload with invalid file type."""
        data = {"file": (b"test content", "test.txt")}
        response = authenticated_client.post(
            "/api/upload",
            data=data,
            content_type="multipart/form-data",
        )
        assert response.status_code == 400


if __name__ == "__main__":
    pytest.main([__file__, "-v"])