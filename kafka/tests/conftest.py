# (C) Datadog, Inc. 2020-present
# All rights reserved
# Licensed under Simplified BSD License (see LICENSE)
import os

import pytest

from datadog_checks.dev import docker_run
from datadog_checks.dev.conditions import CheckDockerLogs
from datadog_checks.dev.utils import load_jmx_config
from datadog_checks.base import is_affirmative

from .common import HERE, HOST, HOST_IP

@pytest.fixture(scope='session')
def dd_environment():
    USE_MULTIPLE_BROKERS = is_affirmative(os.environ['USE_MULTIPLE_BROKERS'])
    if USE_MULTIPLE_BROKERS:
        compose_file = os.path.join(HERE, 'compose', 'multiple-brokers.yaml')
    else:
        compose_file = os.path.join(HERE, 'compose', 'single-broker.yaml')

    with docker_run(
        compose_file, conditions=[CheckDockerLogs(compose_file, [r'\[KafkaServer id=\d+\] started'], matches="all")],
            env_vars={
            # Advertising the hostname doesn't work on docker:dind so we manually
            # resolve the IP address. This seems to also work outside docker:dind
            # so we got that goin for us.
            'KAFKA_HOST': HOST_IP
        },
    ):
        yield load_jmx_config(), {'use_jmx': True}
