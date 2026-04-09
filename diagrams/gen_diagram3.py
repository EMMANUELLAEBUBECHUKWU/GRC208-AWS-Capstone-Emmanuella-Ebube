"""
Diagram 3: Risk Assessment Matrix & Scoring Engine
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import numpy as np

fig = plt.figure(figsize=(20, 12))
C_BG = "#0D1117"
fig.patch.set_facecolor(C_BG)

# ── Left: Risk Matrix heatmap ─────────────────────────────────────────────────
ax1 = fig.add_axes([0.03, 0.12, 0.42, 0.78])
ax1.set_facecolor(C_BG)

C_WHITE  = "#FFFFFF"
C_LIGHT  = "#C9D1D9"
C_ORANGE = "#FF9900"
C_GREEN  = "#3FB950"
C_BLUE   = "#58A6FF"
C_PURPLE = "#BC8CFF"
C_YELLOW = "#E3B341"
C_RED    = "#F85149"
C_DARK_RED = "#8B0000"

# Matrix colours
matrix_colors = [
    ["#1a3a1a", "#2d5a1a", "#4a7a1a", "#6a9a1a", "#8aba2a"],  # Very Low prob
    ["#2d5a1a", "#4a7a1a", "#8aba2a", "#c8a000", "#e07000"],  # Low
    ["#4a7a1a", "#8aba2a", "#c8a000", "#e07000", "#c83000"],  # Medium
    ["#8aba2a", "#c8a000", "#e07000", "#c83000", "#8b0000"],  # High
    ["#c8a000", "#e07000", "#c83000", "#8b0000", "#5a0000"],  # Very High
]

prob_labels = ['Very Low\n(1)', 'Low\n(2)', 'Medium\n(3)', 'High\n(4)', 'Very High\n(5)']
impact_labels = ['Very Low\n(1)', 'Low\n(2)', 'Medium\n(3)', 'High\n(4)', 'Very High\n(5)']
risk_scores = [[1,2,3,4,5],[2,4,6,8,10],[3,6,9,12,15],[4,8,12,16,20],[5,10,15,20,25]]

for i in range(5):
    for j in range(5):
        rect = FancyBboxPatch((j+0.05, i+0.05), 0.9, 0.9,
                              boxstyle="round,pad=0,rounding_size=0.08",
                              facecolor=matrix_colors[i][j],
                              edgecolor="#0D1117", linewidth=1.5, zorder=2)
        ax1.add_patch(rect)
        score = risk_scores[i][j]
        ax1.text(j+0.5, i+0.5, str(score),
                 ha='center', va='center', fontsize=13,
                 color=C_WHITE, fontweight='bold', zorder=3)

# Sample risks plotted on matrix
sample_risks = [
    (4.5, 4.5, 'RISK-001\nUnauth Access', C_RED),
    (3.5, 3.5, 'RISK-002\nData Breach', "#FF6B35"),
    (2.5, 3.5, 'RISK-003\nCompliance', "#FF6B35"),
    (1.5, 2.5, 'RISK-004\nDowntime', C_YELLOW),
    (0.5, 1.5, 'RISK-005\nPhishing', C_GREEN),
    (2.5, 1.5, 'RISK-006\nInsider Threat', C_YELLOW),
]
for (x, y, lbl, col) in sample_risks:
    ax1.plot(x, y, 'o', markersize=14, color=col,
             markeredgecolor=C_WHITE, markeredgewidth=1.5, zorder=5)
    ax1.text(x, y, '●', ha='center', va='center',
             fontsize=6, color="#0D1117", zorder=6)

ax1.set_xlim(0, 5)
ax1.set_ylim(0, 5)
ax1.set_xticks([0.5,1.5,2.5,3.5,4.5])
ax1.set_yticks([0.5,1.5,2.5,3.5,4.5])
ax1.set_xticklabels(impact_labels, fontsize=8, color=C_LIGHT)
ax1.set_yticklabels(prob_labels, fontsize=8, color=C_LIGHT)
ax1.set_xlabel('IMPACT', fontsize=11, color=C_ORANGE, fontweight='bold', labelpad=10)
ax1.set_ylabel('PROBABILITY', fontsize=11, color=C_ORANGE, fontweight='bold', labelpad=10)
ax1.set_title('Risk Assessment Matrix', fontsize=14, color=C_WHITE,
              fontweight='bold', pad=15)
ax1.tick_params(colors=C_LIGHT, length=0)
for spine in ax1.spines.values():
    spine.set_edgecolor("#30363D")

# Legend for matrix
legend_patches = [
    mpatches.Patch(color='#1a3a1a', label='Low Risk (1-4)'),
    mpatches.Patch(color='#c8a000', label='Medium Risk (5-9)'),
    mpatches.Patch(color='#e07000', label='High Risk (10-15)'),
    mpatches.Patch(color='#8b0000', label='Critical Risk (16-25)'),
]
ax1.legend(handles=legend_patches, loc='upper left',
           framealpha=0.3, facecolor='#161B22',
           edgecolor='#30363D', labelcolor=C_LIGHT, fontsize=7.5)

# ── Right: Risk Register & Scoring ───────────────────────────────────────────
ax2 = fig.add_axes([0.50, 0.12, 0.47, 0.78])
ax2.set_xlim(0, 10)
ax2.set_ylim(0, 10)
ax2.axis('off')
ax2.set_facecolor(C_BG)

def rbox2(x, y, w, h, fc, ec, lw=1.5, alpha=0.9, radius=0.2):
    p = FancyBboxPatch((x, y), w, h,
                       boxstyle=f"round,pad=0,rounding_size={radius}",
                       facecolor=fc, edgecolor=ec, linewidth=lw,
                       alpha=alpha, zorder=2)
    ax2.add_patch(p)

def t2(x, y, s, size=9, color=C_WHITE, weight='normal',
       ha='center', va='center'):
    ax2.text(x, y, s, fontsize=size, color=color, fontweight=weight,
             ha=ha, va=va, zorder=5, fontfamily='DejaVu Sans')

ax2.set_title('Risk Register & Scoring Engine', fontsize=14,
              color=C_WHITE, fontweight='bold', pad=15)

# Header
rbox2(0, 8.8, 10, 0.85, "#1C2128", C_ORANGE, lw=2)
t2(1.0, 9.22, 'Risk ID', size=8, color=C_ORANGE, weight='bold', ha='left')
t2(3.0, 9.22, 'Risk Title', size=8, color=C_ORANGE, weight='bold', ha='left')
t2(5.8, 9.22, 'Level', size=8, color=C_ORANGE, weight='bold', ha='left')
t2(7.2, 9.22, 'Score', size=8, color=C_ORANGE, weight='bold', ha='left')
t2(8.5, 9.22, 'Status', size=8, color=C_ORANGE, weight='bold', ha='left')

risks = [
    ('RISK-001', 'Unauthorized Access',   'CRITICAL', 9.0, 'Open',       C_RED,    "#2A1820"),
    ('RISK-002', 'Data Breach',           'HIGH',     7.5, 'Mitigating', "#FF6B35","#2A1E18"),
    ('RISK-003', 'Compliance Violation',  'HIGH',     7.0, 'Mitigating', "#FF6B35","#2A1E18"),
    ('RISK-004', 'System Downtime',       'MEDIUM',   5.0, 'Accepted',   C_YELLOW, "#2A2218"),
    ('RISK-005', 'Phishing Attack',       'MEDIUM',   4.5, 'Mitigating', C_YELLOW, "#2A2218"),
    ('RISK-006', 'Insider Threat',        'LOW',      2.5, 'Monitored',  C_GREEN,  "#1A2820"),
]

for i, (rid, title, level, score, status, col, bg) in enumerate(risks):
    y = 7.8 - i * 1.2
    rbox2(0, y, 10, 1.0, bg, col, lw=1.2, alpha=0.85)
    t2(1.0, y+0.5, rid, size=8, color=C_LIGHT, ha='left')
    t2(3.0, y+0.5, title, size=8, color=C_WHITE, ha='left')
    # Level badge
    rbox2(5.7, y+0.18, 1.3, 0.64, col, col, lw=0, alpha=0.3, radius=0.15)
    t2(6.35, y+0.5, level, size=7, color=col, weight='bold')
    # Score bar
    bar_w = score / 10 * 1.5
    rbox2(7.0, y+0.3, 1.5, 0.4, "#1C2128", "#30363D", lw=1, alpha=1, radius=0.1)
    rbox2(7.0, y+0.3, bar_w, 0.4, col, col, lw=0, alpha=0.8, radius=0.1)
    t2(8.0, y+0.5, f'{score}', size=8, color=col, weight='bold')
    t2(9.0, y+0.5, status, size=7.5, color=C_LIGHT)

# Formula box
rbox2(0, 0.2, 10, 1.4, "#161B22", C_PURPLE, lw=1.5)
t2(5, 1.25, 'Risk Score Formula', size=9, color=C_PURPLE, weight='bold')
t2(5, 0.82, 'Risk Score  =  Probability  ×  Impact', size=10,
   color=C_WHITE, weight='bold')
t2(5, 0.45, 'Critical: ≥8.0   |   High: 6.0–7.9   |   Medium: 4.0–5.9   |   Low: <4.0',
   size=8, color=C_LIGHT)

# ── Main title ────────────────────────────────────────────────────────────────
fig.text(0.5, 0.97, 'GRC Platform — Risk Assessment Engine',
         ha='center', va='top', fontsize=17, color=C_ORANGE,
         fontweight='bold', fontfamily='DejaVu Sans')
fig.text(0.5, 0.93, 'Automated risk scoring using Probability × Impact matrix with real-time register',
         ha='center', va='top', fontsize=9.5, color=C_LIGHT,
         fontfamily='DejaVu Sans')
fig.text(0.5, 0.02,
         'GRC208 Governance, Risk, and Compliance Capstone Project  |  March 2026',
         ha='center', fontsize=7.5, color="#6E7681",
         fontfamily='DejaVu Sans')

plt.savefig('/home/ubuntu/grc-capstone-project/diagrams/03_risk_assessment.png',
            dpi=180, bbox_inches='tight', facecolor=C_BG)
plt.close()
print("Diagram 3 saved.")
