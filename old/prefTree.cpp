#include <iostream>
#include <string>
#include <fstream>
#include <vector>
#include "eDist.h"

using namespace std;


////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

// basic helpers

// WORKS
// string without caps or punctuation
extern "C" string simplifyStr(string str){
    string newStr;
    for(int i=0;i<str.length();i++){
        if(str[i]>64 && str[i]<91) newStr += str[i]+32;
        else if(str[i]>96 && str[i]<123) newStr += str[i];
        else if(str[i]==95||str[i]==33) newStr += str[i];
        else continue;
    }
    return newStr;
}

// checks if two strings are equal up to the short one's length
extern "C" bool namesEq(string curName, string newName){
    for(int i=0;i<newName.length();i++){
        if(curName[i]!=newName[i]) return false;
    }
    return true;
}

// return true for left child, false for right child; left child is lower, right child is higher
// if they're the same to a point, smaller goes left, bigger goes right
extern "C" bool LoR(string curName, string newName){
    int maxLen;
    string C = simplifyStr(curName);
    string N = simplifyStr(newName);
    if(C.length()<N.length()) maxLen = N.length();
    else maxLen = C.length();
    int i=0;
    while(i<maxLen){
        if(C[i]>N[i]) return true;
        else if(C[i]<N[i]) return false;
        else i++;
    }
    if(C.length()>N.length()) return true;
    return false;
}

// WORKS
// checks if a name can be a subnode
extern "C" char childLRES(string curName, string newName, int level){
    string N = simplifyStr(newName);
    string C = simplifyStr(curName);
    if(N.length()<level) return 'S'; // special case -- return S, for short; so it sets its level to its length
    else if(N[level]<C[level]) return 'L'; // return L if left
    else if(N[level]>C[level]) return 'R'; // R if right
    else if(N[level]==C[level]) return 'E'; // special case -- return E, for equal
                                                            // this is so it doesn't increment its level
    return '0';
}

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

//Structs

// WORKS
// Node struct
extern "C" typedef struct node{
    int level;
    string name;
    //string* data = new string[7];
    node* LChild;
    node* RChild;
} node;

// WORKS
// Quick fn to generate a new node given input
//node* newNode(string Name, string* Data){
extern "C" node* newNode(string Name){
    node* newnode = new node;
    newnode->name = Name;
    newnode->LChild = NULL;
    newnode->RChild = NULL;
    //node->data = Data;
    return newnode;
}

// WORKS
// results struct for similarity search
extern "C" typedef struct topRes{
    string name;
    int edit = -1;
} topRes;


////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

// topRes helpers

// WORKS
// finds the max result from topRes array
extern "C" int findMax(topRes* results, int n){
    int max = -1;
    int idx = -1;
    for(int i=0;i<n;i++){
        if(results[i].edit<0){
            return i;
        }
        else if(results[i].edit>max){
            idx = i;
        }
    }
    return idx;
}

// WORKS
// swap elements
extern "C" void swap(topRes* y, topRes* x){
    topRes temp = *x;
    *x = *y;
    *y = temp;
}

// WORKS
// sorts results of a topRes array
extern "C" string sortResults(topRes* results, int n){
    for(int i=0;i<n;i++){
        int min_idx = i;
        for(int j=0;j<n;j++){
            if(results[j].edit<results[min_idx].edit){
                min_idx = j;
                swap(&results[min_idx],&results[i]);
            }
        }
    }
    string strResults;
    for(int i=0;i<n;i++){
        strResults += results[i].name;
        if(i<n-1) strResults+= ", ";
    }
    return strResults;
}


////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

// node functions

// addChild adds children to tree
extern "C" bool addChild(node* root, node* newnode){
    if(root->name == newnode->name) return false;
    if(LoR(root->name,newnode->name)){
        if(root->LChild) return addChild(root->LChild,newnode);
        root->LChild = newnode;
        return true;
    }
    else{
        if(root->RChild) return addChild(root->RChild,newnode);
        root->RChild = newnode;
        return true;
    }
    return false;
}

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

// search for a name
extern "C" node* search(node* root, string cname){
    string C = simplifyStr(cname);
    string R = simplifyStr(root->name);
    if(R == C) return root;
    else if(LoR(R,C)){
        if(!root->LChild) return NULL;
        return search(root->LChild,cname);
    }
    else{
        if(!root->RChild) return NULL;
        return search(root->RChild,cname);
    }
    return NULL;
}

// find a node and get its information as string
extern "C" string findAndPrint(node* root, string cname){
    node* foundCard = search(root, cname);
    if(foundCard == NULL){
        return "No card found";
    }
    string cardData = foundCard->name;
    /*for(int i=0;i<7;i++){
        if(!foundCard->data[i].empty()) cardData += '\n';
        cardData += foundCard.data[i];
    }*/
    return cardData;
}

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/*
// TESTED AND WORKS
// find similar names
extern "C" void findSimilar(node* root, string cname, topRes* results, int n){
    for(int i=0;i<root->children.size();i++){
        findSimilar(root->children.at(i), cname, results, n);
    }
    if(root->name.empty()){
        return;
    }
    string R = simplifyStr(root->name);
    string C = simplifyStr(cname);
    int dist = eDist(R,C,R.length(),C.length());
    int maxIdx = findMax(results, n);
    if(results[maxIdx].edit<0 || results[maxIdx].edit>dist){
        results[maxIdx].name = root->name;
        results[maxIdx].edit = dist;
    }
}

// TESTED AND WORKS
// find all similar names
extern "C" string findAllSim(node* root, string cname, int n){
    topRes* results = new topRes[n];
    for(int i=0;i<n;i++){
        results[n].edit = -1;
    }
    findSimilar(root,cname,results,n);
    return sortResults(results, n);
}*/

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

// TESTED AND WORKS
// read in file and make nodes
extern "C" void readInNodes(string fname, node* root){
    string cardName;
    ifstream inFile(fname);
    int i = 0;
    while(getline(inFile, cardName)){
        try { addChild(root,newNode(cardName)); }
        catch ( exception& e ) { cerr << "Failed to add " << cardName << "; had an " << e.what() << endl; }
    }
    //cout << i << endl;
}

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

/*// prints all children one by one
extern "C" void printAllChildren(node* root){
    for(int i=0;i<root->children.size();i++){
        cout << root->name << endl;
        printAllChildren(root->children.at(i));
    }
}
*/
extern "C" string fromFile(string fname){
    string cardName;
    string allCards;
    ifstream inFile(fname);
    while(getline(inFile, cardName)){
        allCards += cardName + '\n';
    }
    return allCards;
}

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

int main(){

    node* root = newNode("!");
    //string cards = fromFile("allCards.txt");
    //cout << cards;
    readInNodes("allCards.txt",root);
    //printAllChildren(root);
    string tower = findAndPrint(root,"Phyrexian tower");
    cout << tower << endl;
    /*tower = findAndPrint(root,"Phyrexian Tower");
    cout << tower << endl;
    //string towersimil = findAllSim(root,"phyrexin twoer",7);
    //cout <<  towersimil << endl;
    printAllChildren(root);*/

    return 0;
}