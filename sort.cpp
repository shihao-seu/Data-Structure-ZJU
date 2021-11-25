/*=============================================================================
#  Author:           shihao - https://github.com/shihao-seu
#  Email:            shihao10Civil@163.com
#  FileName:         test.cpp
#  Description:      十种排序算法实现及对比
#  Version:          0.0.1
#  CreatingDate:     2021-Nov-Thu
#  History:          None
=============================================================================*/

#include <iostream>
#include <algorithm>
#include <iterator>
#include <typeinfo>  // std::is_integral
#include <type_traits>
#include <memory>
#include <vector>
#include <string>
#include <queue>
#include <map>
#include <stack>
#include <iomanip>  // 格式化打印
#include <random>
#include <sys/time.h>  // gettimeofday
#include <ctime>

/* Remove if already defined */
typedef long long int64; 
typedef unsigned long long uint64;

/* Returns the amount of milliseconds elapsed since the UNIX epoch. */
uint64 GetTimeMs64()
{
    struct timeval tv;
    gettimeofday(&tv, NULL);

    uint64 ret = tv.tv_usec;
    /* Convert from micro seconds (10^-6) to milliseconds (10^-3) */
    ret /= 1000;

    /* Adds the seconds (10^0) after converting them to milliseconds (10^-3) */
    ret += (tv.tv_sec * 1000);

    return ret;
}

using namespace std;

template< class RandomIt >
void bubblesort( RandomIt first, RandomIt last ) {
    while (last-first > 1) {
        int count = 0;
        for (RandomIt it = first; it != last-1; ++it) {
            if (*it > *(it+1)) {
                std::swap(*it, *(it+1));
                ++count;
            }    
        }
        if ( !count )
            return; // 若本轮没有出现交换，说明已经为有序数列
        --last;
    }
}

template< class RandomIt >
void selectionsort( RandomIt first, RandomIt last ) {
    while (last-first > 1) {
        RandomIt imax = first; // 记录每次循环时的最值位置
        for (RandomIt it = first+1; it != last; ++it) {
            if (*it > *imax)
                imax = it;
        }
        std::swap(*imax, *(last-1));
        --last;
    }
}

template< class RandomIt >
void insertionsort( RandomIt first, RandomIt last ) {
    RandomIt head = first;
    while ( ++head != last) {
        typename std::iterator_traits<RandomIt>::value_type insv = *head;
        RandomIt it = head;
        // 待插入值前进，有序值都向后退一
        for (; it > first && *(it-1) > insv; --it)
            *it = *(it-1);
        *it = insv; // 插入值落地
    }
}

template< class RandomIt >
void shellsort( RandomIt first, RandomIt last ) {
    // 确定步长，只要最终缩小到1即可
    typename std::iterator_traits<RandomIt>::difference_type size = last - first;
    for (auto h = size/2; h > 0; h /= 2) {
        RandomIt lead = first; // 每一组的头部
        while (lead < first + h) {
            RandomIt head = lead + h;
            while ( head < last ) {
                auto insv = *head;
                RandomIt it = head;
                for (; it > lead && *(it-h) > insv; it -= h )
                    *it = *(it-h);
                *it = insv;
                head += h;
            }
            ++lead;
        }
    }
}

template< class RandomIt >
void shellsort2( RandomIt first, RandomIt last ) {
    auto size = last - first;
    for (auto h = size/2; h > 0; h /= 2) {
        RandomIt head = first + h;
        while (head < last) {
            auto insv = *head;
            RandomIt it = head;
            // it从第二排开始，因此要> first+h-1
            for (; it > first+h-1 && *(it-h) > insv; it -= h ) {
                *it = *(it-h);
            }
            *it = insv;
            ++head;
        }
    }
}

// 采用手摇算法原地合并，空间复杂度O(1), 时间复杂度O(N)
template< class RandomIt >
void merge_in_place( RandomIt first, RandomIt mid, RandomIt last ) {
    while (first < mid && mid < last) {
        if (*first <= *mid)
            ++first;
        else {
            RandomIt end = mid;
            while ( end < last && *end < *first)
                ++end;
            // 将区间[first, mid) [mid, end)左旋转
            std::reverse(first, mid);
            std::reverse(mid, end);
            std::reverse(first, end);
            first += end - mid;
            mid = end;
        }
    }
}

template< class RandomIt >
void merge_out_of_place( RandomIt first, RandomIt mid, RandomIt last ) {  
    typedef typename iterator_traits<RandomIt>::difference_type Diff;
    typedef typename iterator_traits<RandomIt>::value_type VALUE;
    
    Diff size = last - first;
#if defined __clang__
    vector<VALUE> temp(size);
#else
    VALUE temp[size] = {}; // gcc supports variable-sized array
#endif
    size_t index = 0;

    RandomIt it1 = first, it2 = mid;
    while (it1 < mid && it2 < last)
        temp[index++] = (*it2 < *it1) ? *it2++ : *it1++;
    while (it1 < mid)
        temp[index++] = *it1++;
    while (it2 < last)
        temp[index++] = *it2++;
#if defined __clang__
    copy(temp.begin(), temp.end(), first);
#else
    copy(temp, temp+size, first);
#endif
}

template< class RandomIt >
void mergesort_recursion( RandomIt first, RandomIt last ) {
    auto size = last - first;
    if (size < 2) return;
    RandomIt mid = first + size/2;
    mergesort_recursion(first, mid);
    mergesort_recursion(mid, last);
    // return merge_inplace(first, mid, last);
    return merge_out_of_place(first, mid, last);
}

template< class RandomIt >
void mergesort_iteration( RandomIt first, RandomIt last ) {
    typedef typename iterator_traits<RandomIt>::difference_type Diff;
    typedef typename iterator_traits<RandomIt>::value_type VALUE;
    Diff size = last - first;
    if (size < 2) return;

#if defined __clang__
    vector<VALUE> temp(size);
#else
    VALUE temp[size] = {}; // 辅助空间
#endif

    // 1. 划定小区间最大长度h，从2开始, 直到size < h/2为止
    for (Diff h = 2; h < 2*size ; h *= 2) { 
        RandomIt beg = first;
        // 2. 确定小区间[beg, mid)和[mid, end)
        while (beg + h/2 < last) { 
            RandomIt mid = beg + h/2;
            RandomIt end = (beg+h < last) ? beg+h : last;
            // 3. 两个小区间都已有序，交叉对比拷贝到temp;
            size_t index = static_cast<size_t>(beg-first);
            RandomIt it1 = beg, it2 = mid;
            while (it1 < mid && it2 < end)
                temp[index++] = (*it2 < *it1) ? *it2++ : *it1++;
            while (it1 < mid)
                temp[index++] = *it1++;
            while (it2 < end)
                temp[index++] = *it2++;
            //4. 两小区间已合并，拷贝回原数组
#if defined __clang__
            copy(temp.begin()+(beg-first), temp.begin()+index, beg);
#else
            copy(temp+(beg-first), temp+index, beg);
#endif
            beg = end;
        }
    }
}

// fast-slow two pointers快慢双指针法
template< class RandomIt >
RandomIt partition1( RandomIt first, RandomIt last ) {
    auto pivot = *first;
    RandomIt quick = first+1, slow = first;
    for (; quick < last; ++quick) {
        if (*quick <= pivot) {
            ++slow;
            swap(*quick, *slow);
        }
    }
    swap(*first, *slow);
    return slow;
}

template< class RandomIt >
// collision pointers对撞双指针
RandomIt partition2( RandomIt first, RandomIt last ) {
    // 本例中枢值选择第一个元素，也可以选择随机元素
    auto pivot = *first;
    RandomIt left = first+1, right = last-1;
    while (left <= right) { // left和right可能指向同一个值
        while (left < last && *left <= pivot)
            ++left;
        while (*right > pivot)
            --right;
        if (left < right) {
            swap(*left, *right);
            ++left;
            --right;
        }
    } 
    swap(*right, *first);
    return right;
}

template< class RandomIt >
void quicksort_recursion( RandomIt first, RandomIt last ) {
    typedef typename iterator_traits<RandomIt>::difference_type Diff;
    Diff size = last - first;
    if (size < 2) return;

    RandomIt pivot = partition1(first, last);
    quicksort_recursion(first, pivot);
    quicksort_recursion(pivot+1, last);
}

template< class RandomIt >
void quicksort_iteration( RandomIt first, RandomIt last ) {
    typedef typename iterator_traits<RandomIt>::difference_type Diff;

    // 非递归方法需要手动维护递归中的函数调用栈
    std::stack<std::pair<RandomIt, RandomIt>> s;
    s.push(make_pair(first, last));

    while ( !s.empty() ) {
        RandomIt beg = s.top().first, end = s.top().second;
        s.pop();

        Diff size = end - beg;
        if (size < 2)
            continue;

        RandomIt pivot = partition1(beg, end);
        s.push(make_pair(beg, pivot));
        s.push(make_pair(pivot+1, end));
    }
}

int g_min = 0, g_max = 0;
template< class RandomIt >
void countingsort( RandomIt first, RandomIt last ) {
    // 已知该组整数的范围是: [min, max]
    typedef typename iterator_traits<RandomIt>::value_type VALUE;
    static_assert(std::is_integral<VALUE>::value, "Integral required !!!");

    const int span = g_max - g_min + 1;
#ifdef __clang__
    vector<int> C(span);
    vector<VALUE> temp(last-first);
#else
    int C[span] = {}; // ！有溢栈的风险
    VALUE temp[last - first] = {};
#endif

    for (RandomIt it = first; it != last; ++it)
        ++C[*it - g_min];
        
    for (size_t i = 1; i < span; ++i)
        C[i] += C[i-1];
    
    for (RandomIt it = last-1; it >= first; --it)
        temp[--C[*it-g_min]] = *it;
#ifdef __clang__
    copy(temp.begin(), temp.begin()+(last-first), first);
#else
    copy(temp, temp+(last-first), first);
#endif
}

template< class RandomIt >
void bucketsort( RandomIt first, RandomIt last ) {
    typedef typename iterator_traits<RandomIt>::value_type VALUE;
    static_assert(std::is_integral<VALUE>::value, "Integral required !!!");

    const int BUCKET_BASE = 50;
    const int BUCKET_NUM = g_max / BUCKET_BASE + 1;
    vector<vector<int>> bucks(BUCKET_NUM);
    vector<VALUE> temp;

    for (RandomIt it = first; it != last; ++it)
        bucks[*it / BUCKET_BASE].push_back(*it);
    for (int i = 0; i < BUCKET_NUM; ++i) {
        if ( !bucks[i].empty() ) {
            std::sort(bucks[i].begin(), bucks[i].end());
            temp.insert(temp.end(), bucks[i].begin(), bucks[i].end());
        }
    }
    copy(temp.begin(), temp.end(), first);
}

template< class RandomIt >
void radixsort( RandomIt first, RandomIt last ) {
    typedef typename iterator_traits<RandomIt>::difference_type Diff;
    typedef typename iterator_traits<RandomIt>::value_type VALUE;
    static_assert(std::is_integral<VALUE>::value, "Integral required !!!");
    // 先求最大位数D
    int D = 0;
    int MAX = g_max;
    do {
        ++D;
    } while (MAX /= 10);

    vector<VALUE> temp(last-first);
    // 对每一个位数进行一次计数排序
    for (int d = 0, BASE = 1; d < D; ++d) {
        int C[10] = {};
        for (RandomIt it = first; it != last; ++it)
            ++C[(*it / BASE) % 10];
        for (size_t i = 1; i < 10; ++i)
            C[i] += C[i-1];
        for (RandomIt it = last-1; it >= first; --it)
            temp[--C[(*it / BASE) % 10]] = *it;
        BASE *= 10;
        copy(temp.begin(), temp.begin()+(last-first), first);
    }
}

template< class RandomIt >
void sink( RandomIt first, RandomIt last, RandomIt root ) {
    typedef typename iterator_traits<RandomIt>::difference_type Diff;
    // sink的目的是保证根节点最大，并不保证左节点大于右节点
    while (1) {
        Diff index = root - first;
        RandomIt left = first + (2*index + 1);
        RandomIt right = left + 1;
        if (left < last) {
            RandomIt max = left;
            if (right < last && *left < *right)
                max = right;
            if (*max < *root)
                return;
            swap(*max, *root);
            root = max;
            continue;
        }
        return;
    }
}

template< class RandomIt >
void MakeHeap_iteration( RandomIt first, RandomIt last ) {
    typedef typename iterator_traits<RandomIt>::difference_type Diff;
    // 从两层堆开始sink每一个根节点
    Diff size = last - first;
    Diff init_pos = (size - 2) >> 1;
    for (RandomIt root = first + init_pos; root >= first; --root)
        sink(first, last, root);
}

template< class RandomIt >
void MakeHeap_recursion( RandomIt first, RandomIt last, RandomIt root ) {
    typedef typename iterator_traits<RandomIt>::difference_type Diff;
    
    if (root >= last) return;

    Diff index = root - first;
    RandomIt left = first + (2*index + 1);
    RandomIt right = left + 1;
    MakeHeap_recursion(first, last, left);
    MakeHeap_recursion(first, last, right);
    sink(first, last, root);
}

// 参考https://github.com/boostorg/sort/blob/develop/include/boost/sort/heap_sort/heap_sort.hpp
template< class RandomIt >
void MakeHeap_Boost( RandomIt first, RandomIt last ) {

    typedef typename iterator_traits<RandomIt>::difference_type Diff;
    Diff nelem = last - first;
    Diff pos_father, pos_son;
    RandomIt iter_father = first, iter_son = first;
    bool sw = false;

    // 上浮法，从第二层开始上浮每一个节点
    for (Diff i = 1; i < nelem; ++i) {
        pos_father = i;
        iter_father = first + i;
        sw = false;
        do {
            iter_son = iter_father;
            pos_son = pos_father;
            pos_father = (pos_son - 1) >> 1;
            iter_father = first + pos_father;
            if ((sw = (*iter_father < *iter_son)))
                std::swap (*iter_father, *iter_son);
        } while (sw && pos_father != 0);
    };
};

template< class RandomIt >
void SortHeap( RandomIt first, RandomIt last ) {
    while (first < last) {
        swap(*first, *(--last));
        sink(first, last, first);
    }
}

template< class RandomIt >
void heapsort_recursion( RandomIt first, RandomIt last ) {
    /* STL做法
    std::make_heap(first, last);
    std::sort_heap(first, last);
    */
    MakeHeap_recursion(first, last, first);
    SortHeap(first, last);
}

template< class RandomIt >
void heapsort_iteration( RandomIt first, RandomIt last ) {
    MakeHeap_iteration(first, last);
    SortHeap(first, last);
}

template< class RandomIt >
void heapsort_Boost( RandomIt first, RandomIt last ) {
    MakeHeap_Boost(first, last);
    SortHeap(first, last);
}

#define TEST(func)                                                \
    do {                                                          \
        vector<int> nums1 = nums;                                 \
                                                                  \
        uint64 time0 = GetTimeMs64();                             \
        func(nums1.begin(), nums1.end());                         \
        uint64 time1 = GetTimeMs64();                             \
                                                                  \
        auto res = std::mismatch(nums1.begin(), nums1.end(),      \
                                 nums0.begin(), nums0.end());     \
        if ( res.first != nums1.end() ) {                         \
            cout <<""#func" : nums1 is not same as nums after: "  \
                 << res.first - nums1.begin() << endl;            \
        } else {                                                  \
            cout << std::setw(22) << std::right << ""#func": ";   \
            cout << time1 - time0 << " ms.\n";                    \
        }                                                         \
    } while(0)


int main(int argc, char const *argv[])
{
    int VAR = 500;
    if (argc == 2)
        VAR = stoi(string(argv[1]));
    std::random_device rd;   //  Will be used to obtain a seed for the random number engine
    std::mt19937 gen(rd());  //  Standard mersenne_twister_engine seeded with rd()
    std::uniform_int_distribution<> distrib(1, VAR * 100);
    g_min = 1;
    g_max = VAR * 100;

    vector<int> nums(VAR);

    int i = VAR;
    while (i-- > 0)
        nums[i] = (distrib(gen));

    vector<int> nums0 = nums;
    uint64 time0 = GetTimeMs64();
    std::sort(nums0.begin(), nums0.end());
    uint64 time1 = GetTimeMs64();
    cout << std::setw(22) << std::right << "std::sort: " << time1 - time0 << " ms.\n";

    TEST(bubblesort);
    TEST(selectionsort);
    TEST(insertionsort);
    TEST(shellsort);
    TEST(shellsort2);
    TEST(mergesort_recursion);
    TEST(mergesort_iteration);
    TEST(quicksort_recursion);
    TEST(quicksort_iteration);
    TEST(countingsort);
    TEST(bucketsort);
    TEST(radixsort);
    TEST(heapsort_recursion);
    TEST(heapsort_iteration);
    TEST(heapsort_Boost);

    return 0;
}