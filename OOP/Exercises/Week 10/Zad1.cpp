#include <iostream>

int power(int number, int n);

int main()
{
    int number,n;
    std::cin >> number;
    std::cin >> n;

    std::cout << power(number, n);
}

int power(int number, int n){
    if(n==1){
        return number;
    }

    return number*power(number, n-1);
}