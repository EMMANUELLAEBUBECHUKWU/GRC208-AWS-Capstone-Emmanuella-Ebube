"""
Diagram 4: Security Architecture - Defence in Depth
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Wedge
import numpy as np

fig, ax = plt.subplots(figsize=(20, 13))
ax.set_xlim(0, 20)
ax.set_ylim(0, 13)
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

def rbox(ax, x, y, w, h, fc, ec, lw=1.5, alpha=0.88, radius=0.25, zorder=2):
    p = FancyBboxPatch((x, y), w, h,
                       boxstyle=f"round,pad=0,rounding_size={radius}",
                       facecolor=fc, edgecolor=ec, linewidth=lw,
                       alpha=alpha, zorder=zorder)
    ax.add_patch(p)

def t(ax, x, y, s, size=9, color=C_WHITE, weight='normal',
      ha='center', va='center', zorder=5):
    ax.text(x, y, s, fontsize=size, color=color, fontweight=weight,
            ha=ha, va=va, zorder=zorder, fontfamily='DejaVu Sans')

def arr(ax, x1, y1, x2, y2, col=C_ORANGE, lw=1.8):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color=col, lw=lw,
                                connectionstyle='arc3,rad=0.0'), zorder=4)

# ── Title ─────────────────────────────────────────────────────────────────────
t(ax, 10, 12.55, 'GRC Platform — Security Architecture', size=17,
  color=C_ORANGE, weight='bold')
t(ax, 10, 12.1, 'Defence-in-Depth: Network · Application · Data · Identity · Audit',
  size=9.5, color=C_LIGHT)

# ── Left: Concentric defence layers ──────────────────────────────────────────
cx, cy = 5.5, 6.0
layers = [
    (4.8, "#0D1117",  C_BORDER, 'Outer Perimeter'),
    (4.0, "#0F1A20",  C_TEAL,   'Layer 1: Network'),
    (3.2, "#0F1820",  C_BLUE,   'Layer 2: Transport'),
    (2.4, "#101828",  C_PURPLE, 'Layer 3: Application'),
    (1.6, "#101530",  C_YELLOW, 'Layer 4: Data'),
    (0.8, "#180F18",  C_RED,    'Layer 5: Identity'),
]
for (r, fc, ec, _) in reversed(layers):
    circle = plt.Circle((cx, cy), r, facecolor=fc, edgecolor=ec,
                        linewidth=2, alpha=0.85, zorder=2)
    ax.add_patch(circle)

# Core
core = plt.Circle((cx, cy), 0.55, facecolor="#1A0A2A",
                  edgecolor=C_PURPLE, linewidth=2.5, alpha=1, zorder=6)
ax.add_patch(core)
t(ax, cx, cy, 'GRC\nCore', size=7, color=C_WHITE, weight='bold', zorder=7)

# Layer labels on the rings
ring_labels = [
    (4.4, 0,   'NETWORK PERIMETER', C_TEAL),
    (3.6, 45,  'TLS ENCRYPTION', C_BLUE),
    (2.8, 90,  'WAF / APP LAYER', C_PURPLE),
    (2.0, 135, 'DATA ENCRYPTION', C_YELLOW),
    (1.2, 180, 'IAM / RBAC', C_RED),
]
for (r, angle_deg, lbl, col) in ring_labels:
    angle_rad = np.radians(angle_deg)
    lx = cx + r * np.cos(angle_rad)
    ly = cy + r * np.sin(angle_rad)
    t(ax, lx, ly, lbl, size=6.5, color=col, weight='bold', zorder=8)

# ── Right: Security controls table ───────────────────────────────────────────
rx0 = 10.5
rbox(ax, rx0, 0.5, 9.2, 11.2, "#0F1117", C_BORDER, lw=1.5, alpha=0.95)
t(ax, rx0+4.6, 11.35, 'Security Controls Reference', size=12,
  color=C_WHITE, weight='bold')

controls = [
    ('NETWORK',     C_TEAL,   [
        ('VPC Isolation',          'Public/private subnet separation'),
        ('Security Groups',        'Stateful firewall, least privilege'),
        ('Network ACLs',           'Stateless subnet-level filtering'),
        ('NAT Gateway',            'Outbound-only for private subnets'),
    ]),
    ('TRANSPORT',   C_BLUE,   [
        ('TLS 1.2+',               'Encryption in transit enforced'),
        ('ALB HTTPS',              'Certificate managed by ACM'),
        ('VPC Endpoints',          'Private AWS service connectivity'),
        ('PrivateLink',            'No internet exposure for services'),
    ]),
    ('DATA',        C_YELLOW, [
        ('KMS Encryption',         'AES-256 at rest for all stores'),
        ('RDS Encryption',         'Multi-AZ encrypted MySQL'),
        ('S3 SSE-KMS',             'Server-side encryption + versioning'),
        ('DynamoDB Encryption',    'Managed encryption at rest'),
    ]),
    ('IDENTITY',    C_RED,    [
        ('IAM Roles',              'Least-privilege, no root usage'),
        ('MFA Enforcement',        'Required for console access'),
        ('Service Roles',          'Task/Lambda execution roles'),
        ('SCPs',                   'Organisation-level guardrails'),
    ]),
    ('AUDIT',       C_PURPLE, [
        ('CloudTrail',             'All API calls logged to S3'),
        ('CloudWatch Logs',        'Application & access logs'),
        ('Config Rules',           'Continuous compliance checks'),
        ('Security Hub',           'Aggregated security findings'),
    ]),
]

y_cursor = 10.6
for (section, col, items) in controls:
    rbox(ax, rx0+0.15, y_cursor-0.45, 8.9, 0.5, col, col,
         lw=0, alpha=0.18, radius=0.1)
    t(ax, rx0+0.6, y_cursor-0.2, section, size=8.5, color=col,
      weight='bold', ha='left')
    y_cursor -= 0.55
    for (ctrl, desc) in items:
        t(ax, rx0+0.7, y_cursor-0.15, f'• {ctrl}', size=7.5,
          color=C_WHITE, weight='bold', ha='left')
        t(ax, rx0+3.5, y_cursor-0.15, desc, size=7,
          color=C_LIGHT, ha='left')
        y_cursor -= 0.42
    y_cursor -= 0.1

# ── Bottom: Compliance frameworks bar ────────────────────────────────────────
rbox(ax, 0.3, 0.3, 9.8, 1.0, "#161B22", C_ORANGE, lw=1.5)
t(ax, 5.2, 1.0, 'Compliance Frameworks Supported', size=8.5,
  color=C_ORANGE, weight='bold')
frameworks = ['ISO 27001', 'NIST CSF', 'PCI DSS', 'HIPAA', 'GDPR', 'SOC 2']
fw_colors  = [C_BLUE, C_GREEN, C_YELLOW, C_RED, C_PURPLE, C_TEAL]
for i, (fw, col) in enumerate(zip(frameworks, fw_colors)):
    fx = 0.7 + i * 1.58
    rbox(ax, fx, 0.38, 1.4, 0.52, col, col, lw=0, alpha=0.25, radius=0.12)
    t(ax, fx+0.7, 0.64, fw, size=7.5, color=col, weight='bold')

# ── Footer ────────────────────────────────────────────────────────────────────
t(ax, 10, 0.12,
  'GRC208 Governance, Risk, and Compliance Capstone Project  |  March 2026',
  size=7.5, color="#6E7681")

plt.tight_layout(pad=0.2)
plt.savefig('/home/ubuntu/grc-capstone-project/diagrams/04_security_architecture.png',
            dpi=180, bbox_inches='tight', facecolor=C_BG)
plt.close()
print("Diagram 4 saved.")
