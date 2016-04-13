#include<bits/stdc++.h>
using namespace std;
int main(){
    ios_base::sync_with_stdio(false);
    long long t,p,q,n;
    string s;
    cin>>t;
    while(t--){
        cin>>s;
        map<char ,long long> juggad;
        juggad['a']=0;
        juggad['b']=0;
        juggad['c']=0;
        juggad['d']=0;
        juggad['e']=0;
        juggad['f']=0;
        juggad['g']=0;
        juggad['h']=0;
        juggad['i']=0;
        juggad['j']=0;
        juggad['k']=0;
        juggad['l']=0;
        juggad['m']=0;
        juggad['n']=0;
        juggad['o']=0;
        juggad['p']=0;
        juggad['q']=0;
        juggad['r']=0;
        juggad['s']=0;
        juggad['t']=0;
        juggad['v']=0;
        juggad['w']=0;
        juggad['x']=0;
        juggad['y']=0;
        juggad['z']=0;
        for(int i=0;i<s.length();i++){
            juggad[s[i]]++;
        }
        cin>>p>>q;
        map<char,long long>::iterator it;
        for(it=juggad.begin();it!=juggad.end();it++){
            it->second = it->second*p;
        }
        while(q--){
            cin>>n;
            it = juggad.begin();
            while(it!=juggad.end() && n>0){
                n = n-it->second;
                if(n>0)it++;
            }
            if(it==juggad.end() && n>0){
                cout<<"-1"<<endl;
            }else{
                cout<<it->first<<endl;
            }
        }
    }
    return 0;
}
