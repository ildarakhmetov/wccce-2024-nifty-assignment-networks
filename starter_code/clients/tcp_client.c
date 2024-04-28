/*
* TCP client program
*/

#include <netdb.h>
#include <netinet/in.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <unistd.h>

#define MAX_LINE    256
#define SERVER_PORT 10393

int main(int argc, char* argv[]) {
    struct hostent* hp;
    struct sockaddr_in sin;
    char* host;
    char buf[MAX_LINE];
    int s;
    int len;

    if (argc == 2) {
        host = argv[1];
    } else {
        fprintf(stderr, "usage: tcp_client <server_host>\n");
        exit(1);
    }

    hp = gethostbyname(host);
    if (!hp) {
        fprintf(stderr, "tcp_client: unknown host: %s\n", host);
        exit(1);
    }

    bzero((char*)&sin, sizeof(sin));
    sin.sin_family = AF_INET;
    bcopy(hp->h_addr_list[0], (char*)&sin.sin_addr, hp->h_length);
    sin.sin_port = htons(SERVER_PORT);

    if ((s = socket(PF_INET, SOCK_STREAM, 0)) < 0) {
        perror("tcp_client: socket");
        exit(1);
    }
    if (connect(s, (struct sockaddr*)&sin, sizeof(sin)) < 0) {
        perror("tcp_client: connect");
        close(s);
        exit(1);
    }
    while (fgets(buf, sizeof(buf), stdin)) {
        buf[MAX_LINE - 1] = '\0';
        len = strlen(buf) + 1;

        // send a message to the server
        send(s, buf, len, 0);

        // receive a message from the server
        len = recv(s, buf, sizeof(buf), 0);
        fputs("Server says: ", stdout);
        fputs(buf, stdout);
    }
}