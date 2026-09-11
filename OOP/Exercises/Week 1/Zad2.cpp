#include <iostream>
#include <cmath>

int main()
{
    double a,b,c;
    std::cout << "a=";
    std::cin >> a;
    std::cout << "b=";
    std::cin >> b;

    c = sqrt(a*a + b*b);
    std::cout << "The space between the poihnt is:" << c;
}