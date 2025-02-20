FROM ubuntu:latest
LABEL authors="eduar"

ENTRYPOINT ["top", "-b"]