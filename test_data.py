import pandas as pd
df = pd.read_csv('data/processed_data.csv')
weight_var = df[df['Experiment']=='Weight_Var'].groupby('Block_Config')[['Messwert_Avg','Fn_avg','mu_avg']].mean()
print(weight_var)
print('\n摩擦力 vs 法向力 的增长率:')
f_start = weight_var.iloc[0]['Messwert_Avg']
fn_start = weight_var.iloc[0]['Fn_avg']
f_end = weight_var.iloc[-1]['Messwert_Avg']
fn_end = weight_var.iloc[-1]['Fn_avg']
print(f'摩擦力: {f_start:.2f} -> {f_end:.2f} (增长 {(f_end/f_start-1)*100:.1f}%)')
print(f'法向力: {fn_start:.2f} -> {fn_end:.2f} (增长 {(fn_end/fn_start-1)*100:.1f}%)')
print(f'摩擦系数: {weight_var.iloc[0]["mu_avg"]:.4f} -> {weight_var.iloc[-1]["mu_avg"]:.4f}')
