FROM python:3.13-alpine3.23

RUN addgroup -g 10001 appgroup && adduser -S -D -u 10001 -G appgroup appuser

RUN apk add --no-cache \
    build-base \
    sdl2-dev \
    sdl2_image-dev \
    sdl2_mixer-dev \
    sdl2_ttf-dev \
    freetype-dev \
    libpng-dev \
    jpeg-dev

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

USER appuser

CMD [ "python", "main.py" ]