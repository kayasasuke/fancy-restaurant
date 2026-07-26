import os
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def run_production_command(*command, **environment):
    child_environment = os.environ.copy()
    for key in ("ALLOWED_HOSTS", "DATABASE_URL", "DEBUG", "SECRET_KEY"):
        child_environment.pop(key, None)
    child_environment.update(environment)
    return subprocess.run(
        [sys.executable, *command],
        cwd=PROJECT_ROOT,
        check=False,
        capture_output=True,
        env=child_environment,
        text=True,
    )


def run_production_check(**environment):
    return run_production_command("manage.py", "check", **environment)


def test_production_settings_require_secret_key():
    result = run_production_check(DEBUG="false", ALLOWED_HOSTS="example.com")

    assert result.returncode != 0
    assert "SECRET_KEY must be set when DEBUG is false." in result.stderr


def test_production_settings_accept_environment_configuration():
    result = run_production_check(
        DEBUG="false",
        ALLOWED_HOSTS="example.com",
        SECRET_KEY="test-production-secret-key-0123456789-abcdefghijklmnopqrstuvwxyz",
    )

    assert result.returncode == 0


def test_render_can_disable_django_https_redirect():
    result = run_production_command(
        "manage.py",
        "shell",
        "-c",
        "from django.conf import settings; print(settings.SECURE_SSL_REDIRECT)",
        DEBUG="false",
        ALLOWED_HOSTS="example.com",
        SECRET_KEY="test-production-secret-key-0123456789-abcdefghijklmnopqrstuvwxyz",
        SECURE_SSL_REDIRECT="false",
    )

    assert result.returncode == 0
    assert "False" in result.stdout


def test_production_settings_accept_postgresql_database_url():
    result = run_production_command(
        "manage.py",
        "shell",
        "-c",
        "from django.conf import settings; print(settings.DATABASES['default']['ENGINE'])",
        DEBUG="false",
        ALLOWED_HOSTS="example.com",
        DATABASE_URL="postgresql://user:password@db.example.com:5432/fancy_restaurant",
        SECRET_KEY="test-production-secret-key-0123456789-abcdefghijklmnopqrstuvwxyz",
    )

    assert result.returncode == 0
    assert "django.db.backends.postgresql" in result.stdout


def test_production_collectstatic_writes_manifest(tmp_path):
    result = run_production_command(
        "manage.py",
        "collectstatic",
        "--noinput",
        DEBUG="false",
        ALLOWED_HOSTS="example.com",
        SECRET_KEY="test-production-secret-key-0123456789-abcdefghijklmnopqrstuvwxyz",
        STATIC_ROOT=str(tmp_path),
    )

    assert result.returncode == 0
    assert (tmp_path / "staticfiles.json").exists()
    assert (tmp_path / "FancyRestaurantApp" / "style.css").exists()
