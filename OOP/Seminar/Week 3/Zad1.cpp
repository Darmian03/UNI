#include <iostream>

int main(){
    int x;
    std::cout << "Please enter a positive number: ";
    std::cin >> x;

    if(x>=1){
        for(int i = 1; i<=x; i++){
            if(i%3 == 0){
                std::cout << i << " ";
            }
        }
    }
    else{
        std::cout << "Please enter a positive number!";
    }
    return 0;
}