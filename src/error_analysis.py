import numpy as np
import pandas as pd
from scipy.stats import t

# Constants
g = 9.81  # m/s^2 (Standard gravity)

def calculate_mu_and_delta_mu(df_row):
    """
    Calculates friction coefficient (mu) and its uncertainty (delta_mu)
    using error propagation formula.
    mu = Fr / Fn
    Delta_mu = sqrt( (1/Fn * Delta_Fr)^2 + (Fr/Fn^2 * Delta_Fn)^2 )
    
    Args:
        df_row (pd.Series): A row from the DataFrame containing Fr_avg, Fr_delta, Fn_avg, Fn_delta.
    
    Returns:
        tuple: (mu_avg, mu_delta)
    """
    fr_avg = df_row['Fr_avg']
    fr_delta = df_row['Fr_delta']
    fn_avg = df_row['Fn_avg']
    fn_delta = df_row['Fn_delta']

    if pd.isna(fr_avg) or pd.isna(fn_avg) or fn_avg == 0:
        return np.nan, np.nan

    mu_avg = fr_avg / fn_avg
    
    # Error propagation formula for mu = Fr / Fn
    term1 = (1 / fn_avg * fr_delta)**2
    term2 = (fr_avg / (fn_avg**2) * fn_delta)**2
    
    mu_delta = np.sqrt(term1 + term2)
    
    return mu_avg, mu_delta

def calculate_normal_force_and_delta(mass_g_avg, mass_g_delta):
    """
    Calculates normal force (Fn) and its uncertainty (delta_Fn) from mass.
    Fn = m * g
    Delta_Fn = Delta_m * g (assuming g has negligible uncertainty)
    
    Args:
        mass_g_avg (float): Average mass in grams.
        mass_g_delta (float): Uncertainty in mass in grams.
        
    Returns:
        tuple: (Fn_avg, Fn_delta) in Newtons.
    """
    if pd.isna(mass_g_avg):
        return np.nan, np.nan
        
    mass_kg_avg = mass_g_avg / 1000.0
    mass_kg_delta = mass_g_delta / 1000.0 if not pd.isna(mass_g_delta) else 0.0
    
    fn_avg = mass_kg_avg * g
    fn_delta = mass_kg_delta * g
    
    return fn_avg, fn_delta

def calculate_std_dev_and_sem(data):
    """
    Calculates standard deviation (sigma_68) and standard error of the mean (SEM).
    sigma_68 = sqrt(sum((xi - mean)^2) / N)
    SEM = sigma_68 / sqrt(N)
    
    Args:
        data (pd.Series or list): Numerical data points.
        
    Returns:
        tuple: (std_dev, sem)
    """
    if not isinstance(data, pd.Series):
        data = pd.Series(data)

    data = data.dropna()
    N = len(data)
    if N < 2:
        return np.nan, np.nan # Need at least 2 points for std dev
    
    mean_val = data.mean()
    std_dev = np.sqrt(np.sum((data - mean_val)**2) / N) # As per your slide, N in denominator
    sem = std_dev / np.sqrt(N)
    
    return std_dev, sem

def calculate_confidence_interval(sem, N, confidence_level=0.95):
    """
    Calculates the confidence interval (c_95) using Student's t-factor.
    c = t * SEM
    
    Args:
        sem (float): Standard error of the mean.
        N (int): Number of measurements.
        confidence_level (float): The desired confidence level (e.g., 0.95 for 95%).
        
    Returns:
        float: The half-width of the confidence interval.
    """
    if N < 2:
        return np.nan
        
    degrees_freedom = N - 1
    t_factor = t.ppf((1 + confidence_level) / 2, degrees_freedom)
    
    c_interval = t_factor * sem
    
    return c_interval

def get_t_factor(N, confidence_level=0.95):
    """
    Retrieves the Student's t-factor from tables, or calculates it using scipy.
    This mimics the table lookup on your slide "How many measurements (-1)".
    """
    if N < 2:
        return np.nan
    degrees_freedom = N - 1
    # For common confidence levels and small N, one might hardcode a few values
    # For a general solution, scipy.stats.t.ppf is robust.
    return t.ppf((1 + confidence_level) / 2, degrees_freedom)

def calculate_error_method_1(fr_values):
    """
    Method 1: Treats 3x2 interval boundaries as N=6 measurements.
    Calculates mean, std dev, and 95% confidence interval.
    
    Args:
        fr_values (list): A list of 3 tuples, each with (lower_bound, upper_bound) for Fr.
                          e.g., [(3.0, 3.3), (2.9, 3.4), (2.9, 3.4)]
                          
    Returns:
        dict: {'mean_fr', 'std_dev_fr', 'sem_fr', 'c95_fr'}
    """
    all_measurements = []
    for lower, upper in fr_values:
        all_measurements.extend([lower, upper])
    
    data_series = pd.Series(all_measurements).dropna()
    N = len(data_series)
    
    if N < 2:
        return {'mean_fr': np.nan, 'std_dev_fr': np.nan, 'sem_fr': np.nan, 'c95_fr': np.nan}
        
    mean_fr = data_series.mean()
    std_dev_fr, sem_fr = calculate_std_dev_and_sem(data_series)
    c95_fr = calculate_confidence_interval(sem_fr, N, confidence_level=0.95)
    
    return {'mean_fr': mean_fr, 'std_dev_fr': std_dev_fr, 'sem_fr': sem_fr, 'c95_fr': c95_fr}

def calculate_error_method_2(fr_interval_ranges):
    """
    Method 2: Treats interval boundaries as systematic error.
    Calculates mean as midpoint of interval, and delta as half of fluctuation range.
    If intervals vary, takes the largest or most frequent interval, or middle one for trends.
    Here, for simplicity, we'll use the average of the interval midpoints,
    and the delta of the largest interval.
    
    Args:
        fr_interval_ranges (list): A list of 3 tuples, each with (lower_bound, upper_bound) for Fr.
                                   e.g., [(3.0, 3.3), (2.9, 3.4), (2.9, 3.4)]
                                   
    Returns:
        dict: {'mean_fr', 'delta_fr'}
    """
    midpoints = []
    ranges = []
    
    for lower, upper in fr_interval_ranges:
        if pd.isna(lower) or pd.isna(upper):
            continue
        midpoints.append((lower + upper) / 2)
        ranges.append(upper - lower)
        
    if not midpoints:
        return {'mean_fr': np.nan, 'delta_fr': np.nan}

    # Mean Fr is the average of the midpoints
    mean_fr = np.mean(midpoints)
    
    # Delta Fr is half of the largest fluctuation range
    if ranges:
        delta_fr = max(ranges) / 2
    else:
        delta_fr = np.nan
        
    return {'mean_fr': mean_fr, 'delta_fr': delta_fr, 'std_dev_fr': 'nicht betrachtet', 'sem_fr': 'nicht betrachtet', 'c95_fr': 'nicht betrachtet'}

# Example usage in presentation for specific data points (as requested in PPT)
def error_analysis_example(df):
    """
    Demonstrates error analysis for specific data points as per PPT requirement 6.
    """
    print("\n--- Error Analysis Examples (Method 2 - Systematic Error) ---")
    
    # Example 1: Weiss, Block_Config B+1+2+3+4
    weiss_b4 = df[(df['Material'] == 'Weiss') & (df['Block_Config'] == 'B+1+2+3+4') & (df['Versuch'] == 'Tribologie')]
    if not weiss_b4.empty:
        fr_intervals = [
            (weiss_b4[weiss_b4['Messung_Type']=='M1']['Messwert_Avg'].iloc[0] - weiss_b4[weiss_b4['Messung_Type']=='M1']['Messwert_Delta'].iloc[0], 
             weiss_b4[weiss_b4['Messung_Type']=='M1']['Messwert_Avg'].iloc[0] + weiss_b4[weiss_b4['Messung_Type']=='M1']['Messwert_Delta'].iloc[0]),
            (weiss_b4[weiss_b4['Messung_Type']=='M2']['Messwert_Avg'].iloc[0] - weiss_b4[weiss_b4['Messung_Type']=='M2']['Messwert_Delta'].iloc[0], 
             weiss_b4[weiss_b4['Messung_Type']=='M2']['Messwert_Avg'].iloc[0] + weiss_b4[weiss_b4['Messung_Type']=='M2']['Messwert_Delta'].iloc[0]),
            (weiss_b4[weiss_b4['Messung_Type']=='M3']['Messwert_Avg'].iloc[0] - weiss_b4[weiss_b4['Messung_Type']=='M3']['Messwert_Delta'].iloc[0], 
             weiss_b4[weiss_b4['Messung_Type']=='M3']['Messwert_Avg'].iloc[0] + weiss_b4[weiss_b4['Messung_Type']=='M3']['Messwert_Delta'].iloc[0]),
        ]
        
        # In a real scenario, you'd extract the original range boundaries from source, not re-derive from avg/delta
        # For this example, we'll simulate based on avg/delta as per data_parser.
        # Let's directly use the parsed avg/delta as per "Vorgehen (2)"
        
        # Method 2 values from data_parser already correctly calculate avg and delta from the largest range.
        # We need to take the row where Messwert_Avg is the *average of all 3 measurements' midpoints*
        # And Messwert_Delta is *half of the largest fluctuation range*.
        # To get a single representation for mu for the plot, we'd average the Messwert_Avg from M1,M2,M3
        # and take the maximum Messwert_Delta.

        # To demonstrate method 2 as per the notes:
        # "Wenn ihr z.B. 3 mal hintereinander [ 3,1 N und 3,4 N ] abgelesen habt,
        # dann ist der Mittelwert von <F> = 3,25 N und Delta-F = 0,15 N."
        # This implies: calculate average of interval midpoints for <F>, and half of largest interval width for Delta-F.

        m1_avg = weiss_b4[weiss_b4['Messung_Type']=='M1']['Messwert_Avg'].iloc[0]
        m1_delta = weiss_b4[weiss_b4['Messung_Type']=='M1']['Messwert_Delta'].iloc[0]
        m2_avg = weiss_b4[weiss_b4['Messung_Type']=='M2']['Messwert_Avg'].iloc[0]
        m2_delta = weiss_b4[weiss_b4['Messung_Type']=='M2']['Messwert_Delta'].iloc[0]
        m3_avg = weiss_b4[weiss_b4['Messung_Type']=='M3']['Messwert_Avg'].iloc[0]
        m3_delta = weiss_b4[weiss_b4['Messung_Type']=='M3']['Messwert_Delta'].iloc[0]
        
        all_midpoints = [m1_avg, m2_avg, m3_avg]
        all_deltas = [m1_delta, m2_delta, m3_delta]
        
        avg_fr = np.mean(all_midpoints)
        delta_fr = max(all_deltas) # Use the largest delta from the 3 measurements as the overall delta_Fr

        # For normal force (Fn), we assume a placeholder for now.
        # In a real scenario, you'd fetch the corresponding Fn and Delta_Fn.
        # Placeholder for demonstration:
        fn_avg_placeholder = 10.0 # N
        fn_delta_placeholder = 0.5 # N

        mu_avg, mu_delta = calculate_mu_and_delta_mu(pd.Series({
            'Fr_avg': avg_fr, 'Fr_delta': delta_fr,
            'Fn_avg': fn_avg_placeholder, 'Fn_delta': fn_delta_placeholder
        }))

        print(f"\nExample 1: Material Weiss, Block_Config B+1+2+3+4")
        print(f"  Average Friction Force <F_R> (Method 2): {avg_fr:.3f} N")
        print(f"  Uncertainty in Friction Force ΔF_R (Method 2): {delta_fr:.3f} N")
        print(f"  (Assuming Normal Force <F_N> = {fn_avg_placeholder:.1f} N, ΔF_N = {fn_delta_placeholder:.1f} N)")
        print(f"  Calculated Friction Coefficient μ: {mu_avg:.3f}")
        print(f"  Uncertainty in Friction Coefficient Δμ: {mu_delta:.3f}")
        print("  Standard Deviation (sigma_68): nicht betrachtet")
        print("  Standard Error of Mean (SEM): nicht betrachtet")
        print("  Confidence Interval (c_95): nicht betrachtet")
        
    # You can add two more similar examples here for other data points as required by PPT.
    # e.g., one for Schwarz, B and one for Stahl, kleine Fläche (if friction coefficient is calculated there too).