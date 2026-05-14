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


from requests import post

from firmitas.conf import logrdata, standard
from firmitas.unit import issubody, issuhead


def makenote(
    retcount,
    servname,
    strtdate,
    stopdate,
    daystobt,
    daystodd,
    certfile,
    issuauth,
    serialno,
    assignee,
):
    try:
        logrdata.logrobjc.debug(
            f"[{servname}] Notification request attempt count - {retcount+1} of {standard.maxretry}"
        )
        rqstobjc = post(
            url=f"{standard.repoloca}/api/v1/repos/{standard.reponame}/issues",
            headers={"Authorization": f"token {standard.password}"},
            json={
                "title": issuhead.format(servname=servname, daysqant=standard.daysqant),
                "body": issubody.format(
                    servname=servname,
                    daysqant=standard.daysqant,
                    strtdate=strtdate,
                    stopdate=stopdate,
                    daystobt=abs(daystobt),
                    daystodd=abs(daystodd),
                    certfile=certfile,
                    issuauth=issuauth,
                    serialno=serialno,
                ),
                "assignees": [assignee] if assignee else [],
                "labels": standard.tagslist,
            },
            timeout=standard.rqsttime,
        )
        logrdata.logrobjc.debug(
            f"[{servname}] The notification request was met with response code "
            + f"{rqstobjc.status_code}"
        )
        if rqstobjc.status_code == 201:
            logrdata.logrobjc.debug(
                f"[{servname}] The created notification ticket was created with ID "
                + f"#{rqstobjc.json()['id']} ({rqstobjc.json()['html_url']})."
            )
            return (
                True,
                rqstobjc.json()["html_url"],
                rqstobjc.json()["created_at"],
            )
        else:
            return False, "", ""
    except Exception as expt:
        logrdata.logrobjc.error(
            f"[{servname}] The notification ticket could not be created - {expt}"
        )
        return False, "", ""
