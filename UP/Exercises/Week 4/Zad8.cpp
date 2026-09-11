#include <iostream>

void printInBinary(int number);

int main()
{
    int number;
    std::cin >> number;
}

void printInBinary(int number){
    std::string result = "";
    while(number >0){
        result += std::to_string(number%2);
        number/=2;
    }
    std::cout << result;
}