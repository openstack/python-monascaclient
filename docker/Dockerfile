ARG DOCKER_IMAGE=monasca/client
ARG APP_REPO=https://review.opendev.org/openstack/python-monascaclient

# Branch, tag or git hash to build from.
ARG REPO_VERSION=master
ARG CONSTRAINTS_BRANCH=master

# Always start from `monasca-base` image and use specific tag of it.
ARG BASE_TAG=master
FROM monasca/base:$BASE_TAG

# Environment variables used for our service or wait scripts.
ENV \
    MONASCA_URI=monasca:8070 \
    OS_AUTH_URL=http://keystone:35357/v3 \
    OS_USERNAME=mini-mon \
    OS_PASSWORD=password \
    OS_TENANT_NAME=mini-mon \
    OS_DOMAIN_NAME=Default

RUN monasca --version

# Implement start script in `start.sh` file.
CMD ["/start.sh"]