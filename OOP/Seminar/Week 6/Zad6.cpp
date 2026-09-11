#include <iostream>

void substring(char source[], int beginIndex, int endIndex, char target[]);

int main()
{
    int size = 0;
    std::cin >> size;

    char arr[100] = {};
    char target[100] = {};

    for(int i = 0; i < size; i++){
        char x;
        std::cin >> x;
        arr[i] = x;
    }

    int beginIndex = 0;
    std::cout << "Enter the starting index:";
    std::cin >> beginIndex;

    if(beginIndex > size){
        std::cout << "Error";
    }
    else{
        int endIndex = 0;
        std::cout << "Enter ending index:";
        std::cin >> endIndex;

        if(endIndex > size){
            endIndex = size;
        }

        substring(arr, beginIndex, endIndex, target);
    }
}

void substring(char source[], int beginIndex, int endIndex, char target[]){
    int j = 0;
    for(int i = beginIndex - 1; i <endIndex; i++){
        target[j] = source[i];
        j++;
    }

    for(int i = 0; i < j; i++){
        std::cout << target[i] << " ";
    }
}