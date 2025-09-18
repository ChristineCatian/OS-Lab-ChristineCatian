#include <windows.h>
#include <stdio.h>

int main() {
    STARTUPINFO si;
    PROCESS_INFORMATION pi;
    DWORD myPid = GetCurrentProcessId();
    char cmdLine[100];

    ZeroMemory(&si, sizeof(si));
    si.cb = sizeof(si);
    ZeroMemory(&pi, sizeof(pi));

    printf("create_basic.exe: My PID = %lu\n", (unsigned long)myPid);

    // Pass parent PID to child
    sprintf(cmdLine, "child_echo.exe %lu", (unsigned long)myPid);

    // Create the child process
    if (!CreateProcess(
        NULL,        // application name
        cmdLine,     // command line
        NULL, NULL,  // process & thread security attributes
        FALSE,       // handle inheritance
        0,           // creation flags
        NULL,        // environment
        NULL,        // current directory
        &si, &pi))   // startup info & process info
    {
        printf("create_basic.exe: CreateProcess failed (%lu)\n", GetLastError());
        return -1;
    }

    printf("create_basic.exe: Created child PID = %lu\n", (unsigned long)pi.dwProcessId);

    // Wait for child process to finish
    WaitForSingleObject(pi.hProcess, INFINITE);

    DWORD exitCode;
    GetExitCodeProcess(pi.hProcess, &exitCode);
    printf("create_basic.exe: Child exited with code %lu\n", (unsigned long)exitCode);

    // Close process and thread handles
    CloseHandle(pi.hProcess);
    CloseHandle(pi.hThread);

    return 0;
}
