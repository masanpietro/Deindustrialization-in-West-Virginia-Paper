import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


path= "C:/Users/masan/OneDrive/Desktop/Midterm EconGEO/WestVirginiaGDP.xlsx"
coalgdp= pd.read_excel(path, sheet_name='Table', header=5, skipfooter=6)
df=coalgdp
df.drop(columns=['2024', '2023', '1997', '1998', '1999', '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009'], inplace=True)
year_cols = [col for col in df.columns if col.isdigit()]
df[year_cols] = df[year_cols].apply(pd.to_numeric, errors="coerce")

df_long = df.melt(
    id_vars=["GeoFips", "GeoName", "LineCode", "Description"],
    value_vars=year_cols,
    var_name="year",
    value_name="gdp"
)

df_long["year"] = df_long["year"].astype(int)

industries_to_plot = [
     '    Mining, quarrying, and oil and gas extraction', '    Manufacturing', '    Arts, entertainment, recreation, accommodation, and food services', '    Retail trade',  '  Government and government enterprises',    '    Finance, insurance, real estate, rental, and leasing'
]

df_plot = df_long[df_long["Description"].isin(industries_to_plot)]

new_labels = {
    '    Arts, entertainment, recreation, accommodation, and food services': 'Arts, entertainment, recreation, accommodation, and food services (Tourism)',
    '    Mining, quarrying, and oil and gas extraction': 'Mining, quarrying, and oil and gas extraction (Energy)',
    '    Finance, insurance, real estate, rental, and leasing': 'Finance, insurance, real estate, rental, and leasing (Finance)',
    '  Government and government enterprises': 'Government and government enterprises (Government)',
    '    Manufacturing': 'Manufacturing (Industrial manufacturing)',
    '    Retail trade': 'Retail trade (Retail)'
    }

df_plot["Industry_Label"] = df_plot["Description"].replace(new_labels)
fig, ax = plt.subplots(figsize=(20,20))
labels = sorted(df_plot["Industry_Label"].unique())
palette = sns.color_palette("tab10", n_colors=len(labels))
#unique_labels = df_plot["Industry_Label"].unique()
color_map = dict(zip(labels, palette))
sns.scatterplot(
    data=df_plot,
    x="year",
    y="gdp",
    hue="Industry_Label",
    marker="o",
    palette=color_map,  
    s=60,
    ax=ax
)
for label, group in df_plot.groupby("Industry_Label"):
    sns.regplot(
        data=group,
        x="year",
        y="gdp",
        scatter=False,
        ci=None,
        color=color_map[label],
        ax=ax,                           
        line_kws={"linestyle": "--", "linewidth": 1.8},
    )
ax.set_title("Industry Metrics in West Virginia of Sectors of Interest From 2010 to 2022", fontsize=16, pad=20)
ax.set_xlabel("Year", fontsize=16)
ax.set_ylabel("GDP (in millions of current dollars)", fontsize=16)
ax.grid(True, linestyle="--", alpha=0.4)
leg = ax.legend(
    bbox_to_anchor=(1.05, 1),
    loc="upper left",
    title="Sector",
    frameon=True,
    borderpad=1.2
)

plt.setp(leg.get_title(), fontsize=16)
for text in leg.get_texts():
    text.set_fontsize(14)

# Make legend markers larger
for handle in leg.legend_handles:
    try:
        handle.set_sizes([120])
    except AttributeError:
        pass
plt.tight_layout(pad=2.0)
plt.savefig("gdp_color_matched.png", dpi=300, bbox_inches="tight")
plt.show()
