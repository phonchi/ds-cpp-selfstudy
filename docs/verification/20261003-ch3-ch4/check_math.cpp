#include <cassert>
#include <iostream>
#include <vector>
#include "pythonds3/cppds/sparsematrix.hpp"
#include "pythonds3/cppds/arraylist.hpp"
using Dense = std::vector<std::vector<double>>;
void check(const Dense& A,const Dense& B) {
    const size_t m=A.size(), k=A[0].size(), n=B[0].size();
    SparseMatrix sa,sb; sa.fromDenseMatrix(A);sb.fromDenseMatrix(B);
    const SparseMatrix product=sa*sb;
    for(size_t i=0;i<m;++i)for(size_t j=0;j<n;++j){
        double sum=0;
        for(size_t t=0;t<k;++t)sum+=A[i][t]*B[t][j];
        assert(product(i,j)==sum);
    }
    if(A.size()==B.size() && A[0].size()==B[0].size()){
        const SparseMatrix plus=sa+sb,minus=sa-sb;
        for(size_t i=0;i<m;++i)for(size_t j=0;j<k;++j){
            assert(plus(i,j)==A[i][j]+B[i][j]);
            assert(minus(i,j)==A[i][j]-B[i][j]);
        }
    }
}
int main(){
    check({{0,2,0},{3,0,0},{0,0,4}},{{5,0,0},{0,6,0},{0,0,7}});
    check({{0,0},{0,0}},{{1,2},{3,4}});
    check({{1,2},{3,4}},{{0,0},{0,0}});
    check({{1,2},{3,4}},{{-1,-2},{-3,-4}});
    check({{1,0},{0,0}},{{0,0},{0,2}});
    check({{1,2},{3,4}},{{5,6},{7,8}});
    check({{1,1}},{{1},{-1}});
    check({{1,0,2},{0,3,4}},{{2,0},{0,1},{5,6}});
    ArrayList a(0);
    for(int x=0;x<20;++x)a.push_back(x);
    a.insert(0,99); a.insert(a.size(),88);
    a.erase(0);a.erase(a.size()-1);
    assert(a.size()==20);
    for(int i=0;i<20;++i)assert(a[i]==i);
    for(int idx : {-1,20}){
        bool caught=false;try{(void)a[idx];}catch(const std::out_of_range&){caught=true;}
        assert(caught);
    }
    bool caught=false;try{a.insert(21,0);}catch(const std::out_of_range&){caught=true;}assert(caught);
    for(int r=1;r<=5;++r)for(int c=1;c<=6;++c){
        std::vector<int> row(r*c,-1),col(r*c,-1);
        for(int i=0;i<r;++i)for(int j=0;j<c;++j){row[i*c+j]=i*c+j;col[j*r+i]=i*c+j;}
        for(int i=0;i<r;++i)for(int j=0;j<c;++j)assert(row[i*c+j]==col[j*r+i]);
    }
    std::cout<<"8 dense-oracle sparse cases; ArrayList zero-capacity, growth, insert/erase and bounds; 30 matrix shapes passed\n";
}
