#pragma once
#include "CLI/CLI.hpp"
#include "../tomlplusplus/toml.hpp"
namespace subcommands {
    void CLI_setup(CLI::App& atlas);
    int initialize();
    int configure();
}