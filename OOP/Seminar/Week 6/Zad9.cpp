#include <iostream>
#include <string.h>

void trim(char original[], char trimmed[]);

int main()
{
    char array[100] = {};
    char trimmed[100] = {};

    std::cin.getline(array, 100);

    trim(array, trimmed);
}

void trim(char original[], char trimmed[]){
    int j = 0;
    for(int i = 0; i < strlen(original); i++){
        if(original[i] != ' '){
            trimmed[j] = original[i];
            j++;
        }
    }

    for(int i = 0; i <= j; i++){
        std::cout << trimmed[i];
    }
}