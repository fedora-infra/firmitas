FROM registry.fedoraproject.org/fedora:41

LABEL maintainer "Akashdeep Dhar <t0xic0der@fedoraproject.org>"

ENV PYTHONUNBUFFERED=1

RUN dnf -y install python3-pip
RUN dnf -y clean all
RUN pip3 install --upgrade firmitas==0.1.3a0

ENV FIRMITAS_CONFIG=/etc/firmitas/conf/myconfig.py

ENTRYPOINT ["firmitas"]
CMD ["--conffile", "$FIRMITAS_CONFIG"]
