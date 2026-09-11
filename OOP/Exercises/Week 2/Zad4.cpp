#include <iostream>

int main()
{
    double a,b,c;
    std::cin >> a;
    std::cin >> b;
    std::cin >> c;

    if(a*b*c >= 0){
        std::cout << "+";
    }
    else{
        std::cout << "-";
    }
    return 0;
}