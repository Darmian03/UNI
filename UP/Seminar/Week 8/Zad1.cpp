#include <iostream>

int main()
{
    int a = 10;
    std::cout << &a << std::endl;

    int* b = &a;
    std::cout << *b << "   ";

    int* c = b;
    *c = 5;

    int d = 6;

    c = &d;

    std::cout << a << "   " << *b << "   " << *c << "   " << b << "   " << c;
}