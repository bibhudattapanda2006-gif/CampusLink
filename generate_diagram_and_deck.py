"""
Generates a professional 1920x1080 system architecture diagram image for CampusLink.
"""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1920, 1080
img = Image.new("RGB", (W, H), "#0B0F19") # Dark slate background
draw = ImageDraw.Draw(img)

# Try loading standard Windows TTF fonts, fallback to default
try:
    font_title = ImageFont.truetype("arialbd.ttf", 46)
    font_sub = ImageFont.truetype("arial.ttf", 22)
    font_sec = ImageFont.truetype("arialbd.ttf", 26)
    font_card_h = ImageFont.truetype("arialbd.ttf", 20)
    font_card_b = ImageFont.truetype("arial.ttf", 15)
    font_tag = ImageFont.truetype("arialbd.ttf", 14)
except Exception:
    font_title = font_sub = font_sec = font_card_h = font_card_b = font_tag = ImageFont.load_default()

# 1. Header Banner
draw.rectangle([(0, 0), (W, 110)], fill="#0F172A")
draw.line([(0, 110), (W, 110)], fill="#3B82F6", width=3)

draw.text((60, 25), "CAMPUSLINK", font=font_title, fill="#38BDF8")
draw.text((370, 42), "|  Full-Stack System Architecture & Data Flow Diagram", font=font_sub, fill="#94A3B8")
draw.text((1550, 42), "CAREER INTELLIGENCE OS", font=font_sub, fill="#38BDF8")

# Helper function to draw rounded boxes
def draw_card(x, y, w, h, bg="#1E293B", border="#334155", radius=12):
    draw.rounded_rectangle([(x, y), (x + w, y + h)], radius=radius, fill=bg, outline=border, width=2)

# --- COLUMN 1: CLIENT WORKSPACES (x=60 to 580) ---
draw_card(60, 140, 500, 890, bg="#111827", border="#1E3A8A")
draw.text((80, 160), "1. CLIENT WORKSPACES & ACTORS", font=font_sec, fill="#60A5FA")
draw.text((80, 195), "React 19 · Vite 8 · Tailwind v4 · TanStack Query", font=font_card_b, fill="#64748B")

# Cards inside Col 1
workspaces = [
    ("Student: Career Twin (/twin)", "Self-reported & evidenced skills inventory, verified projects, provenance tracking, academic record.", "#10B981"),
    ("Opportunity Mirror (/mirror)", "Explainable job compatibility matching (0-100%), met criteria, missing gaps, bonus factors.", "#06B6D4"),
    ("Skill Sprint (/sprint)", "Hands-on coding challenges evaluated via Rubric v1; 70+ passing score auto-promotes skill.", "#8B5CF6"),
    ("Interview Arena (/arena)", "Mock interview room; STAR structure & quantitative metrics scoring; anti-cheat points ledger.", "#F59E0B"),
    ("Placement Tower (/tower)", "Staff/Admin analytics: cohort readiness, hiring funnel, What-If simulation laboratory.", "#EC4899"),
    ("Public Authentication (/register, /login)", "3-step email verified student registration (OTP) & secure HttpOnly session gate.", "#3B82F6"),
]

cy = 230
for title, desc, color in workspaces:
    draw_card(80, cy, 460, 115, bg="#1F2937", border="#374151")
    draw.rectangle([(80, cy), (86, cy + 115)], fill=color)
    draw.text((98, cy + 12), title, font=font_card_h, fill="#F9FAFB")
    
    # Wrap description
    words = desc.split()
    line1 = " ".join(words[:8])
    line2 = " ".join(words[8:])
    draw.text((98, cy + 42), line1, font=font_card_b, fill="#9CA3AF")
    draw.text((98, cy + 65), line2, font=font_card_b, fill="#9CA3AF")
    cy += 128

# --- COLUMN 2: API, SECURITY & ENGINES (x=600 to 1260) ---
draw_card(600, 140, 660, 890, bg="#111827", border="#0284C7")
draw.text((620, 160), "2. DETERMINISTIC ENGINES & CONTROLLERS", font=font_sec, fill="#38BDF8")
draw.text((620, 195), "Express 4 · TypeScript · Zod · Zero Black-Box AI", font=font_card_b, fill="#64748B")

# Top Sub-box: Security Gate
draw_card(620, 230, 620, 130, bg="#1E293B", border="#0284C7")
draw.text((640, 245), "Defense-in-Depth Security Gateway", font=font_card_h, fill="#38BDF8")
draw.text((640, 280), "• CSPRNG HMAC-SHA256 Email OTP (10m TTL, attempt caps) + Nodemailer SMTP", font=font_card_b, fill="#E2E8F0")
draw.text((640, 305), "• scrypt Password Hashing + Revocable HttpOnly Sessions (SHA-256 tokens)", font=font_card_b, fill="#E2E8F0")
draw.text((640, 330), "• Strict Loopback CORS (127.0.0.1:5173), CSRF Origin Check, Zod Strict Validation", font=font_card_b, fill="#E2E8F0")

# Middle Sub-boxes: The 4 Engines
engines = [
    ("Explainable Match Engine (lib/match.ts)",
     "Score = min(100, round(100 x (Points / MaxPoints)))\n"
     "• Weights required skills by seniority (Rank x 2)\n"
     "• Linked project evidence bonus (+0.5/project, cap +1.0)\n"
     "• Partial credit (75%) for 1 level below; nice-to-haves (+1)",
     "#06B6D4"),
    ("Rubric Sprint Evaluator (lib/rubric.ts)",
     "Score = 40 (Base) + 25 (Tasks) + 15 (Repo Link) + 15 (Write-up) + 5 (Quality)\n"
     "• Pass threshold: 70+\n"
     "• Transactional Auto-Promotion of Skill Level\n"
     "• Upserts 'Sprint: <Title>' Project row as verifiable evidence",
     "#8B5CF6"),
    ("Interview Arena Evaluator (lib/arena.ts)",
     "Score = 35 (Base) + 30 (Substance) + 15 (Numbers) + 10 (Reasoning) + 10 (STAR)\n"
     "• Practice Points = floor(Score / 10) [0-10]\n"
     "• Saved in ArenaPointLedger keyed by session (anti-duplication)",
     "#F59E0B"),
    ("Holistic Readiness Engine (lib/match.ts)",
     "Readiness = 50% Proficiency + 30% Evidence + 20% Momentum\n"
     "• Proficiency = (Mean Skill Rank / 4) x 50\n"
     "• Evidence = (Evidenced Skills / Total Skills) x 30 (Unverified = 0)\n"
     "• Momentum = min(20, Applications x 4 + Evaluated Sprints x 6)",
     "#10B981")
]

ey = 380
for ename, edesc, ecolor in engines:
    draw_card(620, ey, 620, 145, bg="#1E293B", border="#334155")
    draw.rectangle([(620, ey), (626, ey + 145)], fill=ecolor)
    draw.text((640, ey + 10), ename, font=font_card_h, fill="#F9FAFB")
    
    dlines = edesc.split("\n")
    for idx, dline in enumerate(dlines):
        draw.text((640, ey + 40 + (idx * 24)), dline, font=font_card_b, fill="#CBD5E1")
    ey += 160

# --- COLUMN 3: DATABASE & PERSISTENCE (x=1300 to 1860) ---
draw_card(1300, 140, 560, 890, bg="#111827", border="#047857")
draw.text((1320, 160), "3. DATA PERSISTENCE & PRISMA", font=font_sec, fill="#34D399")
draw.text((1320, 195), "PostgreSQL 16+ · Prisma ORM · Relational Cascades", font=font_card_b, fill="#64748B")

db_tables = [
    ("User & Session", "Authentication accounts (STUDENT, STAFF, RECRUITER, ADMIN), passwordHash (scrypt), revocable tokenHash sessions.", "#3B82F6"),
    ("RegistrationAttempt", "In-flight signup OTP verification, HMAC peppered hashes, attempt counters, 20m completion tokens.", "#60A5FA"),
    ("StudentProfile & Skills", "Academic record, CGPA, 1:N StudentSkill (BEGINNER to EXPERT), 1:N Project with verifiable URLs.", "#10B981"),
    ("JobOpportunity & Apps", "Corporate hiring listings with JSON requiredSkills criteria. 1:N Application with FSM status transitions.", "#06B6D4"),
    ("Assessments & Attempts", "Technical sprint catalog, submitted repo links, write-ups, rule-based rubric feedback scores.", "#8B5CF6"),
    ("Arena Bank & Ledger", "Curated interview question bank, student response transcripts, unique session practice points ledger.", "#F59E0B"),
    ("Announcements & Receipts", "Targeted campus broadcasts (ALL, APPLIED, SHORTLISTED, HIRED) materialized into frozen recipient rows.", "#EC4899"),
]

dy = 230
for tname, tdesc, tcolor in db_tables:
    draw_card(1320, dy, 520, 98, bg="#1E293B", border="#334155")
    draw.rectangle([(1320, dy), (1326, dy + 98)], fill=tcolor)
    draw.text((1340, dy + 10), tname, font=font_card_h, fill="#F9FAFB")
    
    words = tdesc.split()
    line1 = " ".join(words[:10])
    line2 = " ".join(words[10:])
    draw.text((1340, dy + 40), line1, font=font_card_b, fill="#94A3B8")
    draw.text((1340, dy + 63), line2, font=font_card_b, fill="#94A3B8")
    dy += 110

# Connecting Arrows (Horizontal indications)
def draw_arrow(x1, y1, x2, y2, color="#38BDF8"):
    draw.line([(x1, y1), (x2, y2)], fill=color, width=3)
    draw.polygon([(x2, y2), (x2 - 10, y2 - 6), (x2 - 10, y2 + 6)], fill=color)

draw_arrow(560, 450, 600, 450, color="#38BDF8")
draw_arrow(560, 600, 600, 600, color="#8B5CF6")
draw_arrow(560, 750, 600, 750, color="#F59E0B")

draw_arrow(1260, 450, 1300, 450, color="#34D399")
draw_arrow(1260, 600, 1300, 600, color="#34D399")
draw_arrow(1260, 750, 1300, 750, color="#34D399")

# Save diagram
out_path = "CAMPUSLINK_Architecture_Diagram.png"
img.save(out_path, quality=95)
print(f"Architecture diagram generated: {out_path} ({os.path.getsize(out_path):,} bytes)")
