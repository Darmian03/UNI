#include <iostream>

struct Tamagotchi{
    char name[20];
    int energy;

    void printStatus(){
        std::cout << "Your name is: " << name << std::endl;
        std::cout << "Your energy is: " << energy << std::endl;
    }
};

int main(){
    Tamagotchi x;
    std::cin.getline(x.name, 20);
    std::cin >> x.energy;

    x.printStatus();
}