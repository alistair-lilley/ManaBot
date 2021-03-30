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
        if(str[i]>64 && str[i]<91){
            newStr += str[i]+32;
        }
        else if(str[i]>96 && str[i]<123){
            newStr += str[i];
        }
        else continue;
    }
    return newStr;
}

// WORKS
// checks if a name can be a subnode
extern "C" bool canBeSub(string curName, string newName, int level){
    if(newName.length() < level) return false;
    for(int i=0;i<level;i++){
        if(curName[i] != newName[i]){
            return false;
        }
    }
    return true;
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
    vector<node *>children;
} node;

// WORKS
// Quick fn to generate a new node given input
//node* newNode(string Name, string* Data){
extern "C" node* newNode(string Name){
    node* newnode = new node;
    newnode->name = Name;
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

// TESTED AND WORKS
// Add child to node tree
extern "C" bool addChild(node* root, node* newnode){
    node* temp = NULL;
    for(int i=0;i<root->children.size();i++){
        node* temp = root->children.at(i); // set temp node for code readability
        // gets if the names are identical; returns false
        if(temp->name == newnode->name){
            return false;
        }
        // If it can alphabetically go below temp, do it
        else if(canBeSub(simplifyStr(temp->name), simplifyStr(newnode->name), temp->level)){
            return addChild(temp,newnode);
        }
    }
    // make sure the level is incremented
    newnode->level = root->level + 1;
    // Add the child to the node children
    root->children.push_back(newnode);
    return true;
}

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

// TESTED AND WORKS
// search for a name
extern "C" node* search(node* root, string cname){
    string C = simplifyStr(cname);
    string R = simplifyStr(root->name);
    if(R == C){
        return root;
    }
    node* temp = NULL;
    for(int i=0;i<root->children.size();i++){
        temp = root->children.at(i);
        string T = simplifyStr(temp->name);
        if(C == T){
            return temp;
        }
        else if(canBeSub(T,C,temp->level)){
            return search(temp,cname);
        }
    }
    return NULL;
}

// TESTED AND WORKS
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
}

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

// TESTED AND WORKS
// read in file and make nodes
extern "C" void readInNodes(string fname, node* root){
    string cardName;
    ifstream inFile(fname);
    int i = 0;
    while(getline(inFile, cardName)){
        i++;
        node* newnode = newNode(cardName);
        addChild(root,newnode);
    }
}

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

// TESTED AND WORKS
// prints all children one by one
extern "C" void printAllChildren(node* root){
    for(int i=0;i<root->children.size();i++){
        cout << root->name << endl;
        printAllChildren(root->children.at(i));
    }
}

extern "C" string fromFile(string fname){
    string cardName;
    string allCards;
    ifstream inFile(fname);
    while(getline(inFile, cardName)){
        allCards += cardName + '\n';
    }
}

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

int main(){

    node* root = newNode("");
    readInNodes("allCards.txt",root);
    //printAllChildren(root);
    string tower = findAndPrint(root,"Phyrexian grimoire");
    cout << tower << endl;
    tower = findAndPrint(root,"Phyrexian Tower");
    cout << tower << endl;
    //string towersimil = findAllSim(root,"phyrexin twoer",7);
    //cout <<  towersimil << endl;
    printAllChildren(root);

    return 0;
}