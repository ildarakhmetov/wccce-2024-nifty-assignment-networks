// Function pointer type for command functions
typedef int (*CommandFunc)(char*, char*);

// Comparison function for qsort
int compare(const void* a, const void* b);

// Calc command function
int calc(char* arg, char* response);

// Sort command function
int sort(char* arg, char* response);

// Help command function
int help(char* arg, char* response);

// Process function to handle commands
int process(char* buf, char* response);
