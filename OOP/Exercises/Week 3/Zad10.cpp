#include <iostream>
#include <cmath>

int main(){
    int x;

    std::cout << "Enter a positive number:";
    std::cin >> x;

    int counter = 1;
    int x1 = x;
    int x2 = x;
    int sum = 0;

    if(x>0){
        while(x1>9){
            counter++;
            x1 /= 10;
        }

        while(x>0){
            int b = x%10;
            sum += pow(b,counter);
            x/=10;
        }

        if(x2 == sum){
            std::cout << "True";
        }
        else{
            std::cout << "False";
        }
    }
    else{
        std::cout << "Please enter a positive number!";
    }
}