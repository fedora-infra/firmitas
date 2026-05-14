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


issuhead = "TLS certificate for `{servname}` service is about to expire in {daysqant} days"

issubody = """
This is to inform that the TLS certificate for the following service will expire in about **{daysqant} day(s)** from now on **{stopdate} UTC**. Here is the information about the associated TLS certificate.

- **Service name** - **{servname}** (Certificate stored as `{certfile}`)
- **Issuing authority** - **{issuauth}** (ID `#{serialno}`)
- **Validity starting** - **{strtdate} UTC** (`{daystobt} day(s)` passed since beginning)
- **Validity ending** - **{stopdate} UTC** (`{daystodd} day(s)` left before expiring)

The point of contact for the service may be tagged into this issue ticket to be notified about the same. It is strongly recommended that they promptly recreate the TLS certificate before the existing certificate expires.

---

_This issue ticket was automatically created by the [**Firmitas**](https://github.com/fedora-infra/firmitas) notification service._  
_Please contact the [**Fedora Infrastructure**](https://github.com/fedora-infra/firmitas/issues) team if you believe this is a mistake._
"""  # noqa
