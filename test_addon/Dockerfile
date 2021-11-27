ARG BUILD_FROM=ghcr.io/hassio-addons/base/amd64:10.2.3
# hadolint ignore=DL3006
FROM ${BUILD_FROM}

# Setup base
# hadolint ignore=DL3018
RUN apk add --no-cache jq curl findutils python3 python3-dev && \
    pip3 install --no-cache-dir requests==2.26.0 python-dateutil==2.6.1 pytz==2018.3

# Add env
ENV LANG C.UTF-8

# Build arguments
ARG BUILD_ARCH
ARG BUILD_DATE
ARG BUILD_DESCRIPTION
ARG BUILD_NAME
ARG BUILD_REF
ARG BUILD_REPOSITORY
ARG BUILD_VERSION

# Labels
LABEL \
    io.hass.name="${BUILD_NAME}" \
    io.hass.description="${BUILD_DESCRIPTION}" \
    io.hass.arch="${BUILD_ARCH}" \
    io.hass.type="addon" \
    io.hass.version=${BUILD_VERSION} \
    maintainer="Mike van Sighem <mikevansighem@gmail.com>" \
    org.opencontainers.image.title="${BUILD_NAME}" \
    org.opencontainers.image.description="${BUILD_DESCRIPTION}" \
    org.opencontainers.image.vendor="Home Assistant Community Add-ons" \
    org.opencontainers.image.authors="Mike van Sighem <mikevansighem@gmail.com>" \
    org.opencontainers.image.licenses="MIT" \
    org.opencontainers.image.url="https://github.com/${BUILD_REPOSITORY}" \
    org.opencontainers.image.source="https://github.com/${BUILD_REPOSITORY}" \
    org.opencontainers.image.documentation="https://github.com/${BUILD_REPOSITORY}/blob/main/README.md" \
    org.opencontainers.image.created=${BUILD_DATE} \
    org.opencontainers.image.revision=${BUILD_REF} \
    org.opencontainers.image.version=${BUILD_VERSION}

# Copy data
COPY run.sh /
COPY keep_last.py /
RUN ["chmod", "a+x", "/run.sh"]
RUN curl "https://raw.githubusercontent.com/andreafabrizi/Dropbox-Uploader/master/dropbox_uploader.sh" -o /dropbox_uploader.sh
RUN ["chmod", "a+x", "/dropbox_uploader.sh"]
WORKDIR /

CMD [ "/run.sh" ]
