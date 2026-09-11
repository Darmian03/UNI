#include <iostream>

int main()
{
    char arr[50] = {};
    std::cin.getline(arr, 50);
    
    for(int i = 0; i < 50; i++){
        if(arr[i] >= 'A' && arr[i] <= 'Z'){
            arr[i] += 32;
        }
        else if(arr[i] >= 'a' && arr[i] <= 'z'){
            arr[i] -= 32;
        }
    }

    std::cout << arr;
    return 0;
}