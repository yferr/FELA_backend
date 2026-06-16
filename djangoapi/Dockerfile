FROM python:3.12-alpine

ARG USER_ID
ARG GROUP_ID
ARG USERNAME

RUN addgroup -g $GROUP_ID $USERNAME && \
    adduser -D -u $USER_ID -G $USERNAME $USERNAME

WORKDIR /home/$USERNAME

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system build and geospatial dependencies
RUN apk add --no-cache \
    postgresql-dev libpq-dev \
    gdal gdal-dev \
    geos-dev \
    proj-dev \
    gcc g++ musl-dev \
    libffi-dev python3-dev \
    libc-dev linux-headers

RUN pip install --upgrade pip

# Install GDAL Python bindings matching the exact system GDAL version
# (must happen before requirements.txt to avoid version conflicts)
RUN GDAL_VERSION=$(gdal-config --version) && \
    pip install GDAL==${GDAL_VERSION}

USER $USERNAME
COPY . .
USER root
RUN chmod +x initdb.sh
RUN pip install -r requirements.txt
USER $USERNAME
