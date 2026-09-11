#include <iostream>

int main()
{
    char arr1[50] = {};
    std::cin.getline(arr1, 50);
    
    char arr2[50] = {};
    std::cin.getline(arr2, 50);

    char arr3[50] = {};
    std::cin.getline(arr3, 50);

    std::cout << arr1 << arr2 << arr3;
    return 0;
}