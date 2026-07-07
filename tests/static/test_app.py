from pathlib import Path


def test_activity_renderer_contains_innerhtml_assignment():
    # Description: This test verifies the activity card renderer uses an innerHTML template assignment.

    # Arrange
    app_js_path = Path(__file__).resolve().parents[2] / "src" / "static" / "app.js"
    app_js_content = app_js_path.read_text(encoding="utf-8")

    # Act
    contains_renderer_assignment = "activityCard.innerHTML = `" in app_js_content

    # Assert
    assert contains_renderer_assignment


def test_activity_renderer_includes_filter_controls():
    # Description: This test verifies day and category filter controls remain wired.

    # Arrange
    app_js_path = Path(__file__).resolve().parents[2] / "src" / "static" / "app.js"
    app_js_content = app_js_path.read_text(encoding="utf-8")

    # Act
    has_category_filters = "const categoryFilters = document.querySelectorAll" in app_js_content
    has_day_filters = "const dayFilters = document.querySelectorAll" in app_js_content

    # Assert
    assert has_category_filters
    assert has_day_filters
