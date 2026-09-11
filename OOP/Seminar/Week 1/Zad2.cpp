#include <iostream>

int main(){
    double x, y;

    std::cout << "Enter your x axis:";
    std::cin >> x;
    std::cout << "Enter your y axis:";
    std::cin >> y;

    if(x>0){
        if(y>0){
            std::cout << "Your quadrant is 1.";
        }
        if(y<0){
            std::cout << "Your quadrant is 4.";
        }
        else{
            std::cout << "Your dot is on x axis.";
        }
    }
    else if(x<0){
        if(y>0){
            std::cout << "Your quadrant is 2.";
        }
        if(y<0){
            std::cout << "Your quadrant is 3.";
        }
        else{
            std::cout << "Your dot is on x axis.";
        }
    }
    else{
        if(y==0){
            std::cout << "Your dot is in the centre.";
        }
        else{
            std::cout << "Your dot is on y axis.";
        }
    }
    return 0;
}