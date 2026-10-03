"""Standalone C++17 sparse matrix teaching examples and exact outputs."""

EXAMPLES = {
    'coo': (r'''#include <algorithm>
#include <iostream>
#include <stdexcept>
#include <tuple>
#include <vector>

struct COO {
    int rows, cols;
    std::vector<int> row, col;
    std::vector<double> val;
    COO(int r, int c) : rows(r), cols(c) {}
    // Call in increasing (row, col) order, with unique coordinates.
    void append(int r, int c, double v) {
        if (v != 0) { row.push_back(r); col.push_back(c); val.push_back(v); }
    }
    COO combine(const COO& b, double sign) const {
        if (rows != b.rows || cols != b.cols)
            throw std::invalid_argument("shape mismatch");
        COO out(rows, cols);
        std::size_t i = 0, j = 0;
        while (i < val.size() || j < b.val.size()) {
            if (j == b.val.size() || (i < val.size() &&
                std::tie(row[i], col[i]) < std::tie(b.row[j], b.col[j]))) {
                out.append(row[i], col[i], val[i]); ++i;
            } else if (i == val.size() ||
                std::tie(b.row[j], b.col[j]) < std::tie(row[i], col[i])) {
                out.append(b.row[j], b.col[j], sign * b.val[j]); ++j;
            } else {
                out.append(row[i], col[i], val[i] + sign * b.val[j]);
                ++i; ++j;
            }
        }
        return out;
    }
    COO operator+(const COO& b) const { return combine(b, 1); }
    COO operator-(const COO& b) const { return combine(b, -1); }
    COO operator*(const COO& b) const {
        if (cols != b.rows) throw std::invalid_argument("shape mismatch");
        COO out(rows, b.cols);
        if (val.empty() || b.val.empty()) return out;
        std::vector<std::tuple<int, int, double>> products;
        for (std::size_t i = 0; i < val.size(); ++i)
            for (std::size_t j = 0; j < b.val.size(); ++j)
                if (col[i] == b.row[j])
                    products.emplace_back(row[i], b.col[j], val[i] * b.val[j]);
        std::sort(products.begin(), products.end(), [](const auto& x, const auto& y) {
            return std::tie(std::get<0>(x), std::get<1>(x)) <
                   std::tie(std::get<0>(y), std::get<1>(y));
        });
        std::size_t i = 0;
        while (i < products.size()) {
            int r = std::get<0>(products[i]), c = std::get<1>(products[i]);
            double sum = 0;
            do {
                sum += std::get<2>(products[i++]);
            } while (i < products.size() && std::get<0>(products[i]) == r &&
                     std::get<1>(products[i]) == c);
            out.append(r, c, sum);
        }
        return out;
    }
    void print() const {
        for (std::size_t i = 0; i < val.size(); ++i)
            std::cout << '(' << row[i] << ',' << col[i] << "):" << val[i] << ' ';
        std::cout << '\n';
    }
};
int main() {
    COO a(3, 3), b(3, 3);
    a.append(0, 1, 2); a.append(1, 0, 3); a.append(2, 2, 4);
    b.append(0, 0, 5); b.append(1, 1, 6); b.append(2, 2, 7);
    (a + b).print(); (a - b).print(); (a * b).print();
}
''', '(0,0):5 (0,1):2 (1,0):3 (1,1):6 (2,2):11 \n(0,0):-5 (0,1):2 (1,0):3 (1,1):-6 (2,2):-3 \n(0,1):12 (1,0):15 (2,2):28 \n'),
    'dok': (r'''// pythonds3/cppds/sparsematrix.hpp -- Dictionary-Of-Keys sparse matrix (Chapter 3)
#ifndef DSCPP_SPARSEMATRIX_HPP
#define DSCPP_SPARSEMATRIX_HPP
#include <iostream>
#include <map>
#include <vector>
using namespace std;

class SparseMatrix {
    public:
        SparseMatrix() {}
        SparseMatrix(map<pair<size_t, size_t>, double> d) { data = d; }
        void fromDenseMatrix(const vector<vector<double>>& matrix) {
            for (size_t i = 0; i < matrix.size(); ++i)
                for (size_t j = 0; j < matrix[i].size(); ++j)
                    if (matrix[i][j] != 0) data[{i, j}] = matrix[i][j];
        }
        double& operator()(size_t i, size_t j) { return data[{i, j}]; }
        bool operator==(const SparseMatrix& other) const {
            return data == other.data;
        }
        bool operator!=(const SparseMatrix& other) const {
            return !(*this == other);
        }
        double sparsity(size_t rows, size_t cols) const {
            return 1.0 - double(data.size()) / double(rows * cols);
        }
        size_t nnz() const {
            return data.size();   // stored entries; zero values may also be stored
        }
        SparseMatrix operator+(const SparseMatrix& other) const {
            SparseMatrix result;
            for (const auto& item : data) {
                auto found = other.data.find(item.first);
                double rhs = found != other.data.end() ? found->second : 0.0;
                result.data[item.first] = item.second + rhs;
            }
            for (const auto& item : other.data)
                if (data.find(item.first) == data.end()) result.data[item.first] = item.second;
            return result;
        }
        SparseMatrix operator-(const SparseMatrix& other) const {
            SparseMatrix result;
            for (const auto& item : data) {
                auto found = other.data.find(item.first);
                double rhs = found != other.data.end() ? found->second : 0.0;
                result.data[item.first] = item.second - rhs;
            }
            for (const auto& item : other.data)
                if (data.find(item.first) == data.end()) result.data[item.first] = -item.second;
            return result;
        }
        SparseMatrix operator*(const SparseMatrix& other) const {
            SparseMatrix result;
            for (const auto& item1 : data)
                for (const auto& item2 : other.data)
                    if (item1.first.second == item2.first.first)
                        result(item1.first.first, item2.first.second) += item1.second * item2.second;
            return result;
        }
        friend ostream& operator<<(ostream& os, const SparseMatrix& m) {
            for (const auto& item : m.data)
                os << "(" << item.first.first << ", " << item.first.second << "): " << item.second << "  ";
            return os;
        }
    private:
        map<pair<size_t, size_t>, double> data;
};
#endif

int main() {
    SparseMatrix a({{{0, 1}, 2}, {{1, 0}, 3}, {{2, 2}, 4}});
    SparseMatrix b({{{0, 0}, 5}, {{1, 1}, 6}, {{2, 2}, 7}});
    std::cout << a + b << '\n' << a - b << '\n' << a * b << '\n';
}
''', '(0, 0): 5  (0, 1): 2  (1, 0): 3  (1, 1): 6  (2, 2): 11  \n(0, 0): -5  (0, 1): 2  (1, 0): 3  (1, 1): -6  (2, 2): -3  \n(0, 1): 12  (1, 0): 15  (2, 2): 28  \n'),
    'linear': (r'''#include <iostream>
#include <map>
#include <stdexcept>
#include <tuple>
#include <utility>

struct Node {
    int row, col;
    double value;
    Node* next;
};
class Linear {
    int rows, cols;
    Node* head = nullptr;
    Node* tail = nullptr;
public:
    Linear(int r, int c) : rows(r), cols(c) {}
    ~Linear() {
        while (head) { Node* old = head; head = head->next; delete old; }
    }
    Linear(const Linear&) = delete;
    Linear& operator=(const Linear&) = delete;
    Linear(Linear&& other) noexcept
        : rows(other.rows), cols(other.cols), head(other.head), tail(other.tail) {
        other.head = other.tail = nullptr;
    }
    // Call in increasing (row, col) order, with unique coordinates.
    void append(int r, int c, double v) {
        if (v == 0) return;
        Node* node = new Node{r, c, v, nullptr};
        if (tail) tail->next = node;
        else head = node;
        tail = node;
    }
    Linear combine(const Linear& b, double sign) const {
        if (rows != b.rows || cols != b.cols)
            throw std::invalid_argument("shape mismatch");
        Linear out(rows, cols);
        const Node* p = head;
        const Node* t = b.head;
        while (p || t) {
            if (!t || (p && std::tie(p->row, p->col) < std::tie(t->row, t->col))) {
                out.append(p->row, p->col, p->value); p = p->next;
            } else if (!p || std::tie(t->row, t->col) < std::tie(p->row, p->col)) {
                out.append(t->row, t->col, sign * t->value); t = t->next;
            } else {
                out.append(p->row, p->col, p->value + sign * t->value);
                p = p->next; t = t->next;
            }
        }
        return out;
    }
    Linear operator+(const Linear& b) const { return combine(b, 1); }
    Linear operator-(const Linear& b) const { return combine(b, -1); }
    Linear operator*(const Linear& b) const {
        if (cols != b.rows) throw std::invalid_argument("shape mismatch");
        Linear out(rows, b.cols);
        if (!head || !b.head) return out;
        std::map<std::pair<int, int>, double> acc;
        for (const Node* p = head; p; p = p->next)
            for (const Node* t = b.head; t; t = t->next)
                if (p->col == t->row)
                    acc[{p->row, t->col}] += p->value * t->value;
        for (const auto& item : acc)
            out.append(item.first.first, item.first.second, item.second);
        return out;
    }
    void print() const {
        for (const Node* p = head; p; p = p->next)
            std::cout << '(' << p->row << ',' << p->col << "):" << p->value << ' ';
        std::cout << '\n';
    }
};
int main() {
    Linear a(3, 3), b(3, 3);
    a.append(0, 1, 2); a.append(1, 0, 3); a.append(2, 2, 4);
    b.append(0, 0, 5); b.append(1, 1, 6); b.append(2, 2, 7);
    (a + b).print(); (a - b).print(); (a * b).print();
}
''', '(0,0):5 (0,1):2 (1,0):3 (1,1):6 (2,2):11 \n(0,0):-5 (0,1):2 (1,0):3 (1,1):-6 (2,2):-3 \n(0,1):12 (1,0):15 (2,2):28 \n'),
}
