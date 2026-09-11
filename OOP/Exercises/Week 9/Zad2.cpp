#include <iostream>

int sum(int* x, int* y);

int main(){
    int x,y;
    std::cin >> x;
    std::cin >> y;

    std::cout << sum(&x, &y);
}

int sum(int* x, int* y){
    int z = *x + *y;
    return z;
}