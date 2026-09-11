#include <iostream>

int count(int n);

int main(){
    int n = 0;
    std::cin >> n;

    std::cout << count(n);
}

int count(int n){
    if(n<=9){
        return 1;
    }

    return 1 + count(n/10);
}