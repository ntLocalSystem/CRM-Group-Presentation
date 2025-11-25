import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# ==========================================
# UPMC Ransomware Risk Simulation
# ==========================================

# --- Configuration: Simulation Parameters (Unit: $ Million USD) ---
NUM_SIMULATIONS = 10000

# 1. Loss Event Frequency (LEF) - CONSTANT
# Source: Sophos 2024 (67% attack rate in Healthcare)
PROB_ATTACK = 0.67

# 2. Loss Magnitude (LM) - Recovery Time
# Baseline: 2 weeks to 3 months (Paper charts, slow restore)
DAYS_DOWN_BASELINE = [21, 90]

# Mitigated: Rapid Recovery Target (3 to 45 Days)
DAYS_DOWN_MITIGATED = [3, 45]

# 3. Daily Financial Impact (Estimated)
# UPMC Daily Revenue is ~$82M.
# Assumed Impact: 10% to 15% of Daily Revenue. Based on the UHS attack case.
# Assumed Impact: $8M - $12M per day
DAILY_IMPACT_RANGE = [8.0, 12.0] 

def run_simulation(prob_attack, days_range):
    """Executes the Monte Carlo simulation for risk analysis."""
    losses = []
    for _ in range(NUM_SIMULATIONS):
        # Frequency Check
        if np.random.random() > prob_attack:
            losses.append(0)
            continue
        
        # Magnitude Calculation (Net Impact Base)
        days = np.random.uniform(days_range[0], days_range[1])
        daily_loss = np.random.uniform(DAILY_IMPACT_RANGE[0], DAILY_IMPACT_RANGE[1])
        
        # Total Loss = Days * Daily Impact
        total_loss = days * daily_loss
        losses.append(total_loss)
    
    return np.array(losses)

def print_console_report(impact_base, impact_mit):
    """Prints a structured text report of the simulation results."""
    # Metrics Calculation
    avg_base = np.mean(impact_base)
    p90_base = np.percentile(impact_base, 90)
    p95_base = np.percentile(impact_base, 95)
    max_base = np.max(impact_base)

    avg_mit = np.mean(impact_mit)
    p90_mit = np.percentile(impact_mit, 90)
    p95_mit = np.percentile(impact_mit, 95)
    
    # Reduction Stats
    reduct_avg = avg_base - avg_mit
    reduct_p90 = p90_base - p90_mit

    print(f"===== UPMC Risk Analysis (Adjusted for Realistic Net Impact) =====")
    print(f"Assumption: Daily Loss is $20M-$35M (Not full revenue)")
    print("-" * 60)
    print(f" [Baseline: Current Exposure (14-90 Days)]")
    print(f"  - Average Loss:                ${avg_base:,.1f} M")
    print(f"  - 90% VaR (Severe Case):       ${p90_base:,.1f} M")
    print(f"  - 95% VaR (Extreme Case):      ${p95_base:,.1f} M")
    print(f"\n [Mitigated: Optimized Recovery (3-45 Days)]")
    print(f"  - Average Loss:                ${avg_mit:,.1f} M")
    print(f"  - 90% VaR:                     ${p90_mit:,.1f} M")
    print("-" * 60)
    print(f" [Value of Mitigation]")
    print(f"  - Avoided Loss (Average):      ${reduct_avg:,.1f} M per incident")
    print("=" * 60)

def generate_risk_chart(impact_base, impact_mit):
    """Generates, saves, and displays the risk comparison histogram with P90/P95."""
    plt.figure(figsize=(12, 6))

    # Metrics
    avg_base = np.mean(impact_base)
    p90_base = np.percentile(impact_base, 90)
    p95_base = np.percentile(impact_base, 95)

    avg_mit = np.mean(impact_mit)

    # Plot Histograms
    plt.hist(impact_base, bins=50, alpha=0.5, color='firebrick', label='Baseline (Slow Recovery)', density=True)
    plt.hist(impact_mit, bins=50, alpha=0.7, color='dodgerblue', label='Mitigated (Rapid Recovery)', density=True)

    # Add Vertical Lines (Baseline)
    plt.axvline(avg_base, color='darkred', linestyle='-', linewidth=2, label=f'Avg Base: ${avg_base:,.0f}M')
    plt.axvline(p90_base, color='maroon', linestyle='--', linewidth=1.5, label=f'90% Base: ${p90_base:,.0f}M')
    plt.axvline(p95_base, color='black', linestyle=':', linewidth=1.5, label=f'95% Base: ${p95_base:,.0f}M')

    # Add Vertical Lines (Mitigated)
    plt.axvline(avg_mit, color='blue', linestyle='-', linewidth=2, label=f'Avg Mit: ${avg_mit:,.0f}M')

    # Formatting
    plt.title(f'Revenue Loss Mitigation Analysis\n(Reduce Downtime to 3-45 Days)', fontsize=14)
    plt.xlabel('Revenue Loss per Incident ($ Million)', fontsize=12)
    plt.ylabel('Probability Density', fontsize=12)
    plt.legend(loc='upper right')
    plt.grid(axis='y', alpha=0.3)

    # X-axis format ($ M)
    ax = plt.gca()
    ax.xaxis.set_major_formatter(ticker.FormatStrFormatter('$%0.0fM'))

    plt.tight_layout()
    
    # Save and Show
    filename = 'upmc_risk_mitigation_adjusted.png'
    plt.savefig(filename)
    print(f"Chart saved as: {filename}")
    plt.show()

# --- Execution ---
losses_baseline = run_simulation(PROB_ATTACK, DAYS_DOWN_BASELINE)
losses_mitigated = run_simulation(PROB_ATTACK, DAYS_DOWN_MITIGATED)

# Filter for strictly non-zero impacts
impact_baseline = losses_baseline[losses_baseline > 0]
impact_mitigated = losses_mitigated[losses_mitigated > 0]

# --- Report & Visualization ---
print_console_report(impact_baseline, impact_mitigated)
generate_risk_chart(impact_baseline, impact_mitigated)