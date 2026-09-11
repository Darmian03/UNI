#include <iostream>

int main(){
    int x;
    std::cout << "Please enter a positive number: ";
    std::cin >> x;

    int y;
    std::cout << "Please enter a second positive number: ";
    std::cin >> y;

    int sum1 = 0;
    int sum2 = 0;

    if(x>=1 && y>=1){
        while(x>0){
            int a = x%10;
            sum1 += a;
            x/=10;
        }
        while(y>0){
            int b = y%10;
            sum2 += b;
            y/=10;
        }

        if(sum1 == sum2){
            std::cout << "The sums are equal.";
        }
        else{
            std::cout << "The sums are not equal.";
        }
    }
    else{
        std::cout << "Please enter a positive numbers!";
    }
    return 0;
}