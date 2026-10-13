"""
CAMPUSLINK System Architecture, Mechanics & Technology Stack Guide Generator
Outputs a high-quality, comprehensive engineering PDF document.
"""

import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfgen import canvas

# Palette
C_PRIMARY = colors.HexColor("#0F172A")    # Slate 900
C_SECONDARY = colors.HexColor("#1E293B")  # Slate 800
C_BRAND = colors.HexColor("#1E40AF")      # Blue 800
C_ACCENT = colors.HexColor("#0284C7")     # Sky 600
C_TEAL = colors.HexColor("#0F766E")       # Teal 700
C_BG_LIGHT = colors.HexColor("#F8FAFC")   # Slate 50
C_CARD_BG = colors.HexColor("#F1F5F9")    # Slate 100
C_BORDER = colors.HexColor("#CBD5E1")     # Slate 300
C_BORDER_DARK = colors.HexColor("#94A3B8")# Slate 400
C_TEXT_DARK = colors.HexColor("#0F172A")  # Slate 900
C_TEXT_MUTED = colors.HexColor("#475569") # Slate 600
C_GREEN = colors.HexColor("#047857")      # Emerald 700
C_AMBER = colors.HexColor("#B45309")      # Amber 700
C_ROSE = colors.HexColor("#BE123C")       # Rose 700

class NumberedCanvas(canvas.Canvas):
    """
    Two-pass canvas to dynamically compute and print total page count
    along with running headers and running footers.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_decorations(self, total_pages):
        page_w = 8.5 * 72
        page_h = 11.0 * 72

        # Suppress header/footer on cover page
        if self._pageNumber == 1:
            return

        self.saveState()

        # Running Header
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(C_BRAND)
        self.drawString(45, page_h - 32, "CAMPUSLINK")
        self.setFont("Helvetica", 8)
        self.setFillColor(C_TEXT_MUTED)
        self.drawString(108, page_h - 32, "|   System Architecture, Mechanics & Technology Reference Guide")

        self.setStrokeColor(C_BORDER)
        self.setLineWidth(0.6)
        self.line(45, page_h - 38, page_w - 45, page_h - 38)

        # Running Footer
        self.line(45, 42, page_w - 45, 42)
        self.setFont("Helvetica", 8)
        self.setFillColor(C_TEXT_MUTED)
        self.drawString(45, 30, "CAMPUSLINK  |  Career Intelligence OS  |  Deterministic & Local-First")
        
        page_str = f"Page {self._pageNumber} of {total_pages}"
        self.drawRightString(page_w - 45, 30, page_str)

        self.restoreState()


def build_pdf(filename="CAMPUSLINK_System_Guide.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=45,
        rightMargin=45,
        topMargin=50,
        bottomMargin=50
    )

    styles = getSampleStyleSheet()

    # Custom Typography Styles
    body = ParagraphStyle(
        'DocBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14,
        textColor=C_TEXT_DARK,
        alignment=TA_LEFT
    )

    body_justify = ParagraphStyle(
        'DocBodyJustify',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14,
        textColor=C_TEXT_DARK,
        alignment=TA_JUSTIFY
    )

    body_bold = ParagraphStyle(
        'DocBodyBold',
        parent=body,
        fontName='Helvetica-Bold'
    )

    body_muted = ParagraphStyle(
        'DocBodyMuted',
        parent=body,
        fontSize=8.5,
        leading=12,
        textColor=C_TEXT_MUTED
    )

    code_inline = ParagraphStyle(
        'DocCodeInline',
        parent=body,
        fontName='Courier',
        fontSize=8.5,
        leading=11,
        textColor=C_PRIMARY
    )

    title_main = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=26,
        leading=32,
        textColor=C_PRIMARY,
        alignment=TA_CENTER
    )

    title_sub = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=17,
        textColor=C_TEXT_MUTED,
        alignment=TA_CENTER
    )

    h1 = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=16,
        leading=20,
        textColor=C_BRAND,
        spaceBefore=16,
        spaceAfter=8,
        keepWithNext=True
    )

    h2 = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=C_SECONDARY,
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )

    h3 = ParagraphStyle(
        'Heading3_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=14,
        textColor=C_TEAL,
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )

    tbl_head = ParagraphStyle(
        'TableHead',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.white,
        alignment=TA_LEFT
    )

    tbl_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=C_TEXT_DARK
    )

    tbl_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=tbl_cell,
        fontName='Helvetica-Bold'
    )

    tbl_cell_code = ParagraphStyle(
        'TableCellCode',
        parent=tbl_cell,
        fontName='Courier',
        fontSize=7.5,
        leading=10,
        textColor=C_PRIMARY
    )

    callout_text = ParagraphStyle(
        'CalloutText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12.5,
        textColor=C_TEXT_DARK
    )

    formula_text = ParagraphStyle(
        'FormulaText',
        parent=styles['Normal'],
        fontName='Courier-Bold',
        fontSize=8.5,
        leading=12,
        textColor=C_BRAND
    )

    story = []

    # Helper functions for callouts & banners
    def make_callout(title, text, accent_color=C_BRAND, bg_color=C_CARD_BG):
        content = [
            Paragraph(f"<b>{title}</b>", ParagraphStyle('CTitle', parent=callout_text, fontName='Helvetica-Bold', textColor=accent_color)),
            Spacer(1, 3),
            Paragraph(text, callout_text)
        ]
        t = Table([[content]], colWidths=[522])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), bg_color),
            ('BOX', (0,0), (-1,-1), 0.5, C_BORDER),
            ('LINELEFT', (0,0), (-1,-1), 3.5, accent_color),
            ('TOPPADDING', (0,0), (-1,-1), 7),
            ('BOTTOMPADDING', (0,0), (-1,-1), 7),
            ('LEFTPADDING', (0,0), (-1,-1), 12),
            ('RIGHTPADDING', (0,0), (-1,-1), 12),
        ]))
        return t

    def make_formula_box(title, formula, explanation):
        content = [
            Paragraph(f"<b>MATHEMATICAL FORMULA: {title}</b>", ParagraphStyle('FTitle', parent=callout_text, fontName='Helvetica-Bold', fontSize=8, textColor=C_PRIMARY)),
            Spacer(1, 4),
            Paragraph(formula, formula_text),
            Spacer(1, 4),
            Paragraph(explanation, callout_text)
        ]
        t = Table([[content]], colWidths=[522])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EFF6FF")),
            ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#BFDBFE")),
            ('LINELEFT', (0,0), (-1,-1), 3.5, C_BRAND),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ('LEFTPADDING', (0,0), (-1,-1), 10),
            ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ]))
        return t

    def section_divider():
        return HRFlowable(width="100%", thickness=1, color=C_BORDER, spaceBefore=14, spaceAfter=14)

    # =========================================================================
    # COVER PAGE
    # =========================================================================
    story.append(Spacer(1, 40))
    
    # Pill Tag
    badge = Table([[Paragraph("<b>CAMPUSLINK SYSTEM ARCHITECTURE & BLUEPRINT</b>", ParagraphStyle('Badge', fontName='Helvetica-Bold', fontSize=8.5, leading=10, textColor=C_BRAND, alignment=TA_CENTER))]], colWidths=[280])
    badge.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EFF6FF")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#BFDBFE")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ]))
    story.append(badge)
    story.append(Spacer(1, 20))

    story.append(Paragraph("CAMPUSLINK", title_main))
    story.append(Spacer(1, 6))
    story.append(Paragraph("System Architecture, Operational Mechanics<br/>& Complete Technology Reference Guide", ParagraphStyle('SubSub', parent=title_sub, fontSize=15, leading=20, textColor=C_BRAND)))
    story.append(Spacer(1, 10))
    story.append(Paragraph("An In-Depth Engineering Blueprint of <i>How Things Work</i> and <i>What Things Have Been Used for What</i>", title_sub))
    story.append(Spacer(1, 25))

    # Decorative Box on Cover
    cover_meta_content = [
        [Paragraph("<b>Target Platform:</b>", tbl_cell_bold), Paragraph("CAMPUSLINK Career Intelligence Operating System", tbl_cell)],
        [Paragraph("<b>Architecture Pattern:</b>", tbl_cell_bold), Paragraph("Local-First Monorepo (Express/Prisma/PostgreSQL + React/Vite/Tailwind)", tbl_cell)],
        [Paragraph("<b>Core Philosophy:</b>", tbl_cell_bold), Paragraph("Zero Black-Box AI · Fully Deterministic Rubrics & Matching · Cryptographic Provenance", tbl_cell)],
        [Paragraph("<b>Primary User Personas:</b>", tbl_cell_bold), Paragraph("Students, Placement Officers (Staff), Corporate Recruiters, System Administrators", tbl_cell)],
        [Paragraph("<b>Database Engine:</b>", tbl_cell_bold), Paragraph("PostgreSQL Relational DB with Prisma 5 Schema Migrations & Relations", tbl_cell)],
        [Paragraph("<b>Security & Auth:</b>", tbl_cell_bold), Paragraph("scrypt Hashing, CSPRNG HMAC-SHA256 Email OTP, Revocable HttpOnly Sessions, Strict CORS & CSRF", tbl_cell)],
        [Paragraph("<b>Documentation Scope:</b>", tbl_cell_bold), Paragraph("Full System Mechanics, Algorithms, Component Roles, Database Schema & Operational Runbook", tbl_cell)],
    ]
    meta_table = Table(cover_meta_content, colWidths=[140, 350])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_CARD_BG),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER),
        ('INNERGRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(meta_table)

    story.append(Spacer(1, 35))

    cover_note = make_callout(
        "ARCHITECTURAL PRINCIPLE: TRANSPARENT & EVIDENCE-BACKED PLACEMENT",
        "Unlike platforms that rely on opaque black-box AI matchmakers or unverified resume claims, "
        "CAMPUSLINK operates entirely on explainable mathematical models, publicly auditable grading rubrics, "
        "and verifiable project evidence. Every metric, skill level advancement, and job compatibility factor is "
        "backed by persisted relational records in PostgreSQL.",
        accent_color=C_TEAL,
        bg_color=colors.HexColor("#F0FDFA")
    )
    story.append(cover_note)

    story.append(Spacer(1, 35))
    story.append(Paragraph("<b>CONFIDENTIAL & COMPREHENSIVE ENGINEERING REFERENCE</b><br/>Published for Development, Architecture Review & Auditing", ParagraphStyle('FootCenter', parent=body_muted, alignment=TA_CENTER)))

    story.append(PageBreak())

    # =========================================================================
    # SECTION 1: EXECUTIVE SUMMARY & SYSTEM PHILOSOPHY
    # =========================================================================
    story.append(Paragraph("1. Executive Summary & Core System Philosophy", h1))
    story.append(HRFlowable(width="100%", thickness=1.5, color=C_BRAND, spaceBefore=2, spaceAfter=10))

    story.append(Paragraph(
        "<b>CAMPUSLINK</b> is a modern, high-assurance career intelligence and campus placement operating system. "
        "It replaces manual placement tracking, unverified resume claims, and disconnected spreadsheets with a unified, "
        "evidence-backed ecosystem connecting Students, Placement Cell Officers (Staff), and Corporate Recruiters.",
        body_justify
    ))
    story.append(Spacer(1, 8))

    story.append(Paragraph(
        "Modern hiring suffers from a profound credibility crisis: resumes contain exaggerated, self-reported skills, "
        "while companies rely on unpredictable machine learning classifiers that candidates cannot inspect or trust. "
        "CAMPUSLINK was engineered from first principles around three inviolable architectural commitments:",
        body_justify
    ))
    story.append(Spacer(1, 8))

    philosophy_items = [
        ("1. Zero Black-Box AI Guarantee", "Every score in the system—whether job matching compatibility, sprint assessment grading, interview performance, or student placement readiness—is computed using a transparent, published, deterministic rule-based formula. The system never delegates evaluation to unexplainable neural networks or generative LLMs."),
        ("2. Provenance-Based Credentialing", "The platform strictly delineates between <i>Self-Reported</i> claims (which carry minimal weight) and <i>Evidenced</i> credentials (backed by verified project repositories and rubric-evaluated Sprint submissions). Unverified claims earn zero evidence points."),
        ("3. Local-First & Defense-in-Depth Security", "Designed to operate independently on local infrastructure without cloud vendor lock-in. Loopback-only bindings, HttpOnly session cookies, cryptographic scrypt password hashing, CSPRNG HMAC-SHA256 OTP verification, and server-side RBAC ensure enterprise-grade security.")
    ]

    for title_p, desc_p in philosophy_items:
        story.append(Paragraph(f"• <b>{title_p}:</b> {desc_p}", body))
        story.append(Spacer(1, 4))

    story.append(Spacer(1, 6))

    # High-level architecture table
    arch_flow_data = [
        [Paragraph("<b>LAYER</b>", tbl_head), Paragraph("<b>TECHNOLOGY & COMPONENTS</b>", tbl_head), Paragraph("<b>PRIMARY RESPONSIBILITY</b>", tbl_head)],
        [
            Paragraph("<b>Client Layer (Frontend)</b>", tbl_cell_bold),
            Paragraph("React 19, Vite 8, React Router v7, TanStack Query, Tailwind CSS v4, Lucide React", tbl_cell),
            Paragraph("Single-Page Application (SPA) providing responsive workspaces: Career Twin, Opportunity Mirror, Skill Sprint, Interview Arena, Applications, Placement Tower.", tbl_cell)
        ],
        [
            Paragraph("<b>API & Controller Layer (Backend)</b>", tbl_cell_bold),
            Paragraph("Express 4, TypeScript 5, Zod, Helmet, CORS, Express-Rate-Limit", tbl_cell),
            Paragraph("RESTful endpoints with strict JSON schemas, IP rate-limiting budgets, CSRF origin verification, and server-side role-based access control (RBAC).", tbl_cell)
        ],
        [
            Paragraph("<b>Core Business Logic & Engines</b>", tbl_cell_bold),
            Paragraph("Deterministic Matching Engine, Rubric v1 Evaluator, Arena Bank Evaluator, Readiness Calculator", tbl_cell),
            Paragraph("Calculates explainable fit scores, evaluates code sprint submissions, tallies STAR interview answers, and compiles holistic student readiness.", tbl_cell)
        ],
        [
            Paragraph("<b>Data Access & Storage Layer</b>", tbl_cell_bold),
            Paragraph("Prisma ORM 5, PostgreSQL 16+", tbl_cell),
            Paragraph("Relational schema management with forward-only migrations, type-safe transactions, unique constraints, and foreign key cascades.", tbl_cell)
        ],
        [
            Paragraph("<b>Cryptographic & Messaging Layer</b>", tbl_cell_bold),
            Paragraph("Node.js Crypto (scrypt, HMAC-SHA256, CSPRNG), Nodemailer SMTP", tbl_cell),
            Paragraph("Issues rejection-sampled 6-digit OTPs, hashes secrets with salts and peppers, stores SHA-256 session tokens, and sends transactional verification emails.", tbl_cell)
        ],
    ]
    arch_tbl = Table(arch_flow_data, colWidths=[95, 175, 252])
    arch_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_PRIMARY),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER),
        ('INNERGRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, C_CARD_BG]),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(arch_tbl)

    story.append(section_divider())

    # =========================================================================
    # SECTION 2: WHAT THINGS HAVE BEEN USED FOR WHAT? (FULL TECH STACK)
    # =========================================================================
    story.append(Paragraph("2. What Things Have Been Used For What? (Technology Stack Breakdown)", h1))
    story.append(HRFlowable(width="100%", thickness=1.5, color=C_BRAND, spaceBefore=2, spaceAfter=10))

    story.append(Paragraph(
        "Every single package, library, and framework in CAMPUSLINK has been deliberately selected to fulfill a precise "
        "architectural need without introducing bloat or black-box dependencies. Below is the comprehensive audit "
        "of all technologies utilized across the backend and frontend codebases.",
        body_justify
    ))
    story.append(Spacer(1, 8))

    story.append(Paragraph("2.1 Backend Technologies & Runtime Dependencies", h2))

    backend_tech_data = [
        [Paragraph("<b>PACKAGE / TOOL</b>", tbl_head), Paragraph("<b>VERSION</b>", tbl_head), Paragraph("<b>EXACT ROLE IN CAMPUSLINK</b>", tbl_head), Paragraph("<b>WHY IT WAS CHOSEN</b>", tbl_head)],
        [
            Paragraph("<b>Express</b>", tbl_cell_bold),
            Paragraph("4.21.2", tbl_cell_code),
            Paragraph("HTTP REST API web server. Powers all API routes (`/api/auth`, `/api/students`, `/api/opportunities`, etc.), JSON body parsing, and middleware chains.", tbl_cell),
            Paragraph("Lightweight, battle-tested, unopinionated, and provides robust control over request pipelines, cookies, and error filters.", tbl_cell)
        ],
        [
            Paragraph("<b>TypeScript</b>", tbl_cell_bold),
            Paragraph("5.6.3", tbl_cell_code),
            Paragraph("Static type system across the entire backend. Defines strict interfaces for matching inputs, API response contracts, DB queries, and middleware signatures.", tbl_cell),
            Paragraph("Eliminates runtime type errors, guarantees end-to-end data integrity, and synchronizes perfectly with Prisma-generated types.", tbl_cell)
        ],
        [
            Paragraph("<b>Prisma ORM</b><br/>(`@prisma/client`)", tbl_cell_bold),
            Paragraph("5.22.0", tbl_cell_code),
            Paragraph("Data access layer, schema definition (`schema.prisma`), forward-only migration engine, and multi-table atomic transaction manager (`prisma.$transaction`).", tbl_cell),
            Paragraph("Provides compile-time type-safe database queries, auto-generated TypeScript models, transparent relation joining, and declarative migrations.", tbl_cell)
        ],
        [
            Paragraph("<b>PostgreSQL</b>", tbl_cell_bold),
            Paragraph("16+", tbl_cell_code),
            Paragraph("Primary relational database storing users, sessions, student profiles, skills, project evidence, jobs, applications, sprint attempts, and announcements.", tbl_cell),
            Paragraph("Enterprise ACID compliance, robust indexing (B-trees on foreign keys and emails), JSON column querying for hiring criteria, and relational cascade integrity.", tbl_cell)
        ],
        [
            Paragraph("<b>Zod</b>", tbl_cell_bold),
            Paragraph("3.23.8", tbl_cell_code),
            Paragraph("Runtime payload validation and parsing. Enforces strict request schemas (`.strict()`) on registration, job creation, skill updates, and reviews.", tbl_cell),
            Paragraph("Strips or rejects unauthorized client fields, preventing parameter pollution and role escalation (e.g. students attempting to pass `role: 'ADMIN'`).", tbl_cell)
        ],
        [
            Paragraph("<b>scrypt (Node crypto)</b>", tbl_cell_bold),
            Paragraph("Built-in", tbl_cell_code),
            Paragraph("Cryptographic password hashing algorithm for user authentication. Formats hashes as `scrypt$v1$N=16384$r=8$p=1$&lt;salt&gt;$&lt;hash&gt;`.", tbl_cell),
            Paragraph("Memory-hard key derivation function specifically designed to resist hardware-accelerated GPU, ASIC, and brute-force cracking attacks.", tbl_cell)
        ],
        [
            Paragraph("<b>HMAC-SHA256 & CSPRNG</b>", tbl_cell_bold),
            Paragraph("Built-in", tbl_cell_code),
            Paragraph("Generates uniform 6-digit OTPs via `randomInt(0, 1000000)` and hashes them with an application pepper before storing in `RegistrationAttempt`.", tbl_cell),
            Paragraph("Eliminates modulo bias in random number generation. Even if the database is leaked, raw OTP codes cannot be brute-forced without the server pepper.", tbl_cell)
        ],
        [
            Paragraph("<b>Nodemailer</b>", tbl_cell_bold),
            Paragraph("10.1.0", tbl_cell_code),
            Paragraph("SMTP mail client used in the student registration workflow (`POST /api/auth/register/start`) to deliver live 6-digit verification codes to applicant inboxes.", tbl_cell),
            Paragraph("Reliable standard for Node.js email transport with direct TLS/SSL support, app-password authentication, and fail-safe error handling.", tbl_cell)
        ],
        [
            Paragraph("<b>Helmet</b>", tbl_cell_bold),
            Paragraph("8.0.0", tbl_cell_code),
            Paragraph("Sets critical HTTP security response headers (`X-Content-Type-Options`, `X-Frame-Options`, `Strict-Transport-Security`, `X-DNS-Prefetch-Control`).", tbl_cell),
            Paragraph("Mitigates common web vulnerabilities like cross-site scripting (XSS), clickjacking, and MIME-sniffing attacks.", tbl_cell)
        ],
        [
            Paragraph("<b>CORS</b>", tbl_cell_bold),
            Paragraph("2.8.5", tbl_cell_code),
            Paragraph("Restricts cross-origin resource sharing strictly to the configured loopback origin (`http://127.0.0.1:5173`) with explicit credential support.", tbl_cell),
            Paragraph("Dynamic function evaluation ensures unauthorized origins receive zero Access-Control-Allow-Origin headers, blocking external browser reads.", tbl_cell)
        ],
        [
            Paragraph("<b>Express-Rate-Limit</b>", tbl_cell_bold),
            Paragraph("7.4.1", tbl_cell_code),
            Paragraph("IP-based rate-limiting middleware enforcing strict request budgets: Global (300/15m), Login (20/15m), Register Start (20/15m), OTP Verify (60/15m).", tbl_cell),
            Paragraph("Prevents Denial of Service (DoS), automated OTP enumeration, brute-force password guessing, and registration flooding.", tbl_cell)
        ],
        [
            Paragraph("<b>tsx</b>", tbl_cell_bold),
            Paragraph("4.19.2", tbl_cell_code),
            Paragraph("Development runtime executing TypeScript directly via esbuild (`tsx watch src/index.ts`, `tsx prisma/seed.ts`).", tbl_cell),
            Paragraph("Instant startup, high-speed execution, seamless TypeScript module resolution, and file watching without manual compilation steps.", tbl_cell)
        ],
        [
            Paragraph("<b>Vitest</b>", tbl_cell_bold),
            Paragraph("2.1.8", tbl_cell_code),
            Paragraph("Automated test runner executing comprehensive integration tests for auth, CSRF, matching algorithms, rubrics, and application workflows.", tbl_cell),
            Paragraph("Blazing fast execution, full ESM/TypeScript support, and complete compatibility with standard test assertions.", tbl_cell)
        ],
    ]
    backend_tbl = Table(backend_tech_data, colWidths=[80, 48, 215, 179])
    backend_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_PRIMARY),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER),
        ('INNERGRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, C_CARD_BG]),
        ('TOPPADDING', (0,0), (-1,-1), 4.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4.5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(backend_tbl)

    story.append(Spacer(1, 10))
    story.append(Paragraph("2.2 Frontend Technologies & Client Dependencies", h2))

    frontend_tech_data = [
        [Paragraph("<b>PACKAGE / TOOL</b>", tbl_head), Paragraph("<b>VERSION</b>", tbl_head), Paragraph("<b>EXACT ROLE IN CAMPUSLINK</b>", tbl_head), Paragraph("<b>WHY IT WAS CHOSEN</b>", tbl_head)],
        [
            Paragraph("<b>React</b>", tbl_cell_bold),
            Paragraph("19.2.8", tbl_cell_code),
            Paragraph("Core declarative UI component library powering all workspaces, reactive forms, interactive modals, and data dashboards.", tbl_cell),
            Paragraph("Component-based architecture, highly efficient reconciliation, robust hook primitives (`useState`, `useEffect`, `useContext`), and state isolation.", tbl_cell)
        ],
        [
            Paragraph("<b>Vite</b>", tbl_cell_bold),
            Paragraph("8.3.0", tbl_cell_code),
            Paragraph("Next-generation frontend dev server and production bundler configured with `strictPort: true` on loopback `127.0.0.1:5173`.", tbl_cell),
            Paragraph("Sub-second Hot Module Replacement (HMR), lightning-fast esbuild pre-bundling, optimized Rollup production builds, and strict port guarding.", tbl_cell)
        ],
        [
            Paragraph("<b>React Router</b><br/>(`react-router-dom`)", tbl_cell_bold),
            Paragraph("7.18.4", tbl_cell_code),
            Paragraph("Client-side Single Page Application (SPA) routing. Manages public routes (`/`, `/login`, `/register`) and protected routes wrapped in `WorkspaceLayout`.", tbl_cell),
            Paragraph("Clean declarative URL mapping, seamless navigation without full page reloads, query string management, and integration with authentication redirect gates.", tbl_cell)
        ],
        [
            Paragraph("<b>TanStack Query</b><br/>(`@tanstack/react-query`)", tbl_cell_bold),
            Paragraph("5.104.1", tbl_cell_code),
            Paragraph("Server-state management, asynchronous data fetching, client-side caching (`staleTime: 15s`), and automatic cache invalidation on mutations.", tbl_cell),
            Paragraph("Eliminates manual `useEffect` fetch boilerplate, manages loading/error states automatically, prevents duplicate network calls, and synchronizes server state.", tbl_cell)
        ],
        [
            Paragraph("<b>Tailwind CSS v4</b><br/>(`@tailwindcss/vite`)", tbl_cell_bold),
            Paragraph("4.3.3", tbl_cell_code),
            Paragraph("Utility-first styling framework with custom design tokens (`--color-signal`, `--color-ink`, `--color-brand`), glassmorphism effects, and responsive grids.", tbl_cell),
            Paragraph("Next-generation zero-config Vite integration, instant CSS generation, design token consistency, and clean modern dark-mode aesthetic.", tbl_cell)
        ],
        [
            Paragraph("<b>Lucide React</b>", tbl_cell_bold),
            Paragraph("1.55.0", tbl_cell_code),
            Paragraph("Modern, lightweight SVG icon system utilized across navigation bars, metric indicators, status badges, and action buttons.", tbl_cell),
            Paragraph("Clean aesthetic consistency, zero external font downloads, tree-shakeable SVG components, and customizable dimensions and strokes.", tbl_cell)
        ],
        [
            Paragraph("<b>Oxlint</b>", tbl_cell_bold),
            Paragraph("1.81.0", tbl_cell_code),
            Paragraph("High-performance Rust-based linter used to verify code quality, syntax standards, and React best practices during builds.", tbl_cell),
            Paragraph("Executes 50-100x faster than traditional ESLint, catching bugs, bad imports, and type inconsistencies in milliseconds.", tbl_cell)
        ],
    ]
    frontend_tbl = Table(frontend_tech_data, colWidths=[80, 48, 215, 179])
    frontend_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_PRIMARY),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER),
        ('INNERGRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, C_CARD_BG]),
        ('TOPPADDING', (0,0), (-1,-1), 4.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4.5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(frontend_tbl)

    story.append(Spacer(1, 10))
    story.append(Paragraph("2.3 Project Directory & File Manifest", h2))

    manifest_data = [
        [Paragraph("<b>FILE OR DIRECTORY</b>", tbl_head), Paragraph("<b>PRIMARY ARCHITECTURAL ROLE & FUNCTION</b>", tbl_head)],
        [Paragraph("`backend/src/app.ts`", tbl_cell_code), Paragraph("Express application factory. Configures Helmet, strict loopback CORS, JSON limits, CSRF origin checks, rate-limiters, and mounts all API routers.", tbl_cell)],
        [Paragraph("`backend/src/index.ts`", tbl_cell_code), Paragraph("Server entrypoint. Binds Express strictly to `127.0.0.1:4000`, wires graceful shutdown handlers (`SIGTERM`, `SIGINT`), and disconnects Prisma cleanly.", tbl_cell)],
        [Paragraph("`backend/src/lib/auth.ts`", tbl_cell_code), Paragraph("Authentication middleware. Defines `requireAuth`, `requireRole`, cookie serialization/clearing, and request user context population.", tbl_cell)],
        [Paragraph("`backend/src/lib/otp.ts`", tbl_cell_code), Paragraph("CSPRNG one-time code generator (`randomInt`), peppered HMAC-SHA256 hasher, and constant-time string comparison (`timingSafeEqual`).", tbl_cell)],
        [Paragraph("`backend/src/lib/match.ts`", tbl_cell_code), Paragraph("Explainable opportunity matching engine. Computes fit score, met requirements, gaps, bonuses, and step-by-step guidance without AI.", tbl_cell)],
        [Paragraph("`backend/src/lib/rubric.ts`", tbl_cell_code), Paragraph("Deterministic Sprint grading engine (`rubric-v1`). Scores repository link, completion, write-up depth, and engineering tradeoffs.", tbl_cell)],
        [Paragraph("`backend/src/lib/arena.ts`", tbl_cell_code), Paragraph("Interview Arena practice evaluator (`arena-bank-v1`). Grades STAR structure, substance, quantification, and assigns practice points.", tbl_cell)],
        [Paragraph("`backend/src/lib/sprint-evidence.ts`", tbl_cell_code), Paragraph("Transactional evidence upsert utility. Reuses existing project rows for repeated passing attempts to prevent duplicate evidence inflation.", tbl_cell)],
        [Paragraph("`backend/src/routes/register.ts`", tbl_cell_code), Paragraph("Public student onboarding endpoints: Step 1 (`/register/start`) emails code; Step 2 (`/register/verify`) verifies OTP; Step 3 (`/register/complete`) creates account.", tbl_cell)],
        [Paragraph("`frontend/src/main.tsx`", tbl_cell_code), Paragraph("React entrypoint and router configuration. Maps public landing page, login, register, and protected workspace routes inside `WorkspaceLayout`.", tbl_cell)],
        [Paragraph("`frontend/src/store/session.tsx`", tbl_cell_code), Paragraph("IdentityGate context provider. Probes `GET /api/auth/me`, handles 401 redirects to `/login`, and supplies user role and profile ID globally.", tbl_cell)],
        [Paragraph("`frontend/src/pages/CareerTwin.tsx`", tbl_cell_code), Paragraph("Student profile and skill management UI. Visualizes self-reported vs evidenced skills, project links, and personal academic details.", tbl_cell)],
        [Paragraph("`frontend/src/pages/OpportunityMirror.tsx`", tbl_cell_code), Paragraph("Interactive job matching dashboard. Displays transparent fit percentages, met criteria, missing gaps, and one-click application submission.", tbl_cell)],
        [Paragraph("`frontend/src/pages/SkillSprint.tsx`", tbl_cell_code), Paragraph("Practical technical assessment challenge UI. Provides task checklist, repo submission inputs, and displays real-time rubric feedback.", tbl_cell)],
        [Paragraph("`frontend/src/pages/InterviewArena.tsx`", tbl_cell_code), Paragraph("Mock interview practice room. Simulates Behavioral, Technical, and Situational questions with instant rule-based scoring feedback.", tbl_cell)],
        [Paragraph("`frontend/src/pages/PlacementTower.tsx`", tbl_cell_code), Paragraph("Placement officer analytics dashboard. Displays student cohort readiness, application pipeline metrics, and the interactive What-If Lab.", tbl_cell)],
        [Paragraph("`frontend/src/pages/Passport.tsx`", tbl_cell_code), Paragraph("Verifiable student credential passport. Displays skill provenance, linked project proofs, rubric evaluations, and holistic readiness score.", tbl_cell)],
    ]
    manifest_tbl = Table(manifest_data, colWidths=[160, 362])
    manifest_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_PRIMARY),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER),
        ('INNERGRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, C_CARD_BG]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(manifest_tbl)

    story.append(section_divider())

    # =========================================================================
    # SECTION 3: HOW THINGS WORK (CORE SUBSYSTEMS & MECHANICS)
    # =========================================================================
    story.append(Paragraph("3. How Things Work: Deep Technical Mechanics & Workflows", h1))
    story.append(HRFlowable(width="100%", thickness=1.5, color=C_BRAND, spaceBefore=2, spaceAfter=10))

    story.append(Paragraph(
        "This section deconstructs the operational workflows of CAMPUSLINK step by step, illustrating the exact sequence "
        "of events, database mutations, mathematical formulas, and security checks governing every feature.",
        body_justify
    ))
    story.append(Spacer(1, 6))

    # --- 3.1 Authentication & Registration ---
    story.append(Paragraph("3.1 Public Student Onboarding & Session Security", h2))
    story.append(Paragraph(
        "Student registration is public and self-service, but fortified with an uncompromising 3-step email verification protocol. "
        "Crucially, <b>no User or StudentProfile record is created until the student's email address is cryptographically proven</b>.",
        body_justify
    ))
    story.append(Spacer(1, 4))

    onboarding_steps = [
        ("Step 1: Initiation (`POST /api/auth/register/start`)", 
         "The student enters their Full Name, 8-character Enrollment Number (e.g., `21BFH987`), Branch, Graduation Year, College, and Email. "
         "The server strictly validates all inputs with Zod, checks that neither the email nor enrollment number already exists in `User` or `RegistrationAttempt`, "
         "generates an un-biased 6-digit OTP using `crypto.randomInt()`, hashes it with HMAC-SHA256 using an application pepper, persists a `RegistrationAttempt` record, "
         "and dispatches the code via Nodemailer SMTP. A 60-second resend cooldown and 10-minute expiry are enforced."),
        
        ("Step 2: Verification (`POST /api/auth/register/verify`)", 
         "The student inputs the 6-digit code. The server performs a constant-time comparison (`timingSafeEqual`) against the stored HMAC hash. "
         "If correct, the OTP hash is immediately cleared (single-use), `verifiedAt` is recorded, and a high-entropy 256-bit `completionToken` "
         "valid for 20 minutes is returned in memory. If incorrect, an attempt counter increments (capped at 5 wrong attempts before permanent invalidation)."),
        
        ("Step 3: Completion (`POST /api/auth/register/complete`)", 
         "The student submits their chosen password along with the `completionToken`. The password must satisfy the security policy (12–256 chars, letter + number). "
         "In a single atomic database transaction, the server: (a) verifies the completion token hash, (b) marks the attempt as consumed, "
         "(c) hashes the password with scrypt, (d) creates the `User` row with role forced to `STUDENT`, (e) creates the linked `StudentProfile` copying verified data from the attempt row, "
         "and (f) generates a 7-day session token, setting the `campuslink_session` HttpOnly cookie. The user is logged in immediately.")
    ]

    for title_s, desc_s in onboarding_steps:
        story.append(Paragraph(f"<b>{title_s}</b>", h3))
        story.append(Paragraph(desc_s, body_justify))
        story.append(Spacer(1, 3))

    story.append(Spacer(1, 4))

    session_callout = make_callout(
        "SESSION SECURITY ARCHITECTURE: HASH-ONLY SERVER STORAGE",
        "Raw session tokens exist solely inside the client's HttpOnly cookie (`SameSite=Lax`, `Max-Age=7d`). "
        "The database stores exclusively `SHA-256(token)` inside the `Session` table. In the event of a database compromise, "
        "attackers cannot forge or hijack active user sessions. Revoking a session (`POST /api/auth/logout`) sets `revokedAt = now()`, "
        "instantly neutralizing the cookie across all subsequent requests.",
        accent_color=C_BRAND,
        bg_color=colors.HexColor("#EFF6FF")
    )
    story.append(session_callout)

    story.append(Spacer(1, 10))

    # --- 3.2 Career Twin & Provenance ---
    story.append(Paragraph("3.2 Career Twin & Provenance-Based Credentialing", h2))
    story.append(Paragraph(
        "The Career Twin (`/twin`) acts as the student's living digital resume and skill inventory. "
        "Unlike standard job boards where candidates claim 'expert' status with zero proof, CAMPUSLINK institutes "
        "strict provenance tracking across 4 standardized proficiency tiers:",
        body_justify
    ))
    story.append(Spacer(1, 4))

    levels_data = [
        [Paragraph("<b>LEVEL</b>", tbl_head), Paragraph("<b>RANK</b>", tbl_head), Paragraph("<b>PROVENANCE & MEANING</b>", tbl_head), Paragraph("<b>EVIDENCE CRITERIA</b>", tbl_head)],
        [Paragraph("<b>BEGINNER</b>", tbl_cell_bold), Paragraph("1", tbl_cell_code), Paragraph("Foundational theoretical understanding; basic familiarity with syntax and concepts.", tbl_cell), Paragraph("Self-reported claim; awarded automatically when adding skills or unevidenced projects.", tbl_cell)],
        [Paragraph("<b>INTERMEDIATE</b>", tbl_cell_bold), Paragraph("2", tbl_cell_code), Paragraph("Working operational competence; able to build features independently.", tbl_cell), Paragraph("Requires either linked project evidence or scoring 70+ on a beginner Sprint assessment.", tbl_cell)],
        [Paragraph("<b>ADVANCED</b>", tbl_cell_bold), Paragraph("3", tbl_cell_code), Paragraph("In-depth architectural capability; understands tradeoffs, performance, and internal patterns.", tbl_cell), Paragraph("Earned by passing complex Sprint assessments and linking multi-skill repositories.", tbl_cell)],
        [Paragraph("<b>EXPERT</b>", tbl_cell_bold), Paragraph("4", tbl_cell_code), Paragraph("Mastery; capable of debugging framework internals, designing systems, and leading architecture.", tbl_cell), Paragraph("Highest echelon; reserved for verified multi-sprint achievements and verified code reviews.", tbl_cell)],
    ]
    levels_tbl = Table(levels_data, colWidths=[80, 45, 230, 167])
    levels_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_PRIMARY),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER),
        ('INNERGRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, C_CARD_BG]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(levels_tbl)

    story.append(Spacer(1, 10))

    # --- 3.3 Opportunity Mirror & Matching ---
    story.append(Paragraph("3.3 Opportunity Mirror: Explainable Matching Engine", h2))
    story.append(Paragraph(
        "The Opportunity Mirror (`/mirror`) compares a student's verified skills against open corporate job criteria. "
        "Instead of delivering an opaque match percentage from a machine learning black-box, the match score is derived "
        "from a deterministic, published mathematical algorithm (`MATCH_METHOD`).",
        body_justify
    ))
    story.append(Spacer(1, 6))

    matching_formula_box = make_formula_box(
        "OPPORTUNITY MATCHING ALGORITHM (lib/match.ts)",
        "Weight = Rank(minLevel) x 2<br/>"
        "Points = FullWeight + min(linkedProjects, 2) x 0.5  [if student level >= minLevel]<br/>"
        "Points = Weight x 0.75                              [if student level == minLevel - 1 (Partial Credit)]<br/>"
        "Points = 0                                          [if student level &lt; minLevel - 1]<br/>"
        "Bonus  = +1 point                                   [for each nice-to-have skill at INTERMEDIATE+]<br/>"
        "Score  = min(100, round(100 x (Points_Earned / Max_Possible_Points)))",
        "Every job posting specifies requiredSkills with minimum levels and niceToHave skills. "
        "The response explicitly returns the formula method, met criteria, exact skill gaps, bonus points earned, "
        "and a tailored nextStep recommendation (e.g. 'Close React gap with a targeted sprint to lift this match')."
    )
    story.append(matching_formula_box)

    story.append(Spacer(1, 10))

    # --- 3.4 Skill Sprint & Rubric ---
    story.append(Paragraph("3.4 Skill Sprint & Transparent Rubric Evaluation", h2))
    story.append(Paragraph(
        "Skill Sprints (`/sprint`) provide hands-on coding and architecture challenges tied to specific target skills. "
        "When a student submits their solution (checklist tasks completed, Git repository URL, and engineering write-up), "
        "the backend evaluates the submission against a strict rule-based rubric (`rubric-v1`).",
        body_justify
    ))
    story.append(Spacer(1, 6))

    rubric_formula_box = make_formula_box(
        "SPRINT GRADING RUBRIC v1 (lib/rubric.ts)",
        "Score = 40 (Base Points)<br/>"
        "      + 25 (if all checklist tasks attested)<br/>"
        "      + 15 (if valid verifiable HTTP/HTTPS repo or deployment link provided)<br/>"
        "      + 15 (if write-up depth >= 40 words explaining tradeoffs; +8 if >= 15 words)<br/>"
        "      +  5 (bonus: if write-up explicitly names quality attributes: tests, a11y, perf, tradeoffs)<br/>"
        "Total Cap: 100 points  |  Promotion Threshold: 70 points",
        "When a submission achieves a score of 70 or higher, the backend automatically performs a dual transactional promotion: "
        "(1) The rewarded skill is upgraded one level in StudentSkill, and (2) An evidence project named 'Sprint: &lt;Title&gt;' "
        "is upserted in the Project table, establishing permanent verifiable proof."
    )
    story.append(rubric_formula_box)

    story.append(Spacer(1, 10))

    # --- 3.5 Interview Arena ---
    story.append(Paragraph("3.5 Interview Arena & Practice Points Ledger", h2))
    story.append(Paragraph(
        "The Interview Arena (`/arena`) prepares students for rigorous placement interviews across three core categories: "
        "<b>Behavioral</b> (leadership, conflict resolution), <b>Technical</b> (rendering, concurrency, algorithms), "
        "and <b>Situational</b> (deadline triage, stakeholder pressure).",
        body_justify
    ))
    story.append(Spacer(1, 4))

    arena_formula_box = make_formula_box(
        "ARENA ANSWER SCORING & POINTS LEDGER (lib/arena.ts)",
        "Score = 35 (Base Points)<br/>"
        "      + 30 (Substantive depth: >= 80 words; +18 if >= 40 words)<br/>"
        "      + 15 (Quantification: contains explicit numerical metric or impact data)<br/>"
        "      + 10 (Reasoning keywords: 'because', 'tradeoff', 'therefore', 'however')<br/>"
        "      + 10 (STAR structure keywords: 'situation', 'task', 'action', 'result')<br/>"
        "Practice Points = floor(Session_Score / 10)  [Range: 0 to 10 points]",
        "Practice points are recorded in a dedicated ArenaPointLedger table keyed uniquely by sessionId. "
        "If a student re-evaluates or edits their answer, the ledger row updates in-place, mathematically preventing "
        "point duplication or gaming."
    )
    story.append(arena_formula_box)

    story.append(Spacer(1, 10))

    # --- 3.6 Application Lifecycle ---
    story.append(Paragraph("3.6 Application Lifecycle & State Machine Transitions", h2))
    story.append(Paragraph(
        "Job applications follow a strictly guarded Finite State Machine (FSM). "
        "Transition permissions are strictly enforced based on the actor's session role to prevent unauthorized status tampering.",
        body_justify
    ))
    story.append(Spacer(1, 4))

    fsm_data = [
        [Paragraph("<b>CURRENT STATUS</b>", tbl_head), Paragraph("<b>PERMITTED NEXT STATUS</b>", tbl_head), Paragraph("<b>AUTHORIZED ROLES</b>", tbl_head), Paragraph("<b>BUSINESS RULES & BEHAVIOR</b>", tbl_head)],
        [
            Paragraph("<b>APPLIED</b>", tbl_cell_bold),
            Paragraph("SHORTLISTED, REJECTED, WITHDRAWN", tbl_cell),
            Paragraph("Student (WITHDRAWN only); Recruiter & Staff (SHORTLISTED, REJECTED)", tbl_cell),
            Paragraph("Initial state upon student application. Unique constraint on (jobId, studentProfileId) prevents duplicate submissions.", tbl_cell)
        ],
        [
            Paragraph("<b>SHORTLISTED</b>", tbl_cell_bold),
            Paragraph("HIRED, REJECTED, WITHDRAWN", tbl_cell),
            Paragraph("Placement Staff only (HIRED); Recruiter & Staff (REJECTED); Student (WITHDRAWN)", tbl_cell),
            Paragraph("Candidate has cleared preliminary screening. Recruiters can only shortlist for their own company's jobs.", tbl_cell)
        ],
        [
            Paragraph("<b>REJECTED</b>", tbl_cell_bold),
            Paragraph("<i>None (Terminal)</i>", tbl_cell_code),
            Paragraph("N/A", tbl_cell),
            Paragraph("Terminal state. Application cannot transition backward to APPLIED or SHORTLISTED.", tbl_cell)
        ],
        [
            Paragraph("<b>HIRED</b>", tbl_cell_bold),
            Paragraph("<i>None (Terminal)</i>", tbl_cell_code),
            Paragraph("N/A", tbl_cell),
            Paragraph("Terminal state. Only Placement Officers (STAFF/ADMIN) can confirm an application as HIRED.", tbl_cell)
        ],
        [
            Paragraph("<b>WITHDRAWN</b>", tbl_cell_bold),
            Paragraph("<i>None (Terminal)</i>", tbl_cell_code),
            Paragraph("N/A", tbl_cell),
            Paragraph("Terminal state. Student initiated withdrawal from consideration.", tbl_cell)
        ],
    ]
    fsm_tbl = Table(fsm_data, colWidths=[90, 135, 135, 162])
    fsm_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_PRIMARY),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER),
        ('INNERGRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, C_CARD_BG]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(fsm_tbl)

    story.append(Spacer(1, 10))

    # --- 3.7 Placement Tower & Analytics ---
    story.append(Paragraph("3.7 Placement Tower, Cohort Analytics & What-If Lab", h2))
    story.append(Paragraph(
        "The Placement Tower (`/tower`) provides placement officers with macro-level cohort intelligence. "
        "It features live stats: registered students, active jobs, pipeline stage counts, and cohort readiness. "
        "It also incorporates the <b>What-If Lab</b>: a client-side simulation engine that models how targeted cohort interventions "
        "(e.g., closing 2 skill gaps per student or running targeted sprints) will mathematically impact hiring readiness percentages.",
        body_justify
    ))
    story.append(Spacer(1, 6))

    readiness_box = make_formula_box(
        "HOLISTIC STUDENT READINESS SCORE (lib/match.ts & /passport)",
        "Readiness Score = Proficiency_Factor (50%) + Evidence_Coverage (30%) + Activity_Momentum (20%)<br/>"
        "Proficiency     = (Mean_Skill_Rank / 4.0) x 50<br/>"
        "Evidence        = (Count_of_Evidenced_Skills / Total_Skills_Count) x 30<br/>"
        "Momentum        = min(20, (Applications_Filed x 4) + (Evaluated_Sprints x 6))<br/>"
        "Total Scale: 0 to 100",
        "A student with 10 claimed skills but zero linked projects or sprints will receive zero points from the evidence pillar. "
        "The formula directly incentivizes practical code verification and proactive application engagement."
    )
    story.append(readiness_box)

    story.append(Spacer(1, 10))

    # --- 3.8 Announcements & Materialized Delivery ---
    story.append(Paragraph("3.8 Targeted Announcements & Materialized Delivery Pattern", h2))
    story.append(Paragraph(
        "When placement officers publish announcements (`POST /api/announcements`), the backend resolves the target audience "
        "(ALL, APPLIED, SHORTLISTED, INTERVIEW_SELECTED) and executes the <b>Materialized Recipient Pattern</b>:",
        body_justify
    ))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "Instead of querying student states dynamically on every page load, the system resolves the matching students at publication time "
        "and creates permanent `AnnouncementRecipient` records in a single database transaction. This guarantees that: "
        "(1) The audience snapshot is permanently frozen as of broadcast time, (2) Students who register or change status later "
        "do not receive historical notices meant for past cohorts, and (3) Read receipts (`readAt`) are tracked individually per student.",
        body_justify
    ))

    story.append(section_divider())

    # =========================================================================
    # SECTION 4: DATABASE ARCHITECTURE & ENTITY RELATIONSHIPS
    # =========================================================================
    story.append(Paragraph("4. Database Architecture & Relational Data Models", h1))
    story.append(HRFlowable(width="100%", thickness=1.5, color=C_BRAND, spaceBefore=2, spaceAfter=10))

    story.append(Paragraph(
        "CAMPUSLINK utilizes PostgreSQL managed via Prisma ORM. The relational schema is structured into "
        "distinct functional domains: Identity & Sessions, Skills & Evidence, Recruitment & Jobs, Assessments, and Messaging.",
        body_justify
    ))
    story.append(Spacer(1, 8))

    schema_models_data = [
        [Paragraph("<b>DOMAIN & MODEL</b>", tbl_head), Paragraph("<b>PRIMARY ATTRIBUTES & FIELDS</b>", tbl_head), Paragraph("<b>FOREIGN KEYS & RELATIONS</b>", tbl_head), Paragraph("<b>CONSTRAINTS & INDEXES</b>", tbl_head)],
        [
            Paragraph("<b>Identity</b><br/>`User`", tbl_cell_bold),
            Paragraph("id (cuid), email, passwordHash, role (STUDENT, STAFF, RECRUITER, ADMIN), isActive, companyId", tbl_cell),
            Paragraph("1:1 StudentProfile, 1:N Session, 1:N Announcement, N:1 Company", tbl_cell),
            Paragraph("@unique(email), @@index([role]), @@index([companyId])", tbl_cell_code)
        ],
        [
            Paragraph("<b>Security</b><br/>`Session`", tbl_cell_bold),
            Paragraph("id, tokenHash, userId, expiresAt, revokedAt, userAgent, ip", tbl_cell),
            Paragraph("N:1 User (onDelete: Cascade)", tbl_cell),
            Paragraph("@unique(tokenHash), @@index([userId]), @@index([expiresAt])", tbl_cell_code)
        ],
        [
            Paragraph("<b>Onboarding</b><br/>`RegistrationAttempt`", tbl_cell_bold),
            Paragraph("id, email, activeEmail, fullName, enrollmentNo, branch, graduationYear, otpHash, completionTokenHash", tbl_cell),
            Paragraph("Self-contained signup workflow", tbl_cell),
            Paragraph("@unique(activeEmail), @@index([email]), @@index([consumedAt])", tbl_cell_code)
        ],
        [
            Paragraph("<b>Profile</b><br/>`StudentProfile`", tbl_cell_bold),
            Paragraph("id, userId, fullName, enrollmentNo, branch, graduationYear, cgpa, resumeUrl, institution", tbl_cell),
            Paragraph("1:1 User, 1:N StudentSkill, 1:N Project, 1:N Application, 1:N Attempt", tbl_cell),
            Paragraph("@unique(userId), @unique(enrollmentNo), @@index([graduationYear])", tbl_cell_code)
        ],
        [
            Paragraph("<b>Skills</b><br/>`StudentSkill`", tbl_cell_bold),
            Paragraph("id, studentProfileId, skillId, level (BEGINNER, INTERMEDIATE, ADVANCED, EXPERT)", tbl_cell),
            Paragraph("N:1 StudentProfile, N:1 Skill", tbl_cell),
            Paragraph("@@unique([studentProfileId, skillId]), @@index([skillId])", tbl_cell_code)
        ],
        [
            Paragraph("<b>Evidence</b><br/>`Project`", tbl_cell_bold),
            Paragraph("id, studentProfileId, title, description, url, skills (String[]), assessmentId", tbl_cell),
            Paragraph("N:1 StudentProfile (onDelete: Cascade)", tbl_cell),
            Paragraph("@@index([studentProfileId]), @@index([studentProfileId, assessmentId])", tbl_cell_code)
        ],
        [
            Paragraph("<b>Corporate</b><br/>`Company`", tbl_cell_bold),
            Paragraph("id, name, website, industry, createdAt", tbl_cell),
            Paragraph("1:N JobOpportunity, 1:N User", tbl_cell),
            Paragraph("@unique(name)", tbl_cell_code)
        ],
        [
            Paragraph("<b>Hiring</b><br/>`JobOpportunity`", tbl_cell_bold),
            Paragraph("id, companyId, title, description, location, type, status, requiredSkills (Json), niceToHave (String[])", tbl_cell),
            Paragraph("N:1 Company (onDelete: Cascade), 1:N Application", tbl_cell),
            Paragraph("@@index([companyId]), @@index([status]), @@index([type])", tbl_cell_code)
        ],
        [
            Paragraph("<b>Funnel</b><br/>`Application`", tbl_cell_bold),
            Paragraph("id, jobId, studentProfileId, status (APPLIED, SHORTLISTED, REJECTED, HIRED, WITHDRAWN)", tbl_cell),
            Paragraph("N:1 JobOpportunity, N:1 StudentProfile", tbl_cell),
            Paragraph("@@unique([jobId, studentProfileId]), @@index([status])", tbl_cell_code)
        ],
        [
            Paragraph("<b>Assessments</b><br/>`AssessmentAttempt`", tbl_cell_bold),
            Paragraph("id, assessmentId, studentProfileId, score, status, repoUrl, note, feedback, startedAt, submittedAt", tbl_cell),
            Paragraph("N:1 Assessment, N:1 StudentProfile", tbl_cell),
            Paragraph("@@index([assessmentId]), @@index([studentProfileId])", tbl_cell_code)
        ],
        [
            Paragraph("<b>Interview</b><br/>`ArenaPointLedger`", tbl_cell_bold),
            Paragraph("id, studentProfileId, sessionId, points, createdAt", tbl_cell),
            Paragraph("1:1 InterviewSession, N:1 StudentProfile", tbl_cell),
            Paragraph("@unique(sessionId), @@index([studentProfileId])", tbl_cell_code)
        ],
        [
            Paragraph("<b>Messaging</b><br/>`Announcement`", tbl_cell_bold),
            Paragraph("id, title, message, category, audience, isUrgent, authorId, jobId, companyId, eventAt, venue", tbl_cell),
            Paragraph("N:1 User, 1:N AnnouncementRecipient", tbl_cell),
            Paragraph("@@index([authorId]), @@index([jobId]), @@index([createdAt])", tbl_cell_code)
        ],
        [
            Paragraph("<b>Receipts</b><br/>`AnnouncementRecipient`", tbl_cell_bold),
            Paragraph("id, announcementId, studentProfileId, readAt, createdAt", tbl_cell),
            Paragraph("N:1 Announcement (Cascade), N:1 StudentProfile", tbl_cell),
            Paragraph("@@unique([announcementId, studentProfileId])", tbl_cell_code)
        ],
    ]
    schema_tbl = Table(schema_models_data, colWidths=[90, 160, 130, 142])
    schema_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_PRIMARY),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER),
        ('INNERGRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, C_CARD_BG]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(schema_tbl)

    story.append(section_divider())

    # =========================================================================
    # SECTION 5: SECURITY POSTURE & API CONTRACT
    # =========================================================================
    story.append(Paragraph("5. Security Architecture & Defensive Engineering", h1))
    story.append(HRFlowable(width="100%", thickness=1.5, color=C_BRAND, spaceBefore=2, spaceAfter=10))

    story.append(Paragraph(
        "CAMPUSLINK adheres to defense-in-depth principles. Because the application processes student identities, "
        "corporate job postings, and evaluation records, the architecture enforces multi-layered controls:",
        body_justify
    ))
    story.append(Spacer(1, 6))

    security_matrix = [
        ("Network & Binding Isolation", "The backend binds strictly to `127.0.0.1:4000` (IPv4 loopback), and the Vite frontend binds strictly to `127.0.0.1:5173` with `strictPort: true`. Neither binds to wildcard interfaces (`0.0.0.0`), preventing unintended local area network exposure."),
        ("Strict Origin CORS & CSRF Enforcement", "CORS evaluates origins dynamically via a callback, returning zero Access-Control headers to non-whitelisted origins. All mutating requests (POST, PATCH, DELETE) pass through `csrfOriginCheck` verifying the `Origin` or `Referer` header against `CORS_ORIGIN`."),
        ("Server-Side Role-Based Access Control (RBAC)", "Authentication is verified exclusively via session cookies. Client requests carrying foreign `studentProfileId` or `companyId` parameters are disregarded; ownership is derived authoritatively from the validated server session."),
        ("Rate-Limiting Budgets", "Configured via `express-rate-limit`: Global API (300 requests/15 min), Login (20/15 min), Registration Start (20/15 min), and OTP Verification (60/15 min), preventing brute-force attacks and credential stuffing."),
        ("Sanitized Error Handling", "Error middleware intercepts all exceptions. Stack traces, database queries, and credentials are logged solely on the local server console. Client responses return sanitized messages (e.g. `Internal server error`), preventing reconnaissance leaks.")
    ]

    for title_sec, desc_sec in security_matrix:
        story.append(Paragraph(f"• <b>{title_sec}:</b> {desc_sec}", body_justify))
        story.append(Spacer(1, 3))

    story.append(Spacer(1, 6))

    # HTTP Status Contract Table
    status_data = [
        [Paragraph("<b>HTTP CODE</b>", tbl_head), Paragraph("<b>STANDARDIZED MEANING & USAGE IN CAMPUSLINK</b>", tbl_head)],
        [Paragraph("<b>200 OK</b>", tbl_cell_bold), Paragraph("Successful query or state mutation; returns `{ ok: true, data: ... }`.", tbl_cell)],
        [Paragraph("<b>201 Created</b>", tbl_cell_bold), Paragraph("Successful entity creation (e.g. project submitted, application filed, user completed signup).", tbl_cell)],
        [Paragraph("<b>400 Bad Request</b>", tbl_cell_bold), Paragraph("Zod validation failure with specific field path issues, or malformed JSON syntax.", tbl_cell)],
        [Paragraph("<b>401 Unauthorized</b>", tbl_cell_bold), Paragraph("Missing, expired, revoked, or invalid session cookie; account inactive. Routine trigger for login redirect.", tbl_cell)],
        [Paragraph("<b>403 Forbidden</b>", tbl_cell_bold), Paragraph("Authenticated caller lacks permissions (e.g., student attempting recruiter routes, cross-user edit).", tbl_cell)],
        [Paragraph("<b>404 Not Found</b>", tbl_cell_bold), Paragraph("Requested student, job, assessment, application, or prompt does not exist.", tbl_cell)],
        [Paragraph("<b>409 Conflict</b>", tbl_cell_bold), Paragraph("Duplicate record: duplicate email, existing enrollment number, or duplicate job application.", tbl_cell)],
        [Paragraph("<b>410 Gone</b>", tbl_cell_bold), Paragraph("Expired registration OTP code or expired completion token.", tbl_cell)],
        [Paragraph("<b>422 Unprocessable</b>", tbl_cell_bold), Paragraph("Legal request syntax, illegal business state: applying to closed job, invalid FSM transition, empty audience.", tbl_cell)],
        [Paragraph("<b>429 Too Many Requests</b>", tbl_cell_bold), Paragraph("Rate-limit budget exceeded (e.g. >5 incorrect OTP attempts or resend cooldown active).", tbl_cell)],
        [Paragraph("<b>500 Internal Error</b>", tbl_cell_bold), Paragraph("Sanitized server fault; internal details and stack traces logged server-side only.", tbl_cell)],
        [Paragraph("<b>503 Unavailable</b>", tbl_cell_bold), Paragraph("PostgreSQL database unreachable (`/api/ready`) or SMTP mail configuration missing.", tbl_cell)],
    ]
    status_tbl = Table(status_data, colWidths=[100, 422])
    status_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_PRIMARY),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER),
        ('INNERGRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, C_CARD_BG]),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(status_tbl)

    story.append(section_divider())

    # =========================================================================
    # SECTION 6: OPERATIONAL RUNBOOK & DEPLOYMENT GUIDE
    # =========================================================================
    story.append(Paragraph("6. Operational Runbook & Local Setup Guide", h1))
    story.append(HRFlowable(width="100%", thickness=1.5, color=C_BRAND, spaceBefore=2, spaceAfter=10))

    story.append(Paragraph(
        "CAMPUSLINK is architected for immediate local development and deterministic execution on Windows PowerShell.",
        body_justify
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("6.1 Environment Variables Configuration (`backend/.env`)", h2))

    env_data = [
        [Paragraph("<b>VARIABLE</b>", tbl_head), Paragraph("<b>SAMPLE VALUE</b>", tbl_head), Paragraph("<b>PURPOSE & DESCRIPTION</b>", tbl_head)],
        [Paragraph("`DATABASE_URL`", tbl_cell_code), Paragraph("postgresql://postgres:pwd@127.0.0.1:5432/campuslink", tbl_cell_code), Paragraph("PostgreSQL connection string with credentials and database name.", tbl_cell)],
        [Paragraph("`PORT`", tbl_cell_code), Paragraph("4000", tbl_cell_code), Paragraph("Express HTTP server port (Default: 4000).", tbl_cell)],
        [Paragraph("`HOST`", tbl_cell_code), Paragraph("127.0.0.1", tbl_cell_code), Paragraph("Loopback IP interface binding (keep 127.0.0.1 for isolation).", tbl_cell)],
        [Paragraph("`CORS_ORIGIN`", tbl_cell_code), Paragraph("http://127.0.0.1:5173", tbl_cell_code), Paragraph("Permitted client browser origin for CORS and CSRF verification.", tbl_cell)],
        [Paragraph("`SMTP_HOST`", tbl_cell_code), Paragraph("smtp.gmail.com", tbl_cell_code), Paragraph("Outbound SMTP mail server hostname.", tbl_cell)],
        [Paragraph("`SMTP_PORT`", tbl_cell_code), Paragraph("465", tbl_cell_code), Paragraph("SMTP SSL port (465) or TLS port (587).", tbl_cell)],
        [Paragraph("`SMTP_USER`", tbl_cell_code), Paragraph("admissions@college.edu", tbl_cell_code), Paragraph("Authenticated mailbox username / email address.", tbl_cell)],
        [Paragraph("`SMTP_PASS`", tbl_cell_code), Paragraph("16-character-app-password", tbl_cell_code), Paragraph("Google App Password or SMTP account secret (never Git-committed).", tbl_cell)],
        [Paragraph("`MAIL_FROM`", tbl_cell_code), Paragraph("\"CAMPUSLINK\" &lt;admissions@...&gt;", tbl_cell_code), Paragraph("Sender display name and address for verification emails.", tbl_cell)],
        [Paragraph("`OTP_PEPPER`", tbl_cell_code), Paragraph("64-character-hex-secret", tbl_cell_code), Paragraph("Persistent HMAC key preventing OTP invalidation across process restarts.", tbl_cell)],
    ]
    env_tbl = Table(env_data, colWidths=[90, 190, 242])
    env_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_PRIMARY),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER),
        ('INNERGRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, C_CARD_BG]),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(env_tbl)

    story.append(Spacer(1, 8))
    story.append(Paragraph("6.2 Step-by-Step PowerShell Execution Sequence", h2))

    cmd_steps = [
        ("Step 1: Configure Local Database & Environment",
         "cd backend\n"
         ".\\scripts\\Set-LocalEnv.ps1"),
        ("Step 2: Apply Forward-Only Migrations & Verify Connection",
         "npx prisma migrate dev --name init\n"
         "npm run db:check"),
        ("Step 3: Seed Synthetic Baseline Development Dataset",
         "npm run prisma:seed"),
        ("Step 4: Launch Backend API Server (Port 4000)",
         "npm run dev\n"
         "# Listening at http://127.0.0.1:4000"),
        ("Step 5: Launch Frontend Client Server (Port 5173)",
         "cd ..\\frontend\n"
         "npm install\n"
         "npm run dev\n"
         "# Local: http://127.0.0.1:5173/"),
        ("Step 6: Provision Staff or Recruiter Accounts (PowerShell CLI)",
         "cd ..\\backend\n"
         ".\\scripts\\Provision-User.ps1 -Email officer@college.edu -Role STAFF"),
    ]

    for title_c, code_c in cmd_steps:
        story.append(Paragraph(f"<b>{title_c}</b>", h3))
        code_p = Paragraph(f"<font face='Courier' color='#1E40AF'>{code_c.replace(chr(10), '<br/>')}</font>", ParagraphStyle('CmdCode', parent=callout_text, fontName='Courier', fontSize=8, leading=11))
        t = Table([[code_p]], colWidths=[522])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), C_CARD_BG),
            ('BOX', (0,0), (-1,-1), 0.5, C_BORDER),
            ('TOPPADDING', (0,0), (-1,-1), 4),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
            ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ]))
        story.append(t)
        story.append(Spacer(1, 4))

    story.append(Spacer(1, 15))

    # Closing Callout
    final_box = make_callout(
        "CAMPUSLINK ARCHITECTURAL SUMMARY",
        "By fusing deterministic matching algorithms, transparent rubric-based sprint assessments, "
        "cryptographically grounded verification pipelines, and local-first relational storage in PostgreSQL, "
        "CAMPUSLINK provides colleges, students, and corporate recruiters with an honest, verifiable, "
        "and high-integrity Career Intelligence OS.",
        accent_color=C_GREEN,
        bg_color=colors.HexColor("#ECFDF5")
    )
    story.append(final_box)

    # Build Document
    print(f"Building PDF document: {filename} ...")
    doc.build(story, canvasmaker=NumberedCanvas)
    print("PDF build completed successfully.")

if __name__ == "__main__":
    out_file = "CAMPUSLINK_Architecture_And_System_Guide.pdf"
    if len(sys.argv) > 1:
        out_file = sys.argv[1]
    build_pdf(out_file)
