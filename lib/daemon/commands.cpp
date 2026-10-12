#include <iostream>
#include <chrono>
#include <thread>
#include <csignal>
#include <atomic>
#include <sys/wait.h>

void start(int argc, char *argv[]){
if(argc < 1){
    printf("No process arguments passed.\n");
    exit(1);
}

}
//Prints status of child processes, should have some implementation of parent's as well
void status(pid_t pid){
if(pid < 0){
    perror("fork");
    exit(1);
}
if(pid == 0){
    printf("Child PID: %d\n", pid);
    exit(42);
}
int status;
wait(&status);
printf("Child exited with %d\n", WEXITSTATUS(status));
}
//Should print list of active processes and posssibly signals? 
void list(){

}
//Stops a process 
void stop(pid_t pid){
kill(pid, 0);
}
