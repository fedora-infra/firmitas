"""
Firmitas
Copyright (C) 2023-2024 Akashdeep Dhar

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
details.

You should have received a copy of the GNU General Public License along with
this program.  If not, see <https://www.gnu.org/licenses/>.

Any Red Hat trademarks that are incorporated in the source code or
documentation are not subject to the GNU General Public License and may only
be used or replicated with the express permission of Red Hat, Inc.
"""


from unittest.mock import Mock

import pytest
import responses
from requests import post as original_post

from firmitas.unit import forgejo
from test import FORGEJO_TEST_LOCATION, FORGEJO_TEST_REPOPATH


@pytest.mark.parametrize(
    "expt",
    [
        pytest.param(
            Exception,
            id="Generic exception",
        ),
        pytest.param(
            ConnectionError,
            id="Connection timeout",
        ),
    ]
)
def test_forgejo_server_defeat(expt):
    forgejo.post = Mock()
    forgejo.post.side_effect = expt()
    assert (False, "", "") == forgejo.makenote(0, "", "", "", 0, 0, "", "", "", "")  # noqa : S101
    forgejo.post = original_post


@responses.activate
def test_forgejo_make_success():
    responses.add(
        responses.POST,
        f"{FORGEJO_TEST_LOCATION}/api/v1/repos/{FORGEJO_TEST_REPOPATH}/issues",
        json={
            "id": 42,
            "html_url": f"{FORGEJO_TEST_LOCATION}/{FORGEJO_TEST_REPOPATH}/issues/42",
            "created_at": "2024-01-01T00:00:00Z",
        },
        status=201,
    )
    forgejo.standard.repoloca = FORGEJO_TEST_LOCATION
    forgejo.standard.reponame = FORGEJO_TEST_REPOPATH
    forgejo.standard.password = "test_password"  # noqa : S105
    forgejo.standard.tagslist = []
    forgejo.standard.maxretry = 1
    result = forgejo.makenote(0, "test_serv", "", "", 0, 0, "", "", "", "test_user")
    assert result == (  # noqa : S101
        True,
        f"{FORGEJO_TEST_LOCATION}/{FORGEJO_TEST_REPOPATH}/issues/42",
        "2024-01-01T00:00:00Z",
    )


@responses.activate
def test_forgejo_auth_failure():
    responses.add(
        responses.POST,
        f"{FORGEJO_TEST_LOCATION}/api/v1/repos/{FORGEJO_TEST_REPOPATH}/issues",
        json={"message": "Unauthorized"},
        status=401,
    )
    forgejo.standard.repoloca = FORGEJO_TEST_LOCATION
    forgejo.standard.reponame = FORGEJO_TEST_REPOPATH
    forgejo.standard.password = "badtoken"  # noqa : S105
    forgejo.standard.tagslist = []
    forgejo.standard.maxretry = 1
    result = forgejo.makenote(0, "test_serv", "", "", 0, 0, "", "", "", "test_user")
    assert result == (False, "", "")  # noqa : S101
