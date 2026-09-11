#include <iostream>

int main(){
    int x,a,b;

    std::cout << "Enter your a:";
    std::cin >> a;
    std::cout << "Enter your b:";
    std::cin >> b;
    std::cout << "Enter your x:";
    std::cin >> x;

    if(a>=b){
        if(a>=x && x>=b){
           std::cout << "X is in the interval."; 
        }
        else{
            std::cout << "X is not in the interval."; 
        }
    } else if(a<b){

    }
}