#include <iostream>

void changeNumber(int* number);

int main()
{
    int a = 0;
    std::cin >> a;

    changeNumber(&a);
}

void changeNumber(int* number){
    if(*number%2 == 0){
        std::cout << "Even";
    }
    else{
        std::cout << "Odd";
    }
}