"""Flask web application for Blind Box Display website."""
from __future__ import annotations

import os
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any

from flask import (
    Flask,
    abort,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.utils import secure_filename

# Database module path
import sys
sys.path.insert(0, str(Path(__file__).parent))

from init_db import get_connection, verify_admin  # noqa: E402

# Application configuration
BASE_DIR = Path(__file__).parent.parent.parent
app = Flask(__name__, template_folder=str(BASE_DIR / "templates"), static_folder=str(BASE_DIR / "static"))
app.secret_key = os.environ.get("SECRET_KEY", "blind-box-secret-key-change-in-production")
UPLOAD_FOLDER = BASE_DIR / "uploads"
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}
MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5MB

app.config["UPLOAD_FOLDER"] = str(UPLOAD_FOLDER)
app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH


def allowed_file(filename: str) -> bool:
    """Check if file has an allowed extension."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def login_required() -> bool:
    """Check if user is logged in via session."""
    return "admin_id" in session


# ============================================================================
# Public APIs
# ============================================================================


@app.route("/api/boxes", methods=["GET"])
def get_boxes() -> tuple[Any, int]:
    """Return list of all blind boxes as JSON."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, name, description, price, image_path, is_secret, created_at, updated_at FROM BlindBox ORDER BY created_at DESC"
    )
    rows = cursor.fetchall()
    conn.close()

    boxes = []
    for row in rows:
        boxes.append({
            "id": row[0],
            "name": row[1],
            "description": row[2],
            "price": row[3],
            "image_path": row[4],
            "is_secret": bool(row[5]),
            "created_at": row[6],
            "updated_at": row[7],
        })
    return jsonify(boxes), 200


@app.route("/api/boxes/<int:box_id>", methods=["GET"])
def get_box(box_id: int) -> tuple[Any, int]:
    """Return single blind box details as JSON."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, name, description, price, image_path, is_secret, created_at, updated_at FROM BlindBox WHERE id = ?",
        (box_id,),
    )
    row = cursor.fetchone()
    conn.close()

    if row is None:
        return jsonify({"error": "Box not found"}), 404

    box = {
        "id": row[0],
        "name": row[1],
        "description": row[2],
        "price": row[3],
        "image_path": row[4],
        "is_secret": bool(row[5]),
        "created_at": row[6],
        "updated_at": row[7],
    }
    return jsonify(box), 200


# ============================================================================
# Admin APIs
# ============================================================================


@app.route("/api/admin/login", methods=["POST"])
def admin_login() -> tuple[Any, int]:
    """Login with username/password, returns {success: bool}."""
    data = request.get_json() or {}
    username = data.get("username", "")
    password = data.get("password", "")

    if not username or not password:
        return jsonify({"success": False, "error": "Missing credentials"}), 400

    if verify_admin(username, password):
        session["admin_id"] = username
        return jsonify({"success": True}), 200
    return jsonify({"success": False, "error": "Invalid credentials"}), 401


@app.route("/api/admin/logout", methods=["POST"])
def admin_logout() -> tuple[Any, int]:
    """Logout, returns {success: bool}."""
    session.pop("admin_id", None)
    return jsonify({"success": True}), 200


@app.route("/api/admin/check", methods=["GET"])
def admin_check() -> tuple[Any, int]:
    """Check if user is logged in, returns {logged_in: bool}."""
    return jsonify({"logged_in": login_required()}), 200


@app.route("/api/boxes", methods=["POST"])
def create_box() -> tuple[Any, int]:
    """Create new blind box, returns {box: {...}}."""
    if not login_required():
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json() or {}
    name = data.get("name", "")
    description = data.get("description", "")
    price = data.get("price", 0.0)
    image_path = data.get("image_path", "")
    is_secret = bool(data.get("is_secret", False))

    if not name:
        return jsonify({"error": "Name is required"}), 400

    now = datetime.now().isoformat()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO BlindBox (name, description, price, image_path, is_secret, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (name, description, price, image_path, int(is_secret), now, now),
    )
    box_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return jsonify({
        "box": {
            "id": box_id,
            "name": name,
            "description": description,
            "price": price,
            "image_path": image_path,
            "is_secret": is_secret,
            "created_at": now,
            "updated_at": now,
        }
    }), 201


@app.route("/api/boxes/<int:box_id>", methods=["PUT"])
def update_box(box_id: int) -> tuple[Any, int]:
    """Update blind box, returns {box: {...}}."""
    if not login_required():
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json() or {}
    name = data.get("name", "")
    description = data.get("description", "")
    price = data.get("price", 0.0)
    image_path = data.get("image_path", "")
    is_secret = bool(data.get("is_secret", False))

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM BlindBox WHERE id = ?", (box_id,))
    if cursor.fetchone() is None:
        conn.close()
        return jsonify({"error": "Box not found"}), 404

    now = datetime.now().isoformat()
    cursor.execute(
        "UPDATE BlindBox SET name = ?, description = ?, price = ?, image_path = ?, is_secret = ?, updated_at = ? WHERE id = ?",
        (name, description, price, image_path, int(is_secret), now, box_id),
    )
    conn.commit()

    cursor.execute(
        "SELECT id, name, description, price, image_path, is_secret, created_at, updated_at FROM BlindBox WHERE id = ?",
        (box_id,),
    )
    row = cursor.fetchone()
    conn.close()

    if row is None:
        return jsonify({"error": "Box not found"}), 404

    box = {
        "id": row[0],
        "name": row[1],
        "description": row[2],
        "price": row[3],
        "image_path": row[4],
        "is_secret": bool(row[5]),
        "created_at": row[6],
        "updated_at": row[7],
    }
    return jsonify({"box": box}), 200


@app.route("/api/boxes/<int:box_id>", methods=["DELETE"])
def delete_box(box_id: int) -> tuple[Any, int]:
    """Delete blind box, returns {success: bool}."""
    if not login_required():
        return jsonify({"error": "Unauthorized"}), 401

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM BlindBox WHERE id = ?", (box_id,))
    if cursor.fetchone() is None:
        conn.close()
        return jsonify({"success": False, "error": "Box not found"}), 404

    cursor.execute("DELETE FROM BlindBox WHERE id = ?", (box_id,))
    conn.commit()
    conn.close()
    return jsonify({"success": True}), 200


@app.route("/api/upload", methods=["POST"])
def upload_image() -> tuple[Any, int]:
    """Upload image file, returns {image_path: string}."""
    if not login_required():
        return jsonify({"error": "Unauthorized"}), 401

    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    if not allowed_file(file.filename or ""):
        return jsonify({"error": "Invalid file type. Only images are allowed."}), 400

    filename = secure_filename(file.filename or "")
    ext = filename.rsplit(".", 1)[1].lower() if "." in filename else ""
    unique_filename = f"{uuid.uuid4().hex}.{ext}"
    file_path = UPLOAD_FOLDER / unique_filename
    file.save(str(file_path))

    image_path = f"/uploads/{unique_filename}"
    return jsonify({"image_path": image_path}), 200


# ============================================================================
# Page Routes
# ============================================================================


@app.route("/", methods=["GET"])
def index() -> str:
    """Render前台首页 (index.html template)."""
    return render_template("index.html")


@app.route("/box/<int:box_id>", methods=["GET"])
def detail(box_id: int) -> str:
    """Render盲盒详情页 (detail.html template)."""
    return render_template("detail.html", box_id=box_id)


@app.route("/admin/login", methods=["GET"])
def admin_login_page() -> str:
    """Render登录页 (admin/login.html template)."""
    return render_template("admin/login.html")


@app.route("/admin", methods=["GET"])
def admin_dashboard() -> Any:
    """Render管理首页 (admin/dashboard.html template)."""
    if not login_required():
        return redirect(url_for("admin_login_page"))
    return render_template("admin/dashboard.html")


@app.route("/admin/boxes", methods=["GET"])
def admin_boxes() -> Any:
    """Render盲盒列表页 (admin/list.html template)."""
    if not login_required():
        return redirect(url_for("admin_login_page"))
    return render_template("admin/list.html")


@app.route("/admin/boxes/new", methods=["GET"])
def admin_boxes_new() -> Any:
    """Render新增页 (admin/form.html template)."""
    if not login_required():
        return redirect(url_for("admin_login_page"))
    return render_template("admin/form.html", box=None)


@app.route("/admin/boxes/<int:box_id>/edit", methods=["GET"])
def admin_boxes_edit(box_id: int) -> Any:
    """Render编辑页 (admin/form.html template)."""
    if not login_required():
        return redirect(url_for("admin_login_page"))

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, name, description, price, image_path, is_secret, created_at, updated_at FROM BlindBox WHERE id = ?",
        (box_id,),
    )
    row = cursor.fetchone()
    conn.close()

    if row is None:
        abort(404)

    box = {
        "id": row[0],
        "name": row[1],
        "description": row[2],
        "price": row[3],
        "image_path": row[4],
        "is_secret": bool(row[5]),
        "created_at": row[6],
        "updated_at": row[7],
    }
    return render_template("admin/form.html", box=box)


# ============================================================================
# Static files
# ============================================================================


@app.route("/uploads/<path:filename>", methods=["GET"])
def uploaded_file(filename: str) -> Any:
    """Serve uploaded files."""
    from flask import send_from_directory
    return send_from_directory(UPLOAD_FOLDER, filename)


# ============================================================================
# Error handlers
# ============================================================================


@app.errorhandler(413)
def request_entity_too_large(error: Any) -> tuple[Any, int]:
    """Handle file too large error."""
    return jsonify({"error": "File too large. Maximum size is 5MB."}), 413


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)