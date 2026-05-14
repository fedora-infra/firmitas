"""
Firmitas
Copyright (C) 2023-2026 Akashdeep Dhar

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

"""
Variables related to notifications
"""

# The limit for how long a single request must be attempted for
rqsttime = 30

# The URL of the Forgejo instance
repoloca = ""

# The repository path in owner/repo format
reponame = ""

# The username to masquerade as to create notifying issue tickets
username = ""

# The API key for the Forgejo instance pertaining to the username
password = ""

# Number of days from validity expiry to make the notification for
daysqant = 30

# List of integer label IDs to tag the notification tickets with
tagslist = []

# Maximum number of retries to opening the notification ticket
maxretry = 5

"""
Variables related to probing
"""

# The location of the X.509 standard TLS certificates
certloca = "/var/tmp/firmitas/certhere"  # noqa : S108

# The location of the service hostnames and maintainers map
hostloca = "/var/tmp/firmitas/certlist.yml"  # noqa: S108

"""
Variables related to logging
"""

# The default configuration for service logging
logrconf = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "[FMTS] %(asctime)s [%(levelname)s] %(message)s",
            "datefmt": "[%Y-%m-%d %I:%M:%S %z]",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "formatter": "standard",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
    },
    "root": {
        "level": "DEBUG",
        "handlers": ["console"],
    },
}

"""
Variables used for computing
"""

certdict = {}
