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
        initialize();
    }
    if (atlas.got_subcommand("config")){
        configure();
    }


    return 0;
}