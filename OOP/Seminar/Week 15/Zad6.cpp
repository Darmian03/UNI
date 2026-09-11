#include <iostream>

char *arr(char *array, int n){
    int index = 0;
    for(int i = 0; i < n; i++){
        if(array[i] != arr + index){

        }
    }
}

int main(){
    int n = 0;
    std::cout << "n = ";
    std::cin >> n;

    char *array = new char[n];
    std::cin >> array;

    std::cout << arr(array, n);

    delete[] array;
}