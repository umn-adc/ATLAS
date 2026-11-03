cmake_minimum_required(VERSION 3.15)
project(CppWebRequest)

# Force modern C++
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Find the dependencies installed by Homebrew
find_package(cpr REQUIRED)
find_package(nlohmann_json REQUIRED)

# Define your project executable
add_executable(main start_data_fetch.cpp)

# Link the libraries to your executable
target_link_libraries(main PRIVATE cpr::cpr nlohmann_json::nlohmann_json)