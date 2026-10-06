#ifndef CLI_funcs_h
#define CLI_funcs_h
#include "CLI/CLI.hpp"
#include "../tomlplusplus/toml.hpp"

void CLI_setup(CLI::App& atlas);
int initialize();
int configure();
#endif