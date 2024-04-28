

#include <netdb.h>
#include <netinet/in.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <unistd.h>
#include "commands.h"

#define MAX_PENDING 5
#define MAX_LINE    256
#define SERVER_PORT 10393

int main() {
    struct sockaddr_in sin;
    char buf[MAX_LINE];
    char response[MAX_LINE];
    int buf_len, addr_len;
    int s, new_s;

    bzero((char*)&sin, sizeof(sin));
    sin.sin_family = AF_INET;
    sin.sin_addr.s_addr = INADDR_ANY;
    sin.sin_port = htons(SERVER_PORT);

    if ((s = socket(PF_INET, SOCK_STREAM, 0)) < 0) {
        perror("tcp_server: socket");
        exit(1);
    }
    if ((bind(s, (struct sockaddr*)&sin, sizeof(sin))) < 0) {
        perror("tcp_server: bind");
        exit(1);
    }
    listen(s, MAX_PENDING);

    while (1) {
        if ((new_s = accept(s, (struct sockaddr*)&sin, (socklen_t*)&addr_len)) < 0) {
            perror("tcp_server: accept");
            exit(1);
        }
        while (((buf_len) = recv(new_s, buf, sizeof(buf), 0))) {
            fputs(buf, stdout);
            int result = process(buf, response);
            if (result < 0) {
                strcpy(response, "Invalid command\n");
            }
            send(new_s, response, strlen(response) + 1, 0);
        }
    }
    close(new_s);
}