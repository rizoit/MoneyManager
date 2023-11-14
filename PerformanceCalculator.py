class PerformanceCalculator:
    """
    Contains helper methods for detailed performance calculations.
    """
    @staticmethod
    def calculate_annualized_return(start_value, end_value, duration_years):
        """Calculates annualized return."""
        return (end_value / start_value) ** (1 / duration_years) - 1

    @staticmethod
    def calculate_volatility(returns):
        """Calculates portfolio volatility."""
        import numpy as np
        return np.std(returns)