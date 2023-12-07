FROM frolvlad/alpine-gcc
COPY . /usr/src/validator
WORKDIR /usr/src/validator
RUN apk add --no-cache g++
RUN g++ validator.cc -o validator
CMD ["./validator"]