#include <iostream>

int main(){
    int x;

    std::cout << "Enter a positive number:";
    std::cin >> x;

    int counter = 0;

    if(x>0){
        while(x>0){
            int a = x%10;
            if(a == 0){
                counter ++;
            }
            else{
                std::cout << counter;
                x = 0;
            }
            x/=10;
        }
    }
    else{
        std::cout << "Please enter a positive number!";
    }
}