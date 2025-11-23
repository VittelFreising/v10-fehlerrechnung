import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

def plot_mu_vs_force(df, output_path):
    """图1: 摩擦系数 vs 法向力 (重量变化实验)"""
    plt.figure(figsize=(10, 6))
    
    # 过滤出重量变化实验的数据
    subset = df[df['Experiment'] == 'Weight_Var'].copy()
    
    # 聚合 (取均值和最大误差)
    agg_df = subset.groupby(['Material', 'Block_Config']).agg(
        mu_avg=('mu_avg', 'mean'),
        mu_delta=('mu_delta', 'max')
    ).reset_index()

    # 排序
    block_order = ['B', 'B+1', 'B+1+2', 'B+1+2+3', 'B+1+2+3+4']
    agg_df['Block_Config'] = pd.Categorical(agg_df['Block_Config'], categories=block_order, ordered=True)
    agg_df = agg_df.sort_values('Block_Config')

    # 绘图
    materials = agg_df['Material'].unique()
    width = 0.25
    x = np.arange(len(block_order))
    
    for i, mat in enumerate(materials):
        mat_data = agg_df[agg_df['Material'] == mat]
        # 对齐数据
        mat_data = mat_data.set_index('Block_Config').reindex(block_order).reset_index()
        
        offset = (i - 1) * width
        plt.bar(x + offset, mat_data['mu_avg'], width, label=mat, 
                yerr=mat_data['mu_delta'], capsize=5, alpha=0.8)

    plt.xticks(x, block_order)
    plt.xlabel('Block Configuration (Mass Increase)')
    plt.ylabel('Friction Coefficient ($\mu$)')
    plt.title('Friction Coefficient vs Normal Force (5V, Large Area)')
    plt.legend(title='Material')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()

def plot_mu_vs_voltage(df, output_path):
    """图2: 摩擦系数 vs 电压"""
    plt.figure(figsize=(10, 6))
    
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
        mu_delta=('mu_delta', 'max')
    ).reset_index().sort_values('Voltage_Num')

    # 绘图
    for mat in agg_df['Material'].unique():
        data = agg_df[agg_df['Material'] == mat]
        plt.errorbar(data['Voltage_Num'], data['mu_avg'], yerr=data['mu_delta'], 
                     label=mat, fmt='-o', capsize=5)

    plt.xlabel('Voltage (V)')
    plt.ylabel('Friction Coefficient ($\mu$)')
    plt.title('Friction Coefficient vs Voltage (Large Area, Block B)')
    plt.legend(title='Material')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.xticks([5, 7, 9, 11])
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()

def plot_mu_vs_area(df, output_path):
    """图3: 摩擦系数 vs 面积 (对比 小面积 vs 大面积)"""
    plt.figure(figsize=(8, 6))
    
    # 条件: 5V, Block B
    subset = df[(df['Voltage_V'] == '5V') & (df['Block_Config'] == 'B')].copy()
    
    # 标记面积类型
    # 大约 > 30 为大面积，< 30 为小面积
    subset['Area_Type'] = subset['Area_cm2'].apply(lambda x: 'Large' if x > 30 else 'Small')
    
    # 聚合
    agg_df = subset.groupby(['Material', 'Area_Type', 'Area_cm2']).agg(
        mu_avg=('mu_avg', 'mean'),
        mu_delta=('mu_delta', 'max')
    ).reset_index()

    # 绘图 (用简单的 Bar Plot 对比)
    sns.barplot(data=agg_df, x='Material', y='mu_avg', hue='Area_Type', 
                capsize=0.1, alpha=0.8, edgecolor='black')
    
    # 由于 seaborn barplot 的误差棒比较难自定义，我们手动添加误差棒
    # 这里为了代码简洁，直接使用 errorbar 参数在上面的 sns.barplot 中通常不起作用(如果数据是聚合过的)
    # 所以我们使用 matplotlib 的 errorbar 叠加
    
    # 获取柱状图的坐标信息有点复杂，我们简化：直接画 Point Plot 或者手动 Bar
    plt.clf() # 清除
    
    materials = agg_df['Material'].unique()
    x = np.arange(len(materials))
    width = 0.35
    
    for i, area_type in enumerate(['Small', 'Large']):
        type_data = agg_df[agg_df['Area_Type'] == area_type]
        # 确保对齐
        type_data = type_data.set_index('Material').reindex(materials).reset_index()
        
        offset = (i - 0.5) * width
        # Label 包含具体面积信息 (取第一个非空值作为 label 示例)
        area_val = type_data['Area_cm2'].mean() 
        label = f"{area_type} Area (~{area_val:.0f} $cm^2$)"
        
        plt.bar(x + offset, type_data['mu_avg'], width, label=label,
                yerr=type_data['mu_delta'], capsize=5, alpha=0.8)

    plt.xticks(x, materials)
    plt.xlabel('Material')
    plt.ylabel('Friction Coefficient ($\mu$)')
    plt.title('Friction Coefficient vs Contact Area (5V, Block B)')
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()