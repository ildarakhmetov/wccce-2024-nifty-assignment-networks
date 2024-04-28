/*
* This is the header file for the commands module.
* It contains the function prototypes for the command functions and the process function.
* It also contains the function pointer type for command functions.
* Add more command function prototypes to this file as you add more commands.
*/

// Function pointer type for command functions
typedef int (*CommandFunc)(char*, char*);

// Help command function
int help(char* arg, char* response);

// Process function to handle commands
int process(char* buf, char* response);
