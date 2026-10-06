#include "CLI_funcs.h"
#include "CLI/CLI.hpp"
#include "toml.hpp"
#include <iostream>
#include <fstream>

using namespace toml;

struct atlas_config;
table tbl;

// creates all subcommands and flags via CLI11 tools
void CLI_setup(CLI::App& atlas) {
    CLI::App* init = atlas.add_subcommand("init", "Creates a default config file.");
    CLI::App* config = atlas.add_subcommand("config", "Root for config changes.");
}

// creates/overwrites config file from default_config.toml
int initialize() {
    std::ifstream default_config("configs/default_config.toml");
    std::ofstream config("configs/config.toml");

    while (default_config) {
        std::string line;
        std::getline(default_config, line);
        config << line << "\n";
    }
        
    default_config.close();
    config.close();
    return 0;
}

// parses and validates config file, returns when error was encountered if any
int configure() {
    try {
        tbl = parse_file("configs/config.toml");
        std::cout << "Config file parsed successfully!\n" << std::endl;
    }
    catch (const toml::parse_error& err){
        std::cout << "Failed to parse config file.\n" << std::endl;
    }

    try {
        struct config_struct {
            std::string_view host = tbl["host"].value_or(""sv);
            int port = tbl["port"].value_or(-1);
            int frontend_port = tbl["frontend_port"].value_or(-1);
            std::string_view path = tbl["path"].value_or(""sv);
            std::string_view data_dir = tbl["data_dir"].value_or(""sv);
            std::string_view strategy_dir = tbl["strategy_dir"].value_or(""sv);
            std::string_view log_dir = tbl["log_dir"].value_or(""sv);
            std::string_view socket_path = tbl["socket_path"].value_or(""sv);
            std::string_view level = tbl["level"].value_or(""sv);
            std::string_view default_working_dir = tbl["default_working_dir"].value_or(""sv);
        };
        std::cout << "Config file validated successfully!\n";
    }
    catch (const error_t& validate_err){
        std::cout << "Failed to validate config file.\n";
    }

    return 0;
}