#include <iostream>

bool decreasing(int a, int prev){
    if(a == 0){
        return true;
    }
    else if(a%10 < prev){
        return false;
    }

    decreasing(a/10, a%10);
}

int sumDecreasing(int a, int b){
    if(a > b){
        return 0;
    }

    if(decreasing(a, 0)){
        return 1 + sumDecreasing(a+1, b);
    }

    sumDecreasing(a+1, b);
}

int main(){
    int a,b;
    std::cout << "a = ";
    std::cin >> a;
    std::cout << "b = ";
    std::cin >> b;

    std::cout << sumDecreasing(a, b);
}