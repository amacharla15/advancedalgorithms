#include <bits/stdc++.h>
using namespace std;

/* ---------- BFPRT (median-of-medians) with configurable group size s ---------- */
static int median_of_block(vector<int> &a, int start, int len) {
    int i = start + 1;
    while (i < start + len) {
        int key = a[i], j = i - 1;
        while (j >= start && a[j] > key) { a[j + 1] = a[j]; j -= 1; }
        a[j + 1] = key; i += 1;
    }
    return a[start + (len / 2)];
}
static int partition_around(vector<int> &a, int left, int right, int pivot_value) {
    int i = left, lt = left, gt = right;
    while (i <= gt) {
        if (a[i] < pivot_value) { swap(a[i], a[lt]); i += 1; lt += 1; }
        else if (a[i] > pivot_value) { swap(a[i], a[gt]); gt -= 1; }
        else { i += 1; }
    }
    return lt;
}
static int select_value(vector<int> &a, int L, int R, int k0, int s);
static int choose_pivot_value(vector<int> &a, int left, int right, int s) {
    int n = right - left + 1, blocks = (n + s - 1) / s;
    vector<int> meds; meds.reserve(blocks);
    for (int b = 0; b < blocks; ++b) {
        int st = left + b * s, len = s;
        if (st + len - 1 > right) len = right - st + 1;
        meds.push_back(median_of_block(a, st, len));
    }
    function<int(vector<int>&,int,int,int)> sel = [&](vector<int>& x, int L2, int R2, int k02)->int{
        int n2 = R2 - L2 + 1;
        if (n2 <= s) {
            int i = L2 + 1;
            while (i <= R2) {
                int key = x[i], j = i - 1;
                while (j >= L2 && x[j] > key) { x[j + 1] = x[j]; j -= 1; }
                x[j + 1] = key; i += 1;
            }
            return x[L2 + k02];
        }
        int blocks2 = (n2 + s - 1) / s;
        vector<int> m2; m2.reserve(blocks2);
        for (int b2 = 0; b2 < blocks2; ++b2) {
            int st2 = L2 + b2 * s, ln2 = s;
            if (st2 + ln2 - 1 > R2) ln2 = R2 - st2 + 1;
            m2.push_back(median_of_block(x, st2, ln2));
        }
        int pv = sel(m2, 0, (int)m2.size()-1, (int)m2.size()/2);
        int i2 = L2, lt = L2, gt = R2;
        while (i2 <= gt) {
            if (x[i2] < pv) { swap(x[i2], x[lt]); i2 += 1; lt += 1; }
            else if (x[i2] > pv) { swap(x[i2], x[gt]); gt -= 1; }
            else { i2 += 1; }
        }
        int rank = lt - L2;
        if (k02 == rank) return x[lt];
        if (k02 < rank)  return sel(x, L2, lt - 1, k02);
        return sel(x, lt + 1, R2, k02 - rank - 1);
    };
    return sel(meds, 0, (int)meds.size()-1, (int)meds.size()/2);
}
static int select_value(vector<int> &a, int L, int R, int k0, int s) {
    int n = R - L + 1;
    if (n <= s) {
        int i = L + 1;
        while (i <= R) {
            int key = a[i], j = i - 1;
            while (j >= L && a[j] > key) { a[j + 1] = a[j]; j -= 1; }
            a[j + 1] = key; i += 1;
        }
        return a[L + k0];
    }
    int pivot_val = choose_pivot_value(a, L, R, s);
    int p = partition_around(a, L, R, pivot_val);
    int rank = p - L;
    if (k0 == rank) return a[p];
    if (k0 <  rank) return select_value(a, L, p - 1, k0, s);
    return select_value(a, p + 1, R, k0 - rank - 1, s);
}
int select_mom(const vector<int>& L, int k, int s) {
    vector<int> a = L;
    if (k < 1 || k > (int)a.size()) throw runtime_error("k out of range");
    if (s < 3) s = 5; if (s % 2 == 0) s += 1;
    return select_value(a, 0, (int)a.size()-1, k-1, s);
}

/* ------------------------ Randomized Quickselect ------------------------ */
int quickselect(const vector<int> &L, int k) {
    vector<int> a = L;
    if (k < 1 || k > (int)a.size()) throw runtime_error("k out of range");
    int left = 0, right = (int)a.size()-1, t = k-1;
    static random_device rd; static mt19937_64 gen(rd());
    while (left <= right) {
        uniform_int_distribution<int> dist(left, right);
        int pivot = a[dist(gen)];
        int i = left, lt = left, gt = right;
        while (i <= gt) {
            if (a[i] < pivot) { swap(a[i], a[lt]); i += 1; lt += 1; }
            else if (a[i] > pivot) { swap(a[i], a[gt]); gt -= 1; }
            else { i += 1; }
        }
        int lessCount = lt - left, eqCount = gt - lt + 1;
        if (t < left + lessCount) right = lt - 1;
        else if (t >= left + lessCount + eqCount) left = gt + 1;
        else return pivot;
    }
    throw runtime_error("unexpected");
}

/* ------------------------------ Naive ------------------------------ */
// Sort the entire array, then return the (k-1)-th element.
int naive_select(const vector<int>& L, int k) {
    if (k < 1 || k > (int)L.size()) throw runtime_error("k out of range");
    vector<int> a = L;
    sort(a.begin(), a.end());              // O(n log n)
    return a[k - 1];
}

/* --------------------------------- Runner --------------------------------- */
struct Stats { double mean; double stderr; };
Stats time_algo(function<int(const vector<int>&,int)> f,
                int n, int repeats, mt19937_64 &gen)
{
    uniform_int_distribution<int> valdist(INT_MIN, INT_MAX);
    vector<double> times; times.reserve(repeats);
    for (int r = 0; r < repeats; ++r) {
        vector<int> L(n);
        for (int i = 0; i < n; ++i) L[i] = valdist(gen);
        uniform_int_distribution<int> kdist(1, n);
        int k = kdist(gen);

        auto t0 = chrono::steady_clock::now();
        volatile int ans = f(L, k);
        (void)ans;
        auto t1 = chrono::steady_clock::now();
        times.push_back(chrono::duration<double>(t1 - t0).count());
    }
    double sum = 0.0; for (double x : times) sum += x;
    double mean = sum / times.size();
    double sq = 0.0; for (double x : times) { double d = x - mean; sq += d*d; }
    double sdev = sqrt(sq / (times.size() - 1));
    double se   = sdev / sqrt((double)times.size());
    return {mean, se};
}

int main() {
    const int startN = 1000, endN = 20000, step = 1000;
    const int repeats = 30;

    ofstream fn("naive.csv");
    ofstream fq("quickselect.csv");
    ofstream f5("mom5.csv");
    ofstream f3("mom3.csv");
    fn << "n,mean,stderr\n";
    fq << "n,mean,stderr\n";
    f5 << "n,mean,stderr\n";
    f3 << "n,mean,stderr\n";

    mt19937_64 gen(0);

    for (int n = startN; n <= endN; n += step) {
        Stats s_na = time_algo([](const vector<int>& L,int k){ return naive_select(L,k); }, n, repeats, gen);
        Stats s_q  = time_algo([](const vector<int>& L,int k){ return quickselect(L,k); }, n, repeats, gen);
        Stats s_m5 = time_algo([&](const vector<int>& L,int k){ return select_mom(L,k,5); }, n, repeats, gen);
        Stats s_m3 = time_algo([&](const vector<int>& L,int k){ return select_mom(L,k,3); }, n, repeats, gen);

        fn << n << "," << fixed << setprecision(8) << s_na.mean << "," << s_na.stderr << "\n";
        fq << n << "," << fixed << setprecision(8) << s_q.mean  << "," << s_q.stderr  << "\n";
        f5 << n << "," << fixed << setprecision(8) << s_m5.mean << "," << s_m5.stderr << "\n";
        f3 << n << "," << fixed << setprecision(8) << s_m3.mean << "," << s_m3.stderr << "\n";
        cerr << "n=" << n << " done\n";
    }
    return 0;
}
