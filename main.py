import os
import pandas as pd
from src.data_parser import load_and_process_data
from src.error_analysis import calculate_mass_from_config, calculate_physics
from src.plot_generator import plot_mu_vs_force, plot_mu_vs_voltage, plot_mu_vs_area

def main():
    print("Step 1: Parsing Data...")
    df = load_and_process_data()
    
    print("Step 2: Calculating Physics (Mass, Fn, Mu)...")
    # 计算质量
    mass_data = df.apply(
        lambda row: calculate_mass_from_config(row['Block_Config'], row['Material']), 
        axis=1, result_type='expand'
    )
    df['Mass_g_Avg'] = mass_data[0]
    df['Mass_g_Delta'] = mass_data[1]
    
    # 计算物理量
    df = df.join(df.apply(calculate_physics, axis=1))
    
    # 保存中间数据
    os.makedirs('data', exist_ok=True)
    try:
        df.to_csv('data/processed_data.csv', index=False)
        print(f"Data saved to data/processed_data.csv ({len(df)} rows)")
    except PermissionError:
        print(f"Warning: Could not save processed_data.csv (file in use), but continuing with plots...")
    
    print("Step 3: Generating Plots...")
    os.makedirs('plots', exist_ok=True)
    
    plot_mu_vs_force(df, 'plots/mu_vs_normal_force.png')
    plot_mu_vs_voltage(df, 'plots/mu_vs_voltage.png')
    plot_mu_vs_area(df, 'plots/mu_vs_area.png')
    
    print("\n" + "="*50)
    print("ERROR CALCULATION EXAMPLE (Weiss, B+1+2+3+4, 5V)")
    print("="*50)
    example = df[
        (df['Material'] == 'Weiss') & 
        (df['Block_Config'] == 'B+1+2+3+4') & 
        (df['Experiment'] == 'Weight_Var')
    ].iloc[0]
    
    print(f"Force Range: {example['Range']} N")
    print(f"Avg Friction Force (Fr): {example['Messwert_Avg']:.4f} +/- {example['Messwert_Delta']:.4f} N")
    print(f"Mass: {example['Mass_g_Avg']:.2f} g")
    print(f"Normal Force (Fn): {example['Fn_avg']:.4f} N")
    print(f"Mu: {example['mu_avg']:.4f} +/- {example['mu_delta']:.4f}")
    
    print("\nDone! Check the 'plots' folder.")

if __name__ == '__main__':
    main()