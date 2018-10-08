##
# base
#
# The `minimal` image creates a minimal runtime container.
#
# Note: Images based on this image will be built without superuser privileges.
#
FROM python:3.6-slim-stretch as prod

ENV PATH=$PATH:/home/user/.local/bin \
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_USER=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIPENV_COLORBLIND=true \
    PIPENV_NOSPIN=true \
    SHELL=/bin/sh \
    PAGER=cat \
    GUNICORN_CMD_ARGS="--bind 0.0.0.0:5000 --worker-class gevent --workers 3 --logger-class structlogger.GunicornLogger"

# Avoid mixing $HOME and WORKDIR so important persistent files in $HOME such as
# ~/.local don't conflict with service runtime files.
WORKDIR /srv

# Run as a non-root user.
RUN useradd -ms $SHELL user \
 && chown -R user:user /srv
USER user

# Install the newest pipenv.
RUN python -m pip install --upgrade --user pipenv

# Copy required project files into the WORKDIR.
COPY --chown=user:user Pipfile* setup.py setup.cfg /srv/

# Create a dummy service directory for the dependency installation.
RUN mkdir -p /srv/versions_service

# Install environment dependencies with Pipenv. If no lockfile is present, we skip it.
RUN test -f "./Pipfile.lock" && pipenv install --system --keep-outdated --ignore-pipfile || pipenv install --system --skip-lock

# Copy the project directory (https://github.com/moby/moby/issues/29211)
COPY --chown=user:user versions_service /srv/versions_service

# Copy the entrypoint files for booting the application.
COPY --chown=user:user docker-entrypoint.sh autoapp.py structlogger.py /srv/

# Copy migrations for upgrades
COPY --chown=user:user migrations /srv/migrations

# Use an entrypoint to run the application
ENTRYPOINT ["./docker-entrypoint.sh"]

EXPOSE 5000


##
# dev
#
# The `dev` image creates the runtime container for local development
# environments, where the code can be updated on the fly.
#
FROM prod as dev

# Configure gunicorn to reload on code changes.
ENV GUNICORN_CMD_ARGS="$GUNICORN_CMD_ARGS --reload"

# Install environment dependencies with Pipenv.
RUN pipenv install --system --dev --skip-lock

# Copy the rest of the project into the WORKDIR.
COPY --chown=user:user . /srv/

# Mount a volume at `/srv`
VOLUME /srv


##
# utils
#
# The `utils` image provides utility applications for diagnostics and troubleshooting.
#
FROM prod as utils

# Install common system packages needed for utilities.
# Note: The mkdir commands resolve an issue with postgresql-client config.
USER root
RUN apt-get update \
 && mkdir -p /usr/share/man/man1 \
 && mkdir -p /usr/share/man/man7 \
 && apt-get install -y --no-install-recommends \
      bash \
      tmux \
      curl \
      vim  \
      htop \
      less \
      postgresql-client
USER user

# Copy bin scripts locally
COPY --chown=user:user bin /srv/bin


##
# test
#
# The `test` image provides a dedicated container for running the application
# test suite. It is based on the `utils` image so that a developer will have
# diagnostic tools available in the event of a failure.
#
FROM utils as test

# Copy test configuration(s)
COPY --chown=user:user .coveragerc /srv/.coveragerc

# Copy the test suite
COPY --chown=user:user tests /srv/tests

# Install the test reporter for code climate
ENV CC_REPORTER_URL=https://codeclimate.com/downloads/test-reporter/test-reporter-latest-linux-amd64
ADD --chown=user:user "$CC_REPORTER_URL" /srv/cc-test-reporter

# Install testing dependencies with Pipenv.
RUN pipenv install --system --dev --skip-lock
