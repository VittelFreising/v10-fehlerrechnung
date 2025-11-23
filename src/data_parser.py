import pandas as pd
import numpy as np

def parse_range(s):
    """
    解析 '3.0-3.3' 为 (平均值, 误差)
    """
    if isinstance(s, str) and '-' in s:
        try:
            parts = list(map(float, s.split('-')))
            avg = np.mean(parts)
            delta = (max(parts) - min(parts)) / 2
            return avg, delta
        except ValueError:
            return np.nan, np.nan
    try:
        val = float(s)
        return val, 0.0
    except (ValueError, TypeError):
        return np.nan, np.nan

def get_raw_data():
    """
    录入图片中的所有原始数据。
    包含：Block配置、电压、面积、测量的力范围。
    """
    
    # 定义面积常量 (cm^2)
    # Image 2 & Image 1 Bottom (Large Area)
    A_GROSS_STAHL = 10 * 3.9   # 39.0
    A_GROSS_WEISS = 10 * 4.0   # 40.0
    A_GROSS_SCHWARZ = 3.9 * 10 # 39.0
    
    # Image 1 Top (Small Area / Schmale Flächen)
    A_KLEIN_STAHL = 2 * 10.0   # 20.0
    A_KLEIN_WEISS = 2 * 10.0   # 20.0
    A_KLEIN_SCHWARZ = 2 * 10.2 # 20.4

    data_list = []

    # ==========================================
    # 1. 摩擦学实验 (Image 2) - 变重量
    # 条件: 5V, 大面积
    # ==========================================
    # --- STAHL (Steel) ---
    base = {'Material': 'Stahl', 'Voltage_V': '5V', 'Area_cm2': A_GROSS_STAHL, 'Experiment': 'Weight_Var'}
    data_list.extend([
        {**base, 'Block_Config': 'B+1+2+3+4', 'Range': '3.0-3.3'},
        {**base, 'Block_Config': 'B+1+2+3+4', 'Range': '2.95-3.4'},
        {**base, 'Block_Config': 'B+1+2+3+4', 'Range': '2.95-3.4'},
        {**base, 'Block_Config': 'B+1+2+3',   'Range': '2.6-3.1'},
        {**base, 'Block_Config': 'B+1+2+3',   'Range': '2.65-3.1'},
        {**base, 'Block_Config': 'B+1+2+3',   'Range': '2.65-3.1'},
        {**base, 'Block_Config': 'B+1+2',     'Range': '2.35-2.75'},
        {**base, 'Block_Config': 'B+1+2',     'Range': '2.35-2.8'},
        {**base, 'Block_Config': 'B+1+2',     'Range': '2.45-2.8'},
        {**base, 'Block_Config': 'B+1',       'Range': '2.0-2.4'},
        {**base, 'Block_Config': 'B+1',       'Range': '2.0-2.4'},
        {**base, 'Block_Config': 'B+1',       'Range': '2.0-2.4'},
        {**base, 'Block_Config': 'B',         'Range': '1.65-1.9'},
        {**base, 'Block_Config': 'B',         'Range': '1.65-1.9'},
        {**base, 'Block_Config': 'B',         'Range': '1.65-1.85'},
    ])

    # --- WEISS (Polyethylen) ---
    base = {'Material': 'Weiss', 'Voltage_V': '5V', 'Area_cm2': A_GROSS_WEISS, 'Experiment': 'Weight_Var'}
    data_list.extend([
        {**base, 'Block_Config': 'B+1+2+3+4', 'Range': '1.8-2.05'},
        {**base, 'Block_Config': 'B+1+2+3+4', 'Range': '1.75-2.00'},
        {**base, 'Block_Config': 'B+1+2+3+4', 'Range': '1.75-2.05'},
        {**base, 'Block_Config': 'B+1+2+3',   'Range': '1.65-1.85'},
        {**base, 'Block_Config': 'B+1+2+3',   'Range': '1.7-1.85'},
        {**base, 'Block_Config': 'B+1+2+3',   'Range': '1.75-1.85'},
        {**base, 'Block_Config': 'B+1+2',     'Range': '1.6-1.75'},
        {**base, 'Block_Config': 'B+1+2',     'Range': '1.65-1.75'},
        {**base, 'Block_Config': 'B+1+2',     'Range': '1.65-1.8'},
        {**base, 'Block_Config': 'B+1',       'Range': '1.45-1.55'},
        {**base, 'Block_Config': 'B+1',       'Range': '1.45-1.6'},
        {**base, 'Block_Config': 'B+1',       'Range': '1.45-1.6'},
        {**base, 'Block_Config': 'B',         'Range': '1.25-1.35'},
        {**base, 'Block_Config': 'B',         'Range': '1.25-1.35'},
        {**base, 'Block_Config': 'B',         'Range': '1.2-1.35'},
    ])

    # --- SCHWARZ (Polyisopren) ---
    base = {'Material': 'Schwarz', 'Voltage_V': '5V', 'Area_cm2': A_GROSS_SCHWARZ, 'Experiment': 'Weight_Var'}
    data_list.extend([
        {**base, 'Block_Config': 'B+1+2+3+4', 'Range': '4.15-4.25'},
        {**base, 'Block_Config': 'B+1+2+3+4', 'Range': '3.9-4.05'},
        {**base, 'Block_Config': 'B+1+2+3+4', 'Range': '4.0-4.15'},
        {**base, 'Block_Config': 'B+1+2+3',   'Range': '3.55-3.75'},
        {**base, 'Block_Config': 'B+1+2+3',   'Range': '3.6-3.8'},
        {**base, 'Block_Config': 'B+1+2+3',   'Range': '3.65-3.85'},
        {**base, 'Block_Config': 'B+1+2',     'Range': '3.25-3.4'},
        {**base, 'Block_Config': 'B+1+2',     'Range': '3.25-3.45'},
        {**base, 'Block_Config': 'B+1+2',     'Range': '3.25-3.45'},
        {**base, 'Block_Config': 'B+1',       'Range': '2.8-2.95'},
        {**base, 'Block_Config': 'B+1',       'Range': '2.8-2.95'},
        {**base, 'Block_Config': 'B+1',       'Range': '2.8-3.0'},
        {**base, 'Block_Config': 'B',         'Range': '2.3-2.45'},
        {**base, 'Block_Config': 'B',         'Range': '2.3-2.45'},
        {**base, 'Block_Config': 'B',         'Range': '2.3-2.45'},
    ])

    # ==========================================
    # 2. 小表面实验 (Image 1 Top) - schmale Flächen
    # 条件: 5V, 小面积, 假设 Block_Config = B (基础块)
    # ==========================================
    
    # Stahl (5V, Small Area)
    base = {'Material': 'Stahl', 'Voltage_V': '5V', 'Area_cm2': A_KLEIN_STAHL, 'Experiment': 'Small_Area', 'Block_Config': 'B'}
    data_list.extend([
        {**base, 'Range': '1.4-1.5'},
        {**base, 'Range': '1.4-1.5'},
        {**base, 'Range': '1.4-1.5'},
    ])
    
    # Weiss (5V, Small Area)
    base = {'Material': 'Weiss', 'Voltage_V': '5V', 'Area_cm2': A_KLEIN_WEISS, 'Experiment': 'Small_Area', 'Block_Config': 'B'}
    data_list.extend([
        {**base, 'Range': '0.95-1.0'},
        {**base, 'Range': '0.95-1.05'},
        {**base, 'Range': '0.95-1.05'},
    ])

    # Schwarz (5V, Small Area)
    base = {'Material': 'Schwarz', 'Voltage_V': '5V', 'Area_cm2': A_KLEIN_SCHWARZ, 'Experiment': 'Small_Area', 'Block_Config': 'B'}
    data_list.extend([
        {**base, 'Range': '1.85-1.95'},
        {**base, 'Range': '1.85-1.95'},
        {**base, 'Range': '1.9-2.0'},
    ])

    # ==========================================
    # 3. 电压实验 (Image 1 Bottom) - versch. Spannungen
    # 条件: 变电压, 大面积, 假设 Block_Config = B
    # ==========================================
    
    # Stahl (Large Area, Var Voltage)
    base = {'Material': 'Stahl', 'Area_cm2': A_GROSS_STAHL, 'Experiment': 'Voltage_Var', 'Block_Config': 'B'}
    data_list.extend([
        {**base, 'Voltage_V': '7V', 'Range': '1.5-1.9'},
        {**base, 'Voltage_V': '7V', 'Range': '1.5-1.9'},
        {**base, 'Voltage_V': '7V', 'Range': '1.5-1.9'},
        {**base, 'Voltage_V': '9V', 'Range': '1.5-1.95'},
        {**base, 'Voltage_V': '9V', 'Range': '1.5-2.0'},
        {**base, 'Voltage_V': '9V', 'Range': '1.6-2.0'},
        {**base, 'Voltage_V': '11V', 'Range': '1.45-2.5'},
        {**base, 'Voltage_V': '11V', 'Range': '1.35-2.25'},
        {**base, 'Voltage_V': '11V', 'Range': '1.35-2.15'},
    ])

    # Weiss (Large Area, Var Voltage)
    base = {'Material': 'Weiss', 'Area_cm2': A_GROSS_WEISS, 'Experiment': 'Voltage_Var', 'Block_Config': 'B'}
    data_list.extend([
        {**base, 'Voltage_V': '7V', 'Range': '1.25-1.35'},
        {**base, 'Voltage_V': '7V', 'Range': '1.25-1.35'},
        {**base, 'Voltage_V': '7V', 'Range': '1.25-1.35'},
        {**base, 'Voltage_V': '9V', 'Range': '1.35-1.45'},
        {**base, 'Voltage_V': '9V', 'Range': '1.35-1.5'},
        {**base, 'Voltage_V': '9V', 'Range': '1.35-1.45'},
        {**base, 'Voltage_V': '11V', 'Range': '1.4-1.5'},
        {**base, 'Voltage_V': '11V', 'Range': '1.4-1.55'},
        {**base, 'Voltage_V': '11V', 'Range': '1.4-1.55'},
    ])

    # Schwarz (Large Area, Var Voltage)
    base = {'Material': 'Schwarz', 'Area_cm2': A_GROSS_SCHWARZ, 'Experiment': 'Voltage_Var', 'Block_Config': 'B'}
    data_list.extend([
        {**base, 'Voltage_V': '7V', 'Range': '2.35-2.5'},
        {**base, 'Voltage_V': '7V', 'Range': '2.35-2.55'},
        {**base, 'Voltage_V': '7V', 'Range': '2.4-2.6'},
        {**base, 'Voltage_V': '9V', 'Range': '2.4-2.55'},
        {**base, 'Voltage_V': '9V', 'Range': '2.4-2.55'},
        {**base, 'Voltage_V': '9V', 'Range': '2.45-2.6'},
        {**base, 'Voltage_V': '11V', 'Range': '2.4-2.5'},
        {**base, 'Voltage_V': '11V', 'Range': '2.45-2.55'},
        {**base, 'Voltage_V': '11V', 'Range': '2.5-2.6'},
    ])

    return data_list

def load_and_process_data():
    raw_data = get_raw_data()
    df = pd.DataFrame(raw_data)
    
    # 解析范围字符串
    df[['Messwert_Avg', 'Messwert_Delta']] = df['Range'].apply(
        lambda x: pd.Series(parse_range(x))
    )
    
    return df