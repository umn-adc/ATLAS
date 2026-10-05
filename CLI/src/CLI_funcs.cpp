#include "CLI_funcs.h"
#include "../tomlplusplus/toml.hpp"
#include <fstream>

int initialize() {
    std::fstream config("config.toml");

    config << R"(config_version = 1

        [server]
        host = "0.0.0.0"
        port = 8000
        frontend_port = 5173

        [database]
        path = "./data/atlas.db"

        [storage]
        data_dir = "./data"
        strategy_dir = "./data/strategies"
        log_dir = "./data/logs"

        [daemon]
        socket_path = "/tmp/atlasd.sock"

        [logging]
        level = "info"

        [deployment]
        default_working_dir = "./data/deployments")"sv;
        
        config.close();
}