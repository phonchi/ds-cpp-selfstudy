#include <iostream>
#include "pythonds3/cppds/sparsematrix.hpp"
int main() {
    SparseMatrix m;
    m(0, 1) = 2;
    const SparseMatrix& view = m;
    std::cout << view(0, 1) << ' ' << view(7, 7) << '\n'; // 讀到 2 與 0
    std::cout << m.nnz() << '\n';    // 仍只有 (0,1) 這一項
    double x = m(5, 5);             // 非 const 版本：插入 (5,5):0
    std::cout << x << ' ' << m.nnz() << '\n';
}
