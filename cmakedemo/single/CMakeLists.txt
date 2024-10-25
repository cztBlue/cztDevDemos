# 构建makefile不能识别中文路径
# 在buiud中执行：
# $ cmake -G "MINGW makefiles"..
# $ cmake 

cmake_minimum_required(VERSION 3.15) 
# 指定 CMake 的最低版本

project (singlemain) 
# 指定PROJECT_NAME变量的值，也可以这样写set(PROJECT_NAME HELLO)

set(SOURCE main.cpp) 
# SOURCE实际上是一个“数组变量”，
# 你可以通过set(SOURCE main.cc utils.cc helper.cc)形式来设定多个值
# 可以通过list(GET SOURCE 1 UTIL_SRC)将SOURCE数组中的utils.cc赋给UTIL_SRC

include_directories(include)
# 可以添加一个头文件的路径文件夹名(相对.txt)
# 如果有其它的头文件路径(多层路径)，按如下形式多添加一行include_directories(header2/myheader)

add_executable(${PROJECT_NAME} ${SOURCE}) 
# 第一个参数是程序名，第二个参数是源代码路径
# 创建exe，用 add_library(MyLibrary ${SOURCES})创建dll
