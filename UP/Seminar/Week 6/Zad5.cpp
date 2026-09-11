#include <iostream>
#include <cmath>

int polinom(int array[], int size, int x);

int main()
{
    int size = 0;
    std::cin >> size;

    int arr[100] = {};

    for(int i = 0; i < size; i++){
        int a;
        std::cin >> a;
        arr[i] = a;
    }

    int x = 0;
    std::cout << "Enter x:";
    std::cin >> x;

    std::cout << polinom(arr, size, x);
}

int polinom(int array[], int size, int x){
    int sum = 0;
    int power = 0;

    for(int i = 0; i < size; i++){
        sum += array[i]*pow(x, power);
        power ++;
    }

    return sum;
}