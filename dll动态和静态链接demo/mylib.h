#ifndef MYLIB_H //保证一次编译
#define MYLIB_H

#ifdef MYLIB_EXPORTS //dll中使用dllexport
#define MYLIB_API __declspec(dllexport)
#define MYLIB_API_ "__declspec(dllexport)"
#else //exe中使用dllimport
#define MYLIB_API __declspec(dllimport)
#define MYLIB_API_ "__declspec(dllimport)"
#endif

class MYLIB_API MathTool {
public: int max(int,int);
public: int add(int,int);
public: int sub(int,int);
public: void tip();
};

extern "C" MYLIB_API void hello();
extern "C" MYLIB_API MathTool* createMathTool(); 

#endif 
