
cmake_minimum_required(VERSION 3.10)
project(dynamicmain)

add_subdirectory(../mylib ${CMAKE_CURRENT_BINARY_DIR}/mylib)
# 一个add_subdirectory对应一个新的cmakelist.txt
# add_subdirectory(source_dir binary_dir)
# 第一个参数制定了源代码路径，第二个参数是编译后存放程序(相对于build中的这个main文件夹)的路径

add_executable(${PROJECT_NAME} dynamicmain.cpp)
# 第一个参数是程序名，第二个参数是源代码路径

set_target_properties(${PROJECT_NAME} PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY ${CMAKE_RUNTIME_OUTPUT_DIRECTORY})
# 把dynamicmain的输出路径属性设置为$CMAKE_RUNTIME_OUTPUT_DIRECTORY
# 这是为了保证dll能和exe在一起

target_link_libraries(${PROJECT_NAME} PRIVATE mylib)
# 第一个参数是连接的主程序，第二个参数是要连接的dll

