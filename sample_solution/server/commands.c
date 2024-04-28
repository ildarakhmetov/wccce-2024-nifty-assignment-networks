#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "commands.h"

// Comparison function for qsort
int compare(const void* a, const void* b) { return (*(int*)a - *(int*)b); }

/*
The calc function takes a string argument and a response buffer, and calculates
the result of the expression in the argument.
- The argument is a string containing an expression in the form "a op b", where a and b
are integers and op is an operator (+, -, *, /).
- The response buffer should contain the result of the calculation as a string.
*/
int calc(char* arg, char* response) {
    int a, b;
    char op;
    sscanf(arg, "%d%c%d", &a, &op, &b);
    // Calculate the result and store it in the response buffer
    switch (op) {
        case '+': sprintf(response, "%d\n", a + b); break;
        case '-': sprintf(response, "%d\n", a - b); break;
        case '*': sprintf(response, "%d\n", a * b); break;
        case '/': sprintf(response, "%d\n", a / b); break;
        default: return -1; // Invalid operator
    }
    return 0;
}

/*
The sort function takes a string argument and a response buffer, and sorts the
numbers in the argument.
- The argument is a string containing a list of integers separated by spaces.
- The response buffer should contain the sorted list of numbers as a string.
Students can use any sorting algorithm they want.
*/
int sort(char* arg, char* response) {
    int numbers[1000]; // assuming the maximum number of integers is 1000
    int count = 0;

    char* token = strtok(arg, " ");
    while (token != NULL) {
        numbers[count++] = atoi(token);
        token = strtok(NULL, " ");
    }

    qsort(numbers, count, sizeof(int), compare);

    char* resp_ptr = response;
    for (int i = 0; i < count; i++) {
        resp_ptr += sprintf(resp_ptr, "%d ", numbers[i]);
    }

    // Replace the last space with a newline
    if (count > 0) {
        *(resp_ptr - 1) = '\n';
    }

    return 0;
}

/*
The help function takes a string argument and a response buffer, and returns
the help message.
- The argument is a string containing the name of a command, or an empty string.
- If the argument is an empty string, the response buffer should contain the list
of available commands.
- If the argument is the name of a command, the response buffer should contain
the help message for that command. 
*/
int help(char* arg, char* response) {
    if (strlen(arg) == 0) {
        strcpy(response, "Available commands: calc, sort, help\n");
    } else if (strcmp(arg, "calc") == 0) {
        strcpy(response, "Calculates the result of a op b. Usage: calc a op b\n");
    } else if (strcmp(arg, "sort") == 0) {
        strcpy(response, "Sorts a list of numbers. Usage: sort n1 n2 n3 ...\n");
    } else {
        strcpy(response, "This command does not exist\n");
    }
    return 0;
}

/*
Parse the request and call the appropriate function to process it.
- if the request starts with "calc", call the calc function
- if the request starts with "sort", call the sort function
- if the request starts with "help", call the help function
*/
int process(char* buf, char* response) {
    CommandFunc commands[] = {calc, sort, help};
    char* commandNames[] = {"calc", "sort", "help"};
    int numCommands = sizeof(commands) / sizeof(commands[0]);

    for (int i = 0; i < numCommands; i++) {
        if (strncmp(buf, commandNames[i], strlen(commandNames[i])) == 0) {
            // Get the rest of the string after the command name, ignoring leading whitespace
            char* arg = buf + strlen(commandNames[i]);
            while (*arg == ' ') {
                arg++;
            }
            // strip the newline character from the end of the argument
            if (arg[strlen(arg) - 1] == '\n') {
                arg[strlen(arg) - 1] = '\0';
            }
            return commands[i](arg, response);
        }
    }

    return -1; // Invalid command
}