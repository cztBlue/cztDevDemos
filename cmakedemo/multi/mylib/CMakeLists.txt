cmake_minimum_required(VERSION 3.10)
project(mylib)

add_library(${PROJECT_NAME} SHARED mylib.cpp)
# SHARED 关键字说明是动态链接库

set_target_properties(${PROJECT_NAME} PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY ${CMAKE_RUNTIME_OUTPUT_DIRECTORY})
# 把mylib的输出路径属性设置为$CMAKE_RUNTIME_OUTPUT_DIRECTORY

target_include_directories(${PROJECT_NAME} PUBLIC ../header)

