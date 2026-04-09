"""
Diagram 5: Deployment Pipeline & Phase Timeline
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

fig, ax = plt.subplots(figsize=(20, 11))
ax.set_xlim(0, 20)
ax.set_ylim(0, 11)
ax.axis('off')

C_BG     = "#0D1117"
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

fig.patch.set_facecolor(C_BG)
ax.set_facecolor(C_BG)

def rbox(x, y, w, h, fc, ec, lw=1.5, alpha=0.9, radius=0.22, zorder=2):
    p = FancyBboxPatch((x, y), w, h,
                       boxstyle=f"round,pad=0,rounding_size={radius}",
                       facecolor=fc, edgecolor=ec, linewidth=lw,
                       alpha=alpha, zorder=zorder)
    ax.add_patch(p)

def t(x, y, s, size=9, color=C_WHITE, weight='normal',
      ha='center', va='center', zorder=5):
    ax.text(x, y, s, fontsize=size, color=color, fontweight=weight,
            ha=ha, va=va, zorder=zorder, fontfamily='DejaVu Sans')

def arr(x1, y1, x2, y2, col=C_ORANGE, lw=2.2):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color=col, lw=lw,
                                connectionstyle='arc3,rad=0.0'), zorder=4)

# ── Title ─────────────────────────────────────────────────────────────────────
t(10, 10.55, 'GRC Platform — Deployment Pipeline', size=17,
  color=C_ORANGE, weight='bold')
t(10, 10.1, 'Five-phase CloudFormation deployment  |  Estimated time: 25–40 minutes',
  size=9.5, color=C_LIGHT)

# ── Phase definitions ─────────────────────────────────────────────────────────
phases = [
    {
        'num': '1', 'title': 'NETWORK\nINFRASTRUCTURE',
        'time': '5–10 min', 'col': C_TEAL,
        'bg': "#0F1E18",
        'items': ['Create VPC\n10.0.0.0/16', 'Public &\nPrivate Subnets',
                  'Internet &\nNAT Gateway', 'Route Tables\n& ACLs',
                  'Security\nGroups'],
    },
    {
        'num': '2', 'title': 'DATABASE\nINFRASTRUCTURE',
        'time': '10–15 min', 'col': C_BLUE,
        'bg': "#0F1828",
        'items': ['RDS MySQL\nMulti-AZ', 'S3 Buckets\nEvidence', 'DynamoDB\nTables',
                  'KMS Keys\nEncryption', 'IAM Roles\n& Policies'],
    },
    {
        'num': '3', 'title': 'LAMBDA\nFUNCTIONS',
        'time': '2–3 min', 'col': C_PURPLE,
        'bg': "#180F28",
        'items': ['Package\nLambda Code', 'Deploy\nFunction', 'Set Env\nVariables',
                  'EventBridge\nTrigger', 'Test\nInvocation'],
    },
    {
        'num': '4', 'title': 'MONITORING\n& COMPLIANCE',
        'time': '3–5 min', 'col': C_YELLOW,
        'bg': "#1E1A08",
        'items': ['Enable\nAWS Config', 'Create Config\nRules', 'Enable\nCloudTrail',
                  'CloudWatch\nAlarms', 'SNS\nTopics'],
    },
    {
        'num': '5', 'title': 'DATA &\nVERIFICATION',
        'time': '1–2 min', 'col': C_GREEN,
        'bg': "#0F1E10",
        'items': ['Load Sample\nSQL Data', 'Seed\nDynamoDB', 'Run Test\nSuite',
                  'Verify\nDashboard', 'Health\nChecks'],
    },
]

phase_w = 3.4
phase_gap = 0.35
total_w = len(phases) * phase_w + (len(phases)-1) * phase_gap
x_start = (20 - total_w) / 2

for i, ph in enumerate(phases):
    px = x_start + i * (phase_w + phase_gap)
    col = ph['col']
    bg  = ph['bg']

    # Phase header
    rbox(px, 7.2, phase_w, 2.3, bg, col, lw=2.5, alpha=0.95)
    # Number badge
    circle = plt.Circle((px+0.42, 8.95), 0.32, color=col, zorder=6)
    ax.add_patch(circle)
    t(px+0.42, 8.95, ph['num'], size=11, color="#0D1117", weight='bold', zorder=7)
    t(px+phase_w/2+0.1, 8.82, ph['title'], size=9, color=C_WHITE,
      weight='bold', va='top')
    # Time badge
    rbox(px+0.2, 7.28, phase_w-0.4, 0.42, col, col, lw=0, alpha=0.2, radius=0.1)
    t(px+phase_w/2, 7.49, ph['time'], size=7.5, color=col, weight='bold')

    # Items column
    rbox(px, 0.6, phase_w, 6.4, bg, col, lw=1.5, alpha=0.6)
    for j, item in enumerate(ph['items']):
        iy = 6.3 - j * 1.12
        rbox(px+0.15, iy-0.38, phase_w-0.3, 0.82, "#161B22", col,
             lw=1, alpha=0.85, radius=0.15)
        t(px+phase_w/2, iy+0.03, item, size=7.5, color=C_WHITE)

    # Arrow to next phase
    if i < len(phases)-1:
        ax_end = px + phase_w
        ax_start2 = ax_end + phase_gap
        arr(ax_end+0.02, 8.35, ax_start2-0.02, 8.35, col=C_ORANGE, lw=2.5)

# ── Timeline bar at bottom ────────────────────────────────────────────────────
rbox(x_start-0.2, 0.25, total_w+0.4, 0.28, "#161B22", C_BORDER, lw=1, alpha=1)
total_mins = [7.5, 12.5, 2.5, 4.0, 1.5]
total_time = sum(total_mins)
x_cursor = x_start - 0.2
for i, (ph, mins) in enumerate(zip(phases, total_mins)):
    seg_w = (mins / total_time) * (total_w + 0.4)
    rbox(x_cursor, 0.25, seg_w, 0.28, ph['col'], ph['col'],
         lw=0, alpha=0.7, radius=0.05)
    x_cursor += seg_w

t(10, 0.12,
  'GRC208 Governance, Risk, and Compliance Capstone Project  |  March 2026',
  size=7.5, color="#6E7681")

# Total time label
rbox(x_start + total_w - 3.5, 7.22, 3.3, 0.4, "#1C2128", C_ORANGE, lw=1.5, alpha=0.9)
t(x_start + total_w - 1.85, 7.42, 'Total: 25–40 minutes', size=8,
  color=C_ORANGE, weight='bold')

plt.tight_layout(pad=0.2)
plt.savefig('/home/ubuntu/grc-capstone-project/diagrams/05_deployment_pipeline.png',
            dpi=180, bbox_inches='tight', facecolor=C_BG)
plt.close()
print("Diagram 5 saved.")
