#define MYLIB_EXPORTS
#include "mylib.h"
#include <iostream>

int MathTool::add(int a, int b)
{
    return a + b;
}

int MathTool::sub(int a, int b)
{
    return a - b;
}

int MathTool::max(int a, int b)
{
    return a > b ? a : b;
}

void MathTool::tip(){
    std::cout<<"MathTool!"<<std::endl;
}

void hello(){
    
    std::cout<<"Ciallo～(∠・ω< )"<<std::endl;
}

MathTool* createMathTool()
{
    return new MathTool();
}