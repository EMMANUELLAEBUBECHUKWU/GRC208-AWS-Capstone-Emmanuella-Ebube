"""
Diagram 6: Compliance Frameworks Dashboard & Control Status
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Wedge
import numpy as np

fig = plt.figure(figsize=(20, 12))
C_BG = "#0D1117"
fig.patch.set_facecolor(C_BG)

C_WHITE  = "#FFFFFF"
C_LIGHT  = "#C9D1D9"
C_ORANGE = "#FF9900"
C_GREEN  = "#3FB950"
C_BLUE   = "#58A6FF"
C_PURPLE = "#BC8CFF"
C_YELLOW = "#E3B341"
C_RED    = "#F85149"
C_TEAL   = "#39D353"
C_BORDER = "#30363D"

def rbox(ax, x, y, w, h, fc, ec, lw=1.5, alpha=0.9, radius=0.22, zorder=2):
    p = FancyBboxPatch((x, y), w, h,
                       boxstyle=f"round,pad=0,rounding_size={radius}",
                       facecolor=fc, edgecolor=ec, linewidth=lw,
                       alpha=alpha, zorder=zorder)
    ax.add_patch(p)

def t(ax, x, y, s, size=9, color=C_WHITE, weight='normal',
      ha='center', va='center', zorder=5):
    ax.text(x, y, s, fontsize=size, color=color, fontweight=weight,
            ha=ha, va=va, zorder=zorder, fontfamily='DejaVu Sans')

# ── Title ─────────────────────────────────────────────────────────────────────
fig.text(0.5, 0.97, 'GRC Platform — Compliance Dashboard Overview',
         ha='center', fontsize=17, color=C_ORANGE, fontweight='bold',
         fontfamily='DejaVu Sans')
fig.text(0.5, 0.935, 'Real-time compliance scores across six frameworks with control implementation status',
         ha='center', fontsize=9.5, color=C_LIGHT, fontfamily='DejaVu Sans')

# ── Top row: KPI cards ────────────────────────────────────────────────────────
ax_kpi = fig.add_axes([0.02, 0.76, 0.96, 0.14])
ax_kpi.set_xlim(0, 20)
ax_kpi.set_ylim(0, 3)
ax_kpi.axis('off')
ax_kpi.set_facecolor(C_BG)

kpis = [
    ('Average\nCompliance', '85%',   C_GREEN,  "#0F1E10"),
    ('Critical\nRisks',     '1',     C_RED,    "#1E0F10"),
    ('Controls\nImplemented','38/45',C_BLUE,   "#0F1020"),
    ('Frameworks\nMonitored','6',    C_ORANGE, "#1E1208"),
    ('Alerts\nThis Week',   '3',     C_YELLOW, "#1E1A08"),
    ('Assets\nProtected',   '12',    C_PURPLE, "#180F28"),
]
kpi_w = 3.0
for i, (label, val, col, bg) in enumerate(kpis):
    kx = 0.3 + i * (kpi_w + 0.22)
    rbox(ax_kpi, kx, 0.15, kpi_w, 2.7, bg, col, lw=2, alpha=0.95)
    t(ax_kpi, kx+kpi_w/2, 2.1, label, size=8, color=C_LIGHT)
    t(ax_kpi, kx+kpi_w/2, 1.2, val, size=22, color=col, weight='bold')

# ── Middle-left: Compliance bar chart ────────────────────────────────────────
ax_bar = fig.add_axes([0.02, 0.30, 0.44, 0.42])
ax_bar.set_facecolor(C_BG)

frameworks = ['ISO 27001:2022', 'NIST CSF', 'PCI DSS 3.2', 'HIPAA', 'GDPR', 'SOC 2']
scores     = [85, 78, 92, 88, 81, 90]
colors_bar = [C_GREEN, C_YELLOW, C_GREEN, C_GREEN, C_YELLOW, C_GREEN]

y_pos = np.arange(len(frameworks))
bars = ax_bar.barh(y_pos, scores, color=colors_bar, alpha=0.8,
                   height=0.65, edgecolor='none')

# Background bars
ax_bar.barh(y_pos, [100]*6, color='#1C2128', alpha=0.5,
            height=0.65, edgecolor='none', zorder=1)
ax_bar.barh(y_pos, scores, color=colors_bar, alpha=0.85,
            height=0.65, edgecolor='none', zorder=2)

for i, (score, col) in enumerate(zip(scores, colors_bar)):
    ax_bar.text(score+1, i, f'{score}%', va='center', ha='left',
                fontsize=10, color=col, fontweight='bold',
                fontfamily='DejaVu Sans')
    # Threshold line at 80%
    ax_bar.axvline(x=80, color='#F85149', linestyle='--', linewidth=1.2,
                   alpha=0.6, zorder=3)

ax_bar.set_yticks(y_pos)
ax_bar.set_yticklabels(frameworks, fontsize=9, color=C_LIGHT,
                        fontfamily='DejaVu Sans')
ax_bar.set_xlim(0, 108)
ax_bar.set_xlabel('Compliance Score (%)', fontsize=9, color=C_LIGHT,
                  fontfamily='DejaVu Sans')
ax_bar.set_title('Compliance Scores by Framework', fontsize=12,
                 color=C_WHITE, fontweight='bold', pad=10,
                 fontfamily='DejaVu Sans')
ax_bar.tick_params(colors=C_LIGHT, labelsize=9)
ax_bar.set_facecolor(C_BG)
for spine in ax_bar.spines.values():
    spine.set_edgecolor(C_BORDER)
ax_bar.text(80.5, -0.7, 'Min. Threshold\n80%', fontsize=7,
            color=C_RED, fontfamily='DejaVu Sans')

# ── Middle-right: Donut chart - Control Status ────────────────────────────────
ax_donut = fig.add_axes([0.50, 0.30, 0.24, 0.42])
ax_donut.set_facecolor(C_BG)

ctrl_vals   = [38, 5, 2]
ctrl_labels = ['Implemented\n(38)', 'In Progress\n(5)', 'Not Started\n(2)']
ctrl_colors = [C_GREEN, C_YELLOW, C_RED]

wedges, _ = ax_donut.pie(ctrl_vals, colors=ctrl_colors,
                          startangle=90, counterclock=False,
                          wedgeprops=dict(width=0.55, edgecolor=C_BG, linewidth=2))
ax_donut.text(0, 0, '45\nControls', ha='center', va='center',
              fontsize=12, color=C_WHITE, fontweight='bold',
              fontfamily='DejaVu Sans')
ax_donut.set_title('Control Implementation\nStatus', fontsize=11,
                   color=C_WHITE, fontweight='bold', pad=8,
                   fontfamily='DejaVu Sans')
legend_patches = [mpatches.Patch(color=c, label=l)
                  for c, l in zip(ctrl_colors, ctrl_labels)]
ax_donut.legend(handles=legend_patches, loc='lower center',
                bbox_to_anchor=(0.5, -0.22), ncol=1,
                framealpha=0.2, facecolor='#161B22',
                edgecolor=C_BORDER, labelcolor=C_LIGHT, fontsize=8)

# ── Middle-far-right: Asset criticality ──────────────────────────────────────
ax_asset = fig.add_axes([0.76, 0.30, 0.22, 0.42])
ax_asset.set_facecolor(C_BG)

asset_cats   = ['Critical', 'High', 'Medium', 'Low']
asset_counts = [4, 5, 3, 0]
asset_colors = [C_RED, C_ORANGE, C_YELLOW, C_GREEN]

bars2 = ax_asset.bar(asset_cats, asset_counts, color=asset_colors,
                     alpha=0.85, edgecolor='none', width=0.6)
for bar, val in zip(bars2, asset_counts):
    if val > 0:
        ax_asset.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.1,
                      str(val), ha='center', va='bottom', fontsize=12,
                      color=C_WHITE, fontweight='bold',
                      fontfamily='DejaVu Sans')
ax_asset.set_title('Asset Criticality\nDistribution', fontsize=11,
                   color=C_WHITE, fontweight='bold', pad=8,
                   fontfamily='DejaVu Sans')
ax_asset.set_ylabel('Count', fontsize=9, color=C_LIGHT,
                    fontfamily='DejaVu Sans')
ax_asset.set_ylim(0, 7)
ax_asset.tick_params(colors=C_LIGHT, labelsize=8)
ax_asset.set_facecolor(C_BG)
for spine in ax_asset.spines.values():
    spine.set_edgecolor(C_BORDER)

# ── Bottom: Compliance trend line ────────────────────────────────────────────
ax_trend = fig.add_axes([0.02, 0.07, 0.96, 0.20])
ax_trend.set_facecolor(C_BG)

months = ['Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar']
fw_trends = {
    'ISO 27001': ([72, 75, 78, 80, 83, 85], C_BLUE),
    'NIST CSF':  ([68, 70, 72, 74, 76, 78], C_GREEN),
    'PCI DSS':   ([85, 87, 88, 89, 91, 92], C_YELLOW),
    'HIPAA':     ([80, 82, 84, 85, 87, 88], C_RED),
    'GDPR':      ([74, 76, 77, 78, 80, 81], C_PURPLE),
    'SOC 2':     ([83, 85, 86, 87, 89, 90], C_TEAL),
}
x = np.arange(len(months))
for fw, (vals, col) in fw_trends.items():
    ax_trend.plot(x, vals, color=col, linewidth=2.2, marker='o',
                  markersize=5, label=fw, alpha=0.9)
    ax_trend.text(x[-1]+0.08, vals[-1], fw, fontsize=7.5, color=col,
                  va='center', fontfamily='DejaVu Sans')

ax_trend.axhline(y=80, color=C_RED, linestyle='--', linewidth=1.2,
                 alpha=0.5, label='Min. Threshold (80%)')
ax_trend.fill_between(x, 80, 100, alpha=0.04, color=C_GREEN)
ax_trend.fill_between(x, 0, 80, alpha=0.04, color=C_RED)
ax_trend.set_xticks(x)
ax_trend.set_xticklabels(months, fontsize=9, color=C_LIGHT,
                          fontfamily='DejaVu Sans')
ax_trend.set_ylim(60, 100)
ax_trend.set_ylabel('Compliance %', fontsize=9, color=C_LIGHT,
                    fontfamily='DejaVu Sans')
ax_trend.set_title('6-Month Compliance Trend (Oct 2025 – Mar 2026)',
                   fontsize=11, color=C_WHITE, fontweight='bold', pad=8,
                   fontfamily='DejaVu Sans')
ax_trend.tick_params(colors=C_LIGHT, labelsize=9)
ax_trend.set_facecolor(C_BG)
for spine in ax_trend.spines.values():
    spine.set_edgecolor(C_BORDER)
ax_trend.grid(axis='y', color=C_BORDER, alpha=0.4, linewidth=0.8)

# ── Footer ────────────────────────────────────────────────────────────────────
fig.text(0.5, 0.01,
         'GRC208 Governance, Risk, and Compliance Capstone Project  |  March 2026',
         ha='center', fontsize=7.5, color="#6E7681",
         fontfamily='DejaVu Sans')

plt.savefig('/home/ubuntu/grc-capstone-project/diagrams/06_compliance_dashboard.png',
            dpi=180, bbox_inches='tight', facecolor=C_BG)
plt.close()
print("Diagram 6 saved.")
