import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def generate_pipeline_visualizations(processed_dir: str = "data/processed", output_dir: str = "data/plots"):
    """
    Reads the separate, processed bank assets and generates analytical plots
    for stakeholder presentations and KPI verification.
    """
    banks = ["CBE", "Abyssinia", "Dashen"]
    combined_data = []

    
    for bank in banks:
        safe_name = bank.lower().replace(" ", "_")
        file_path = os.path.join(processed_dir, f"{safe_name}_thematic_reviews.csv")
        
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            df['bank'] = bank  
            combined_data.append(df)

    if not combined_data:
        print("No processed files found to visualize.")
        return

    final_df = pd.concat(combined_data, ignore_index=True)
    os.makedirs(output_dir, exist_ok=True)
    
    sns.set_theme(style="whitegrid")
    plt.rcParams.update({'font.size': 11, 'axes.labelsize': 12, 'axes.titlesize': 14})

   
    plt.figure(figsize=(10, 6))
    ax1 = sns.countplot(
        data=final_df, 
        x='bank', 
        hue='sentiment_label', 
        palette={'POSITIVE': '#2ecc71', 'NEGATIVE': '#e74c3c', 'NEUTRAL': '#95a5a6'}
    )
    plt.title("Sentiment Label Distribution by Bank (3-Class Model Validation)")
    plt.xlabel("Bank Entity")
    plt.ylabel("Review Count")
    plt.legend(title="Sentiment Category")
    plt.tight_layout()
    
    plot1_path = os.path.join(output_dir, "sentiment_distribution.png")
    plt.savefig(plot1_path, dpi=300)
    plt.close()

    
    plt.figure(figsize=(12, 7))
   
    theme_df = final_df[final_df['identified_theme'] != 'General Feedback']
    
    ax2 = sns.countplot(
        data=theme_df,
        y='identified_theme',
        hue='bank',
        palette='viridis',
        order=theme_df['identified_theme'].value_counts().index
    )
    plt.title("Actionable Business Themes Identified per Bank (KPI: 3+ Themes)")
    plt.xlabel("Review Frequency Count")
    plt.ylabel("Identified Corporate Issues")
    plt.legend(title="Bank Tenant")
    plt.tight_layout()

    plot2_path = os.path.join(output_dir, "thematic_breakdown.png")
    plt.savefig(plot2_path, dpi=300)
    plt.close()

    print(f"\n Charts successfully plotted and saved to the storage layer!")
    print(f"Check out the new visual assets inside: {output_dir}/")