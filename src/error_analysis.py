import numpy as np
import pandas as pd

def calculate_mass_from_config(config_str, material):
    """
    根据白板数据（图3）计算总质量。
    """
    if not isinstance(config_str, str):
        return np.nan, np.nan

    # 砝码质量 (g)
    weights_map = {
        '1': 160.8,
        '2': 153.9,
        '3': 154.1,
        '4': 156.4
    }
    
    # 基础滑块质量 (g)
    if material == 'Stahl':
        block_mass = 616.0
    else:
        # Weiss 和 Schwarz 都是塑料 (Kunststoff)
        block_mass = 678.0 

    # 假设质量测量的不确定度为 0.1g
    base_uncertainty = 0.1
    
    parts = config_str.split('+')
    total_mass = 0.0
    uncertainty_sq = 0.0
    
    for part in parts:
        part = part.strip()
        if part == 'B':
            total_mass += block_mass
            uncertainty_sq += base_uncertainty**2
        elif part in weights_map:
            total_mass += weights_map[part]
            uncertainty_sq += base_uncertainty**2
            
    return total_mass, np.sqrt(uncertainty_sq)

def calculate_physics(df_row):
    """
    计算法向力 (Fn) 和 摩擦系数 (mu)。
    """
    g = 9.81
    
    # 1. 计算法向力 Fn = m * g
    mass_kg = df_row['Mass_g_Avg'] / 1000.0
    mass_delta_kg = df_row['Mass_g_Delta'] / 1000.0
    
    fn_avg = mass_kg * g
    fn_delta = mass_delta_kg * g
    
    # 2. 获取摩擦力 Fr (从表格数据)
    fr_avg = df_row['Messwert_Avg']
    fr_delta = df_row['Messwert_Delta']
    
    # 3. 计算摩擦系数 mu = Fr / Fn
    if fn_avg > 0:
        mu_avg = fr_avg / fn_avg
        # 误差传递: delta_mu = sqrt( (1/Fn * dFr)^2 + (Fr/Fn^2 * dFn)^2 )
        term1 = (1 / fn_avg * fr_delta)**2
        term2 = (fr_avg / (fn_avg**2) * fn_delta)**2
        mu_delta = np.sqrt(term1 + term2)
    else:
        mu_avg = np.nan
        mu_delta = np.nan
        
    return pd.Series([fn_avg, fn_delta, mu_avg, mu_delta], 
                     index=['Fn_avg', 'Fn_delta', 'mu_avg', 'mu_delta'])