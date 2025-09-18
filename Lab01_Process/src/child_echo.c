#include <windows.h>
#include <stdio.h>

int main(int argc, char* argv[]) {
    DWORD pid = GetCurrentProcessId();
    DWORD ppid = 0;

    if (argc > 1) {
        ppid = atoi(argv[1]);
    }

    printf("child_echo.exe: My PID = %lu\n", pid);
    printf("child_echo.exe: Parent PID (arg) = %lu\n", (unsigned long)ppid);

    // Sleep for 60 seconds so you can test forced termination
    printf("child_echo.exe: Doing some work (sleep 60s)...\n");
    Sleep(60000);  // 60,000 milliseconds = 60 seconds

    printf("child_echo.exe: Normal exit with code 7\n");
    return 7;
}
