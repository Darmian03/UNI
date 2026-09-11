#include <iostream>

int main(){
    double kg, h;

    std::cout << "Enter your kilograms:";
    std::cin >> kg;
    std::cout << "Enter your height in metres:";
    std::cin >> h;

    std::cout << "YourBMI is:" << kg/(h*h);
    return 0;
}