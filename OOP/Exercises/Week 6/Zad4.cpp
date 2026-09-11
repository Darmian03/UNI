#include <iostream>

int main()
{
    char arr1[50] = {};
    std::cin.getline(arr1, 50);
    
    char arr2[50] = {};
    std::cin.getline(arr2, 50);

    for(int i = 0; i < 50; i++){
        arr1[i] = arr2[i];
    }

    std::cout << arr1 << std::endl;
    std::cout << arr2 << std::endl;
    return 0;
}