#include <iostream>

struct Tamagotchi{
    char name[20];
};

void readTamagotchi(Tamagotchi name);

int main(){
    Tamagotchi x;
    std::cin.getline(x.name, 20);

    readTamagotchi(x);
}

void readTamagotchi(Tamagotchi x){
    std::cout << "The name is: " << x.name;
}