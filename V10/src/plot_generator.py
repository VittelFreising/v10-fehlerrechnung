import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

def plot_friction_results(df_analyzed, plot_type, x_axis_label, y_axis_label, save_path):
    """
    Generates bar plots with error bars for friction coefficient.
    
    Args:
        df_analyzed (pd.DataFrame): DataFrame containing analyzed friction data (mu_avg, mu_delta).
        plot_type (str): Type of plot (e.g., 'normal_force', 'normal_area', 'voltage').
        x_axis_label (str): Label for the x-axis.
        y_axis_label (str): Label for the y-axis (friction coefficient).
        save_path (str): Path to save the plot image.
    """
    plt.figure(figsize=(10, 6))
    
    # Filter for relevant data (Tribologie measurements)
    df_plot = df_analyzed[df_analyzed['Versuch'] == 'Tribologie'].copy()
    
    # Aggregate data to have one mu_avg and mu_delta per Block_Config and Material
    # This assumes that for a given (Block_Config, Material), we have a single mu and delta
    # If multiple measurements (M1, M2, M3) lead to slightly different mu,
    # we might need to average them or represent them separately.
    # For now, let's group and take the mean of mu_avg and max of mu_delta for simplicity in plotting.
    # This is a simplification; ideally, the error propagation would already yield a single mu_avg/delta for a set of measurements.
    
    if plot_type == 'normal_force':
        # For 'normal_force', x-axis would be related to Block_Config/Fn_avg.
        # Let's use Block_Config as categorical x-axis for now.
        x_col = 'Block_Config'
        # Sort Block_Config if they represent increasing normal force
        block_order = ['B', 'B+1', 'B+1+2', 'B+1+2+3', 'B+1+2+3+4']
        df_plot[x_col] = pd.Categorical(df_plot[x_col], categories=block_order, ordered=True)
        df_plot = df_plot.sort_values(x_col)
        
    elif plot_type == 'normal_area':
        # This plot type would require specific 'normal area A' values.
        # For now, we don't have this in a clear column, so let's stick to Block_Config.
        # If 'normal area A' is directly calculable or available, it should be added to the DataFrame.
        x_col = 'Block_Config' # Placeholder
    elif plot_type == 'voltage':
        # This would use the 'Grosse_Flaeche_Spannung' data.
        # For friction coefficient (mu) vs voltage, this implies mu is calculated for these specific voltage measurements.
        # Currently, mu is only explicitly calculated for Tribologie data.
        # If mu is also relevant for voltage data, it needs to be calculated in error_analysis.py.
        
        # For now, let's create a placeholder plot using existing mu data, or you might need to adjust the scope.
        # For PPT requirement "friction coefficient μ versus voltage U", this means mu should be derived from
        # the voltage experiment (Messwert_Avg / Fn_avg for that experiment).
        # We need to calculate mu for df_large_surface_voltage data.
        
        # Let's focus on Tribologie data for the initial plots.
        print(f"Warning: Plot type '{plot_type}' for friction coefficient vs voltage requires specific mu calculation for voltage data. Generating placeholder plot with existing friction data.")
        x_col = 'Block_Config'
    else:
        x_col = 'Block_Config' # Default

    sns.barplot(x=x_col, y='mu_avg', hue='Material', data=df_plot, yerr=df_plot['mu_delta'], capsize=0.1, errorbar=None)
    
    # Manually add error bars for better control (yerr in barplot sometimes requires specific data format)
    # This assumes df_plot has unique rows for each bar (x_col, hue)
    for i, row in df_plot.iterrows():
        plt.errorbar(x=row[x_col], y=row['mu_avg'], yerr=row['mu_delta'], color='black', capsize=5)

    plt.title(f'{y_axis_label} vs {x_axis_label} with Error Bars')
    plt.xlabel(x_axis_label)
    plt.ylabel(y_axis_label)
    plt.legend(title='Material')
    plt.grid(axis='y', linestyle='--')
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()

def plot_mu_vs_voltage(df_voltage_analyzed, save_path):
    """
    Generates a plot for friction coefficient (μ) versus voltage (U).
    This requires 'Voltage_V' to be a numerical column and 'mu_avg', 'mu_delta' to be calculated
    for the large surface voltage experiments.
    """
    plt.figure(figsize=(10, 6))

    df_plot = df_voltage_analyzed[df_voltage_analyzed['Versuch'] == 'Grosse_Flaeche_Spannung'].copy()
    
    if df_plot.empty:
        print(f"No data available for 'Grosse_Flaeche_Spannung' to plot mu vs voltage. Skipping plot: {save_path}")
        return

    # Convert Voltage_V to numerical for plotting
    df_plot['Voltage_Num'] = df_plot['Voltage_V'].str.extract('(\d+)').astype(float)
    
    # Sort by voltage for better visualization
    df_plot = df_plot.sort_values(['Material', 'Voltage_Num'])

    # Plot for each material
    sns.lineplot(x='Voltage_Num', y='mu_avg', hue='Material', marker='o', data=df_plot)
    
    # Add error bars
    for material in df_plot['Material'].unique():
        material_data = df_plot[df_plot['Material'] == material]
        plt.errorbar(x=material_data['Voltage_Num'], y=material_data['mu_avg'], 
                     yerr=material_data['mu_delta'], fmt='none', capsize=5, color='black')

    plt.title('Friction Coefficient (μ) vs Voltage (U) with Error Bars')
    plt.xlabel('Voltage (U)')
    plt.ylabel('Friction Coefficient (μ)')
    plt.legend(title='Material')
    plt.grid(axis='both', linestyle='--')
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()