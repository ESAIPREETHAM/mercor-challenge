"""ReferralNetwork: core data structures and influencer metrics.

This module implements Parts 1-3 of the Mercor challenge:
- Directed referral graph with constraints (no self-referral, unique referrer, acyclic)
- Reach computations (I used BFS here)
- Unique reach expansion (I used greedy set cover)
- Flow centrality (It is a simple, correct implementation via all-pairs BFS)

The implementation favors clarity and correctness and complexity notes are in docstrings.
"""

from collections import deque, defaultdict
from typing import Dict, Set, List, Tuple
import math

class ReferralNetwork:
    def __init__(self):
        # adjacency list: referrer -> set of direct referrals
        self.graph: Dict[str, Set[str]] = defaultdict(set)
        # candidate -> referrer (enforces unique referrer)
        self.parent: Dict[str, str] = {}

    # ------------------ Part 1: Graph operations ------------------
    def add_user(self, user: str) -> None:
        """Ensure a user exists in the graph."""
        if user not in self.graph:
            self.graph[user] = set()

    def add_referral(self, referrer: str, candidate: str) -> bool:
        """Attempt to add a directed edge referrer -> candidate.

        Returns True if added successfully, False if rejected due to constraints.

        Constraints enforced:
        - No self-referrals
        - Candidate must not already have a referrer
        - Adding the edge must not create a cycle
        """
        # Basic user setup
        self.add_user(referrer)
        self.add_user(candidate)

        # No self-referrals
        if referrer == candidate:
            return False
        # Unique referrer
        if candidate in self.parent:
            return False
        # I am Preventing cycles such that candidate should not be able to reach referrer
        if self._is_reachable(candidate, referrer):
            return False

        # Add edge
        if candidate in self.graph[referrer]:
            # already present - idempotent
            self.parent.setdefault(candidate, referrer)
            return True

        self.graph[referrer].add(candidate)
        self.parent[candidate] = referrer
        return True

    def get_direct_referrals(self, user: str) -> List[str]:
        """Return a list of direct referrals for `user`."""
        return list(self.graph.get(user, []))

    # ------------------ Part 2: Reach / Top-k ------------------
    def get_total_referrals(self, user: str) -> int:
        """Return the total number of downstream referrals (direct + indirect).

        Complexity: O(V + E) using BFS.
        """
        return len(self._downstream_set(user))

    def top_k_referrers(self, k: int) -> List[Tuple[str, int]]:
        """Return top-k users by total reach as (user, reach) pairs sorted desc."""
        counts = [(u, self.get_total_referrals(u)) for u in self.graph.keys()]
        counts.sort(key=lambda x: x[1], reverse=True)
        return counts[:k]

    # ------------------ Part 3: Influencer metrics ------------------
    def unique_reach_expansion(self) -> List[str]:
        """My Greedy selection that return users ordered by marginal unique reach.

        1. Precompute full downstream set for every user
        2. Repeatedly select the user who contributes the largest number of
           not-yet-covered nodes
        """
        reach_sets = {u: self._downstream_set(u) for u in self.graph.keys()}
        covered: Set[str] = set()
        selected: List[str] = []
        remaining = set(self.graph.keys())

        while True:
            best_user = None
            best_gain = 0
            for u in remaining:
                gain = len(reach_sets[u] - covered)
                if gain > best_gain:
                    best_gain = gain
                    best_user = u
            if best_user is None or best_gain == 0:
                break
            selected.append(best_user)
            covered |= reach_sets[best_user]
            remaining.remove(best_user)

        return selected

    def flow_centrality(self) -> List[Tuple[str, int]]:
        """Simple flow-centrality (betweenness-like) via all-pairs BFS distances.

        For each triple (s, t, v), v != s != t, if dist(s,v)+dist(v,t) == dist(s,t)
        then v lies on at least one shortest path from s to t and we increment v's score.

        Complexity: O(V*(V+E)) to compute distances + O(V^3) triple-checks in worst-case.
        """
        users = list(self.graph.keys())
        # Precompute distances from every source to optimise time complexity
        dist: Dict[str, Dict[str, int]] = {}
        for u in users:
            dist[u] = self._bfs_distances(u)

        centrality: Dict[str, int] = defaultdict(int)
        for s in users:
            for t in users:
                if s == t:
                    continue
                if dist[s].get(t, math.inf) == math.inf:
                    continue
                d_st = dist[s][t]
                for v in users:
                    if v == s or v == t:
                        continue
                    d_sv = dist[s].get(v, math.inf)
                    d_vt = dist[v].get(t, math.inf)
                    if d_sv + d_vt == d_st and d_sv != math.inf and d_vt != math.inf:
                        centrality[v] += 1

        items = list(centrality.items())
        items.sort(key=lambda x: x[1], reverse=True)
        return items

    # ------------------ Helpers ------------------
    def _is_reachable(self, src: str, tgt: str) -> bool:
        """Return True if tgt reachable from src (directed). BFS."""
        if src == tgt:
            return True
        visited = set()
        q = deque([src])
        while q:
            cur = q.popleft()
            for nei in self.graph.get(cur, []):
                if nei == tgt:
                    return True
                if nei not in visited:
                    visited.add(nei)
                    q.append(nei)
        return False

    def _downstream_set(self, user: str) -> Set[str]:
        """Return set of all nodes reachable from user (excluding user)."""
        visited: Set[str] = set()
        q = deque(self.graph.get(user, []))
        while q:
            cur = q.popleft()
            if cur in visited:
                continue
            visited.add(cur)
            for nei in self.graph.get(cur, []):
                if nei not in visited:
                    q.append(nei)
        return visited

    def _bfs_distances(self, start: str) -> Dict[str, int]:
        """Return dictionary node->distance from start (math.inf for unreachable)."""
        dist = {u: math.inf for u in self.graph.keys()}
        if start not in self.graph:
            return dist
        dist[start] = 0
        q = deque([start])
        while q:
            cur = q.popleft()
            for nei in self.graph.get(cur, []):
                if dist[nei] == math.inf:
                    dist[nei] = dist[cur] + 1
                    q.append(nei)
        return dist


# Simple convenience usage when running as script (manual quick smoke test)
if __name__ == "__main__":
    rn = ReferralNetwork()
    rn.add_referral('A', 'B')
    rn.add_referral('A', 'C')
    rn.add_referral('B', 'D')
    print('A direct:', rn.get_direct_referrals('A'))
    print('A total reach:', rn.get_total_referrals('A'))
    print('Top-2:', rn.top_k_referrers(2))