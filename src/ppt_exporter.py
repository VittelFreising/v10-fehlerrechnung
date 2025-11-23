import numpy as np
import pandas as pd

def print_single_template(df, material_name, config_name, exp_type='Weight_Var', voltage_select='5V'):
    """
    内部辅助函数：计算并打印单个案例的 PPT 模板数据
    """
    # 1. 筛选数据
    if exp_type == 'Weight_Var':
        subset = df[
            (df['Material'] == material_name) & 
            (df['Block_Config'] == config_name) & 
            (df['Experiment'] == exp_type) &
            (df['Voltage_V'] == voltage_select)
        ]
    else: # Voltage_Var
        subset = df[
            (df['Material'] == material_name) & 
            (df['Voltage_V'] == voltage_select) & 
            (df['Experiment'] == exp_type)
        ]

    if len(subset) == 0:
        print(f"Error: No data found for {material_name}, {config_name}")
        return

    # 2. 提取参数
    # 质量 (kg)
    mass_g = subset['Mass_g_Avg'].iloc[0] 
    mass_kg = mass_g / 1000.0
    delta_m_kg = 0.0001 # 0.1g = 0.0001kg
    
    # 面积 & 电压 & 法向力
    area = subset['Area_cm2'].iloc[0]
    voltage = subset['Voltage_V'].iloc[0]
    g = 9.81
    fn = mass_kg * g 

    # 3. 摩擦力数据 (F1, F2, F3)
    f_measurements = subset['Messwert_Avg'].values
    f_mean = f_measurements.mean()

    # 4. 确定 Delta F (取最大值)
    # 模板要求：Delta F is the largest of "error newton meter" and "fluctuation"
    fluctuation_range = subset['Messwert_Delta'].max() # 取三次测量中波动最大的那个
    error_newton_meter = 0.05 # 牛顿计刻度误差
    delta_f = max(fluctuation_range, error_newton_meter)

    # 5. 计算 Mu
    mu = f_mean / fn

    # 6. 误差传递项
    # Term 1: [Delta F / (m * g)]^2
    term1 = (delta_f / fn) ** 2
    
    # Term 2: [(F * Delta m) / (m^2 * g)]^2
    term2 = ((f_mean * delta_m_kg) / (mass_kg**2 * g)) ** 2

    # 总误差 Delta mu
    delta_mu = np.sqrt(term1 + term2)

    # --- 打印输出 ---
    print(f"\n>>> PPT DATA SLIDE FOR: {material_name} | {config_name} | {voltage}")
    print("-" * 50)
    print(f"Material:                      {material_name}")
    print(f"Mass m [kg]:                   {mass_kg:.4f}")
    print(f"Area A [cm^2]:                 {area}")
    print(f"Voltage U [V]:                 {voltage}")
    print("-" * 50)
    print(f"Measured F [N] (F1..Fn):       {f_measurements}")
    print(f"Number n of measurements:      {len(f_measurements)}")
    print(f"Mean friction force <F> [N]:   {f_mean:.4f}")
    print(f"Error Newton meter [N]:        {error_newton_meter}")
    print(f"Fluctuation range (from data): {fluctuation_range:.4f}")
    print(f"-> DELTA F [N] (Largest):      {delta_f:.4f}")
    print("-" * 50)
    print(f"Friction coefficient <mu>:     {mu:.4f}")
    print("-" * 50)
    print("Error Propagation Formulas (Intermediate Values):")
    print(f"Term 1: [Delta F / (m g)]^2:       {term1:.8f}")
    print(f"Term 2: [(F Delta m) / (m^2 g)]^2: {term2:.8f}")
    print("-" * 50)
    print(f"Total Delta mu:                {delta_mu:.4f}")
    print(f"FINAL RESULT:                  mu = {mu:.2f} +/- {delta_mu:.2f}")
    print("=" * 60)


def generate_ppt_report(df):
    """
    主函数：被 main.py 调用，输出所有选定的案例
    """
    print("\n" + "#"*60)
    print("   GENERATING PPT ERROR CALCULATION TEMPLATES")
    print("#"*60)

    # 案例 1: Stahl (钢), B+1+2, 5V
    print_single_template(df, 'Stahl', 'B+1+2')

    # 案例 2: Weiss (聚乙烯), B+1+2+3+4, 5V
    print_single_template(df, 'Weiss', 'B+1+2+3+4')

    # 案例 3: Schwarz (橡胶), B, 5V
    print_single_template(df, 'Schwarz', 'B')