"""Hosted initialization must never serve requests with database-owner access."""
from types import SimpleNamespace
from unittest.mock import patch

import pytest
from sqlalchemy.engine import make_url

from app.hosted_start import main


OWNER = "postgresql://owner:encoded%40password@db.example/janvastu?sslmode=require"


def test_hosted_start_uses_restricted_role_and_redacts_output(capsys):
    environment = {
        "JANVASTU_OWNER_DATABASE_URL": OWNER,
        "SECRET_KEY": "test-only-secret-" * 4,
        "PORT": "10000",
    }
    with patch.dict("os.environ", environment, clear=True), patch(
        "app.hosted_start.subprocess.run",
        return_value=SimpleNamespace(returncode=0, stdout=OWNER, stderr="encoded@password"),
    ) as run, patch("app.hosted_start.os.execvpe") as execute:
        main()
    assert [call.args[0][2] for call in run.call_args_list] == [
        "alembic", "app.db.provision", "app.db.seed"
    ]
    setup = run.call_args.kwargs["env"]
    runtime = execute.call_args.args[2]
    assert "JANVASTU_OWNER_DATABASE_URL" not in runtime
    assert "RUNTIME_DB_PASSWORD" not in runtime
    url = make_url(runtime["DATABASE_URL"])
    assert url.username == "janvastu_api"
    assert url.password == setup["RUNTIME_DB_PASSWORD"]
    assert len(url.password) == 64
    assert url.query["sslmode"] == "require"
    assert execute.call_args.args[1][-1] == "10000"
    output = capsys.readouterr().out
    assert OWNER not in output and "encoded@password" not in output


def test_failed_initialization_never_launches_server():
    with patch.dict("os.environ", {
        "JANVASTU_OWNER_DATABASE_URL": OWNER,
        "SECRET_KEY": "test-only-secret-" * 4,
    }, clear=True), patch("app.hosted_start.subprocess.run", return_value=SimpleNamespace(
        returncode=1, stdout="", stderr="migration failed"
    )) as run, patch("app.hosted_start.os.execvpe") as execute:
        with pytest.raises(SystemExit, match="initialization failed"):
            main()
    assert run.call_count == 1
    execute.assert_not_called()


def test_hosted_initialization_rejects_development_secret():
    with patch.dict("os.environ", {
        "JANVASTU_OWNER_DATABASE_URL": OWNER,
        "SECRET_KEY": "development-" + "x" * 40,
    }, clear=True), patch("app.hosted_start.subprocess.run") as run:
        with pytest.raises(SystemExit, match="generated SECRET_KEY"):
            main()
    run.assert_not_called()


def test_existing_runtime_url_needs_no_owner():
    with patch.dict("os.environ", {"DATABASE_URL": OWNER}, clear=True), patch(
        "app.hosted_start.subprocess.run"
    ) as run, patch("app.hosted_start.os.execvpe") as execute:
        main()
    run.assert_not_called()
    assert execute.call_args.args[2]["DATABASE_URL"] == OWNER
