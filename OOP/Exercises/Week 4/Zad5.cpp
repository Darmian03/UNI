#include <iostream>
#include <cmath>

bool isSubNumber(int find, int search);

int main()
{
    int number;
    std::cin >> number;
}

bool isSubNumber(int find, int search){
    int a = search;
    int power = 0;
    while(a > 0){
        a/10;
        power++;
    }

    power = pow(10, power);

    while(find>0){
        if(find%power == search)
    }
}