#include <iostream>

int sum(int a, int b);

int main()
{
    int a,b;
    std::cin >> a;
    std::cin >> b;
    if(a>b){
        int c = a;
        a = b;
        b = c;
    }

    std::cout << sum(a,b);
}

int sum(int a, int b){
    if(a==b){
        return a;
    }
    else{
        return a+sum(a+1, b);
    }
}