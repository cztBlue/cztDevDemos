// compiler:
// gcc

// file:
// dynamicmain.cpp 
// mylib.c 
// mylib.h

// command(dynamic linking:):
// g++ -shared -o mylib.dll ./mylib.cpp
// g++ -o dynamicmain ./dynamicmain.cpp -L. -lmylib

#include "mylib.h"
#include <iostream>
#include <windows.h>
#include <tchar.h>

typedef void (*helloFuncp)(); // 定义 hello 函数指针类型,注意typedef的写法
typedef MathTool* (*createMathToolFunc)(); 

int main() {
    SetConsoleOutputCP(CP_UTF8); 

    //dll映射到hModule
    HMODULE hModule = LoadLibrary(TEXT("mylib.dll"));
    if (!hModule) {
        std::cerr << "DLL Loss" << std::endl;
        return 1;
    }

    // 获取hello函数
    helloFuncp hello = (helloFuncp)GetProcAddress(hModule, "hello");
    if (!hello) {
        std::cerr << "function 'hello' Loss" << std::endl;
        FreeLibrary(hModule);
        return 1;
    }
    hello();

    // 获取mathtool对象
    createMathToolFunc getmathtool = (createMathToolFunc)GetProcAddress(hModule, "createMathTool");
    if (!getmathtool) {
        std::cerr << "OBJ 'MathTool' Loss" << std::endl;
        FreeLibrary(hModule);
        return 1;
    }
    MathTool* m = getmathtool();
    m->tip();

    // 释放 DLL
    FreeLibrary(hModule);
    std::cin.ignore();

    return 0;
}
