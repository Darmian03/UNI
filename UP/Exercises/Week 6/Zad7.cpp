#include <iostream>

int main()
{
    char arr[50] = {};
    std::cin.getline(arr, 50);
    int counter = 0;

    for(int i = 0; i < 50; i++){
        if(arr[i] == 'a' || arr[i] == 'e' || arr[i] == 'i' || arr[i] == 'o' || arr[i] == 'u'){
            counter++;
        }
    }
    std::cout << counter;
    return 0;
}