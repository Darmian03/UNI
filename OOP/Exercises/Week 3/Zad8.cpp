#include <iostream>

int main(){
    int x;

    std::cout << "Enter a positive number:";
    std::cin >> x;

    int perfect = 0;
    bool prime = true;

    if(x>0){
        for(int i=1; i<x; i++){
            if(x%i == 0){
                perfect += i;
            }
        }
        for(int i=2; i<x; i++){
            if(x%i == 0){
                prime = false;
            }
        }

        std::cout << "Prime: ";
        if(prime == true){
            std::cout << "true" << std::endl;
        }
        else{
            std::cout << "false" << std::endl;
        }

        std::cout << "Perfect: ";
        if(x == perfect || x==1){
            std::cout << "true" << std::endl;
        }
        else{
            std::cout << "false" << std::endl;
        }
    }
    else{
        std::cout << "Please enter a positive number!";
    }
}