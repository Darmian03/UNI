#include <iostream>

struct Boss{
    char name[1024];
    double payment;
};

struct Worker{
    char name[1024];
    double payment;
    Boss B;
};

struct Team{
    char name[1024];
    Worker workers[99];
    int numbers;
};

struct Company{
    char name[1024];
    Team teams[49];
    int numbers;
};

bool workerCheck(Worker W, Company C){
    for(int i=0; i < C.numbers; i++){
        for(int j = 0; j < C.teams[i].numbers; j++){
            if(W.name == C.teams[i].workers[j].name){
                return true;
            }
        }
    }
    return false;
}

int main(){

}