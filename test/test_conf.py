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


from os import makedirs, path
from secrets import token_hex
from shutil import rmtree

import pytest
from click.testing import CliRunner

from firmitas.main import main


def locate_config() -> str:
    """
    Create a makeshift configuration file for specific testing purposes
    """

    # Generate an unpredictably random hexadecimal
    # number for the temporary working directory
    secret_identity = token_hex(4)
    existing_config_location = f"{path.dirname(path.realpath(__name__))}/firmitas/conf"
    workable_config_location = f"/var/tmp/firmitas-{secret_identity}"  # noqa : S108
    makedirs(f"{workable_config_location}/certificates")

    # Copy over the standard configuration file to the temporary working directory
    # while making necessary changes to the standard configuration file
    with open(f"{existing_config_location}/standard.py") as standard_config_file:
        standard_config_data = standard_config_file.read().replace(
            "/var/tmp/firmitas/certhere",  # noqa : S108
            f"{workable_config_location}/certificates"
        ).replace(
            "/var/tmp/firmitas/certlist.yml",  # noqa : S108
            f"{workable_config_location}/certlist.yml"
        )
    with open(f"{workable_config_location}/myconfig.py", "w") as myconfig_config_file:
        myconfig_config_file.write(standard_config_data)

    # Copy over the certificate listing file to the temporary working directory
    # while making necessary changes to the certificate listing file
    with open(f"{existing_config_location}/certlist.yml") as standard_certlist_file:
        standard_certlist_data = standard_certlist_file.read()
    with open(f"{workable_config_location}/certlist.yml", "w") as myconfig_certlist_file:
        myconfig_certlist_file.write(standard_certlist_data)

    # Return the location of the newly created configuration file
    return f"{workable_config_location}/myconfig.py"


def locate_config_gitforge() -> str:
    """
    Make specific changes to the standard configuration file to invoke a certain condition

    POSITION - Set a disallowed Git Forge type as the value for the Git Forge variable
    EXPECTED - Exception related to the allowed and disallowed Git Forge types
    """

    workable_config_location = locate_config()
    with open(workable_config_location) as myconfig_config_file:
        myconfig_config_data = myconfig_config_file.read()
    with open(workable_config_location, "w") as myconfig_config_file:
        myconfig_config_file.write(
            myconfig_config_data.replace("gitforge = \"pagure\"", "gitforge = \"gogs\"")
        )
    return workable_config_location


def locate_config_strgdate() -> str:
    """
    Make specific changes to the standard configuration file to invoke a certain condition

    POSITION - Set a string data as the value for the alert duration variable
    EXPECTED - Exception related to the data types allowed for the alert duration variable
    """

    workable_config_location = locate_config()
    with open(workable_config_location) as myconfig_config_file:
        myconfig_config_data = myconfig_config_file.read()
    with open(workable_config_location, "w") as myconfig_config_file:
        myconfig_config_file.write(
            myconfig_config_data.replace("daysqant = 30", "daysqant = \"THIRTY\"")
        )
    return workable_config_location


def locate_config_negative() -> str:
    """
    Make specific changes to the standard configuration file to invoke a certain condition

    POSITION - Set a negative number as the value for the alert duration variable
    EXPECTED - Exception related to the data types allowed for the alert duration variable
    """

    workable_config_location = locate_config()
    with open(workable_config_location) as myconfig_config_file:
        myconfig_config_data = myconfig_config_file.read()
    with open(workable_config_location, "w") as myconfig_config_file:
        myconfig_config_file.write(
            myconfig_config_data.replace("daysqant = 30", "daysqant = -30")
        )
    return workable_config_location


def locate_config_location() -> str:
    """
    Make specific changes to the standard configuration file to invoke a certain condition

    POSITION - Point towards a certificate directory that does not exist
    EXPECTED - Exception related to certificate directory not being read
    """

    workable_config_location = locate_config()
    with open(workable_config_location) as myconfig_config_file:
        myconfig_config_data = myconfig_config_file.read()
    with open(workable_config_location, "w") as myconfig_config_file:
        myconfig_config_file.write(
            myconfig_config_data.replace(
                f"{workable_config_location.replace('/myconfig.py', '')}/certificates",
                f"{workable_config_location.replace('/myconfig.py', '')}/ZEROEXISTENT"
            )
        )
    return workable_config_location


def locate_config_hostname() -> str:
    """
    Make specific changes to the standard configuration file to invoke a certain condition

    POSITION - Point towards a certificate listing file that does not exist
    EXPECTED - Exception related to certificate listing file not being read
    """

    workable_config_location = locate_config()
    with open(workable_config_location) as myconfig_config_file:
        myconfig_config_data = myconfig_config_file.read()
    with open(workable_config_location, "w") as myconfig_config_file:
        myconfig_config_file.write(
            myconfig_config_data.replace(
                f"{workable_config_location.replace('/myconfig.py', '')}/certlist.yml",
                f"{workable_config_location.replace('/myconfig.py', '')}/ZEROEXISTENT.yml"
            )
        )
    return workable_config_location


@pytest.mark.parametrize(
    "cmdl, code, text",
    [
        pytest.param(
            f"--conffile {locate_config()}",
            0,
            [
                "[INFO] Probing into the configured directory",
                "[INFO] Validating",
                "X.509-standard TLS certificate(s)",
                "[INFO] Of",
                "TLS certificate(s),",
                "TLS certificate(s) were read successfully while",
                "TLS certificate(s) could not be read",
            ],
            id="Configuration - Standard",
        ),
        pytest.param(
            f"--conffile {locate_config_gitforge()}",
            1,
            [
                "[ERROR] The specified ticketing repository",
                "forge is not yet supported",
            ],
            id="Configuration - Invalid ticketing repository",
        ),
        pytest.param(
            f"--conffile {locate_config_strgdate()}",
            1,
            [
                "[ERROR] The variable 'daysqant' must have",
                "a value of the integer data type only",
            ],
            id="Configuration - Invalid data type",
        ),
        pytest.param(
            f"--conffile {locate_config_negative()}",
            1,
            [
                "[ERROR] The variable 'daysqant' must have",
                "a non-zero positive integer value",
            ],
            id="Configuration - Negative integer",
        ),
        pytest.param(
            f"--conffile {locate_config_location()}",
            1,
            [
                "[ERROR] Please set the directory containing",
                "X.509 standard TLS certificates properly",
            ],
            id="Configuration - Invalid directory",
        ),
        pytest.param(
            f"--conffile {locate_config_hostname()}",
            0,
            [
                "[WARNING] Generating a new service hostname dictionary",
            ],
            id="Configuration - Unavailable hostfile",
        ),
    ]
)
def test_conf(cmdl, code, text) -> None:
    runner = CliRunner()
    result = runner.invoke(main, cmdl)
    assert result.exit_code == code  # noqa: S101
    for indx in text:
        assert indx in result.output  # noqa: S101
    folder_location = cmdl.split(" ")[1].replace("/myconfig.py", "")
    rmtree(folder_location)
