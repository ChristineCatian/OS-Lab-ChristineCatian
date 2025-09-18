#include <windows.h>
#include <stdio.h>

int main() {
    STARTUPINFO si;
    PROCESS_INFORMATION pi;

    ZeroMemory(&si, sizeof(si));
    si.cb = sizeof(si);
    ZeroMemory(&pi, sizeof(pi));

    printf("Parent (exec-sim): My PID = %lu\n", (unsigned long)GetCurrentProcessId());

    // This simulates "exec" by running another program (e.g., cmd.exe /c dir)
    char commandLine[] = "cmd.exe /c dir";  

    if (!CreateProcess(
            NULL,           // application name
            commandLine,    // command line
            NULL, NULL,     // process/thread security
            FALSE,          // handle inheritance
            0,              // creation flags
            NULL,           // environment
            NULL,           // current directory
            &si,            // startup info
            &pi             // process info
        )) {
        printf("Parent: CreateProcess failed (%lu).\n", GetLastError());
        return 1;
    }

    printf("Parent: Created child to run '%s' with PID = %lu\n", commandLine, (unsigned long)pi.dwProcessId);

    // Wait for child to finish
    WaitForSingleObject(pi.hProcess, INFINITE);

    DWORD exitCode;
    GetExitCodeProcess(pi.hProcess, &exitCode);
    printf("Parent: Child exited with code = %lu\n", (unsigned long)exitCode);

    // Close handles
    CloseHandle(pi.hProcess);
    CloseHandle(pi.hThread);

    return 0;
}
