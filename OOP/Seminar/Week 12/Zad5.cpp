#include <iostream>
#include <string.h>

struct Traveler{
    char name[20];
    int energy;
    char action[20];
    int hours;

    void printStatus(){
        std::cout << "Your name is: " << name << std::endl;
        if(strcmp(action, "sleep") == 0){
            sleep(hours);
        }
        else if(strcmp(action, "speak") == 0){
            speak(energy);
        }
    }

    void sleep(int hours){
        energy += 8*hours;
        if(energy > 100){
            energy = 100;
        }

        std::cout << "You are well rested with " << energy << " energy!";
    }

    void speak(int energy){
        int i = 0;
        char arr[60] = {"Hi, how are you?"};
        while(energy > 0){
            std::cout << arr[i];
            i++;
            energy -= 2;
        }
        std::cout << std::endl;
        std::cout << "Your remaining energy is: " << energy << std::endl;
    }
};

int main(){
    Traveler x;
    std::cout << "Please enter your name: ";
    std::cin.getline(x.name, 20);
    std::cout << "Please choose action (sleep or speak): ";
    std::cin.getline(x.action, 20);
    std::cout << "What are your levels of eneregy: ";
    std::cin >> x.energy;

    if(strcmp(x.action, "sleep") == 0){
        std::cout << "How many hours should I sleep? ";
        std::cin >> x.hours;
    }

    x.printStatus();
}