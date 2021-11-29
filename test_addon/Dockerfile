# Set build env
ARG BUILD_FROM=ghcr.io/hassio-addons/base/amd64:10.2.3
FROM ${BUILD_FROM}

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
    org.opencontainers.image.vendor="Mike`s Home Assistant Add-on" \
    org.opencontainers.image.authors="Mike van Sighem <mikevansighem@gmail.com>" \
    org.opencontainers.image.licenses="MIT" \
    org.opencontainers.image.url="https://github.com/${BUILD_REPOSITORY}" \
    org.opencontainers.image.source="https://github.com/${BUILD_REPOSITORY}" \
    org.opencontainers.image.documentation="https://github.com/${BUILD_REPOSITORY}/blob/main/README.md" \
    org.opencontainers.image.created=${BUILD_DATE} \
    org.opencontainers.image.revision=${BUILD_REF} \
    org.opencontainers.image.version=${BUILD_VERSION}

# Install dependancies
COPY requirements.txt /
RUN apk add --no-cache findutils==4.8.0-r1 python3==3.9.5-r2 python3-dev==3.9.5-r2 py3-pip==20.3.4-r1 && \
    pip3 install --no-cache-dir -r requirements.txt

# Copy keep last
COPY keep_last.py /

# Copy run and allow to execute
COPY run.sh /
RUN ["chmod", "a+x", "/run.sh"]

# Get the dropbox_uploader file from a specific commit and allow to execute.
RUN curl "https://raw.githubusercontent.com/andreafabrizi/Dropbox-Uploader/4ccc5c10a7b0b7a41ab4faa52585f015ed2ae568/dropbox_uploader.sh" -o /dropbox_uploader.sh && \
    ["chmod", "a+x", "/dropbox_uploader.sh"]

WORKDIR /

CMD [ "/run.sh" ]
