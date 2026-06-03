import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
from scipy import stats
import os

# ─────────────────────────────────────────────
# HR Analytics — Employee Attrition Analysis
# Script 02: Attrition Analysis & Visualisation
# ─────────────────────────────────────────────

sns.set_theme(style="whitegrid")
os.makedirs("outputs/figures", exist_ok=True)


def generate_hr_data(n=1470):
    """Generate an IBM HR Analytics-style dataset."""
    np.random.seed(42)
    departments = ["Sales", "Research & Development", "Human Resources"]
    job_roles = {
        "Sales": ["Sales Executive", "Sales Representative", "Manager"],
        "Research & Development": ["Research Scientist", "Laboratory Technician",
                                    "Research Director", "Healthcare Representative"],
        "Human Resources": ["Human Resources", "Manager"]
    }
    dept = np.random.choice(departments, n, p=[0.30, 0.60, 0.10])
    role = [np.random.choice(job_roles[d]) for d in dept]
    age = np.random.randint(18, 60, n)
    tenure = np.random.randint(0, 40, n)
    monthly_income = np.round(np.random.lognormal(8.5, 0.5, n)).astype(int)
    job_satisfaction = np.random.randint(1, 5, n)
    work_life_balance = np.random.randint(1, 5, n)
    overtime = np.random.choice(["Yes", "No"], n, p=[0.28, 0.72])
    distance = np.random.randint(1, 30, n)
    job_level = np.random.randint(1, 6, n)

    # Attrition probability
    p = (
        0.05
        + 0.15 * (dept == "Sales")
        + 0.12 * (overtime == "Yes")
        + 0.10 * (job_satisfaction <= 2)
        + 0.08 * (tenure < 2)
        + 0.05 * (distance > 20)
        - 0.08 * (job_level >= 4)
        - 0.05 * (monthly_income > 10000)
    )
    p = np.clip(p, 0.02, 0.90)
    attrition = (np.random.rand(n) < p).astype(int)

    df = pd.DataFrame({
        "employee_id": range(1000, 1000 + n),
        "age": age,
        "department": dept,
        "job_role": role,
        "job_level": job_level,
        "years_at_company": tenure,
        "monthly_income": monthly_income,
        "job_satisfaction": job_satisfaction,
        "work_life_balance": work_life_balance,
        "overtime": overtime,
        "distance_from_home": distance,
        "gender": np.random.choice(["Male", "Female"], n),
        "education": np.random.randint(1, 6, n),
        "attrition": attrition
    })
    return df


def overview(df):
    total = len(df)
    churned = df["attrition"].sum()
    print("=" * 55)
    print("HR ATTRITION ANALYSIS — OVERVIEW")
    print("=" * 55)
    print(f"Total employees:      {total:,}")
    print(f"Attrited employees:   {churned:,}")
    print(f"Overall attrition:    {churned/total*100:.1f}%")
    print(f"Retained:             {total - churned:,} ({(1 - churned/total)*100:.1f}%)")
    print(f"\nAge range:            {df['age'].min()} – {df['age'].max()} yrs")
    print(f"Avg tenure:           {df['years_at_company'].mean():.1f} yrs")
    print(f"Median monthly income: ${df['monthly_income'].median():,.0f}")


def plot_department_attrition(df):
    dept_stats = df.groupby("department").agg(
        total=("attrition", "count"),
        attrited=("attrition", "sum")
    ).reset_index()
    dept_stats["rate"] = dept_stats["attrited"] / dept_stats["total"]

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    palette = ["#C00000", "#2E74B5", "#70AD47"]

    sns.barplot(data=dept_stats, x="department", y="rate", palette=palette, ax=axes[0])
    axes[0].set_title("Attrition Rate by Department", fontweight="bold")
    axes[0].set_ylabel("Attrition Rate")
    axes[0].set_xlabel("")
    axes[0].yaxis.set_major_formatter(mticker.FuncFormatter(lambda y, _: f"{y:.0%}"))
    axes[0].set_xticklabels(axes[0].get_xticklabels(), rotation=10)

    role_stats = df.groupby("job_role").agg(
        total=("attrition", "count"),
        attrited=("attrition", "sum")
    ).reset_index()
    role_stats["rate"] = role_stats["attrited"] / role_stats["total"]
    role_stats = role_stats.sort_values("rate", ascending=False)

    sns.barplot(data=role_stats, x="rate", y="job_role", palette="Reds_d", ax=axes[1])
    axes[1].set_title("Attrition Rate by Job Role", fontweight="bold")
    axes[1].set_xlabel("Attrition Rate")
    axes[1].set_ylabel("")
    axes[1].xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:.0%}"))

    plt.tight_layout()
    plt.savefig("outputs/figures/department_attrition.png", dpi=150)
    print("Saved: department_attrition.png")
    plt.show()


def plot_key_drivers(df):
    fig, axes = plt.subplots(2, 2, figsize=(13, 10))

    # Satisfaction score
    sat = df.groupby("job_satisfaction")["attrition"].mean().reset_index()
    sns.barplot(data=sat, x="job_satisfaction", y="attrition",
                palette="RdYlGn_r", ax=axes[0][0])
    axes[0][0].set_title("Attrition by Job Satisfaction", fontweight="bold")
    axes[0][0].set_xlabel("Job Satisfaction (1=Low, 4=High)")
    axes[0][0].set_ylabel("Attrition Rate")
    axes[0][0].yaxis.set_major_formatter(mticker.FuncFormatter(lambda y, _: f"{y:.0%}"))

    # Overtime
    ot = df.groupby("overtime")["attrition"].mean().reset_index()
    sns.barplot(data=ot, x="overtime", y="attrition",
                palette=["#2E74B5", "#C00000"], ax=axes[0][1])
    axes[0][1].set_title("Attrition Rate: Overtime vs No Overtime", fontweight="bold")
    axes[0][1].set_xlabel("")
    axes[0][1].set_ylabel("Attrition Rate")
    axes[0][1].yaxis.set_major_formatter(mticker.FuncFormatter(lambda y, _: f"{y:.0%}"))

    # Monthly income distribution
    sns.boxplot(data=df, x="attrition", y="monthly_income",
                palette=["#2E74B5", "#C00000"], ax=axes[1][0])
    axes[1][0].set_title("Monthly Income vs Attrition", fontweight="bold")
    axes[1][0].set_xticklabels(["Retained", "Attrited"])
    axes[1][0].set_ylabel("Monthly Income ($)")
    axes[1][0].set_xlabel("")
    axes[1][0].yaxis.set_major_formatter(mticker.FuncFormatter(lambda y, _: f"${y:,.0f}"))

    # Tenure risk window
    df["tenure_bucket"] = pd.cut(
        df["years_at_company"], bins=[-1, 1, 3, 7, 15, 100],
        labels=["0–1 yr", "2–3 yrs", "4–7 yrs", "8–15 yrs", "15+ yrs"])
    ten = df.groupby("tenure_bucket")["attrition"].mean().reset_index()
    sns.barplot(data=ten, x="tenure_bucket", y="attrition",
                palette="Blues_r", ax=axes[1][1])
    axes[1][1].set_title("Attrition Rate by Tenure", fontweight="bold")
    axes[1][1].set_xlabel("Years at Company")
    axes[1][1].set_ylabel("Attrition Rate")
    axes[1][1].yaxis.set_major_formatter(mticker.FuncFormatter(lambda y, _: f"{y:.0%}"))

    plt.suptitle("Key Drivers of Employee Attrition", fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.savefig("outputs/figures/key_drivers.png", dpi=150)
    print("Saved: key_drivers.png")
    plt.show()


def statistical_tests(df):
    print("\n" + "=" * 55)
    print("STATISTICAL VALIDATION")
    print("=" * 55)

    # Chi-squared: overtime vs attrition
    ct = pd.crosstab(df["overtime"], df["attrition"])
    chi2, p, dof, _ = stats.chi2_contingency(ct)
    print(f"\nChi-squared test — Overtime vs Attrition:")
    print(f"  chi2 = {chi2:.3f}, p = {p:.4f} {'✓ Significant' if p < 0.05 else '✗ Not significant'}")

    # Mann-Whitney U: monthly income
    retained = df[df["attrition"] == 0]["monthly_income"]
    attrited = df[df["attrition"] == 1]["monthly_income"]
    stat, p = stats.mannwhitneyu(retained, attrited, alternative="greater")
    print(f"\nMann-Whitney U — Monthly Income (Retained > Attrited):")
    print(f"  U = {stat:.0f}, p = {p:.4f} {'✓ Significant' if p < 0.05 else '✗ Not significant'}")
    print(f"  Median retained: ${retained.median():,.0f} | Median attrited: ${attrited.median():,.0f}")

    # Chi-squared: job satisfaction vs attrition
    ct2 = pd.crosstab(df["job_satisfaction"], df["attrition"])
    chi2, p, dof, _ = stats.chi2_contingency(ct2)
    print(f"\nChi-squared test — Job Satisfaction vs Attrition:")
    print(f"  chi2 = {chi2:.3f}, p = {p:.4f} {'✓ Significant' if p < 0.05 else '✗ Not significant'}")


if __name__ == "__main__":
    df = generate_hr_data()
    overview(df)
    plot_department_attrition(df)
    plot_key_drivers(df)
    statistical_tests(df)
    print("\nAnalysis complete. Outputs saved to outputs/figures/")
