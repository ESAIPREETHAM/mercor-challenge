# This is my simulation file

class Simulation:
    def __init__(self, initial_referrers=100, referral_capacity=10):
        self.initial_referrers = initial_referrers
        self.referral_capacity = referral_capacity

    def simulate(self, p, days):
        """
        Simulates the growth of the referral network over the given number of days.
        Returns a list where the element at index i is the cumulative expected referrals
        at the end of day i.
        """
        active_referrers = self.initial_referrers
        remaining_capacity = {i: self.referral_capacity for i in range(active_referrers)}
        cumulative_referrals = 0
        daily_totals = []

        for day in range(days):
            expected_new = active_referrers * p
            expected_new = min(expected_new, sum(remaining_capacity.values()))
            cumulative_referrals += expected_new

            # Reduce capacity for each active referrer
            reduction_per_referrer = expected_new / active_referrers if active_referrers > 0 else 0
            for ref_id in list(remaining_capacity.keys()):
                remaining_capacity[ref_id] -= reduction_per_referrer
                if remaining_capacity[ref_id] <= 0:
                    del remaining_capacity[ref_id]

            active_referrers = len(remaining_capacity)
            daily_totals.append(cumulative_referrals)

        return daily_totals

    def days_to_target(self, p, target_total):
        """
        Calculates the minimum number of days required to reach or exceed the target referrals.
        """
        active_referrers = self.initial_referrers
        remaining_capacity = {i: self.referral_capacity for i in range(active_referrers)}
        cumulative_referrals = 0
        days = 0

        while cumulative_referrals < target_total and active_referrers > 0:
            days += 1
            expected_new = active_referrers * p
            expected_new = min(expected_new, sum(remaining_capacity.values()))
            cumulative_referrals += expected_new

            reduction_per_referrer = expected_new / active_referrers if active_referrers > 0 else 0
            for ref_id in list(remaining_capacity.keys()):
                remaining_capacity[ref_id] -= reduction_per_referrer
                if remaining_capacity[ref_id] <= 0:
                    del remaining_capacity[ref_id]

            active_referrers = len(remaining_capacity)

        return days if cumulative_referrals >= target_total else None
