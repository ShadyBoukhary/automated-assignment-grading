cmake_minimum_required (VERSION 2.6)
function(message)
  list(GET ARGV 0 MessageType)
  if(MessageType STREQUAL FATAL_ERROR OR
     MessageType STREQUAL SEND_ERROR OR
     MessageType STREQUAL WARNING OR
     MessageType STREQUAL AUTHOR_WARNING)
    list(REMOVE_AT ARGV 0)
    _message(${MessageType} "${ARGV}")
  endif()
endfunction()
project (REPLACE_PROJECT_NAME)
set(CMAKE_INSTALL_MESSAGE LAZY)
set(CMAKE_INSTALL_MESSAGE NEVER)
set(EXECUTABLE_NAME REPLACE_EXECUTABLE_NAME)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY REPLACE_OUTPUT_DIRECTORY)
include_directories(REPLACE_INCLUDE_DIRS)

file(GLOB source REPLACE_SOURCE_GLOB)
add_executable(${EXECUTABLE_NAME} ${source})
