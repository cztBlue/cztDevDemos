// #ifndef MYLIB_H //保证一次编译 ,旧写法
// #define MYLIB_H

#pragma once //新写法
#ifdef MYLIB_EXPORTS //dll中使用dllexport
#define MYLIB_API __declspec(dllexport)
#define MYLIB_API_ "__declspec(dllexport)"
// #pragma comment(lib, "Dllname.lib") MSVC中使用这种语句来链接dll

#else //exe中使用dllimport
#define MYLIB_API __declspec(dllimport)
#define MYLIB_API_ "__declspec(dllimport)"
#endif

class MYLIB_API MathTool {
public: int max(int,int); //在MSVC中不用min，max这种，改成名字，被std用了，会报错
// public: int max_(int,int); 
public: int add(int,int);
public: int sub(int,int);
public: void tip();
};

extern "C" MYLIB_API void hello();
extern "C" MYLIB_API MathTool* createMathTool(); 

// #endif 
