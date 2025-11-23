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
    r"""图1: 摩擦系数 vs 法向力 (重量变化实验)
    左Y轴: 摩擦系数 μ
    右Y轴: 摩擦力 F
    """
    fig, ax1 = plt.subplots(figsize=(12, 6))
    
    # 过滤出重量变化实验的数据
    subset = df[df['Experiment'] == 'Weight_Var'].copy()
    
    # 聚合 (取均值和最大误差)
    agg_df = subset.groupby(['Material', 'Block_Config']).agg(
        mu_avg=('mu_avg', 'mean'),
        mu_delta=('mu_delta', 'max'),
        messwert_avg=('Messwert_Avg', 'mean'),
        messwert_delta=('Messwert_Delta', 'max')
    ).reset_index()

    # 排序
    block_order = ['B', 'B+1', 'B+1+2', 'B+1+2+3', 'B+1+2+3+4']
    agg_df['Block_Config'] = pd.Categorical(agg_df['Block_Config'], categories=block_order, ordered=True)
    agg_df = agg_df.sort_values('Block_Config')

    # 绘制μ (左Y轴)
    materials = agg_df['Material'].unique()
    colors = {'Stahl': '#1f77b4', 'Weiss': '#ff7f0e', 'Schwarz': '#2ca02c'}
    width = 0.25
    x = np.arange(len(block_order))
    
    for i, mat in enumerate(materials):
        mat_data = agg_df[agg_df['Material'] == mat]
        # 对齐数据
        mat_data = mat_data.set_index('Block_Config').reindex(block_order).reset_index()
        
        offset = (i - 1) * width
        ax1.bar(x + offset, mat_data['mu_avg'], width, label=f"{get_material_label(mat)} (μ)", 
                yerr=mat_data['mu_delta'], capsize=5, alpha=0.8, color=colors.get(mat, None))

    ax1.set_xlabel('Block Configuration (Mass Increase)', fontsize=11)
    ax1.set_ylabel(r'Friction Coefficient ($\mu$)', fontsize=11, color='steelblue')
    ax1.tick_params(axis='y', labelcolor='steelblue')
    ax1.set_xticks(x)
    ax1.set_xticklabels(block_order)
    ax1.grid(axis='y', linestyle='--', alpha=0.3)

    # 创建右Y轴 (摩擦力F)
    ax2 = ax1.twinx()
    
    for i, mat in enumerate(materials):
        mat_data = agg_df[agg_df['Material'] == mat]
        # 对齐数据
        mat_data = mat_data.set_index('Block_Config').reindex(block_order).reset_index()
        
        offset = (i - 1) * width
        # 在中心位置绘制F的线条和点
        x_pos = x + offset
        ax2.errorbar(x_pos, mat_data['messwert_avg'], yerr=mat_data['messwert_delta'], 
                    fmt='o--', color=colors.get(mat, None), linewidth=2, 
                    markersize=6, capsize=3, label=f"{get_material_label(mat)} (F)", alpha=0.6)

    ax2.set_ylabel('Friction Force (F) [N]', fontsize=11, color='darkred')
    ax2.tick_params(axis='y', labelcolor='darkred')

    fig.suptitle('Friction Coefficient vs Normal Force (5V, Large Area)', fontsize=12, fontweight='bold')
    
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
    subset['Voltage_Num'] = subset['Voltage_V'].str.extract('(\d+)').astype(float)
    
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
        mu_avg=('mu_avg', 'mean'),
        mu_delta=('mu_delta', 'max'),
        messwert_avg=('Messwert_Avg', 'mean'),
        messwert_delta=('Messwert_Delta', 'max')
    ).reset_index()

    materials = agg_df['Material'].unique()
    colors = {'Stahl': '#1f77b4', 'Weiss': '#ff7f0e', 'Schwarz': '#2ca02c'}
    x = np.arange(len(materials))
    width = 0.35

    # 绘制μ的柱状图 (左Y轴)
    for i, area_type in enumerate(['Small', 'Large']):
        type_data = agg_df[agg_df['Area_Type'] == area_type]
        # 确保对齐
        type_data = type_data.set_index('Material').reindex(materials).reset_index()
        
        offset = (i - 0.5) * width
        area_val = type_data['Area_cm2'].mean() 
        label = f"{area_type} Area (~{area_val:.0f} cm²) - μ"
        
        ax1.bar(x + offset, type_data['mu_avg'], width, label=label,
                yerr=type_data['mu_delta'], capsize=5, alpha=0.8)

    ax1.set_xticks(x)
    ax1.set_xticklabels([get_material_label(mat) for mat in materials])
    ax1.set_xlabel('Material', fontsize=11)
    ax1.set_ylabel(r'Friction Coefficient ($\mu$)', fontsize=11, color='steelblue')
    ax1.tick_params(axis='y', labelcolor='steelblue')
    ax1.grid(axis='y', linestyle='--', alpha=0.3)

    # 创建右Y轴 (摩擦力F)
    ax2 = ax1.twinx()
    
    for i, area_type in enumerate(['Small', 'Large']):
        type_data = agg_df[agg_df['Area_Type'] == area_type]
        type_data = type_data.set_index('Material').reindex(materials).reset_index()
        
        offset = (i - 0.5) * width
        area_val = type_data['Area_cm2'].mean()
        label = f"{area_type} Area (~{area_val:.0f} cm²) - F"
        
        # 在柱状图中间位置绘制F的线条
        x_pos = x + offset
        ax2.errorbar(x_pos, type_data['messwert_avg'], yerr=type_data['messwert_delta'], 
                    fmt='o--', linewidth=1.5, markersize=5, capsize=3, 
                    label=label, alpha=0.6)

    ax2.set_ylabel('Friction Force (F) [N]', fontsize=11, color='darkred')
    ax2.tick_params(axis='y', labelcolor='darkred')

    fig.suptitle('Friction Coefficient vs Contact Area (5V, Block B)', fontsize=12, fontweight='bold')
    
    # 合并两个图例
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=9)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()