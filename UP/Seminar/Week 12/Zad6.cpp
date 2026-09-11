#include <iostream>
#include <string.h>

struct Traveler{
    char name[20];
    int energy;
    char action[20];
    int hours;
    int attackPower;

    void printStatus(){
        if(strcmp(action, "sleep") == 0){
            sleep(hours);
        }
        else if(strcmp(action, "speak") == 0){
            speak(energy);
        }
        else if(strcmp(action, "fight") == 0 && energy >= 10){
            fight(attackPower, energy);
        }
        else if(strcmp(action, "fight") == 0 && energy < 10){
            std::cout << "Looks like you are tired champ. Rest a little.";
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

    void fight(int attackPower, int energy){
        int enemy = rand()%1000 + 1;
        if(energy > 100){
            energy = 100;
        }
        attackPower += energy;
        if(enemy == attackPower){
            std::cout << "Wow! It's a draw!";
            attackPower -= 50;
        }
        else if(enemy >= attackPower){
            std::cout << "Retreat!";
            attackPower -= 100;
        }
        else if(enemy <= attackPower){
            std::cout << "Good job! You won!";
        }
        energy -= 40;
        if(energy < 0){
            energy = 0;
        }
    }
};

int main(){
    Traveler x;
    int actions = 1;
    std::cout << "Please enter your name: ";
    std::cin.getline(x.name, 20);
    std::cout << "What are your levels of eneregy: ";
    std::cin >> x.energy;
    std::cout << "What is your attack power? ";
    std::cin >> x.attackPower;
    std::cout << "How many actions do you want to make? ";
    std::cin >> actions;

    for(int i = 0; i <= actions; i++){
        std::cout << "Please choose action (sleep, speak or fight): ";
        std::cin.getline(x.action, 20);

        if(strcmp(x.action, "sleep") == 0){
            std::cout << "How many hours should I sleep? ";
            std::cin >> x.hours;
        }

        x.printStatus();
        std::cout << std::endl;
    }
}