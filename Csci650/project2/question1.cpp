#include <bits/stdc++.h>
using namespace std;

// Monte Carlo estimator of pi using n samples
static double approxPi(long long n, mt19937_64 &gen) {
    uniform_real_distribution<double> dist(-1.0, 1.0);
    long long inside = 0;
    for (long long i = 0; i < n; ++i) {
        double x = dist(gen), y = dist(gen);
        if (x * x + y * y <= 1.0) inside += 1;
    }
    return 4.0 * double(inside) / double(n);
}

int main() {
    const long long start_n = 10, end_n = 10000, step = 100;
    const int repeats = 10;

    mt19937_64 gen(0); // reproducible
    ofstream out("approx_pi_errorbars.csv");
    if (!out) { cerr << "could not open output file\n"; return 1; }
    out << "n,mean_abs_error,std_error\n";

    for (long long n = start_n; n <= end_n; n += step) {
        vector<double> errs; errs.reserve(repeats);
        for (int r = 0; r < repeats; ++r) {
            double pi_hat = approxPi(n, gen);
            errs.push_back(fabs(M_PI - pi_hat)); // |π - π̂|
        }
        // mean
        double sum = 0.0; for (double e : errs) sum += e;
        double mean = sum / errs.size();
        // sample std (ddof=1) and standard error
        double sq = 0.0; for (double e : errs) { double d = e - mean; sq += d*d; }
        double sdev = sqrt(sq / (errs.size() - 1));
        double stderr = sdev / sqrt(double(errs.size()));

        out << n << "," << fixed << setprecision(8) << mean << "," << stderr << "\n";
    }
    cerr << "Wrote approx_pi_errorbars.csv\n";
    return 0;
}
