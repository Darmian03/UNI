#include <iostream>

int main()
{
    int a,b;
    std::cout << "a=";
    std::cin >> a;
    std::cout << "b=";
    std::cin >> b;

    std::cout << "Sum:" << a+b << std::endl;
    std::cout << "Diff:" << a-b << std::endl;
    std::cout << "Mult:" << a*b << std::endl;
    std::cout << "Div:" << a/b << std::endl;
    std::cout << "Remain:" << a%b << std::endl;
    return 0;
}