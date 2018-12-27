cmake_minimum_required (VERSION 2.6)
project (Hello_World)

set(EXECUTABLE_NAME main)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY "../")
include_directories("./")

file(GLOB source "./*.cpp")
add_executable(${EXECUTABLE_NAME} ${source})
