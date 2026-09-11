#include <iostream>
#include <cstring>

void printArrays(char arrays[][31], int n){
    for(int i = 0; i < n; i++){
        std::cout << arrays[i] << std::endl;
    }
}

bool compareArrays(char array1[31], char array2[31]){
    int index1 = 0;
    char arr1[30];
    while(array1[index1] != '\0'){
        arr1[index1] = std::tolower(array1[index1]);
        index1++;
    }

    int index2 = 0;
    char arr2[30];
    while(array2[index2] != '\0'){
        arr2[index2] = std::tolower(array2[index2]);
        index2++;
    }

    if(std::strcmp(arr1, arr2) > 0){
        return true;
    }
    else{
        if(std::strcmp(arr1, arr2) == 0 && index1 > index2){
            return true;
        }
        else{
            return false;
        }
    }
}

void bubbleSortArrays(char arrays[][31], int n){
    for(int i = 0; i < n; i++){
        for(int j = 0; j < n - i - 1; j++){
            if(compareArrays(arrays[j], arrays[j+1])){
                std::swap(arrays[j], arrays[j+1]);
            }
        }
    }
}

int main(){
    char arrays[49][31];
    int n = 0;
    std::cin >> n;
    n++;

    for(int i = 0; i < n; i++){
        std::cin.getline(arrays[i], 31);
    }

    bubbleSortArrays(arrays, n);
    std::cout << std::endl;
    std::cout << "Sorted arrays:" << std::endl;
    printArrays(arrays, n);
}