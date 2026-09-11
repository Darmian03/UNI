#include <iostream>

int factoriel(int n);

int main()
{
    int n;
    std::cin >> n;

    std::cout << factoriel(n);
}

int factoriel(int n){
    if(n==0){
        return 1;
    }
    return n*factoriel(n-1);
}