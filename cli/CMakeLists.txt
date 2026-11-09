cmake_minimum_required(VERSION 4.0)

project(atlas)

include(FetchContent)

add_executable(atlas
    src/main.cpp
    src/CLI_funcs.cpp
)

set_target_properties(atlas PROPERTIES
    CXX_STANDARD 17
    CXX_STANDARD_REQUIRED ON
)

add_subdirectory(tomlplusplus)
add_subdirectory(cli11)


include_directories(
    PRIVATE
        ${CMAKE_CURRENT_SOURCE_DIR}/tomlplusplus
        ${CMAKE_CURRENT_SOURCE_DIR}/cli11/include
        ${CMAKE_CURRENT_SOURCE_DIR}/src
)

target_link_libraries(atlas
    PRIVATE
        CLI11::CLI11
            )
