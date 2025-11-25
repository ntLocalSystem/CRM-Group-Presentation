import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# ==========================================
# UPMC Ransomware Risk Simulation(Baseline)
# ==========================================

# --- Configuration: Simulation Parameters (Unit: $ Million USD) ---
NUM_SIMULATIONS = 10000

# 1. Loss Event Frequency (LEF) - CONSTANT
# Source: Sophos 2024 (67% attack rate in Healthcare)
PROB_ATTACK = 0.67

# 2. Loss Magnitude (LM) - Recovery Time
# Source: Sophos 2024 (Volume zone: 1 month to 3 months)
# Modeling range: 21 days to 90 days
DAYS_DOWN_BASELINE = [21, 90]

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
        
        # Magnitude Calculation
        days = np.random.uniform(days_range[0], days_range[1])
        daily_loss = np.random.uniform(DAILY_IMPACT_RANGE[0], DAILY_IMPACT_RANGE[1])
        
        # Total Loss = Days * Daily Impact
        total_loss = days * daily_loss
        losses.append(total_loss)
    
    return np.array(losses)

def print_console_report(impact_base):
    """Prints a structured text report of the baseline results."""
    # Metrics Calculation
    avg_base = np.mean(impact_base)
    p90_base = np.percentile(impact_base, 90) # Significant risk
    p95_base = np.percentile(impact_base, 95) # Extreme risk
    min_base = np.min(impact_base)
    max_base = np.max(impact_base)

    print(f"===== Healthcare Ransomware Risk Analysis (Baseline) =====")
    print(f"Data Source: Sophos 2024 (67% Attack Rate)")
    print(f"Recovery Time Assumption: 21 - 90 Days")
    print("-" * 60)
    print(f" [Simulation Statistics (n={NUM_SIMULATIONS})]")
    print(f"  - Average Loss Estimate:       ${avg_base:,.1f} M")
    print(f"  - 90% VaR (Severe Case):       ${p90_base:,.1f} M")
    print(f"  - 95% VaR (Extreme Case):      ${p95_base:,.1f} M")
    print("-" * 60)
    print(f"  - Minimum Impact Case:         ${min_base:,.1f} M")
    print(f"  - Maximum Impact Case:         ${max_base:,.1f} M")
    print("=" * 60)

def generate_risk_chart(impact_base):
    """Generates, saves, and displays the baseline risk histogram."""
    plt.figure(figsize=(10, 6))

    # Metrics for plotting lines
    avg_base = np.mean(impact_base)
    p90_base = np.percentile(impact_base, 90)
    p95_base = np.percentile(impact_base, 95)

    # Plot Histogram
    plt.hist(impact_base, bins=50, alpha=0.6, color='firebrick', label='Baseline Loss Distribution', density=True)

    # Add Vertical Lines
    plt.axvline(avg_base, color='darkred', linestyle='-', linewidth=2, label=f'Average: ${avg_base:,.0f}M')
    plt.axvline(p90_base, color='maroon', linestyle='--', linewidth=1.5, label=f'90% VaR: ${p90_base:,.0f}M')
    plt.axvline(p95_base, color='black', linestyle=':', linewidth=1.5, label=f'95% VaR: ${p95_base:,.0f}M')

    # Formatting
    plt.title('Baseline Revenue Loss by Ransomware Analysis\n(Healthcare Sector: 14-90 Days to Recovery)', fontsize=14)
    plt.xlabel('Revenue Loss per Incident ($ Million)', fontsize=12)
    plt.ylabel('Probability Density', fontsize=12)
    plt.legend(loc='upper right')
    plt.grid(axis='y', alpha=0.3)

    # X-axis format ($ M)
    ax = plt.gca()
    ax.xaxis.set_major_formatter(ticker.FormatStrFormatter('$%0.0fM'))

    plt.tight_layout()
    
    # Save and Show
    filename = 'baseline_risk_analysis.png'
    plt.savefig(filename)
    print(f"Chart saved as: {filename}")
    plt.show()

# --- Execution ---
losses_baseline = run_simulation(PROB_ATTACK, DAYS_DOWN_BASELINE)

# Filter for strictly non-zero impacts (Successful attacks only)
impact_baseline = losses_baseline[losses_baseline > 0]

# --- Report & Visualization ---
print_console_report(impact_baseline)
generate_risk_chart(impact_baseline)