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


import pytest
from click.testing import CliRunner

from firmitas.main import main


@pytest.mark.parametrize(
    "cmdl, code, text",
    [
        pytest.param(
            "--help",
            0,
            [
                "Usage: firmitas [OPTIONS]",
                "Options:",
                "-c, --conffile PATH",
                "Read configuration from the specified Python file",
                "--version",
                "Show the version and exit.",
                "--help",
                "Show this message and exit.",
            ],
            id="Option - Basic help",
        ),
        pytest.param(
            "--version",
            0,
            [
                "firmitas, version",
            ],
            id="Option - Version information",
        ),
        pytest.param(
            "--zeroexistent",
            2,
            [
                "Usage: firmitas [OPTIONS]",
                "Try 'firmitas --help' for help.",
                "Error: No such option: --zeroexistent",
            ],
            id="Option - Invalid invocation",
        ),
        pytest.param(
            "zeroexistent",
            2,
            [
                "Usage: firmitas [OPTIONS]",
                "Try 'firmitas --help' for help.",
                "Error: Got unexpected extra argument (zeroexistent)",
            ],
            id="Option - Invalid argument",
        ),
        pytest.param(
            "--conffile",
            2,
            [
                "Error: Option '--conffile' requires an argument.",
            ],
            id="Configuration - Parameter absent",
        ),
        pytest.param(
            "--conffile ZEROEXISTENT",
            2,
            [
                "Usage: firmitas [OPTIONS]",
                "Try 'firmitas --help' for help.",
                "Error: Invalid value for '-c' / '--conffile': Path 'ZEROEXISTENT' does not exist.",
            ],
            id="Configuration - Parameter invalid",
        ),
    ]
)
def test_main(cmdl, code, text) -> None:
    runner = CliRunner()
    result = runner.invoke(main, cmdl)
    assert result.exit_code == code  # noqa: S101
    for indx in text:
        assert indx in result.output  # noqa: S101
