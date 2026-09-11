#include <iostream>

int main(){
    double x, y;

    std::cout << "Enter your x axis:";
    std::cin >> x;
    std::cout << "Enter your y axis:";
    std::cin >> y;

    if(x>0){
        if(y>0){
            std::cout << "I";
        }
        if(y<0){
            std::cout << "IV";
        }
        else{
            std::cout << "X-axis";
        }
    }
    else if(x<0){
        if(y>0){
            std::cout << "II";
        }
        if(y<0){
            std::cout << "III";
        }
        else{
            std::cout << "X-axis";
        }
    }
    else{
        if(y==0){
            std::cout << "Centre";
        }
        else{
            std::cout << "Y-axis";
        }
    }
    return 0;
}