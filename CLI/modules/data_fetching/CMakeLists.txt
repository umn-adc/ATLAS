cmake_minimum_required(VERSION 3.15)
project(CppWebRequest)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Fetch dependencies straight from source

include(FetchContent)
FetchContent_Declare(
    cpr
    GIT_REPOSITORY https://github.com/libcpr/cpr.git
    GIT_TAG        1.12.0
    GIT_SHALLOW    TRUE
)
FetchContent_Declare(
    nlohmann_json
    GIT_REPOSITORY https://github.com/nlohmann/json.git
    GIT_TAG        v3.12.0
    GIT_SHALLOW    TRUE
)
FetchContent_MakeAvailable(cpr nlohmann_json)

# Compile as a library

add_library(data_fetch_lib STATIC start_data_fetch.cpp)
# Exposes current directory as a public header search path, 
# so the corresponding header file is found automatically.
target_include_directories(data_fetch_lib PUBLIC $(CMAKE_CURRENT_SOURCE_DIR))
target_link_libraries(data_fetch_lib PRIVATE cpr::cpr nlohmann_json::nhlomann_json)

# Add example executable

add_executable(example example.cpp)
target_link_libraries(example PRIVATE data_fetch_lib)