"""
演示: 双轴图表功能

这个脚本展示了如何使用新的双轴图表功能。
每个图表现在都包含两个Y轴:
- 左轴 (蓝色): 摩擦系数 μ
- 右轴 (红色): 摩擦力 F

特点:
1. 三个完整的图表，每个展示不同的关系
2. 3条曲线用于3种不同的材料
3. 垂直误差棒显示测量的不确定度
4. 一致的颜色编码和图例
"""

import pandas as pd
from src.data_parser import load_and_process_data
from src.error_analysis import calculate_mass_from_config, calculate_physics
from src.plot_generator import plot_mu_vs_force, plot_mu_vs_voltage, plot_mu_vs_area
import os

def generate_dual_axis_plots():
    """生成具有双Y轴的三个图表"""
    
    print("=" * 60)
    print("生成带有双Y轴的图表 (Dual Axis Plots)")
    print("=" * 60)
    
    # 数据处理
    print("\n[1/3] 加载和处理数据...")
    df = load_and_process_data()
    
    mass_data = df.apply(
        lambda row: calculate_mass_from_config(row['Block_Config'], row['Material']), 
        axis=1, result_type='expand'
    )
    df['Mass_g_Avg'] = mass_data[0]
    df['Mass_g_Delta'] = mass_data[1]
    df = df.join(df.apply(calculate_physics, axis=1))
    
    # 生成图表
    os.makedirs('plots', exist_ok=True)
    
    print("[2/3] 生成图表 1: μ vs Normal Force (质量变化)")
    plot_mu_vs_force(df, 'plots/mu_vs_normal_force.png')
    
    print("[3/3] 生成图表 2: μ vs Voltage (电压变化)")
    plot_mu_vs_voltage(df, 'plots/mu_vs_voltage.png')
    
    print("[4/3] 生成图表 3: μ vs Contact Area (接触面积)")
    plot_mu_vs_area(df, 'plots/mu_vs_area.png')
    
    print("\n" + "=" * 60)
    print("✓ 所有图表已生成!")
    print("=" * 60)
    print("\n图表详情:")
    print("  1. plots/mu_vs_normal_force.png")
    print("     - 左轴: 摩擦系数 μ (柱状图)")
    print("     - 右轴: 摩擦力 F (虚线)")
    print("     - X轴: Block Configuration (质量增加)")
    print()
    print("  2. plots/mu_vs_voltage.png")
    print("     - 左轴: 摩擦系数 μ (实线-圆点)")
    print("     - 右轴: 摩擦力 F (虚线-方块)")
    print("     - X轴: 电压 U (5V, 7V, 9V, 11V)")
    print()
    print("  3. plots/mu_vs_area.png")
    print("     - 左轴: 摩擦系数 μ (柱状图)")
    print("     - 右轴: 摩擦力 F (虚线点)")
    print("     - X轴: 材料 (Stahl, Polyethylen, Polyisopren)")
    print()
    print("颜色编码:")
    print("  - Stahl (钢): 蓝色")
    print("  - Polyethylen (聚乙烯): 橙色")
    print("  - Polyisopren (聚异戊二烯): 绿色")
    print()

if __name__ == '__main__':
    generate_dual_axis_plots()
