FROM python:3.10 AS build
RUN pip install poetry
WORKDIR /build
COPY . .
RUN poetry build

FROM python:3.10-alpine
WORKDIR /lisum_chat
COPY --from=build /build/dist/*.whl .
RUN pip install *.whl
VOLUME /lisum_chat/data
CMD ["lisum_chat"]
