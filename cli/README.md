Command Line tool for the ATLAS trading program.
Using the atlas command after building will allow command line arguments to perform
or test some actions and features.

# Dependencies:
[Cmake 4.0](https://cmake.org/download/)

# Building:
Run the following from the command line
```
git submodule update
cmake -S . -B build -G "MinGW Makefiles"
cmake --build build
```
