#include <iostream>

int main()
{
    char arr[50] = {};
    std::cin.getline(arr, 50);
    
    int i = 0;
    int j = sizeof(arr) / sizeof(char) - 1;

    while(i < j){
        char a = arr[i];
        arr[i] = arr[j];
        arr[j] = a;

        i++;
        j--;
    }

    std::cout << arr;
    return 0;
}