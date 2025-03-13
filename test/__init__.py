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

standard_list = [
    "[INFO] Probing into the configured directory",
    "[INFO] Validating X.509-standard TLS certificate(s)",
    "[DEBUG] [joystick.stg] Issued by RabbitMQ STAGING CA",
    "[DEBUG] [joystick.stg] Serial number 44541479035547978831580614561088909678",
    "[DEBUG] [joystick.stg] Valid from 2019-05-28 23:04:35",
    "[DEBUG] [joystick.stg] Valid until 2029-05-25 23:04:35",
    "[INFO] [joystick.stg] The specified X.509-standard TLS certificate was read successfully",  # noqa : E501
    "[DEBUG] [nuancier.stg] Issued by RabbitMQ STAGING CA",
    "[DEBUG] [nuancier.stg] Serial number 209068775949833699801370873051828148798",
    "[DEBUG] [nuancier.stg] Valid from 2019-02-21 18:34:13",
    "[DEBUG] [nuancier.stg] Valid until 2029-02-18 18:34:13",
    "[INFO] [nuancier.stg] The specified X.509-standard TLS certificate was read successfully",  # noqa : E501
    "[DEBUG] [robosign.stg] Issued by RabbitMQ STAGING CA",
    "[DEBUG] [robosign.stg] Serial number 38988970076690016170053187069021997563",
    "[DEBUG] [robosign.stg] Valid from 2019-09-20 22:29:56",
    "[DEBUG] [robosign.stg] Valid until 2029-09-17 22:29:56",
    "[INFO] [robosign.stg] The specified X.509-standard TLS certificate was read successfully",  # noqa : E501
    "[DEBUG] [waiverdb.stg] Issued by RabbitMQ STAGING CA",
    "[DEBUG] [waiverdb.stg] Serial number 6931031601876762538483728070539648010",
    "[DEBUG] [waiverdb.stg] Valid from 2019-03-06 23:58:40",
    "[DEBUG] [waiverdb.stg] Valid until 2029-03-03 23:58:40",
    "[INFO] [waiverdb.stg] The specified X.509-standard TLS certificate was read successfully",  # noqa : E501
    "[ERROR] [mistaken.stg] The specified X.509-standard TLS certificate could not be read",  # noqa : E501
    "[INFO] Of 6 TLS certificate(s), 5 TLS certificate(s) were read successfully while 1 TLS certificate(s) could not be read",  # noqa : E501
]


def list_etoe_pagure(list_etoe: list = standard_list.copy()) -> list:  # noqa : B008
    list_etoe += [
        "[WARNING] [dtfedmsg.stg] The specified X.509 TLS certificate is not valid anymore",
        "[INFO] Of 6 TLS certificate(s), 1 TLS certificate(s) were not valid yet, 1 TLS certificate(s) were not valid anymore and 0 TLS certificate(s) were notified of being near their validity expiry",  # noqa : E501
    ]
    return list_etoe


def list_etoe_gitlab(list_etoe: list = standard_list.copy()) -> list:  # noqa : B008
    list_etoe += [
        "[ERROR] The notification has not yet been implemented on GitLab"
    ]
    return list_etoe


def list_etoe_github(list_etoe: list = standard_list.copy()) -> list:  # noqa : B008
    list_etoe += [
        "[ERROR] The notification has not yet been implemented on GitHub"
    ]
    return list_etoe


def list_etoe_auth(list_etoe: list = standard_list.copy()) -> list:  # noqa : B008
    list_etoe += [
        "[WARNING] [joystick.stg] The specified X.509 TLS certificate is about to expire in under",  # noqa : E501
        "[DEBUG] [joystick.stg] Notification request attempt count - 1 of 5",
        "[DEBUG] Starting new HTTPS connection (1): pagure.io:443",
        f"[DEBUG] https://pagure.io:443 \"POST /api/0/{envr['FIRMITAS_TEST_REPONAME']}/new_issue HTTP/",  # noqa : E501
        "[DEBUG] [joystick.stg] The notification request was met with response code 200",
        "[DEBUG] [joystick.stg] The created notification ticket was created with ID",
        "[INFO] [joystick.stg] The notification ticket for renewing the TLS certificate has now been created",  # noqa : E501
        "[WARNING] [nuancier.stg] The specified X.509 TLS certificate is about to expire in under",  # noqa : E501
        "[DEBUG] [nuancier.stg] Notification request attempt count - 1 of 5",
        "[DEBUG] Starting new HTTPS connection (1): pagure.io:443",
        f"[DEBUG] https://pagure.io:443 \"POST /api/0/{envr['FIRMITAS_TEST_REPONAME']}/new_issue HTTP/",  # noqa : E501
        "[DEBUG] [nuancier.stg] The notification request was met with response code 200",
        "[DEBUG] [nuancier.stg] The created notification ticket was created with ID",
        "[INFO] [nuancier.stg] The notification ticket for renewing the TLS certificate has now been created",  # noqa : E501
        "[WARNING] [robosign.stg] The specified X.509 TLS certificate is about to expire in under",  # noqa : E501
        "[DEBUG] [robosign.stg] Notification request attempt count - 1 of 5",
        "[DEBUG] Starting new HTTPS connection (1): pagure.io:443",
        f"[DEBUG] https://pagure.io:443 \"POST /api/0/{envr['FIRMITAS_TEST_REPONAME']}/new_issue HTTP/",  # noqa : E501
        "[DEBUG] [robosign.stg] The notification request was met with response code 200",
        "[DEBUG] [robosign.stg] The created notification ticket was created with ID",
        "[INFO] [robosign.stg] The notification ticket for renewing the TLS certificate has now been created",  # noqa : E501
        "[WARNING] [waiverdb.stg] The specified X.509 TLS certificate is about to expire in under",  # noqa : E501
        "[DEBUG] [waiverdb.stg] Notification request attempt count - 1 of 5",
        "[DEBUG] Starting new HTTPS connection (1): pagure.io:443",
        f"[DEBUG] https://pagure.io:443 \"POST /api/0/{envr['FIRMITAS_TEST_REPONAME']}/new_issue HTTP/",  # noqa : E501
        "[DEBUG] [waiverdb.stg] The notification request was met with response code 200",
        "[DEBUG] [waiverdb.stg] The created notification ticket was created with ID",
        "[INFO] [waiverdb.stg] The notification ticket for renewing the TLS certificate has now been created",  # noqa : E501
        "[INFO] Of 6 TLS certificate(s), 1 TLS certificate(s) were not valid yet, 1 TLS certificate(s) were not valid anymore and 4 TLS certificate(s) were notified of being near their validity expiry",  # noqa : E501
    ]
    return list_etoe


def list_etoe_nope(list_etoe: list = standard_list.copy()) -> list:  # noqa : B008
    list_etoe += [
        "[WARNING] [joystick.stg] The specified X.509 TLS certificate is about to expire in under",
        "[DEBUG] [joystick.stg] Notification request attempt count - 1 of 5",
        "[DEBUG] [joystick.stg] Notification request attempt count - 2 of 5",
        "[DEBUG] [joystick.stg] Notification request attempt count - 3 of 5",
        "[DEBUG] [joystick.stg] Notification request attempt count - 4 of 5",
        "[DEBUG] [joystick.stg] Notification request attempt count - 5 of 5",
        "[DEBUG] [nuancier.stg] Notification request attempt count - 1 of 5",
        "[DEBUG] [nuancier.stg] Notification request attempt count - 2 of 5",
        "[DEBUG] [nuancier.stg] Notification request attempt count - 3 of 5",
        "[DEBUG] [nuancier.stg] Notification request attempt count - 4 of 5",
        "[DEBUG] [nuancier.stg] Notification request attempt count - 5 of 5",
        "[DEBUG] [robosign.stg] Notification request attempt count - 1 of 5",
        "[DEBUG] [robosign.stg] Notification request attempt count - 2 of 5",
        "[DEBUG] [robosign.stg] Notification request attempt count - 3 of 5",
        "[DEBUG] [robosign.stg] Notification request attempt count - 4 of 5",
        "[DEBUG] [robosign.stg] Notification request attempt count - 5 of 5",
        "[DEBUG] [waiverdb.stg] Notification request attempt count - 1 of 5",
        "[DEBUG] [waiverdb.stg] Notification request attempt count - 2 of 5",
        "[DEBUG] [waiverdb.stg] Notification request attempt count - 3 of 5",
        "[DEBUG] [waiverdb.stg] Notification request attempt count - 4 of 5",
        "[DEBUG] [waiverdb.stg] Notification request attempt count - 5 of 5",
        "[DEBUG] Starting new HTTPS connection (1): pagure.io:443",
        f"[DEBUG] https://pagure.io:443 \"POST /api/0/{envr['FIRMITAS_TEST_REPONAME']}/new_issue HTTP/",  # noqa : E501
        "[DEBUG] [joystick.stg] The notification request was met with response code 401",
        "[DEBUG] [nuancier.stg] The notification request was met with response code 401",
        "[DEBUG] [robosign.stg] The notification request was met with response code 401",
        "[DEBUG] [waiverdb.stg] The notification request was met with response code 401",
        "[WARNING] [mistaken.stg] The specified X.509 TLS certificate is not valid yet",
        "[WARNING] [nuancier.stg] The specified X.509 TLS certificate is about to expire in under",
        "[WARNING] [robosign.stg] The specified X.509 TLS certificate is about to expire in under",
        "[WARNING] [waiverdb.stg] The specified X.509 TLS certificate is about to expire in under",
        "[INFO] Of 6 TLS certificate(s), 1 TLS certificate(s) were not valid yet, 1 TLS certificate(s) were not valid anymore and 0 TLS certificate(s) were notified of being near their validity expiry"  # noqa : E501
    ]
    return list_etoe
