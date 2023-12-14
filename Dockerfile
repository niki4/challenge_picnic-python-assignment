FROM python:3.10.7-alpine3.16

## Create a group and user
RUN addgroup -S teampicnic && adduser -D picnic -G teampicnic
USER picnic

ENV PATH=/home/picnic/.local/bin:${PATH}

COPY --chown=picnic:teampicnic picnic-assignment /home/picnic/picnic-assignment

WORKDIR /home/picnic/picnic-assignment

## Install stage
RUN pip install ".[test]"

## Test stage
RUN pytest

## Run stage
ENTRYPOINT ["event-process"]
CMD ["100", "30"]  # max_events = 100 messages, max_time = 30 seconds
