#include <iostream>

int main()
{
    int birthday;
    static int ns;
    std::string result[1000] = {};

    std::cout << "Enter your birthday:";
    std::cin >> birthday;
    std::cout << "Enter the number system:";
    std::cin >> ns; //Избираме в коя броична система да превърнем даденото число

    if(ns<2 || ns>16 || birthday<0){
        std::cout << "Please enter a valid number system/birthday.";
    } else{
        int index = 0;
        
        while(birthday>0){
            int num = birthday%ns;
            if(num>9){
                switch(num){ //Превръщаме остатъка в буква (ако остатъкът е по голям от 9)
                    case 10:
                    result[index]= "A";
                    break;
                    case 11:
                    result[index]= "B";
                    break;
                    case 12:
                    result[index]= "C";
                    break;
                    case 13:
                    result[index]= "D";
                    break;
                    case 14:
                    result[index]= "E";
                    break;
                    case 15:
                    result[index]= "F";
                    break;
                }
            } else{
                result[index]= std::to_string(num); //Записваме цифрата(остатъка) в array
            }
            
            birthday = birthday/ns;
            index++;
        }

        int size = sizeof(result)/sizeof(result[0]);
        std::string num;
        int a = 0;
        int b = size-1;

        while(a<b){ //Обръщаме редицата в обратен ред
            num = result[a];
            result[a]=result[b];
            result[b]=num;
            a++;
            b--;
        }

        while(result[0]=="0"){ //Понеже редицата има 1000 елемента, а поради обръщането и нашият отговор стои в края на редицата, махаме всички елементи(нули), които не са ни нужни
            for(int i=0;i<size;i++){
                result[i]=result[i+1];
            }
            size--;
        }

        std::cout << "Your number in " << ns << " number system is:";
        for(int i=0; i <size; i++){ // Извеждаме масива като редица от числа
            std::cout << result[i];
        }
    }
    return 0;
}