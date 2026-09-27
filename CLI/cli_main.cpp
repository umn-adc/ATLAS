#include <iostream>
#include <tomlplusplus/toml.hpp>
#include "cli_funcs.cpp"
using namespace toml;


void handle_command(char *argv[]) {
    if (argv[0] == "config") {
        // to do
    }
    else if (argv[0] == "init") {
        cli_init.init();
    }
    else if (argv[0] == "start") {
        // to do
    }
    else if (argv[0] == "stop") {
        // to do
    }
    else if (argv[0] == "status") {
        // to do   
    }
    else {
        std::cout << "Atlas: Argument " << *argv[0] << " is an invalid argument" << std::endl;
    }
}

int main(int argc, char *argv[]) {
    
    handle_command(argv);

    return 0;
}