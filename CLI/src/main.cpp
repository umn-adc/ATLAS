#include <iostream>
#include "flags.h"
#include "../tomlplusplus/toml.hpp"
#include "../CLI11/include/CLI/CLI.hpp"

int main(int argc, char *argv[]) {
    CLI::App atlas;
    // setup_flags(atlas);
    CLI::App* init = atlas.add_subcommand("init", "Creates a default config file.");
    CLI::App* config = atlas.add_subcommand("config", "Root for config changes.");
    CLI::App* check = config->add_subcommand("check", "Loads, parses, and validates config file.");

    CLI11_PARSE(atlas, argc, argv);

    if (*init) {
        initialize();
    }
    if (*config) {
        std::cout << "config registered\n";
        if (*check) {
            std::cout << "check registered\n";
        }
    }

    return 0;
}