#include <iostream>
#include <cmath>

int main()
{
    int a,b,BD;
    std::cin >> a;
    std::cin >> b;

    if(a > 0 && b>0){
        if(a == b){
            std::cout << a;
        }
        else{
            for(int i=1; i < a && i < b; i++){
                if(a%i == 0 && b%i == 0){
                    BD = i;
                }
            }
            std::cout << BD;
        }
    }
    else{
        std::cout << "Enter positive numbers.";
    }
}