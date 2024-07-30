import numpy as np

def general_formula(a, ef, c=0, r=0):
    """general activity-based emissions equation

    ... math::

        E = \\sum_i (A_i \\cdot EF_i) \\cdot C - R

    where i is some category.

    Parameters
    ----------
    a : float
        activity
    ef : float
        emission factor
    c : float, optional
        conversion, by default 0
    r : float, optional
        removal, by default 0

    Returns
    -------
    float
        emissions
    """

    return np.sum(a * ef) * c - r