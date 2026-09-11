#include <iostream>

struct IntVector{
    int size;
    int *array = new int[size];
};

void push_back(IntVector vec, int a){
    vec.size ++;
    vec.array[vec.size-1] = a;

    for(int i = 0; i < vec.size; i++){
        std::cout << vec.array[i];
    }
}

void pop_back(IntVector vec){
    vec.size--;

    for(int i = 0; i < vec.size; i++){
        std::cout << vec.array[i];
    }
}

int getOnIndex(IntVector vec, int idx){
    return vec.array[idx];
}

int main(){
    IntVector vec;

    std::cin >> vec.size;

    for(int i = 0; i < vec.size; i++){
        std::cin >> vec.array[i];
    }

    std::cout << getOnIndex(vec,2);
}