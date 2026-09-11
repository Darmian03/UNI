#include <iostream>

int main(){
    int x;

    std::cout << "Enter a positive number:";
    std::cin >> x;

    if(x>0){
    for(int i = 1; i<=x; i++){
        std::cout << i << " ";
    }
    }else {
        std::cout << "Please enter a positive number!";
    }
}