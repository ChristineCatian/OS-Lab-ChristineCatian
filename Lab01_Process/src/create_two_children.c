#include <windows.h>
#include <stdio.h>

int main() {
    STARTUPINFO si1, si2;
    PROCESS_INFORMATION pi1, pi2;
    DWORD myPid = GetCurrentProcessId();
    char cmdLine1[100], cmdLine2[100];

    ZeroMemory(&si1, sizeof(si1));
    si1.cb = sizeof(si1);
    ZeroMemory(&pi1, sizeof(pi1));

    ZeroMemory(&si2, sizeof(si2));
    si2.cb = sizeof(si2);
    ZeroMemory(&pi2, sizeof(pi2));

    printf("Parent: My PID = %lu\n", (unsigned long)myPid);

    // Build command lines, pass parent PID to both children
    sprintf(cmdLine1, "child_echo.exe %lu", (unsigned long)myPid);
    sprintf(cmdLine2, "child_echo.exe %lu", (unsigned long)myPid);

    // Create first child
    if (!CreateProcess(
        NULL, cmdLine1,
        NULL, NULL, FALSE, 0,
        NULL, NULL, &si1, &pi1))
    {
        printf("Parent: Failed to create child1 (%lu)\n", GetLastError());
        return -1;
    }
    printf("Parent: Created child1 with PID = %lu\n", (unsigned long)pi1.dwProcessId);

    // Create second child
    if (!CreateProcess(
        NULL, cmdLine2,
        NULL, NULL, FALSE, 0,
        NULL, NULL, &si2, &pi2))
    {
        printf("Parent: Failed to create child2 (%lu)\n", GetLastError());
        return -1;
    }
    printf("Parent: Created child2 with PID = %lu\n", (unsigned long)pi2.dwProcessId);

    // Wait for both children to finish
    WaitForSingleObject(pi1.hProcess, INFINITE);
    WaitForSingleObject(pi2.hProcess, INFINITE);

    DWORD exitCode1, exitCode2;
    GetExitCodeProcess(pi1.hProcess, &exitCode1);
    GetExitCodeProcess(pi2.hProcess, &exitCode2);

    printf("Parent: Child1 exit code = %lu\n", (unsigned long)exitCode1);
    printf("Parent: Child2 exit code = %lu\n", (unsigned long)exitCode2);

    // Clean up
    CloseHandle(pi1.hProcess);
    CloseHandle(pi1.hThread);
    CloseHandle(pi2.hProcess);
    CloseHandle(pi2.hThread);

    return 0;
}
