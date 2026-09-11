#include <iostream>

struct Tamagotchi{
    char name[20];

    void printStatus(){
        std::cout << "The name is: " << name;
    }
};

int main(){
    Tamagotchi x;
    std::cin.getline(x.name, 20);

    x.printStatus();
}