#include <iostream>

int main()
{
    char arr[50] = {};
    std::cin.getline(arr, 50);
    char a,b;

    /*for(int i = 0; i < strlen(arr) - 1; i++){
        if(arr[i]%2==1){
            if(arr[i+1]%2==1){
                a = arr[i+1];
                arr[i+1] = '-';
                for(int j = i+1; j < 50; j++){
                    b = arr[j+1];
                    arr[j+1] = a;
                    a = b;
                }
            }
        }
    }*/

    for(int i = 0; i < strlen(arr) - 1; i++){
        if(arr[i]%2==1){
            if(arr[i+1]%2==1){
                char arr1[50] = {};
                for(int j = 0; j < strlen(arr1); j++){
                    arr1[j] = arr[i+1];
                }

                arr[i+1] = '-';
                for(int j = i+2; j < strlen(arr1); j++){
                    arr[j] = arr1[j-2];
                }
            }
        }
    }

    std::cout << arr;
    return 0;
}