#include <iostream>
#include <cmath>

int main()
{
    double a,b,c,r;
    std::cout << "a=";
    std::cin >> a;
    std::cout << "b=";
    std::cin >> b;
    std::cout << "r=";
    std::cin >> r;

    c = sqrt(a*a + b*b);
    if(r<=0){
        std::cout << "Please enter a positive number for the radius.";
    }
    else if(r>=c){
        std::cout << "The point is in the circle.";
    } else{
        std::cout << "The point is not in the circle.";
    }
}