#include <iostream>
#include "CLI_funcs.h"
#include "toml.hpp"
#include "CLI/CLI.hpp"

int main(int argc, char *argv[]) {
    CLI::App atlas;
    CLI_setup(atlas);

    CLI11_PARSE(atlas, argc, argv);

    // checks any command line inputs for commands
    if (atlas.got_subcommand("init")) {
        std::cout << "init ran\n";
        initialize();
    }
    if (atlas.got_subcommand("config")){
        std::cout << "config registered\n";
        configure();
    }


    return 0;
}