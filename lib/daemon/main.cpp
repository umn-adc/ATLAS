#include <iostream>
#include <chrono>
#include <thread>
#include <csignal>
#include <atomic>

//Basic boilerplating for singals
static void daemonize(){
//Creating processes     
pid_t pid;

pid = fork();

if(pid < 0){
    exit(EXIT_FAILURE);
}

if(pid > 0){
    exit(EXIT_SUCCESS);
}

//TODO Skeleton signals 

}

int main(){
  
}