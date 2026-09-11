#include <iostream>

int reverse(int n,int c);
int count(int n);
int power(int index);

int main(){
    int n = 0;
    std::cin >> n;

    std::cout << reverse(n, count(n)-1);
}

int count(int n){
    if(n<=9){
        return 1;
    }

    return 1 + count(n/10);
}

int power(int index){
    if(index==0){
        return 1;
    }

    return 10*power(index-1);
}

int reverse(int n,int c){
    if(n==0){
        return 0;
    }

    int a = n%10;
    return a*power(c) + reverse(n/10, c-1);
}