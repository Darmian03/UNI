#include <iostream>

int main(){
    int x;
    std::cout << "Please enter a positive number: ";
    std::cin >> x;

    int sum = 0;

    if(x>=1){
        for(int i = 1; i<=x; i++){
            sum += i*i;
        }
        std::cout << sum;
    }
    else{
        std::cout << "Please enter a positive number!";
    }
    return 0;
}