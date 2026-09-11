#include <iostream>

struct Vector3D{
    double x;
    double y;
    double z;
};

double length(const Vector3D& V){
    return sqrt(V.x*V.x + V.y*V.y + V.z*V.z);
}

double dotProduct(const Vector3D& V1, const Vector3D& V2){
    return V1.x*V2.x + V1.y*V2.y + V1.z*V2.z;
}

Vector3D CrossProduct(const Vector3D& V1, const Vector3D& V2){
    Vector3D v;
    v.x = V1.y*V2.z - V2.y*V1.z;
    v.y = V1.z*V2.x - V2.z*V1.x;
    v.z = V1.x*V2.y - V2.x*V1.y;
    return v;
}

double triple(const Vector3D& V1, const Vector3D& V2, const Vector3D& V3){
    return dotProduct(V1, CrossProduct(V2,V3));
}

void MultiplyByScalar(Vector3D& V, double scalar){
    std::cout << V.x*scalar;
    std::cout << V.y*scalar;
    std::cout << V.z*scalar;
}

void NormalizeVector(Vector3D& V){

}

Vector3D GetNegative(const Vector3D& V){
    Vector3D vec;
    vec.x = - V.x;
    vec.y = - V.y;
    vec.z = - V.z;
    return vec;
}

Vector3D Sum(const Vector3D& V1, const Vector3D& V2){
    Vector3D v;
    v.x = V1.x + V2.x;
    v.y = V1.y + V2.y;
    v.z = V1.z + V2.z;
    return v;
}

Vector3D Difference(const Vector3D& V1, const Vector3D& V2){
    Vector3D v;
    v.x = Sum(V1,V2).x - 2*GetNegative(V2).x;
    v.y = Sum(V1,V2).y - 2*GetNegative(V2).y;
    v.z = Sum(V1,V2).z - 2*GetNegative(V2).z;
    return v;
}

int main(){

}