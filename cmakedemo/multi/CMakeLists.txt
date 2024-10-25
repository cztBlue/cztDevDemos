# 多级makefile，一般一个dll/exe就做一个cmakelist
# 这里是顶层的的cmakelist
# 确保你安装了camke,gcc,g++,并将ming32-cmake改名为make.exe
# 然后在powershell中运行.\compiler.ps1，编译结果在./build/output/bin

cmake_minimum_required(VERSION 3.10)

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/output/bin)
set(CMAKE_SHARED_LIBRARY_PREFIX "")
# 清除生产dll的lib前缀

file(MAKE_DIRECTORY ${CMAKE_RUNTIME_OUTPUT_DIRECTORY})
# 创建 bin 目录

add_subdirectory(main)
# 添加子目录
