Command Line tool for the ATLAS trading program.
Using the atlas command after building will allow command line arguments to perform
or test some actions and features.

Dependencies:
Cmake: https://cmake.org/download/
toml++: run 'git submodule add https://github.com/marzer/tomlplusplus.git'
CLI11:  run 'git submodule add https://github.com/cliutils/cli11'

Building:
Run the following from the command line
cmake -S . -B build -G "MinGW Makefiles"
cmake --build build
