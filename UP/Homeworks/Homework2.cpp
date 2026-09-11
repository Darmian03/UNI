#include <iostream>

int sumCalories(int numbRations){
    int sum = 0;
    for(int j = 0; j < numbRations; j++){
        int calories = 0;
        std::cin >> calories;
        sum += calories;
    }

    return sum;
}

int main(){
    int numbElves = 0;
    std::cout << "Enter the number of the elves: ";
    std::cin  >> numbElves;

    int maxCalories = 0;
    int elf = 0;

    for(int i = 1; i <= numbElves; i++){
        int numbRations = 0;
        std::cout << "Enter the number of the elf's rations: ";
        std::cin  >> numbRations;

        int sum = sumCalories(numbRations);

        if(maxCalories < sum){
            elf = i;
            maxCalories = sum;
        }
    }

    std::cout << "Elf №" << elf << " has the most calories - " << maxCalories;
}