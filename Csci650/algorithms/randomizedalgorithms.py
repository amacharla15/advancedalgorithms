"""
Monte Carlo vs. Las Vegas (Randomized Algorithms)
=================================================

------------------------------------------------------------
1) Core definitions
------------------------------------------------------------

- Monte Carlo algorithm
  • Correctness: May be wrong with small probability ε.
  • Runtime: Bounded (deterministic bound).
  • Control knob: Choose ε via number of samples/trials.
  • Tagline: “Fast with (tiny) chance of error.”

- Las Vegas algorithm
  • Correctness: Always correct.
  • Runtime: Random variable (analyze expectation / high probability).
  • Control knob: Tune expected time by randomization/restarts until a success condition.
  • Tagline: “Always right; time may vary.”

------------------------------------------------------------
2) Quick contrast (at a glance)
------------------------------------------------------------

Aspect            | Monte Carlo                         | Las Vegas
------------------|-------------------------------------|-----------------------------------------
Output            | Can be wrong (prob ≤ ε)             | Always correct
Time bound        | Fixed / tight worst-case            | Random; analyze E[time] / w.h.p.
Tradeoff          | More time ⇒ lower error             | More retries ⇒ lower tail on time
Typical use       | Testing, estimation, approximation  | Exact algorithms with randomized time
Example           | Miller–Rabin primality              | Randomized Quicksort (exact sorting)

Notes:
- “w.h.p.” = with high probability (e.g., ≥ 1 − n^{-c} for some c > 0).
- “Expectation” = average over algorithm’s internal randomness.

------------------------------------------------------------
3) Canonical examples
------------------------------------------------------------

Monte Carlo:
  • Two-sided error: Karger’s Min-Cut. Repeat O(n^2 log n) times to drive success w.h.p.
  • One-sided error: Miller–Rabin primality test. If it says “composite,” it’s certainly composite; 
    “probably prime” has exponentially small false-positive rate with independent rounds.

Las Vegas:
  • Randomized Quicksort: Always sorts correctly; expected O(n log n) time (worst-case O(n^2) but rare).
  • Randomized incremental geometry (e.g., Delaunay/Voronoi): Exact output; randomness gives expected bounds.

------------------------------------------------------------
4) Amplification patterns
------------------------------------------------------------

Monte Carlo error amplification:
  • If a single run fails with prob ≤ ε:
      - “Find-a-good-result” tasks (e.g., min-cut): run k times, keep best; failure ≤ ε^k (independent runs).
      - Decision tests (e.g., primality): majority vote over k runs; error drops exponentially in k.

Las Vegas time amplification:
  • Restart-until-success: If a trial succeeds with prob ≥ p, expected trials = 1/p.
  • Cutoff + restart: Cap each attempt’s time; restart with fresh randomness. Tames heavy tails in practice.

------------------------------------------------------------
5) How hashing relates (Las Vegas vs. Monte Carlo)
------------------------------------------------------------

Hashing is a central source of randomness. Depending on the structure/goal, you get either:
- Las Vegas behavior: exact answers; randomized build/time.
- Monte Carlo behavior: tiny probability of an incorrect positive (often one-sided error).

(A) Universal hashing ⇒ Las Vegas dictionaries
  • Pick hash function uniformly from a universal family.
  • Lookups are ALWAYS correct; expected O(1) time due to random collision behavior.
  • Why Las Vegas? Correctness is not probabilistic; only time is.

(B) Perfect hashing (FKS) ⇒ Las Vegas construction
  • Keep choosing random hash functions until there are no collisions for the static key set.
  • Correctness: exact; Build time: expected linear (retries possible).
  • Pattern: “Try random h until success_condition() holds.”

(C) Cuckoo hashing ⇒ Las Vegas rebuilds
  • Two (or more) hash functions; insert may trigger displacements.
  • If a cycle occurs, rebuild with fresh hashes.
  • Correctness exact; runtime random due to occasional rebuilds.

(D) Bloom filters ⇒ Monte Carlo membership
  • Space-efficient set representation using k hash functions.
  • One-sided error: No false negatives; allows false positives with tunable probability p.
  • Monte Carlo: Fixed, fast operations with small chance an “in set” answer is wrong.

(E) Random fingerprints / polynomial hashing ⇒ Monte Carlo checks
  • Use random mod primes or polynomial hashing as fingerprints.
  • If fingerprints match, strings are likely equal (tiny collision probability).
  • Typically one-sided error (false equal rarely); time/space fixed.

Summary map:
  • Las Vegas via hashing: universal hashing, perfect hashing (FKS), cuckoo hashing (exact answers; random time).
  • Monte Carlo via hashing: Bloom filters, randomized fingerprints (possible tiny error; fixed time).

------------------------------------------------------------
6) Choosing between them (practical )
------------------------------------------------------------

Choose MONTE CARLO when:
  • You need predictable runtime/space and can tolerate a tiny error.
  • Error can be pushed down arbitrarily by repetition (e.g., primality testing, approximate/streaming tasks).

Choose LAS VEGAS when:
  • Exact correctness is non-negotiable.
  • Expected/w.h.p. time is acceptable (e.g., exact data structures, exact combinatorial outputs).
  • Hashing can randomize layout to achieve expected O(1) operations (dictionaries, static sets).


------------------------------------------------------------
7) Tiny pseudocode sketches (language-neutral)
------------------------------------------------------------

# Monte Carlo amplifier (majority vote over k runs)
repeat k times:
    ans_i = RandomTest(x)    # each run wrong with prob ≤ ε (independent)
return Majority(ans_1..ans_k)

# Las Vegas “try until success” (e.g., perfect hashing build)
while True:
    h = pick_random_hash()
    build_structure_with(h)
    if success_condition():   # e.g., no collisions / no cycle / invariant satisfied
        return structure      # correctness guaranteed
    # else retry with fresh randomness


"""

"""
#Bloom filters:

"""
