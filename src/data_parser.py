import pandas as pd
import numpy as np

def parse_range(s):
    """Parses a string in 'X-Y' format to its average and half-range (delta)."""
    if isinstance(s, str) and '-' in s:
        try:
            parts = list(map(float, s.split('-')))
            avg = np.mean(parts)
            delta = (max(parts) - min(parts)) / 2
            return avg, delta
        except ValueError:
            return np.nan, np.nan
    try:
        return float(s), 0.0
    except (ValueError, TypeError):
        return np.nan, np.nan

def load_and_process_data():
    """
    Loads raw data from images (represented as predefined lists here)
    and processes them into a unified Pandas DataFrame.
    """
    
    # --- 1. 摩擦学实验数据 (来自图片二) ---
    friction_data_raw = [
        {'Material': 'Weiss', 'Block_Config': 'B+1+2+3+4', 'Kraft_N_Range': '30-3.3', 'Messung_Type': 'M1'},
        {'Material': 'Weiss', 'Block_Config': 'B+1+2+3', 'Kraft_N_Range': '2.6-3.1', 'Messung_Type': 'M1'},
        {'Material': 'Weiss', 'Block_Config': 'B+1+2', 'Kraft_N_Range': '2.35-2.8', 'Messung_Type': 'M1'},
        {'Material': 'Weiss', 'Block_Config': 'B+1', 'Kraft_N_Range': '2.0-2.4', 'Messung_Type': 'M1'},
        {'Material': 'Weiss', 'Block_Config': 'B', 'Kraft_N_Range': '1.65-1.9', 'Messung_Type': 'M1'},
        
        {'Material': 'Weiss', 'Block_Config': 'B+1+2+3+4', 'Kraft_N_Range': '2.95-3.4', 'Messung_Type': 'M2'},
        {'Material': 'Weiss', 'Block_Config': 'B+1+2+3', 'Kraft_N_Range': '2.65-3.1', 'Messung_Type': 'M2'},
        {'Material': 'Weiss', 'Block_Config': 'B+1+2', 'Kraft_N_Range': '2.75-2.8', 'Messung_Type': 'M2'},
        {'Material': 'Weiss', 'Block_Config': 'B+1', 'Kraft_N_Range': '2.0-2.4', 'Messung_Type': 'M2'},
        {'Material': 'Weiss', 'Block_Config': 'B', 'Kraft_N_Range': '1.65-1.9', 'Messung_Type': 'M2'},

        {'Material': 'Weiss', 'Block_Config': 'B+1+2+3+4', 'Kraft_N_Range': '2.95-3.4', 'Messung_Type': 'M3'},
        {'Material': 'Weiss', 'Block_Config': 'B+1+2+3', 'Kraft_N_Range': '2.65-3.1', 'Messung_Type': 'M3'},
        {'Material': 'Weiss', 'Block_Config': 'B+1+2', 'Kraft_N_Range': '2.75-2.8', 'Messung_Type': 'M3'},
        {'Material': 'Weiss', 'Block_Config': 'B+1', 'Kraft_N_Range': '2.0-2.4', 'Messung_Type': 'M3'},
        {'Material': 'Weiss', 'Block_Config': 'B', 'Kraft_N_Range': '1.65-1.9', 'Messung_Type': 'M3'},

        {'Material': 'Schwarz', 'Block_Config': 'B+1+2+3+4', 'Kraft_N_Range': '4.15-4.25', 'Messung_Type': 'M1'},
        {'Material': 'Schwarz', 'Block_Config': 'B+1+2+3', 'Kraft_N_Range': '3.55-3.75', 'Messung_Type': 'M1'},
        {'Material': 'Schwarz', 'Block_Config': 'B+1+2', 'Kraft_N_Range': '3.25-3.4', 'Messung_Type': 'M1'},
        {'Material': 'Schwarz', 'Block_Config': 'B+1', 'Kraft_N_Range': '2.8-2.95', 'Messung_Type': 'M1'},
        {'Material': 'Schwarz', 'Block_Config': 'B', 'Kraft_N_Range': '2.3-2.45', 'Messung_Type': 'M1'},
        
        {'Material': 'Schwarz', 'Block_Config': 'B+1+2+3+4', 'Kraft_N_Range': '3.9-4.05', 'Messung_Type': 'M2'},
        {'Material': 'Schwarz', 'Block_Config': 'B+1+2+3', 'Kraft_N_Range': '3.6-3.8', 'Messung_Type': 'M2'},
        {'Material': 'Schwarz', 'Block_Config': 'B+1+2', 'Kraft_N_Range': '3.25-3.4', 'Messung_Type': 'M2'},
        {'Material': 'Schwarz', 'Block_Config': 'B+1', 'Kraft_N_Range': '2.8-3.0', 'Messung_Type': 'M2'},
        {'Material': 'Schwarz', 'Block_Config': 'B', 'Kraft_N_Range': '2.3-2.45', 'Messung_Type': 'M2'},

        {'Material': 'Schwarz', 'Block_Config': 'B+1+2+3+4', 'Kraft_N_Range': '4.0-4.15', 'Messung_Type': 'M3'},
        {'Material': 'Schwarz', 'Block_Config': 'B+1+2+3', 'Kraft_N_Range': '3.65-3.85', 'Messung_Type': 'M3'},
        {'Material': 'Schwarz', 'Block_Config': 'B+1+2', 'Kraft_N_Range': '3.25-3.4', 'Messung_Type': 'M3'},
        {'Material': 'Schwarz', 'Block_Config': 'B+1', 'Kraft_N_Range': '2.8-3.0', 'Messung_Type': 'M3'},
        {'Material': 'Schwarz', 'Block_Config': 'B', 'Kraft_N_Range': '2.3-2.45', 'Messung_Type': 'M3'},
    ]

    processed_friction_data = []
    for row in friction_data_raw:
        avg, delta = parse_range(row['Kraft_N_Range'])
        processed_friction_data.append({
            'Versuch': 'Tribologie',
            'Material': row['Material'],
            'Block_Config': row['Block_Config'],
            'Messung_Type': row['Messung_Type'],
            'Kraft_N_Avg': avg,
            'Kraft_N_Delta': delta
        })

    df_friction = pd.DataFrame(processed_friction_data)

    # --- 2. 小表面数据 (来自图片一) ---
    small_surface_data = [
        {'Material': 'Stahl', 'Messung_Type': 'M1', 'Value_Range': '1.7-1.9'},
        {'Material': 'Stahl', 'Messung_Type': 'M2', 'Value_Range': '1.7-1.9'},
        {'Material': 'Stahl', 'Messung_Type': 'M3', 'Value_Range': '1.7-1.9'},
        {'Material': 'Weiss', 'Messung_Type': 'M1', 'Value_Range': '0.95-1.0'},
        {'Material': 'Weiss', 'Messung_Type': 'M2', 'Value_Range': '0.95-1.05'},
        {'Material': 'Weiss', 'Messung_Type': 'M3', 'Value_Range': '0.95-1.05'},
        {'Material': 'Schwarz', 'Messung_Type': 'M1', 'Value_Range': '1.85-1.95'},
        {'Material': 'Schwarz', 'Messung_Type': 'M2', 'Value_Range': '1.9-2.0'},
        {'Material': 'Schwarz', 'Messung_Type': 'M3', 'Value_Range': '1.9-2.0'},
    ]

    processed_small_surface_data = []
    for row in small_surface_data:
        avg, delta = parse_range(row['Value_Range'])
        processed_small_surface_data.append({
            'Oberflaeche_Art': 'Kleine_Flaeche',
            'Material': row['Material'],
            'Messung_Type': row['Messung_Type'],
            'Messwert_Avg': avg,
            'Messwert_Delta': delta
        })
    df_small_surface = pd.DataFrame(processed_small_surface_data)


    # --- 3. 大表面电压数据 (来自图片一) ---
    large_surface_voltage_data = [
        {'Material': 'Stahl', 'Voltage_V': '7V', 'Messung_Type': 'M1', 'Value_Range': '1.5-1.9'},
        {'Material': 'Stahl', 'Voltage_V': '7V', 'Messung_Type': 'M2', 'Value_Range': '1.5-1.9'},
        {'Material': 'Stahl', 'Voltage_V': '7V', 'Messung_Type': 'M3', 'Value_Range': '1.5-1.9'},
        {'Material': 'Stahl', 'Voltage_V': '9V', 'Messung_Type': 'M1', 'Value_Range': '1.5-1.95'},
        {'Material': 'Stahl', 'Voltage_V': '9V', 'Messung_Type': 'M2', 'Value_Range': '1.5-2.0'},
        {'Material': 'Stahl', 'Voltage_V': '9V', 'Messung_Type': 'M3', 'Value_Range': '1.6-2.0'},
        {'Material': 'Stahl', 'Voltage_V': '11V', 'Messung_Type': 'M1', 'Value_Range': '1.45-2.5'},
        {'Material': 'Stahl', 'Voltage_V': '11V', 'Messung_Type': 'M2', 'Value_Range': '1.55-2.25'},
        {'Material': 'Stahl', 'Voltage_V': '11V', 'Messung_Type': 'M3', 'Value_Range': '1.35-2.15'},

        {'Material': 'Weiss', 'Voltage_V': '7V', 'Messung_Type': 'M1', 'Value_Range': '1.25-1.35'},
        {'Material': 'Weiss', 'Voltage_V': '7V', 'Messung_Type': 'M2', 'Value_Range': '1.25-1.35'},
        {'Material': 'Weiss', 'Voltage_V': '7V', 'Messung_Type': 'M3', 'Value_Range': '1.25-1.35'},
        {'Material': 'Weiss', 'Voltage_V': '9V', 'Messung_Type': 'M1', 'Value_Range': '1.35-1.45'},
        {'Material': 'Weiss', 'Voltage_V': '9V', 'Messung_Type': 'M2', 'Value_Range': '1.35-1.5'},
        {'Material': 'Weiss', 'Voltage_V': '9V', 'Messung_Type': 'M3', 'Value_Range': '1.35-1.45'},
        {'Material': 'Weiss', 'Voltage_V': '11V', 'Messung_Type': 'M1', 'Value_Range': '1.4-1.5'},
        {'Material': 'Weiss', 'Voltage_V': '11V', 'Messung_Type': 'M2', 'Value_Range': '1.4-1.55'},
        {'Material': 'Weiss', 'Voltage_V': '11V', 'Messung_Type': 'M3', 'Value_Range': '1.4-1.55'},

        {'Material': 'Schwarz', 'Voltage_V': '7V', 'Messung_Type': 'M1', 'Value_Range': '2.35-2.5'},
        {'Material': 'Schwarz', 'Voltage_V': '7V', 'Messung_Type': 'M2', 'Value_Range': '2.35-2.55'},
        {'Material': 'Schwarz', 'Voltage_V': '7V', 'Messung_Type': 'M3', 'Value_Range': '2.4-2.6'},
        {'Material': 'Schwarz', 'Voltage_V': '9V', 'Messung_Type': 'M1', 'Value_Range': '2.4-2.55'},
        {'Material': 'Schwarz', 'Voltage_V': '9V', 'Messung_Type': 'M2', 'Value_Range': '2.4-2.55'},
        {'Material': 'Schwarz', 'Voltage_V': '9V', 'Messung_Type': 'M3', 'Value_Range': '2.45-2.6'},
        {'Material': 'Schwarz', 'Voltage_V': '11V', 'Messung_Type': 'M1', 'Value_Range': '2.4-2.5'},
        {'Material': 'Schwarz', 'Voltage_V': '11V', 'Messung_Type': 'M2', 'Value_Range': '2.45-2.55'},
        {'Material': 'Schwarz', 'Voltage_V': '11V', 'Messung_Type': 'M3', 'Value_Range': '2.5-2.6'},
    ]

    processed_large_surface_data = []
    for row in large_surface_voltage_data:
        avg, delta = parse_range(row['Value_Range'])
        processed_large_surface_data.append({
            'Oberflaeche_Art': 'Grosse_Flaeche_Voltage',
            'Material': row['Material'],
            'Voltage_V': row['Voltage_V'],
            'Messung_Type': row['Messung_Type'],
            'Messwert_Avg': avg,
            'Messwert_Delta': delta
        })
    df_large_surface_voltage = pd.DataFrame(processed_large_surface_data)

    # --- 4. 整合所有数据并添加 Kontaktflaeche 和 Gewicht 占位符 ---
    
    # 接触面积映射
    contact_area_mapping = {
        'Stahl': '10x3.9', # 根据你的说明 for 5v
        'Weiss': '10x4',
        'Schwarz': '3.9x10'
    }
    
    # 摩擦学数据整合
    df_friction['Kontaktflaeche_cm2'] = df_friction['Material'].map(contact_area_mapping)
    df_friction['Gewicht_Block_g_Avg'] = np.nan # Placeholder
    df_friction['Gewicht_Block_g_Delta'] = np.nan # Placeholder
    df_friction['Voltage_V'] = None # Not applicable for this data type

    # 小表面数据整合
    df_small_surface['Kontaktflaeche_cm2'] = df_small_surface['Material'].map(contact_area_mapping)
    df_small_surface['Versuch'] = 'Kleine_Flaeche_Messung'
    df_small_surface['Block_Config'] = None # Not applicable
    df_small_surface['Gewicht_Block_g_Avg'] = np.nan # Placeholder
    df_small_surface['Gewicht_Block_g_Delta'] = np.nan # Placeholder
    df_small_surface['Voltage_V'] = None # Not applicable

    # 大表面电压数据整合
    df_large_surface_voltage['Kontaktflaeche_cm2'] = df_large_surface_voltage['Material'].map(contact_area_mapping)
    df_large_surface_voltage['Versuch'] = 'Grosse_Flaeche_Spannung'
    df_large_surface_voltage['Block_Config'] = None # Not applicable
    df_large_surface_voltage['Gewicht_Block_g_Avg'] = np.nan # Placeholder
    df_large_surface_voltage['Gewicht_Block_g_Delta'] = np.nan # Placeholder
    
    # 统一列名以便合并
    df_friction.rename(columns={'Kraft_N_Avg': 'Messwert_Avg', 'Kraft_N_Delta': 'Messwert_Delta'}, inplace=True)

    # 合并所有数据
    combined_df = pd.concat([df_friction, df_small_surface, df_large_surface_voltage], ignore_index=True, sort=False)

    # 重新排序列，确保一致性
    final_combined_df = combined_df[[
        'Versuch', 'Oberflaeche_Art', 'Material', 'Block_Config', 'Voltage_V', 
        'Messung_Type', 'Kontaktflaeche_cm2', 'Gewicht_Block_g_Avg', 'Gewicht_Block_g_Delta',
        'Messwert_Avg', 'Messwert_Delta'
    ]]

    # 替换 NaN 为 None，便于导出和阅读
    final_combined_df = final_combined_df.replace({np.nan: None})

    return final_combined_df

if __name__ == '__main__':
    # 示例用法
    df_integrated = load_and_process_data()
    output_path = 'data/integrated_experiment_data.csv'
    df_integrated.to_csv(output_path, index=False)
    print(f"Integrated data saved to {output_path}")
    print(df_integrated.head())