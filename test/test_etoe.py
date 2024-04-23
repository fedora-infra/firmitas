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


from os import environ as envr
from os import makedirs, path
from secrets import token_hex
from shutil import copyfile, rmtree
from test import (
    list_etoe_auth,
    list_etoe_github,
    list_etoe_gitlab,
    list_etoe_nope,
    list_etoe_pagure,
)

import pytest
from click.testing import CliRunner

from firmitas.main import main


def locate_config(gitforge: str = "pagure") -> str:
    """
    Create a makeshift configuration file for specific testing purposes
    """

    namelist = [
        "dtfedmsg.stg.crt",
        "joystick.stg.crt",
        "mistaken.stg.crt",
        "nuancier.stg.crt",
        "robosign.stg.crt",
        "waiverdb.stg.crt"
    ]

    # Generate an unpredictably random hexadecimal
    # number for the temporary working directory
    secret_identity = token_hex(4)

    # Source
    base_location = f"{path.dirname(path.realpath(__name__))}"
    base_standard_location = f"{base_location}/firmitas/conf/standard.py"
    base_certlist_location = f"{base_location}/test/assets/certlist.yml"
    base_testcert_localist = [f"{base_location}/test/assets/certificates/{indx}" for indx in namelist]  # noqa : E501

    # Destination
    test_location = f"/var/tmp/firmitas-{secret_identity}"  # noqa : S108
    test_standard_location = f"{test_location}/myconfig.py"
    test_certlist_location = f"{test_location}/certlist.yml"
    test_testcert_localist = [f"{test_location}/certificates/{indx}" for indx in namelist]

    makedirs(f"{test_location}/certificates")

    # Copy over the standard configuration file to the temporary working directory
    # while making necessary changes to the standard configuration file
    with open(base_standard_location) as base_standard_file:
        test_standard_data = base_standard_file.read().replace(
            "/var/tmp/firmitas/certhere",  # noqa : S108
            f"{test_location}/certificates"
        ).replace(
            "/var/tmp/firmitas/certlist.yml",  # noqa : S108
            test_certlist_location
        ).replace(
            "gitforge = \"pagure\"", f"gitforge = \"{gitforge}\""
        )
    with open(test_standard_location, "w") as test_standard_file:
        test_standard_file.write(test_standard_data)

    # Copy over the certificate listing file to the temporary working directory
    # while making necessary changes to the certificate listing file
    copyfile(base_certlist_location, test_certlist_location)

    # Copy over the specific certificates required for the testing purposes from
    # the source location to the destination location
    for indx in range(len(base_testcert_localist)):
        copyfile(base_testcert_localist[indx], test_testcert_localist[indx])

    # Return the location of the newly created configuration file
    return test_standard_location


def locate_config_with_simulate_coming_expiry(daysqant: int = 2000, password: str = envr["FIRMITAS_TEST_PASSWORD"]) -> str:  # noqa : E501
    """
    Make specific changes to the standard configuration file to invoke a certain condition
    """

    test_standard_location = locate_config()
    with open(test_standard_location) as test_standard_file:
        test_standard_data = test_standard_file.read().replace(
            "daysqant = 30", f"daysqant = {daysqant}"
        ).replace(
            "username = \"\"", f"username = \"{envr['FIRMITAS_TEST_USERNAME']}\""
        ).replace(
            "password = \"\"", f"password = \"{password}\""
        ).replace(
            "reponame = \"\"", f"reponame = \"{envr['FIRMITAS_TEST_REPONAME']}\""
        )
    with open(test_standard_location, "w") as test_standard_file:
        test_standard_file.write(test_standard_data)
    return test_standard_location


@pytest.mark.vcr(filter_headers=["Authorization"])
@pytest.mark.parametrize(
    "cmdl, code, text",
    [
        pytest.param(
            f"--conffile {locate_config()}",
            0,
            list_etoe_pagure(),
            id = "Standard and mistaken certificates - Pagure",
        ),
        pytest.param(
            f"--conffile {locate_config('gitlab')}",
            1,
            list_etoe_gitlab(),
            id="Standard and mistaken certificates - GitLab",
        ),
        pytest.param(
            f"--conffile {locate_config('github')}",
            1,
            list_etoe_github(),
            id="Standard and mistaken certificates - GitHub",
        ),
        pytest.param(
            f"--conffile {locate_config_with_simulate_coming_expiry()}",
            0,
            list_etoe_auth(),
            id="Invoke notifications with accurate password",
        ),
        pytest.param(
            f"--conffile {locate_config_with_simulate_coming_expiry(password="MISTAKEN")}",  # noqa : S106
            0,
            list_etoe_nope(),
            id="Invoke notifications with mistaken password",
        )
    ]
)
def test_etoe(cmdl, code, text) -> None:
    runner = CliRunner()
    result = runner.invoke(main, cmdl)
    assert result.exit_code == code  # noqa: S101
    for indx in text:
        assert indx in result.output  # noqa: S101
    folder_location = cmdl.split(" ")[1].replace("/myconfig.py", "")
    rmtree(folder_location)
