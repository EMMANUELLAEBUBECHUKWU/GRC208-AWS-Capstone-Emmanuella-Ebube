"""
AWS Access Options Diagram
GRC208 Governance, Risk, and Compliance Capstone Project
International Cybersecurity and Digital Forensics Academy (ICDFA)
March 2026
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import matplotlib.patheffects as pe
import numpy as np

# ── Brand colours ──────────────────────────────────────────────────────────────
PRIMARY   = '#0D3265'
SECONDARY = '#07ADF6'
SUCCESS   = '#4cc9f0'
WARNING   = '#f8961e'
DANGER    = '#f94144'
LIGHT     = '#FCFDFD'
DARK      = '#212529'
GRAY      = '#6c757d'

BG        = '#0a0f1e'
CARD_BG   = '#111827'
BORDER    = '#1e2d4a'

# ── Option palette ─────────────────────────────────────────────────────────────
OPT_COLORS = {
    'A': {'border': '#f8961e', 'badge': '#f8961e', 'glow': '#f8961e33', 'label': 'RECOMMENDED'},
    'B': {'border': '#07ADF6', 'badge': '#07ADF6', 'glow': '#07ADF633', 'label': 'FREE'},
    'C': {'border': '#4cc9f0', 'badge': '#4cc9f0', 'glow': '#4cc9f033', 'label': 'PERSONAL'},
    'D': {'border': '#a78bfa', 'badge': '#a78bfa', 'glow': '#a78bfa33', 'label': 'ADVANCED'},
}

# ── Option data ────────────────────────────────────────────────────────────────
OPTIONS = [
    {
        'key': 'A',
        'title': 'AWS Academy\nLearner Lab',
        'subtitle': 'ICDFA is an AWS Academy Member',
        'icon': 'A',
        'credits': '$50 – $100',
        'card_req': 'No Credit Card',
        'duration': 'Up to 4 hrs/session',
        'steps': [
            '1. Contact instructor Aminu Idris',
            '2. Receive email invitation',
            '3. Login: awsacademy.instructure.com',
            '4. Open course > Click Learner Lab',
            '5. Click Start Lab (60 sec launch)',
            '6. Click green AWS button to open console',
        ],
        'benefits': [
            'Pre-loaded AWS credits',
            'No personal billing',
            'Pre-configured IAM roles',
            'Instructor can monitor progress',
            'Data persists between sessions',
            'All project services available',
        ],
        'best_for': 'All GRC208 students at ICDFA',
    },
    {
        'key': 'B',
        'title': 'AWS Educate',
        'subtitle': 'Free — No Credit Card Required',
        'icon': 'B',
        'credits': 'Free Sandbox',
        'card_req': 'No Credit Card',
        'duration': 'Unlimited sessions',
        'steps': [
            '1. Go to aws.amazon.com/education/awseducate',
            '2. Click Join AWS Educate',
            '3. Select Student',
            '4. Use institutional email address',
            '5. Verify email (approval ~24 hrs)',
            '6. Access AWS Builder Labs sandbox',
        ],
        'benefits': [
            'Completely free',
            'No credit card needed',
            'Pre-built lab environments',
            'Free courses and badges',
            'AWS Console access via sandbox',
            'Global student programme',
        ],
        'best_for': 'Students without credit cards',
    },
    {
        'key': 'C',
        'title': 'AWS Free Tier\nPersonal Account',
        'subtitle': '12 Months Free on New Accounts',
        'icon': 'C',
        'credits': '12 Months Free',
        'card_req': 'Card for Verification',
        'duration': '12 months',
        'steps': [
            '1. Go to aws.amazon.com/free',
            '2. Click Create a Free Account',
            '3. Enter email and account name',
            '4. Verify phone number',
            '5. Add card (identity check only)',
            '6. Select Basic Support (Free)',
        ],
        'benefits': [
            'RDS MySQL: 750 hrs/month FREE',
            'Lambda: 1M requests/month FREE',
            'S3: 5 GB storage FREE',
            'DynamoDB: 25 GB FREE',
            'CloudTrail: First trail FREE',
            'Total project cost: $0 – $5/mo',
        ],
        'best_for': 'Students wanting own AWS account',
    },
    {
        'key': 'D',
        'title': 'AWS Activate',
        'subtitle': 'Up to $1,000 in Credits',
        'icon': 'D',
        'credits': 'Up to $1,000',
        'card_req': 'Account Required',
        'duration': '1 year validity',
        'steps': [
            '1. Go to aws.amazon.com/activate',
            '2. Click Apply Now (Founders tier)',
            '3. Complete application form',
            '4. Describe your project',
            '5. Submit and await approval',
            '6. Credits applied within 1–2 weeks',
        ],
        'benefits': [
            'Up to $1,000 in AWS credits',
            'Technical support included',
            'Ideal for portfolio projects',
            'Startup-grade resources',
            'Access to AWS partner network',
            'Great for independent study',
        ],
        'best_for': 'Independent / portfolio projects',
    },
]

# ── Figure setup ───────────────────────────────────────────────────────────────
fig = plt.figure(figsize=(26, 20), facecolor=BG)
fig.patch.set_facecolor(BG)

# ── Title block ────────────────────────────────────────────────────────────────
ax_title = fig.add_axes([0, 0.91, 1, 0.09])
ax_title.set_facecolor(BG)
ax_title.axis('off')

ax_title.text(0.5, 0.75, 'AWS Access Options for GRC208 Students',
              ha='center', va='center', fontsize=28, fontweight='bold',
              color=WARNING, transform=ax_title.transAxes)
ax_title.text(0.5, 0.30,
              'Choose the option that best suits your situation  |  All options are FREE',
              ha='center', va='center', fontsize=13, color=LIGHT,
              transform=ax_title.transAxes, alpha=0.85)

# Horizontal divider
ax_title.axhline(y=0.02, color=SECONDARY, linewidth=1.5, alpha=0.4)

# ── Helper: draw one option card ───────────────────────────────────────────────
def draw_card(ax, opt, col):
    c = OPT_COLORS[opt['key']]
    ax.set_facecolor(CARD_BG)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    # Outer glow border
    for lw, alpha in [(12, 0.08), (6, 0.15), (2, 0.9)]:
        rect = FancyBboxPatch((0.01, 0.01), 0.98, 0.98,
                              boxstyle='round,pad=0.02',
                              linewidth=lw, edgecolor=c['border'],
                              facecolor='none', alpha=alpha,
                              transform=ax.transAxes, clip_on=False)
        ax.add_patch(rect)

    # Option badge (top-left circle)
    badge_circle = plt.Circle((0.09, 0.93), 0.065,
                               color=c['badge'], zorder=5,
                               transform=ax.transAxes, clip_on=False)
    ax.add_patch(badge_circle)
    ax.text(0.09, 0.93, opt['key'],
            ha='center', va='center', fontsize=18, fontweight='bold',
            color=DARK, transform=ax.transAxes, zorder=6)

    # RECOMMENDED / FREE / etc. label badge
    label_bg = FancyBboxPatch((0.72, 0.895), 0.25, 0.055,
                               boxstyle='round,pad=0.01',
                               facecolor=c['badge'], edgecolor='none',
                               alpha=0.9, transform=ax.transAxes, zorder=4)
    ax.add_patch(label_bg)
    ax.text(0.845, 0.922, c['label'],
            ha='center', va='center', fontsize=8, fontweight='bold',
            color=DARK, transform=ax.transAxes, zorder=5)

    # Title
    ax.text(0.5, 0.845, opt['title'],
            ha='center', va='center', fontsize=14, fontweight='bold',
            color=LIGHT, transform=ax.transAxes, linespacing=1.3)

    # Subtitle
    ax.text(0.5, 0.785, opt['subtitle'],
            ha='center', va='center', fontsize=9.5, color=c['border'],
            transform=ax.transAxes, style='italic')

    # ── KPI strip ──────────────────────────────────────────────────────────────
    kpi_y = 0.715
    kpi_data = [
        ('Credits', opt['credits']),
        ('Card', opt['card_req']),
        ('Duration', opt['duration']),
    ]
    for i, (label, value) in enumerate(kpi_data):
        x = 0.17 + i * 0.33
        kpi_box = FancyBboxPatch((x - 0.13, kpi_y - 0.045), 0.26, 0.09,
                                  boxstyle='round,pad=0.01',
                                  facecolor=PRIMARY, edgecolor=c['border'],
                                  linewidth=0.8, alpha=0.7,
                                  transform=ax.transAxes)
        ax.add_patch(kpi_box)
        ax.text(x, kpi_y + 0.015, value,
                ha='center', va='center', fontsize=7.5, fontweight='bold',
                color=c['badge'], transform=ax.transAxes)
        ax.text(x, kpi_y - 0.022, label,
                ha='center', va='center', fontsize=6.5, color=GRAY,
                transform=ax.transAxes)

    # Divider
    ax.axhline(y=0.655, xmin=0.04, xmax=0.96,
               color=c['border'], linewidth=0.6, alpha=0.4)

    # ── Steps column ───────────────────────────────────────────────────────────
    ax.text(0.26, 0.625, 'HOW TO ACCESS',
            ha='center', va='center', fontsize=8, fontweight='bold',
            color=c['border'], transform=ax.transAxes)

    for i, step in enumerate(opt['steps']):
        y = 0.575 - i * 0.072
        # Step dot
        dot = plt.Circle((0.055, y + 0.008), 0.018,
                          color=c['badge'], alpha=0.85,
                          transform=ax.transAxes, zorder=4)
        ax.add_patch(dot)
        ax.text(0.055, y + 0.008, str(i + 1),
                ha='center', va='center', fontsize=6, fontweight='bold',
                color=DARK, transform=ax.transAxes, zorder=5)
        ax.text(0.095, y + 0.008, step,
                ha='left', va='center', fontsize=7.2, color=LIGHT,
                transform=ax.transAxes, alpha=0.9)

    # Vertical divider between columns
    ax.axvline(x=0.52, ymin=0.04, ymax=0.61,
               color=c['border'], linewidth=0.6, alpha=0.35)

    # ── Benefits column ────────────────────────────────────────────────────────
    ax.text(0.76, 0.625, 'KEY BENEFITS',
            ha='center', va='center', fontsize=8, fontweight='bold',
            color=c['border'], transform=ax.transAxes)

    for i, benefit in enumerate(opt['benefits']):
        y = 0.575 - i * 0.072
        # Checkmark tick
        ax.text(0.545, y + 0.008, '✓',
                ha='left', va='center', fontsize=9, fontweight='bold',
                color=SUCCESS, transform=ax.transAxes)
        ax.text(0.585, y + 0.008, benefit,
                ha='left', va='center', fontsize=7.2, color=LIGHT,
                transform=ax.transAxes, alpha=0.9)

    # ── Best-for footer ────────────────────────────────────────────────────────
    footer_box = FancyBboxPatch((0.03, 0.025), 0.94, 0.055,
                                 boxstyle='round,pad=0.01',
                                 facecolor=c['glow'], edgecolor=c['border'],
                                 linewidth=0.8, transform=ax.transAxes)
    ax.add_patch(footer_box)
    ax.text(0.5, 0.052, f'Best For:  {opt["best_for"]}',
            ha='center', va='center', fontsize=8.5, fontweight='bold',
            color=LIGHT, transform=ax.transAxes)


# ── Draw four cards in a 2x2 grid ─────────────────────────────────────────────
positions = [
    [0.02, 0.44, 0.46, 0.46],   # A  top-left
    [0.52, 0.44, 0.46, 0.46],   # B  top-right
    [0.02, 0.02, 0.46, 0.41],   # C  bottom-left  (shorter — no recommended badge)
    [0.52, 0.02, 0.46, 0.41],   # D  bottom-right
]

for opt, pos in zip(OPTIONS, positions):
    ax = fig.add_axes(pos)
    draw_card(ax, opt, OPT_COLORS[opt['key']])


# ── Decision guide strip between title and cards ───────────────────────────────
ax_guide = fig.add_axes([0.02, 0.905, 0.96, 0.0])   # invisible height — just for text
# Actually embed decision table as a text block inside the title area
ax_title.text(0.5, -0.55,
    'Option A: GRC208 students at ICDFA   |   '
    'Option B: No credit card available   |   '
    'Option C: Want your own AWS account   |   '
    'Option D: Independent / portfolio project',
    ha='center', va='center', fontsize=9.5, color=GRAY,
    transform=ax_title.transAxes, style='italic')


# ── Footer ─────────────────────────────────────────────────────────────────────
ax_footer = fig.add_axes([0, 0, 1, 0.022])
ax_footer.set_facecolor(PRIMARY)
ax_footer.axis('off')
ax_footer.text(0.5, 0.5,
    'GRC208 Governance, Risk, and Compliance Capstone Project   |   '
    'International Cybersecurity and Digital Forensics Academy (ICDFA)   |   March 2026',
    ha='center', va='center', fontsize=8.5, color=LIGHT,
    transform=ax_footer.transAxes)

# ── Save ───────────────────────────────────────────────────────────────────────
out = '/home/ubuntu/grc-capstone-project/diagrams/07_aws_access_options.png'
plt.savefig(out, dpi=180, bbox_inches='tight',
            facecolor=BG, edgecolor='none')
plt.close()
print(f'Saved: {out}')
