import os
import sys
from datetime import datetime
from pathlib import Path

import yaml
from cryptography import x509
from cryptography.hazmat.backends import default_backend

from firmitas.conf import logrdata, standard
from firmitas.unit import gopagure


def readcert(certobjc):
    commname = certobjc.subject.rfc4514_string().split("=")[1]
    issuauth = certobjc.issuer.rfc4514_string().split("=")[1]
    serialno = certobjc.serial_number
    strtdate, stopdate = certobjc.not_valid_before, certobjc.not_valid_after
    daystobt, daystodd = (strtdate - datetime.now()).days, (stopdate - datetime.now()).days
    cstarted, cstopped = False if daystobt >= 0 else True, False if daystodd >= 0 else True
    logrdata.logrobjc.debug(f"[{commname}] Issued by {issuauth}")
    logrdata.logrobjc.debug(f"[{commname}] Serial number {serialno}")
    logrdata.logrobjc.debug(
        f"[{commname}] Valid from {strtdate} ({abs(daystobt)} days {'passed since beginning' if cstarted else 'left before beginning'})"  # noqa
    )
    logrdata.logrobjc.debug(
        f"[{commname}] Valid until {stopdate} ({abs(daystodd)} days {'passed since expiring' if cstopped else 'left before expiring'})"  # noqa
    )
    return strtdate, stopdate, cstarted, cstopped, daystobt, daystodd, issuauth, serialno


def probedir():
    logrdata.logrobjc.info("Probing into the configured directory")
    logrdata.logrobjc.info(f"Validating {len(standard.certdict)} X.509-standard TLS certificates")
    doneqant, failqant, totlqant = 0, 0, 0
    for nameindx in standard.certdict:
        totlqant += 1
        certpath = Path(standard.certloca, standard.certdict[nameindx]["path"])
        if os.path.exists(certpath):
            certobjc = x509.load_pem_x509_certificate(certpath.read_bytes(), default_backend())
            (
                standard.certdict[nameindx]["certstat"]["strtdate"],
                standard.certdict[nameindx]["certstat"]["stopdate"],
                standard.certdict[nameindx]["certstat"]["cstarted"],
                standard.certdict[nameindx]["certstat"]["cstopped"],
                standard.certdict[nameindx]["certstat"]["daystobt"],
                standard.certdict[nameindx]["certstat"]["daystodd"],
                standard.certdict[nameindx]["certstat"]["issuauth"],
                standard.certdict[nameindx]["certstat"]["serialno"],
            ) = readcert(certobjc)
            doneqant += 1
            logrdata.logrobjc.info(
                f"[{nameindx}] The specified X.509-standard TLS certificate was read successfully"
            )
        else:
            failqant += 1
            logrdata.logrobjc.warning(
                f"[{nameindx}] The specified X.509-standard TLS certificate could not be located"
            )
    logrdata.logrobjc.info(
        f"Of {totlqant} TLS certificates, {doneqant} TLS certificate(s) were read successfully "
        + f"while {failqant} TLS certificate(s) could not be read"
    )
    with open(standard.hostloca, "w") as yamlfile:
        yaml.safe_dump(standard.certdict, yamlfile)


def gonotify():
    bfstrtcn, afstopcn, totlqant, succqant = 0, 0, 0, 0
    if standard.gitforge == "pagure":
        for certindx in standard.certdict:
            totlqant += 1
            if standard.certdict[certindx]["certstat"]["cstarted"]:
                if standard.certdict[certindx]["certstat"]["cstopped"]:
                    afstopcn += 1
                    logrdata.logrobjc.warning(
                        f"[{certindx}] The specified X.509 TLS certificate is not valid anymore"
                    )
                else:
                    if standard.certdict[certindx]["certstat"]["daystodd"] <= standard.daysqant:
                        logrdata.logrobjc.warning(
                            f"[{certindx}] The specified X.509 TLS certificate is about to expire "
                            + f"in under {standard.daysqant} days from now"
                        )
                        if not standard.certdict[certindx]["notistat"]["done"]:
                            for retcount in range(standard.maxretry):
                                rtrnobjc = gopagure.makenote(
                                    retcount=retcount,
                                    servname=certindx,
                                    strtdate=standard.certdict[certindx]["certstat"]["strtdate"],
                                    stopdate=standard.certdict[certindx]["certstat"]["stopdate"],
                                    daystobt=standard.certdict[certindx]["certstat"]["daystobt"],
                                    daystodd=standard.certdict[certindx]["certstat"]["daystodd"],
                                    certfile=standard.certdict[certindx]["path"],
                                    issuauth=standard.certdict[certindx]["certstat"]["issuauth"],
                                    serialno=standard.certdict[certindx]["certstat"]["serialno"],
                                    assignee=standard.certdict[certindx]["user"],
                                )
                                if rtrnobjc[0]:
                                    succqant += 1
                                    logrdata.logrobjc.info(
                                        f"[{certindx}] The notification ticket for renewing the "
                                        + "TLS certificate has now been created"
                                    )
                                    standard.certdict[certindx]["notistat"]["done"] = rtrnobjc[0]
                                    standard.certdict[certindx]["notistat"]["link"] = rtrnobjc[1]
                                    standard.certdict[certindx]["notistat"]["time"] = rtrnobjc[2]
                                    break
            else:
                bfstrtcn += 1
                logrdata.logrobjc.warning(
                    f"[{certindx}] The specified X.509 TLS certificate is not valid yet"
                )
        logrdata.logrobjc.info(
            f"Of {totlqant} TLS certificates, {bfstrtcn} TLS certificate(s) were not valid "
            + f"yet, {afstopcn} TLS certificates were not valid anymore and {succqant} TLS "
            + "certificates were notified of being near their validity expiry"
        )
        with open(standard.hostloca, "w") as yamlfile:
            yaml.safe_dump(standard.certdict, yamlfile)
    elif standard.gitforge == "gitlab":
        logrdata.logrobjc.error("The notification has not yet been implemented on GitLab")
        sys.exit(1)
    elif standard.gitforge == "github":
        logrdata.logrobjc.error("The notification has not yet been implemented on GitHub")
        sys.exit(1)
    else:
        logrdata.logrobjc.error("The specified ticketing repository forge is not yet supported")
        sys.exit(1)
