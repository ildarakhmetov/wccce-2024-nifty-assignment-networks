CC = gcc
CFLAGS = -Wall -g
DEPS = commands.h
OBJ = tcp_server.o commands.o

%.o: %.c $(DEPS)
	$(CC) -c -o $@ $< $(CFLAGS)

tcp_server: $(OBJ)
	$(CC) -o $@ $^ $(CFLAGS)

clean:
	rm -f $(OBJ) tcp_server