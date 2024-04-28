#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "commands.h"

/*
* This function is called when the "help" command is entered.
* It writes a response to the response buffer.
* The argument is the rest of the string after the command name.
*/
int help(char* arg, char* response) {
    sprintf(response, "Helping you with %s\n", arg);
    return 0;
}

/*
* This function processes the command in the buffer and writes the response to the response buffer.
* It uses the commandFunc array to find the function to call based on the command name.
* The command name is the first word in the buffer, and the rest of the buffer is the argument to the command.
*/
int process(char* buf, char* response) {
    CommandFunc commands[] = {help}; // Add more commands here
    char* commandNames[] = {"help"}; // Add more command names here
    int numCommands = sizeof(commands) / sizeof(commands[0]);

    for (int i = 0; i < numCommands; i++) {
        if (strncmp(buf, commandNames[i], strlen(commandNames[i])) == 0) {
            // Get the rest of the string after the command name, ignoring leading whitespace
            char* arg = buf + strlen(commandNames[i]);
            // Skip leading whitespace
            while (*arg == ' ') {
                arg++;
            }
            // strip the newline character from the end of the argument
            if (arg[strlen(arg) - 1] == '\n') {
                arg[strlen(arg) - 1] = '\0';
            }
            return commands[i](arg, response); // Call the command function
        }
    }

    return -1; // Invalid command
}