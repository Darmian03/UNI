#include <iostream>

int main(){
    int n;
    std::cout << "Please enter how many numbers you will enter: ";
    std::cin >> n;

    int sum = 0;

    if(n>=1){
        for(int i = 1; i<=n; i++){
            int x;
            std::cin >> x;
            sum += x;
        }
        std::cout << sum;
    }
    else{
        std::cout << "Please enter a positive number!";
    }
    return 0;
}