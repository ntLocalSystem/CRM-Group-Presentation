import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd

# ==========================================
# UPMC Ransomware Risk Simulation (Final Sophos Data Edition)
# ==========================================
# Strategic Context:
# 1. UPMC Scale: $30B Revenue ($82.2M/day), 100k Employees.
# 2. Sophos 2024 Data (Image Analysis): 
#    - 36% of Healthcare victims take >1 month to recover.
#    - 7% take 3-6 months. (Long-tail risk is massive).
#    - Attack Rate: 67% (Industry Average).

# --- Configuration: Simulation Parameters (Unit: $ Million USD) ---
NUM_SIMULATIONS = 10000
INVESTMENT_COST = 15.0  # $15M Investment in Resilience (Immutable Backups)

# 1. Loss Event Frequency (LEF)
# Source: Sophos 2024 (67% attack rate in Healthcare)
PROB_ATTACK_BASELINE = 0.67  # High frequency
PROB_ATTACK_MITIGATED = 0.15 # Reduced success rate

# 2. Loss Magnitude (LM) - Uniform Distribution

# A. Downtime Days (CRITICAL UPDATE based on Sophos Chart)
# Previous: [10, 35] -> Too optimistic.
# New: [15, 120]
# Rationale: 
# - Min (15): Skips the lucky 21% who recover in <1 week.
# - Max (120): Covers the 29% (1-3 months) and the tail of 7% (3-6 months).
DAYS_DOWN_BASELINE = [15, 120]       
DAYS_DOWN_MITIGATED = [2, 14] # Resilience strategy aims for <2 weeks.      

# B. Daily Financial Loss (Revenue + Operational Cost)
# Revenue: $82.2M/day. 
# Range: $30M (Partial/Long-tail drag) to $95M (Acute Total Halt).
DAILY_LOSS_RANGE = [30.0, 95.0]  

# C. Response & Recovery Costs
# "Hybrid Recovery" (Pay + Restore) doubles costs.
RESPONSE_COST_RANGE = [25.0, 85.0]

# D. Secondary Loss (Legal, Fines, Reputation)
# 4M Insurance members + Class Actions.
SECONDARY_LOSS_RANGE = [50.0, 650.0] 

def run_fair_simulation(prob_attack, days_range, label):
    losses = []
    for _ in range(NUM_SIMULATIONS):
        # Frequency
        if np.random.random() > prob_attack:
            losses.append(0)
            continue
        
        # Magnitude (Uniform Distribution)
        days = np.random.uniform(days_range[0], days_range[1])
        daily_cost = np.random.uniform(DAILY_LOSS_RANGE[0], DAILY_LOSS_RANGE[1])
        
        downtime_loss = days * daily_cost
        response_loss = np.random.uniform(RESPONSE_COST_RANGE[0], RESPONSE_COST_RANGE[1])
        secondary_loss = np.random.uniform(SECONDARY_LOSS_RANGE[0], SECONDARY_LOSS_RANGE[1])
        
        total_loss = downtime_loss + response_loss + secondary_loss
        losses.append(total_loss)
    
    return np.array(losses)

# --- Execution ---
losses_baseline = run_fair_simulation(PROB_ATTACK_BASELINE, DAYS_DOWN_BASELINE, "Baseline")
losses_mitigated = run_fair_simulation(PROB_ATTACK_MITIGATED, DAYS_DOWN_MITIGATED, "Mitigated")

# --- Metrics Calculation ---
ale_baseline = np.mean(losses_baseline)
ale_mitigated = np.mean(losses_mitigated)
roi_reduction = ale_baseline - ale_mitigated
rosi = ((roi_reduction - INVESTMENT_COST) / INVESTMENT_COST) * 100

impact_baseline = losses_baseline[losses_baseline > 0]
impact_mitigated = losses_mitigated[losses_mitigated > 0]

# --- Console Report ---
print(f"===== UPMC Strategic Risk Analysis (Sophos 'Long-Tail' Model) =====")
print(f"CRITICAL UPDATE: Downtime Max set to 120 days (reflecting 36% >1 month stat).")
print(f"Investment: ${INVESTMENT_COST}M | Revenue Basis: $30B/yr")
print("-" * 60)
print(f" [Current State (Critical Risk)]")
print(f"  - ALE (Annual Expected Loss):   ${ale_baseline:,.1f} M") 
print(f"  - 90% VaR (Worst Case):         ${np.percentile(losses_baseline, 90):,.1f} M")
print(f"  - Max Simulated Loss:           ${np.max(losses_baseline):,.1f} M")
print(f"\n [Mitigated State]")
print(f"  - ALE (Annual Expected Loss):   ${ale_mitigated:,.1f} M")
print("-" * 60)
print(f" [Strategic Value]")
print(f"  - ROSI (Return on Investment):  {rosi:,.0f}%")


# ==========================================
# Visualization 1: Histogram
# ==========================================
plt.figure(figsize=(12, 6))
plt.hist(impact_baseline, bins=50, alpha=0.6, color='firebrick', label='Baseline Impact (Max 120 Days)', density=True)
plt.hist(impact_mitigated, bins=50, alpha=0.7, color='seagreen', label='Mitigated Impact', density=True)
plt.axvline(np.mean(impact_baseline), color='darkred', linestyle='--', linewidth=2, label=f'Avg: ${np.mean(impact_baseline):.0f}M')
plt.axvline(np.mean(impact_mitigated), color='darkgreen', linestyle='--', linewidth=2, label=f'Avg: ${np.mean(impact_mitigated):.0f}M')

plt.title('Financial Impact Distribution: Including "Long-Tail" Recovery Risk\n(Sophos 2024 Data Integration)', fontsize=14)
plt.xlabel('Financial Loss ($ Million)', fontsize=12)
plt.ylabel('Probability Density', fontsize=12)
plt.legend()
plt.grid(axis='y', alpha=0.3)
ax = plt.gca()
ax.xaxis.set_major_formatter(ticker.FormatStrFormatter('$%0.0fM'))
plt.tight_layout()
print("Generated: Histogram (Long-Tail)")
plt.show()

# ==========================================
# Visualization 2: Loss Exceedance Curve
# ==========================================
def plot_lec(losses, label, color, linestyle='-'):
    sorted_losses = np.sort(losses)
    sorted_losses_non_zero = sorted_losses[sorted_losses > 0]
    if len(sorted_losses_non_zero) == 0: return
    n_exceeding = np.arange(len(sorted_losses_non_zero), 0, -1)
    prob_exceed = n_exceeding / len(losses)
    plt.plot(sorted_losses_non_zero, prob_exceed, label=label, color=color, linewidth=2.5, linestyle=linestyle)

plt.figure(figsize=(12, 6))
plot_lec(losses_baseline, "Current State (High Risk)", "firebrick")
plot_lec(losses_mitigated, "With Strategy", "seagreen")

plt.title("Loss Exceedance Curve: The Cost of Extended Downtime", fontsize=14)
plt.xlabel("Financial Loss ($ Million)", fontsize=12)
plt.ylabel("Probability of Exceeding Loss", fontsize=12)
plt.grid(True, which="both", linestyle='--', alpha=0.5)
plt.legend(fontsize=11)
ax = plt.gca()
ax.xaxis.set_major_formatter(ticker.FormatStrFormatter('$%0.0fM'))
plt.ylim(0, 0.5) 

var90_base = np.percentile(losses_baseline, 90)
var90_mit = np.percentile(losses_mitigated, 90)
plt.annotate(f'Current 90% VaR: ${var90_base:.0f}M', xy=(var90_base, 0.1), xytext=(var90_base + 200, 0.25), arrowprops=dict(facecolor='black', shrink=0.05), fontsize=10)
plt.annotate(f'Mitigated 90% VaR: ${var90_mit:.0f}M', xy=(var90_mit, 0.02), xytext=(var90_mit + 100, 0.08), arrowprops=dict(facecolor='green', shrink=0.05), fontsize=10)

plt.tight_layout()
print("Generated: LEC")
plt.show()

# ==========================================
# Visualization 3: Executive Summary Table
# ==========================================
tbl_prob_base = f"{PROB_ATTACK_BASELINE*100:.1f}%"
tbl_prob_mit = f"{PROB_ATTACK_MITIGATED*100:.1f}%"
tbl_impact_base = f"${np.mean(impact_baseline):,.0f} M"
tbl_impact_mit = f"${np.mean(impact_mitigated):,.0f} M"
tbl_ale_base = f"${ale_baseline:,.1f} M"
tbl_ale_mit = f"${ale_mitigated:,.1f} M"
tbl_var_base = f"${np.percentile(losses_baseline, 90):,.0f} M"
tbl_var_mit = f"${np.percentile(losses_mitigated, 90):,.0f} M"
tbl_invest = f"${INVESTMENT_COST} M"
tbl_benefit = f"${roi_reduction:,.1f} M / yr"
tbl_rosi = f"{rosi:,.0f}%"

imp_prob = f"▼ {(PROB_ATTACK_BASELINE - PROB_ATTACK_MITIGATED)*100:.0f} pts"
imp_impact = f"▼ ${np.mean(impact_baseline) - np.mean(impact_mitigated):,.0f} M"
imp_ale = f"▼ ${ale_baseline - ale_mitigated:,.1f} M"
imp_var = f"▼ ${np.percentile(losses_baseline, 90) - np.percentile(losses_mitigated, 90):,.0f} M"

data = {
    "Metric": ["Annual Attack Probability", "Avg. Financial Impact (per Incident)", "Annual Expected Loss (ALE)", "Worst Case Risk (90% VaR)", "--------------------------------", "Implementation Cost", "Net Risk Reduction (Benefit)", "Return on Investment (ROSI)"],
    "Current State (Max 120 Days)": [tbl_prob_base, tbl_impact_base, tbl_ale_base, tbl_var_base, "-", "$0 M", "-", "-"],
    "After Strategy": [tbl_prob_mit, tbl_impact_mit, tbl_ale_mit, tbl_var_mit, "-", tbl_invest, tbl_benefit, tbl_rosi],
    "Improvement": [imp_prob, imp_impact, imp_ale, imp_var, "-", "(Investment)", "Benefit", "High Return"]
}
df = pd.DataFrame(data)

fig, ax = plt.subplots(figsize=(12, 6))
ax.axis('off')
table = ax.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center', colColours=["#f2f2f2", "#ffcccc", "#ccffcc", "#e6f7ff"])
table.auto_set_font_size(False); table.set_fontsize(12); table.scale(1.2, 2.5)

for (row, col), cell in table.get_celld().items():
    cell.set_edgecolor('white'); cell.set_linewidth(2)
    if row == 0: cell.set_text_props(weight='bold', color='white'); cell.set_facecolor('#404040')
    elif col == 1 and row < 5: cell.set_text_props(color='#cc0000', weight='bold')
    elif col == 2 and row < 5: cell.set_text_props(color='#006600', weight='bold')
    if row == 8: cell.set_facecolor('#ffffcc'); cell.set_text_props(weight='bold', color='black')
    if row == 5: cell.set_text_props(text=""); cell.set_facecolor('#d9d9d9'); cell.set_height(0.05)

plt.title("Executive Summary: Risk Analysis (Sophos 2024 Data Integrated)\n(36% of Victims take >1 Month to Recover)", fontsize=16, weight='bold', y=0.95)
plt.tight_layout()
print("Generated: Summary Table")
plt.show()

# ==========================================
# Visualization 4: Simple Baseline Histogram
# ==========================================
plt.figure(figsize=(10, 6))
plt.hist(impact_baseline, bins=50, color='skyblue', edgecolor='black', alpha=0.7)
avg_baseline = np.mean(impact_baseline)
var90_baseline = np.percentile(impact_baseline, 90)
plt.axvline(avg_baseline, color='green', linestyle='--', linewidth=2, label=f'Average: ${avg_baseline:,.0f}M')
plt.axvline(var90_baseline, color='red', linestyle='--', linewidth=2, label=f'90% VaR: ${var90_baseline:,.0f}M')
plt.title('Current Risk Profile (Including Long-Tail Risk)\nUPMC Case Study', fontsize=14)
plt.xlabel('Financial Loss ($ Million)', fontsize=12)
plt.ylabel('Frequency', fontsize=12)
plt.legend()
plt.grid(axis='y', alpha=0.5)
ax = plt.gca()
ax.xaxis.set_major_formatter(ticker.FormatStrFormatter('$%0.0fM'))
plt.tight_layout()
print("Generated: Simple Baseline")
plt.show()