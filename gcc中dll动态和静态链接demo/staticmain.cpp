//compiler:
// gcc

// file:
// staticmain.cpp 
// mylib.c 
// mylib.h

// command(static linking:):
// g++ -shared -o mylib.dll ./mylib.cpp
// g++ -o staticmain ./staticmain.cpp -L. -lmylib

//gun使用命令参数的形式来链接dll，而MSVC则是在文件中使用 #pragma comment(lib, "Dllname.lib")来链接
#include "mylib.h"
#include <iostream>
#include <windows.h>


int main() {
    SetConsoleOutputCP(CP_UTF8); //指定控制台输出
    std::cout <<"Mode Here:"<<MYLIB_API_<<std::endl;
    MathTool* m = new MathTool();
    std::cout <<m->add(5, 3)<<std::endl;
    std::cout <<m->sub(5, 3)<<std::endl;
    m->tip();
    hello();
    std::cin.ignore();
    return 0;
}
