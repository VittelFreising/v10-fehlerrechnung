import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

"""
Material Color Mapping:
- Stahl: Steel (Stahlblock)
- Weiss: Polyethylen (white block/polyethylene)
- Schwarz: Polyisopren (black block/polyisoprene)
"""

def get_material_label(material_name):
    """将材料代码转换为显示标签"""
    material_map = {
        'Weiss': 'Polyethylen',
        'Schwarz': 'Polyisopren',
        'Stahl': 'Stahl'
    }
    return material_map.get(material_name, material_name)

def plot_mu_vs_force(df, output_path):
    r"""图1: 摩擦系数 vs 重量 (重量变化实验)
    左Y轴: 摩擦系数 μ
    右Y轴: 摩擦力 F
    横轴: 重量 (kg)
    """
    fig, ax1 = plt.subplots(figsize=(12, 6))
    
    # 过滤出重量变化实验的数据
    subset = df[df['Experiment'] == 'Weight_Var'].copy()
    
    # 聚合 (取均值和最大误差)
    agg_df = subset.groupby(['Material', 'Block_Config']).agg(
        mass_g=('Mass_g_Avg', 'mean'),
        mu_avg=('mu_avg', 'mean'),
        mu_delta=('mu_delta', 'max'),
        messwert_avg=('Messwert_Avg', 'mean'),
        messwert_delta=('Messwert_Delta', 'max')
    ).reset_index()

    # 排序
    block_order = ['B', 'B+1', 'B+1+2', 'B+1+2+3', 'B+1+2+3+4']
    agg_df['Block_Config'] = pd.Categorical(agg_df['Block_Config'], categories=block_order, ordered=True)
    agg_df = agg_df.sort_values(['Block_Config'])
    
    # 将重量从克转换为千克
    agg_df['Weight_kg'] = agg_df['mass_g'] / 1000.0

    # 颜色定义
    colors = {'Stahl': '#1f77b4', 'Weiss': '#ff7f0e', 'Schwarz': '#2ca02c'}
    
    # 绘制μ (左Y轴) - 线条图
    for mat in agg_df['Material'].unique():
        mat_data = agg_df[agg_df['Material'] == mat].sort_values('Weight_kg')
        ax1.errorbar(mat_data['Weight_kg'], mat_data['mu_avg'], yerr=mat_data['mu_delta'], 
                     label=f"{get_material_label(mat)} (μ)", fmt='-o', capsize=5, 
                     color=colors.get(mat, None), linewidth=2, markersize=7)

    ax1.set_xlabel('Weight (kg)', fontsize=11)
    ax1.set_ylabel(r'Friction Coefficient ($\mu$)', fontsize=11, color='steelblue')
    ax1.tick_params(axis='y', labelcolor='steelblue')
    ax1.grid(True, linestyle='--', alpha=0.3)

    # 创建右Y轴 (摩擦力F)
    ax2 = ax1.twinx()
    
    for mat in agg_df['Material'].unique():
        mat_data = agg_df[agg_df['Material'] == mat].sort_values('Weight_kg')
        ax2.errorbar(mat_data['Weight_kg'], mat_data['messwert_avg'], yerr=mat_data['messwert_delta'], 
                    fmt='--s', color=colors.get(mat, None), linewidth=2, 
                    markersize=6, capsize=3, label=f"{get_material_label(mat)} (F)", alpha=0.6)

    ax2.set_ylabel('Friction Force (F) [N]', fontsize=11, color='darkred')
    ax2.tick_params(axis='y', labelcolor='darkred')

    fig.suptitle('Friction Coefficient vs Weight (5V, Large Area)', fontsize=12, fontweight='bold')
    
    # 合并两个图例
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=9)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()

def plot_mu_vs_voltage(df, output_path):
    r"""图2: 摩擦系数 vs 电压
    左Y轴: 摩擦系数 μ
    右Y轴: 摩擦力 F
    """
    fig, ax1 = plt.subplots(figsize=(12, 6))
    
    # 包含 5V (Weight_Var 中 Block B 的数据) 和 7-11V (Voltage_Var)
    # 过滤条件: Block B, 大面积
    subset = df[(df['Block_Config'] == 'B') & 
                ((df['Experiment'] == 'Voltage_Var') | 
                 ((df['Experiment'] == 'Weight_Var') & (df['Voltage_V'] == '5V')))
               ].copy()
    
    # 提取电压数字
    subset['Voltage_Num'] = subset['Voltage_V'].str.extract(r'(\d+)').astype(float)
    
    # 聚合
    agg_df = subset.groupby(['Material', 'Voltage_Num']).agg(
        mu_avg=('mu_avg', 'mean'),
        mu_delta=('mu_delta', 'max'),
        messwert_avg=('Messwert_Avg', 'mean'),
        messwert_delta=('Messwert_Delta', 'max')
    ).reset_index().sort_values('Voltage_Num')

    # 颜色定义
    colors = {'Stahl': '#1f77b4', 'Weiss': '#ff7f0e', 'Schwarz': '#2ca02c'}
    
    # 绘制μ (左Y轴)
    for mat in agg_df['Material'].unique():
        data = agg_df[agg_df['Material'] == mat]
        ax1.errorbar(data['Voltage_Num'], data['mu_avg'], yerr=data['mu_delta'], 
                     label=f"{get_material_label(mat)} (μ)", fmt='-o', capsize=5, 
                     color=colors.get(mat, None), linewidth=2, markersize=7)

    ax1.set_xlabel('Voltage (V)', fontsize=11)
    ax1.set_ylabel(r'Friction Coefficient ($\mu$)', fontsize=11, color='steelblue')
    ax1.tick_params(axis='y', labelcolor='steelblue')
    ax1.set_xticks([5, 7, 9, 11])
    ax1.grid(True, linestyle='--', alpha=0.3)

    # 创建右Y轴 (摩擦力F)
    ax2 = ax1.twinx()
    
    for mat in agg_df['Material'].unique():
        data = agg_df[agg_df['Material'] == mat]
        ax2.errorbar(data['Voltage_Num'], data['messwert_avg'], yerr=data['messwert_delta'], 
                    fmt='--s', color=colors.get(mat, None), linewidth=2, 
                    markersize=6, capsize=3, label=f"{get_material_label(mat)} (F)", alpha=0.6)

    ax2.set_ylabel('Friction Force (F) [N]', fontsize=11, color='darkred')
    ax2.tick_params(axis='y', labelcolor='darkred')

    fig.suptitle('Friction Coefficient vs Voltage (Large Area, Block B)', fontsize=12, fontweight='bold')
    
    # 合并两个图例
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='best', fontsize=9)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()

def plot_mu_vs_area(df, output_path):
    r"""图3: 摩擦系数 vs 面积 (对比 小面积 vs 大面积)
    左Y轴: 摩擦系数 μ
    右Y轴: 摩擦力 F
    """
    fig, ax1 = plt.subplots(figsize=(12, 6))
    
    # 条件: 5V, Block B
    subset = df[(df['Voltage_V'] == '5V') & (df['Block_Config'] == 'B')].copy()
    
    # 标记面积类型
    # 大约 > 30 为大面积，< 30 为小面积
    subset['Area_Type'] = subset['Area_cm2'].apply(lambda x: 'Large' if x > 30 else 'Small')
    
    # 聚合
    agg_df = subset.groupby(['Material', 'Area_Type', 'Area_cm2']).agg(
        mass_g=('Mass_g_Avg', 'mean'),
        mu_avg=('mu_avg', 'mean'),
        mu_delta=('mu_delta', 'max'),
        messwert_avg=('Messwert_Avg', 'mean'),
        messwert_delta=('Messwert_Delta', 'max')
    ).reset_index()
    
    # 将重量从克转换为千克
    agg_df['weight_kg'] = agg_df['mass_g'] / 1000.0

    # 颜色定义
    colors = {'Stahl': '#1f77b4', 'Weiss': '#ff7f0e', 'Schwarz': '#2ca02c'}
    
    # 绘制μ的线条图 (左Y轴) - 按面积排序
    for mat in agg_df['Material'].unique():
        mat_data = agg_df[agg_df['Material'] == mat].sort_values('Area_cm2')
        # 创建包含重量信息的标签
        labels = [f"{get_material_label(mat)} (μ)\n{w:.2f} kg" for w in mat_data['weight_kg']]
        ax1.errorbar(mat_data['Area_cm2'], mat_data['mu_avg'], yerr=mat_data['mu_delta'],
                     label=f"{get_material_label(mat)} (μ)", fmt='-o', capsize=5,
                     color=colors.get(mat, None), linewidth=2, markersize=7)

    ax1.set_xlabel('Contact Area (cm²)', fontsize=11)
    ax1.set_ylabel(r'Friction Coefficient ($\mu$)', fontsize=11, color='steelblue')
    ax1.tick_params(axis='y', labelcolor='steelblue')
    ax1.grid(True, linestyle='--', alpha=0.3)

    # 创建右Y轴 (摩擦力F)
    ax2 = ax1.twinx()
    
    for mat in agg_df['Material'].unique():
        mat_data = agg_df[agg_df['Material'] == mat].sort_values('Area_cm2')
        ax2.errorbar(mat_data['Area_cm2'], mat_data['messwert_avg'], yerr=mat_data['messwert_delta'],
                    fmt='--s', color=colors.get(mat, None), linewidth=2,
                    markersize=6, capsize=3, label=f"{get_material_label(mat)} (F)", alpha=0.6)

    ax2.set_ylabel('Friction Force (F) [N]', fontsize=11, color='darkred')
    ax2.tick_params(axis='y', labelcolor='darkred')

    fig.suptitle('Friction Coefficient vs Contact Area (5V)', fontsize=12, fontweight='bold')
    
    # 合并两个图例
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=9)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()