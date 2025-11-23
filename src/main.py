import pandas as pd
import numpy as np
import os
from src.data_parser import load_and_process_data, parse_range
from src.error_analysis import calculate_mu_and_delta_mu, calculate_normal_force_and_delta, error_analysis_example
from src.plot_generator import plot_friction_results, plot_mu_vs_voltage

# Constants
G = 9.81  # m/s^2

def main():
    # 1. Load and process data
    print("Step 1: Loading and processing raw data...")
    df_integrated = load_and_process_data()
    
    # Create data directory if it doesn't exist
    os.makedirs('data', exist_ok=True)
    integrated_data_path = 'data/integrated_experiment_data.csv'
    df_integrated.to_csv(integrated_data_path, index=False)
    print(f"Integrated raw data saved to {integrated_data_path}")

    # 2. Prepare data for friction coefficient calculation (Tribologie data)
    print("Step 2: Preparing Tribologie data for friction coefficient calculation...")
    df_tribologie = df_integrated[df_integrated['Versuch'] == 'Tribologie'].copy()

    # --- 法向力 (Normal Force) 估算 ---
    # 根据你的描述，重量信息分散在多个地方，且需要根据 Block_Config 来推断。
    # 这里我们使用一个更详细的映射来模拟法向力及其不确定度。
    # **重要提示：这些值是基于对你第一张表格和描述的解释进行的假设。**
    # **你必须根据实际实验的准确质量测量来替换这些值。**
    
    # 假设 Block (Metallblock) 基础质量是 616g
    # 假设每个 Blockmit (小块) 大约是 150g-160g
    # 假设 Stahl块的质量是 1241.2g, 1084.8g 等等
    
    # 以下 Fn 和 Delta_Fn 仅为演示目的的示例值。
    # 在实际应用中，你需要从实验数据中精确计算这些值。
    
    # Placeholder mapping for Block_Config to estimated mass (in grams) and its delta
    mass_config_mapping = {
        'B': {'mass_g_avg': 616, 'mass_g_delta': 5}, # Just the Metalblock
        'B+1': {'mass_g_avg': 616 + 155, 'mass_g_delta': 7},
        'B+1+2': {'mass_g_avg': 616 + 2*155, 'mass_g_delta': 10},
        'B+1+2+3': {'mass_g_avg': 616 + 3*155, 'mass_g_delta': 12},
        'B+1+2+3+4': {'mass_g_avg': 616 + 4*155, 'mass_g_delta': 15}, # Block + 4 small weights
        # 如果有其他配置，请在这里添加
    }

    df_tribologie['Mass_g_Avg'] = df_tribologie['Block_Config'].map(lambda x: mass_config_mapping.get(x, {}).get('mass_g_avg', np.nan))
    df_tribologie['Mass_g_Delta'] = df_tribologie['Block_Config'].map(lambda x: mass_config_mapping.get(x, {}).get('mass_g_delta', np.nan))

    # 计算法向力 F_N 及其不确定度 ΔF_N
    df_tribologie[['Fn_avg', 'Fn_delta']] = df_tribologie.apply(
        lambda row: pd.Series(calculate_normal_force_and_delta(row['Mass_g_Avg'], row['Mass_g_Delta'])),
        axis=1
    )
    
    # 为摩擦力 Fr 及其不确定度 ΔFr 准备列名
    df_tribologie['Fr_avg'] = df_tribologie['Messwert_Avg']
    df_tribologie['Fr_delta'] = df_tribologie['Messwert_Delta']

    # 3. Calculate friction coefficient (μ) and its uncertainty (Δμ) using error propagation
    print("Step 3: Calculating friction coefficient (μ) and its uncertainty (Δμ)...")
    df_tribologie[['mu_avg', 'mu_delta']] = df_tribologie.apply(
        lambda row: pd.Series(calculate_mu_and_delta_mu(row)),
        axis=1
    )
    
    # Aggregate mu_avg and mu_delta for plotting.
    # For a given (Material, Block_Config), we might have M1, M2, M3 measurements.
    # For plotting, we'll take the average of mu_avg and max of mu_delta across M1, M2, M3.
    df_friction_plot_data = df_tribologie.groupby(['Material', 'Block_Config']).agg(
        mu_avg=('mu_avg', 'mean'),
        mu_delta=('mu_delta', 'max'), # Max delta as a conservative estimate for overall uncertainty
        Fn_avg=('Fn_avg', 'mean') # Also include Fn_avg for plotting vs Normal Force
    ).reset_index()

    # Create plots directory
    os.makedirs('plots', exist_ok=True)

    # 4. Generate plots as per presentation requirements
    print("Step 4: Generating plots...")
    
    # Plot 1: friction coefficient μ versus normal force m g
    # For this, we'll use Fn_avg as the X-axis, which is directly derived from mass m g.
    # The x-axis label will be "Normal Force (N)"
    plot_friction_results(df_friction_plot_data, 'normal_force', 
                          'Normal Force (N) [from Block Configuration]', 'Friction Coefficient (μ)', 
                          'plots/mu_vs_normal_force.png')
    
    # Plot 2: friction coefficient μ versus normal area A
    # This plot type requires 'normal area A' as an independent variable.
    # Currently, 'Kontaktflaeche_cm2' is a string. We need to convert it to a numerical area.
    # And relate it to the friction data.
    
    # First, parse Kontaktflaeche_cm2 into numerical area
    df_tribologie_area = df_tribologie.copy()
    def parse_area_string(area_str):
        if area_str and isinstance(area_str, str) and 'x' in area_str:
            try:
                dims = list(map(float, area_str.split('x')))
                return dims[0] * dims[1]
            except ValueError:
                return np.nan
        return np.nan
        
    df_tribologie_area['Normal_Area_cm2'] = df_tribologie_area['Kontaktflaeche_cm2'].apply(parse_area_string)
    
    # For this plot, we need to decide if mu changes significantly with area for a given material.
    # If Contact Area is constant for Tribologie data within a material, this plot won't show variation.
    # Assuming Block_Config implicitly changes the contact area or material setup in some way
    # For a meaningful plot, we need variation in 'Normal_Area_cm2' that affects 'mu'.
    # If Block_Config does not directly influence 'Normal_Area_cm2' in a varied way for this plot,
    # then this might not be the most insightful plot for the Tribologie data as structured.
    # Let's use Block_Config as a proxy for now, but highlight this limitation.
    
    # If the 'small surface' data (df_small_surface) should contribute to mu vs area,
    # mu would need to be calculated for that data as well, which requires Fr and Fn.
    # For now, we stick to Tribologie data.
    
    # As Kontaktflaeche_cm2 is largely constant per material in the Tribologie experiment (10x4, 3.9x10),
    # a plot of mu vs Area based on df_friction_plot_data wouldn't show much variation if Area is constant.
    # This might be a point to discuss in the presentation regarding the experimental setup.
    # For now, I'll generate a plot, but it might just show constant mu if area doesn't vary.
    # A more relevant "mu vs normal area" might come from comparing 'Kleine_Flaeche' vs 'Grosse_Flaeche'
    # if 'mu' can be calculated for those.

    # Let's make an attempt for mu vs Area by grouping by Material and Kontaktflaeche
    df_mu_vs_area = df_tribologie_area.groupby(['Material', 'Normal_Area_cm2']).agg(
        mu_avg=('mu_avg', 'mean'),
        mu_delta=('mu_delta', 'max')
    ).reset_index()

    plot_friction_results(df_mu_vs_area, 'normal_area', 
                          'Normal Area (cm²)', 'Friction Coefficient (μ)', 
                          'plots/mu_vs_normal_area.png')

    # Plot 3: friction coefficient μ versus voltage U
    # This plot requires calculating mu for the 'Grosse_Flaeche_Spannung' data.
    # For this, we need Messwert_Avg (assuming this is Fr) and a corresponding Fn.
    # We do not have explicit Fn for this experiment in the data.
    # **You need to define what Fr and Fn are for the voltage experiments.**
    
    # Assuming 'Messwert_Avg' from df_large_surface_voltage is Fr.
    # We still need a placeholder for Fn for these voltage measurements.
    df_voltage_data = df_integrated[df_integrated['Versuch'] == 'Grosse_Flaeche_Spannung'].copy()
    
    # Placeholder for Normal Force for voltage experiments
    df_voltage_data['Fn_avg'] = 10.0 # N, Example placeholder
    df_voltage_data['Fn_delta'] = 0.5 # N, Example placeholder
    df_voltage_data['Fr_avg'] = df_voltage_data['Messwert_Avg']
    df_voltage_data['Fr_delta'] = df_voltage_data['Messwert_Delta']

    df_voltage_data[['mu_avg', 'mu_delta']] = df_voltage_data.apply(
        lambda row: pd.Series(calculate_mu_and_delta_mu(row)),
        axis=1
    )
    
    # Aggregate if multiple measurements per (Material, Voltage_V)
    df_voltage_plot_data = df_voltage_data.groupby(['Material', 'Voltage_V']).agg(
        mu_avg=('mu_avg', 'mean'),
        mu_delta=('mu_delta', 'max')
    ).reset_index()

    plot_mu_vs_voltage(df_voltage_plot_data, 'plots/mu_vs_voltage.png')

    # 5. Error analysis examples (Method 2)
    error_analysis_example(df_integrated)
    
    print("\n--- All steps completed. Check 'data/' and 'plots/' directories. ---")


if __name__ == '__main__':
    main()