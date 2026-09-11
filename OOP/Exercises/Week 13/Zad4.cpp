#include <iostream>

struct DynArray{
    int size;
    int *array = new int[size];
};

DynArray merge(DynArray a1, DynArray a2){
    DynArray array;
    array.size = a1.size + a2.size;

    for(int i = 0; i < a1.size; i++){
        array.array[i] = a1.array[i];
    }
    for(int i = a1.size; i < array.size; i++){
        array.array[i] = a2.array[i-a1.size];
    }

    return array;
};

int main(){
    
}