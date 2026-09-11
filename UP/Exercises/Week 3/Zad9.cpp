#include <iostream>

int main(){
    int x;

    std::cout << "Enter a positive number:";
    std::cin >> x;

    std::string revx = "";
    int sum = 0;

    if(x>0){
        while(x>0){
            int a = x%10;
            sum += a;
            revx += std::to_string(a);
            x/=10;
        }

        std::cout << "Reversed: " << revx << std::endl;
        std::cout << "Sums of digits: " << sum << std::endl;
    }
    else{
        std::cout << "Please enter a positive number!";
    }
}