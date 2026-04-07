import logging

class AAM_Engine:
    def __init__(self, profile):
        self.profile = profile

    def decide(self, task_id: str, value: float, criticality: float, uncertainty: float):
        """
        Calculates the optimal Autonomy Level (Lx) for an Agentic Task.
        
        Args:
            value (V): Financial or operational value of the task.
            criticality (Ce): The cost of a failure/error.
            uncertainty (P(e)): Probability of error (stochastic reasoning).
        """
        # 1. Calculate Control Cost (Cc) based on profile
        cc = self.profile["control_cost_coefficient"] * criticality
        
        # 2. Calculate Expected Cost of Error (E[Ce])
        expected_error_cost = uncertainty * (criticality * self.profile["error_cost_multiplier"])
        
        # 3. Compute Net Utility (U)
        utility = value - cc - expected_error_cost
        
        # 4. Map Utility to the Lx Scale (L0 - L4)
        if utility >= self.profile["utility_threshold"]:
            decision = "L4 - Audited Autonomy (Full Execution)"
        elif utility > (self.profile["utility_threshold"] * 0.7):
            decision = "L3 - Conditional Autonomy (Execute with Alert)"
        elif utility > (self.profile["utility_threshold"] * 0.4):
            decision = "L2 - Supervised (Human-Side Validation)"
        elif utility > 0:
            decision = "L1 - Human-in-the-Loop (Mandatory Review)"
        else:
            decision = "L0 - No Autonomy (Task Rejected/Hard Block)"

        audit_log = {
            "task_id": task_id,
            "utility_score": round(utility, 4),
            "parameters": {"V": value, "Cc": round(cc, 4), "Pe": uncertainty},
            "lx_level": decision
        }
        
        return decision, audit_log