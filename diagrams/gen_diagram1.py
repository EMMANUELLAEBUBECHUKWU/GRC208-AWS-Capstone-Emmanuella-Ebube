"""
Diagram 1: AWS Integrated GRC Platform - System Architecture Overview
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import matplotlib.patheffects as pe

fig, ax = plt.subplots(1, 1, figsize=(20, 14))
ax.set_xlim(0, 20)
ax.set_ylim(0, 14)
ax.axis('off')

# ── Colour palette ──────────────────────────────────────────────────────────
C_BG        = "#0D1117"
C_AWS_ORANGE= "#FF9900"
C_AWS_DARK  = "#232F3E"
C_VPC_BG    = "#1A2332"
C_PUB_BG    = "#1E3A2F"
C_PRIV_BG   = "#1A2840"
C_SVC_BG    = "#1E2A3A"
C_MON_BG    = "#2A1E3A"
C_WHITE     = "#FFFFFF"
C_LIGHT     = "#C9D1D9"
C_ORANGE    = "#FF9900"
C_GREEN     = "#3FB950"
C_BLUE      = "#58A6FF"
C_PURPLE    = "#BC8CFF"
C_YELLOW    = "#E3B341"
C_RED       = "#F85149"
C_TEAL      = "#39D353"
C_BORDER    = "#30363D"

fig.patch.set_facecolor(C_BG)
ax.set_facecolor(C_BG)

def box(ax, x, y, w, h, color, alpha=0.85, radius=0.25, lw=1.5, ec=None):
    ec = ec or color
    p = FancyBboxPatch((x, y), w, h,
                       boxstyle=f"round,pad=0,rounding_size={radius}",
                       facecolor=color, edgecolor=ec,
                       linewidth=lw, alpha=alpha, zorder=2)
    ax.add_patch(p)
    return p

def label(ax, x, y, text, size=9, color=C_WHITE, weight='normal',
          ha='center', va='center', zorder=5):
    ax.text(x, y, text, fontsize=size, color=color, fontweight=weight,
            ha=ha, va=va, zorder=zorder,
            fontfamily='DejaVu Sans')

def arrow(ax, x1, y1, x2, y2, color=C_ORANGE, lw=1.5, style='->', zorder=3):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle=style, color=color,
                                lw=lw, connectionstyle='arc3,rad=0.0'),
                zorder=zorder)

def service_box(ax, x, y, w, h, title, subtitle='', bg=C_SVC_BG,
                icon_color=C_ORANGE, title_size=8):
    box(ax, x, y, w, h, bg, alpha=0.9, radius=0.2, ec=icon_color, lw=1.2)
    label(ax, x+w/2, y+h*0.65, title, size=title_size,
          color=C_WHITE, weight='bold')
    if subtitle:
        label(ax, x+w/2, y+h*0.28, subtitle, size=6.5, color=C_LIGHT)

# ── Title ────────────────────────────────────────────────────────────────────
label(ax, 10, 13.4, 'AWS Integrated GRC Platform', size=18,
      color=C_ORANGE, weight='bold')
label(ax, 10, 12.95, 'GRC208 Capstone Project  |  System Architecture Overview',
      size=10, color=C_LIGHT)

# ── Internet user ────────────────────────────────────────────────────────────
box(ax, 0.3, 10.5, 2.2, 1.6, "#1C2128", alpha=1, ec=C_BLUE, lw=1.5)
label(ax, 1.4, 11.65, 'Internet', size=9, color=C_BLUE, weight='bold')
label(ax, 1.4, 11.25, 'Users /\nAdministrators', size=7.5, color=C_LIGHT)

# ── AWS Account outer border ──────────────────────────────────────────────────
box(ax, 2.8, 0.4, 16.8, 12.2, C_AWS_DARK, alpha=0.4, radius=0.4,
    ec=C_ORANGE, lw=2)
label(ax, 4.0, 12.35, 'AWS Account', size=9, color=C_ORANGE,
      weight='bold', ha='left')

# ── VPC ───────────────────────────────────────────────────────────────────────
box(ax, 3.1, 0.7, 10.0, 11.4, C_VPC_BG, alpha=0.6, radius=0.3,
    ec=C_GREEN, lw=1.8)
label(ax, 4.3, 11.8, 'VPC  10.0.0.0/16', size=8.5, color=C_GREEN,
      weight='bold', ha='left')

# Public subnet
box(ax, 3.4, 9.0, 9.4, 2.6, C_PUB_BG, alpha=0.7, radius=0.2,
    ec=C_TEAL, lw=1.2)
label(ax, 4.6, 11.3, 'Public Subnets', size=7.5, color=C_TEAL,
      weight='bold', ha='left')

service_box(ax, 3.6, 9.2, 2.4, 1.9, 'Internet', 'Gateway',
            bg="#1A3028", icon_color=C_TEAL)
service_box(ax, 6.3, 9.2, 2.4, 1.9, 'Application', 'Load Balancer',
            bg="#1A3028", icon_color=C_TEAL)
service_box(ax, 9.1, 9.2, 3.4, 1.9, 'NAT Gateway', 'Outbound Traffic',
            bg="#1A3028", icon_color=C_TEAL)

# Private subnet
box(ax, 3.4, 1.0, 9.4, 7.7, C_PRIV_BG, alpha=0.7, radius=0.2,
    ec=C_BLUE, lw=1.2)
label(ax, 4.6, 8.45, 'Private Subnets', size=7.5, color=C_BLUE,
      weight='bold', ha='left')

service_box(ax, 3.6, 5.8, 2.8, 2.2, 'ECS Fargate', 'GRC Application',
            bg="#1A2840", icon_color=C_BLUE)
service_box(ax, 6.7, 5.8, 2.8, 2.2, 'RDS MySQL', 'Multi-AZ Database',
            bg="#1A2840", icon_color=C_BLUE)
service_box(ax, 9.8, 5.8, 2.6, 2.2, 'Lambda', 'Compliance Monitor',
            bg="#1A2840", icon_color=C_PURPLE)

service_box(ax, 3.6, 1.3, 2.8, 4.0, 'Security\nGroups', 'Least Privilege',
            bg="#1E2030", icon_color="#F85149", title_size=7.5)
service_box(ax, 6.7, 1.3, 2.8, 4.0, 'KMS', 'Encryption Keys',
            bg="#1E2030", icon_color=C_YELLOW)
service_box(ax, 9.8, 1.3, 2.6, 4.0, 'IAM Roles\n& Policies', 'Access Control',
            bg="#1E2030", icon_color=C_RED)

# ── AWS Native Services (right column) ───────────────────────────────────────
box(ax, 13.5, 5.5, 5.8, 6.6, C_SVC_BG, alpha=0.6, radius=0.3,
    ec=C_ORANGE, lw=1.5)
label(ax, 14.2, 11.8, 'AWS Native Services', size=8.5,
      color=C_ORANGE, weight='bold', ha='left')

svc_items = [
    ('AWS Config',     'Compliance Rules',  C_ORANGE),
    ('CloudTrail',     'Audit Logging',     C_YELLOW),
    ('Security Hub',   'Security Findings', C_RED),
    ('S3 Buckets',     'Evidence & Reports',C_GREEN),
    ('DynamoDB',       'Real-time Status',  C_BLUE),
    ('EventBridge',    'Event Routing',     C_PURPLE),
]
for i, (title, sub, col) in enumerate(svc_items):
    row = i // 2
    col_idx = i % 2
    sx = 13.7 + col_idx * 2.8
    sy = 9.8 - row * 1.55
    service_box(ax, sx, sy, 2.5, 1.3, title, sub,
                bg=C_SVC_BG, icon_color=col, title_size=7.5)

# ── Monitoring (bottom right) ─────────────────────────────────────────────────
box(ax, 13.5, 0.7, 5.8, 4.5, C_MON_BG, alpha=0.6, radius=0.3,
    ec=C_PURPLE, lw=1.5)
label(ax, 14.2, 4.95, 'Monitoring & Alerting', size=8.5,
      color=C_PURPLE, weight='bold', ha='left')

mon_items = [
    ('CloudWatch',  'Metrics & Logs',    C_PURPLE),
    ('SNS Topics',  'Notifications',     C_RED),
    ('CloudWatch\nAlarms', 'Thresholds', C_YELLOW),
    ('Cost Explorer','Budget Alerts',    C_GREEN),
]
for i, (title, sub, col) in enumerate(mon_items):
    row = i // 2
    col_idx = i % 2
    sx = 13.7 + col_idx * 2.8
    sy = 3.1 - row * 1.55
    service_box(ax, sx, sy, 2.5, 1.3, title, sub,
                bg=C_MON_BG, icon_color=col, title_size=7.5)

# ── Arrows ────────────────────────────────────────────────────────────────────
# User → IGW
arrow(ax, 2.5, 11.3, 3.6, 11.3, color=C_BLUE, lw=2)
# IGW → ALB
arrow(ax, 6.0, 10.15, 6.3, 10.15, color=C_TEAL, lw=1.8)
# ALB → ECS
arrow(ax, 7.5, 9.2, 7.5, 8.0, color=C_TEAL, lw=1.8)
# ECS → RDS
arrow(ax, 6.4, 6.9, 6.7, 6.9, color=C_BLUE, lw=1.5)
# ECS → Lambda
arrow(ax, 9.8, 6.9, 9.8+0.1, 6.9, color=C_PURPLE, lw=1.5)
# Lambda → Config
arrow(ax, 12.4, 7.0, 13.5, 10.4, color=C_ORANGE, lw=1.5)
# Lambda → DynamoDB
arrow(ax, 12.4, 6.5, 13.5, 8.85, color=C_BLUE, lw=1.5)
# Lambda → SNS
arrow(ax, 12.4, 6.0, 13.5, 2.45, color=C_RED, lw=1.5)
# CloudTrail → S3
arrow(ax, 16.2, 9.8, 16.2, 9.2, color=C_YELLOW, lw=1.2)
# CloudWatch → Alarms
arrow(ax, 14.95, 1.7, 14.95, 1.3+0.1, color=C_PURPLE, lw=1.2)

# ── Legend ────────────────────────────────────────────────────────────────────
legend_items = [
    (C_TEAL,   'Public Network'),
    (C_BLUE,   'Private Network'),
    (C_ORANGE, 'AWS Services'),
    (C_PURPLE, 'Serverless / Monitoring'),
    (C_YELLOW, 'Audit & Encryption'),
    (C_RED,    'Security & Alerting'),
]
box(ax, 0.2, 0.3, 2.4, 5.8, "#161B22", alpha=0.95, ec=C_BORDER, lw=1)
label(ax, 1.4, 5.8, 'Legend', size=8, color=C_WHITE, weight='bold')
for i, (col, txt) in enumerate(legend_items):
    y_pos = 5.2 - i * 0.78
    rect = FancyBboxPatch((0.35, y_pos-0.18), 0.35, 0.36,
                          boxstyle="round,pad=0,rounding_size=0.05",
                          facecolor=col, edgecolor=col, linewidth=0, zorder=4)
    ax.add_patch(rect)
    label(ax, 1.45, y_pos, txt, size=7, color=C_LIGHT, ha='left', va='center')

# ── Footer ────────────────────────────────────────────────────────────────────
label(ax, 10, 0.15,
      'GRC208 Governance, Risk, and Compliance Capstone Project  |  March 2026',
      size=7.5, color="#6E7681")

plt.tight_layout(pad=0.2)
plt.savefig('/home/ubuntu/grc-capstone-project/diagrams/01_system_architecture.png',
            dpi=180, bbox_inches='tight', facecolor=C_BG)
plt.close()
print("Diagram 1 saved.")
