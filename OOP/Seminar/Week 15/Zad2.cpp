#include <iostream>

int sumArr(int *array, int n){
    int sum = 0;
    for(int i = 0; i < n; i++){
        sum += array[i];
    }
    return sum;
}

void arr(int *array, int n, int expected){
    int sum = sumArr(array, n);
    int avg = sum/n;

    while(avg > expected){
        array[n] = 0;
        n++;
    }

    for(int i = 0; i < n; i++){
        std::cout << array[i];
    }
}

int main(){
    int n = 0;
    std::cout << "n = ";
    std::cin >> n;

    int expected = 0;
    std::cout << "expected = ";
    std::cin >> expected;

    if(expected > 0){
        int *array = new int[n];
        for(int i = 0; i < n; i++){
            std::cin >> array[i];
        }

        if(sumArr(array, n)/n <= expected){
            for(int i = 0; i < n; i++){
                std::cout << array[i];
            }
        }
        else{
            arr(array, n, expected);
        }
        delete[] array;
    }
    else{
        std::cout << "Expected is too low!";
    }
}