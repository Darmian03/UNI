#include <iostream>

int main(){
    int x;
    std::cout << "Please enter a positive number: ";
    std::cin >> x;

    int sum = 1;

    if(x>=1){
        for(int i = 1; i<=x; i++){
            if(x%2 == 0 && i%2 == 0){
                sum *= i;
            }
            else if(x%2 != 0 && i%2 != 0){
                sum *= i;
            }
        }
        std::cout << sum;
    }
    else{
        std::cout << "Please enter a positive number!";
    }
    return 0;
}