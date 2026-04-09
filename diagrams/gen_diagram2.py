"""
Diagram 2: Compliance Monitoring Data Flow
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import numpy as np

fig, ax = plt.subplots(figsize=(20, 10))
ax.set_xlim(0, 20)
ax.set_ylim(0, 10)
ax.axis('off')

C_BG     = "#0D1117"
C_BORDER = "#30363D"
C_WHITE  = "#FFFFFF"
C_LIGHT  = "#C9D1D9"
C_ORANGE = "#FF9900"
C_GREEN  = "#3FB950"
C_BLUE   = "#58A6FF"
C_PURPLE = "#BC8CFF"
C_YELLOW = "#E3B341"
C_RED    = "#F85149"
C_TEAL   = "#39D353"

fig.patch.set_facecolor(C_BG)
ax.set_facecolor(C_BG)

def rbox(ax, x, y, w, h, fc, ec, lw=1.5, alpha=0.92, radius=0.3, zorder=2):
    p = FancyBboxPatch((x, y), w, h,
                       boxstyle=f"round,pad=0,rounding_size={radius}",
                       facecolor=fc, edgecolor=ec, linewidth=lw,
                       alpha=alpha, zorder=zorder)
    ax.add_patch(p)

def txt(ax, x, y, s, size=9, color=C_WHITE, weight='normal',
        ha='center', va='center', zorder=5):
    ax.text(x, y, s, fontsize=size, color=color, fontweight=weight,
            ha=ha, va=va, zorder=zorder, fontfamily='DejaVu Sans')

def arr(ax, x1, y1, x2, y2, col=C_ORANGE, lw=2.0, label=''):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color=col, lw=lw,
                                connectionstyle='arc3,rad=0.0'), zorder=4)
    if label:
        mx, my = (x1+x2)/2, (y1+y2)/2
        txt(ax, mx, my+0.22, label, size=6.5, color=col)

# ── Title ─────────────────────────────────────────────────────────────────────
txt(ax, 10, 9.55, 'GRC Platform — Compliance Monitoring Data Flow',
    size=16, color=C_ORANGE, weight='bold')
txt(ax, 10, 9.1, 'End-to-end flow from AWS resource detection to alerting and reporting',
    size=9, color=C_LIGHT)

# ── Stage definitions (x_center, y_center, width, height, title, subtitle, fc, ec) ──
stages = [
    (1.5,  6.5, 2.6, 1.5, 'AWS\nResources',    'EC2 · RDS · S3\nLambda · IAM',   "#1A2332", C_TEAL),
    (4.5,  6.5, 2.6, 1.5, 'AWS Config',         'Compliance Rules\nEvaluation',    "#1A2820", C_ORANGE),
    (7.5,  6.5, 2.6, 1.5, 'EventBridge',        'Event Routing\nTrigger',          "#1E2030", C_PURPLE),
    (10.5, 6.5, 2.6, 1.5, 'Lambda\nFunction',   'Compliance Analysis\nRisk Calc',  "#1A2030", C_BLUE),
    (13.5, 6.5, 2.6, 1.5, 'DynamoDB',           'Real-time Status\nStorage',       "#1A2840", C_BLUE),
    (16.5, 6.5, 2.6, 1.5, 'SNS Alert',          'Notification\nEscalation',        "#2A1820", C_RED),
]

for (cx, cy, w, h, title, sub, fc, ec) in stages:
    rbox(ax, cx-w/2, cy-h/2, w, h, fc, ec, lw=2)
    txt(ax, cx, cy+0.22, title, size=9.5, color=C_WHITE, weight='bold')
    txt(ax, cx, cy-0.28, sub, size=7, color=C_LIGHT)

# Arrows between stages
for i in range(len(stages)-1):
    x1 = stages[i][0]  + stages[i][2]/2
    x2 = stages[i+1][0]- stages[i+1][2]/2
    y  = stages[i][1]
    arr(ax, x1, y, x2, y, col=C_ORANGE, lw=2.2)

# ── Second row: Storage & Reporting ──────────────────────────────────────────
stores = [
    (4.5,  3.5, 2.6, 1.5, 'RDS MySQL',       'GRC Platform\nDatabase',      "#1A2840", C_BLUE),
    (7.5,  3.5, 2.6, 1.5, 'S3 Bucket',       'Evidence &\nAudit Logs',      "#1A2820", C_GREEN),
    (10.5, 3.5, 2.6, 1.5, 'Dashboard',       'React Frontend\nVisualization',"#1E2830", C_TEAL),
    (13.5, 3.5, 2.6, 1.5, 'Reports',         'PDF / CSV\nExports',           "#1E2030", C_YELLOW),
    (16.5, 3.5, 2.6, 1.5, 'Email / SMS',     'Team\nNotifications',          "#2A1820", C_RED),
]

for (cx, cy, w, h, title, sub, fc, ec) in stores:
    rbox(ax, cx-w/2, cy-h/2, w, h, fc, ec, lw=2)
    txt(ax, cx, cy+0.22, title, size=9.5, color=C_WHITE, weight='bold')
    txt(ax, cx, cy-0.28, sub, size=7, color=C_LIGHT)

# Lambda → RDS
arr(ax, 10.5, 5.75, 10.5-3.0+0.1, 4.25, col=C_BLUE, lw=1.8, label='Store GRC Data')
# Lambda → S3
arr(ax, 10.5, 5.75, 10.5-3.0+3.0+0.1, 4.25, col=C_GREEN, lw=1.8)
# DynamoDB → Dashboard
arr(ax, 13.5, 5.75, 10.5, 4.25, col=C_TEAL, lw=1.8, label='Real-time Feed')
# RDS → Reports
arr(ax, 5.8, 3.5, 12.2, 3.5, col=C_YELLOW, lw=1.5, label='Generate Reports')
# SNS → Email
arr(ax, 16.5, 5.75, 16.5, 4.25, col=C_RED, lw=1.8, label='Send Alert')

# CloudTrail side note
rbox(ax, 0.3, 2.8, 2.8, 1.4, "#1A2030", C_YELLOW, lw=1.5)
txt(ax, 1.7, 3.7, 'CloudTrail', size=9, color=C_YELLOW, weight='bold')
txt(ax, 1.7, 3.3, 'All API Calls\nAudit Logging', size=7, color=C_LIGHT)
arr(ax, 3.1, 3.5, 4.5-1.3, 3.5, col=C_YELLOW, lw=1.5, label='Logs to S3')

# ── Step numbers ──────────────────────────────────────────────────────────────
step_labels = ['1', '2', '3', '4', '5', '6']
for i, (cx, cy, w, h, *_) in enumerate(stages):
    circle = plt.Circle((cx-w/2+0.22, cy+h/2-0.22), 0.18,
                         color=C_ORANGE, zorder=6)
    ax.add_patch(circle)
    txt(ax, cx-w/2+0.22, cy+h/2-0.22, step_labels[i],
        size=7.5, color="#0D1117", weight='bold', zorder=7)

# ── Legend ────────────────────────────────────────────────────────────────────
legend = [
    (C_TEAL,   'AWS Resources'),
    (C_ORANGE, 'Config & Events'),
    (C_BLUE,   'Compute & Storage'),
    (C_GREEN,  'Evidence Store'),
    (C_YELLOW, 'Audit & Reports'),
    (C_RED,    'Alerting'),
]
rbox(ax, 0.2, 5.0, 2.6, 4.2, "#161B22", C_BORDER, lw=1, alpha=0.95)
txt(ax, 1.5, 8.95, 'Legend', size=8, color=C_WHITE, weight='bold')
for i, (col, lbl) in enumerate(legend):
    yp = 8.45 - i * 0.6
    rect = FancyBboxPatch((0.35, yp-0.15), 0.3, 0.3,
                          boxstyle="round,pad=0,rounding_size=0.04",
                          facecolor=col, edgecolor=col, zorder=6)
    ax.add_patch(rect)
    txt(ax, 1.55, yp, lbl, size=7, color=C_LIGHT, ha='left', va='center')

# ── Footer ────────────────────────────────────────────────────────────────────
txt(ax, 10, 0.3,
    'GRC208 Governance, Risk, and Compliance Capstone Project  |  March 2026',
    size=7.5, color="#6E7681")

plt.tight_layout(pad=0.2)
plt.savefig('/home/ubuntu/grc-capstone-project/diagrams/02_data_flow.png',
            dpi=180, bbox_inches='tight', facecolor=C_BG)
plt.close()
print("Diagram 2 saved.")
