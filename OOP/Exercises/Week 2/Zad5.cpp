#include <iostream>
#include <cmath>

int main()
{
    double a,b,c;
    std::cin >> a;
    std::cin >> b;
    std::cin >> c;

    double D = b*b - 4*a*c;
    double x1 = 0;
    double x2 = 0;
    if(D > 0){
        x1 = (-b - sqrt(D))/(2*a);
        x2 = (-b + sqrt(D))/(2*a);
        std::cout << x1 << " " << x2;
    }
    else if(D =0){
        x1 = (-b)/(2*a);
        std::cout << x1;
    }
    else{
        std::cout << "No roots.";
    }
}