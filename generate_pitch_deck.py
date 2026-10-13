"""
Generates a 7-slide, 16:9 landscape Pitch Deck PDF for CampusLink hackathon submission.
"""
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas
import os

# 16:9 Landscape dimensions (11 x 6.1875 inches or 11 x 8.5 letter landscape)
P_WIDTH, P_HEIGHT = landscape(letter)

C_PRIMARY = colors.HexColor("#0F172A")
C_BRAND = colors.HexColor("#1E40AF")
C_ACCENT = colors.HexColor("#0284C7")
C_TEAL = colors.HexColor("#0F766E")
C_CARD_BG = colors.HexColor("#F8FAFC")
C_CARD_BORDER = colors.HexColor("#E2E8F0")
C_TEXT_DARK = colors.HexColor("#0F172A")
C_TEXT_MUTED = colors.HexColor("#475569")
C_GREEN = colors.HexColor("#047857")

class SlideCanvas(canvas.Canvas):
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
            if self._pageNumber > 1:
                self.saveState()
                # Running footer
                self.setFont("Helvetica-Bold", 8)
                self.setFillColor(C_BRAND)
                self.drawString(40, 24, "CAMPUSLINK PITCH DECK")
                self.setFont("Helvetica", 8)
                self.setFillColor(C_TEXT_MUTED)
                self.drawString(160, 24, "|  Career Intelligence OS  |  Confidential & Proprietary")
                self.drawRightString(P_WIDTH - 40, 24, f"Slide {self._pageNumber} of {num_pages}")
                self.setStrokeColor(C_CARD_BORDER)
                self.setLineWidth(0.5)
                self.line(40, 36, P_WIDTH - 40, 36)
                self.restoreState()
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

def build_pitch_deck(filename="CAMPUSLINK_Pitch_Deck.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=(P_WIDTH, P_HEIGHT),
        leftMargin=40,
        rightMargin=40,
        topMargin=35,
        bottomMargin=45
    )

    styles = getSampleStyleSheet()

    slide_title = ParagraphStyle(
        'SlideTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=C_PRIMARY,
        spaceAfter=4
    )

    slide_sub = ParagraphStyle(
        'SlideSub',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=C_TEXT_MUTED,
        spaceAfter=12
    )

    body = ParagraphStyle(
        'DeckBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=C_TEXT_DARK
    )

    body_bold = ParagraphStyle(
        'DeckBodyBold',
        parent=body,
        fontName='Helvetica-Bold'
    )

    def slide_header(title, subtitle):
        return [
            Paragraph(title, slide_title),
            Paragraph(subtitle, slide_sub),
            HRFlowable(width="100%", thickness=1, color=C_BRAND, spaceBefore=0, spaceAfter=10)
        ]

    def card(title, desc, color=C_BRAND, width=225, height=130):
        content = [
            Paragraph(f"<b>{title}</b>", ParagraphStyle('CTitle', parent=body, fontName='Helvetica-Bold', fontSize=10, leading=13, textColor=color)),
            Spacer(1, 4),
            Paragraph(desc, ParagraphStyle('CDesc', parent=body, fontSize=8.5, leading=11.5, textColor=C_TEXT_DARK))
        ]
        t = Table([[content]], colWidths=[width])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), C_CARD_BG),
            ('BOX', (0,0), (-1,-1), 1, C_CARD_BORDER),
            ('LINELEFT', (0,0), (-1,-1), 3.5, color),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
            ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ]))
        return t

    story = []

    # =========================================================================
    # SLIDE 1: COVER
    # =========================================================================
    story.append(Spacer(1, 40))
    story.append(Paragraph("<font color='#1E40AF'><b>CAMPUSLINK</b></font>", ParagraphStyle('CoverH1', fontName='Helvetica-Bold', fontSize=36, leading=42, alignment=TA_CENTER)))
    story.append(Spacer(1, 8))
    story.append(Paragraph("<b>The Career Intelligence Operating System for Higher Education</b>", ParagraphStyle('CoverH2', fontName='Helvetica-Bold', fontSize=16, leading=20, textColor=C_ACCENT, alignment=TA_CENTER)))
    story.append(Spacer(1, 6))
    story.append(Paragraph("Bridging the campus-to-corporate credibility gap through explainable matching, rubric-verified skills, and zero black-box AI.", ParagraphStyle('CoverP', fontName='Helvetica', fontSize=11, leading=15, textColor=C_TEXT_MUTED, alignment=TA_CENTER)))
    story.append(Spacer(1, 25))

    cover_box_data = [
        [Paragraph("<b>Target Audience:</b> Colleges, Students, Placement Cells, Recruiters", body), Paragraph("<b>Status:</b> Fully Functional Local-First Architecture", body)],
        [Paragraph("<b>Core Innovation:</b> Deterministic Rubric & Verified Provenance", body), Paragraph("<b>Tech Stack:</b> React 19, TypeScript, Express, PostgreSQL, Prisma", body)]
    ]
    cover_tbl = Table(cover_box_data, colWidths=[350, 350])
    cover_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_CARD_BG),
        ('BOX', (0,0), (-1,-1), 1, C_CARD_BORDER),
        ('INNERGRID', (0,0), (-1,-1), 0.5, C_CARD_BORDER),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(cover_tbl)
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 2: THE PROBLEM VS OUR SOLUTION
    # =========================================================================
    story.extend(slide_header("1. Problem Statement & The CampusLink Solution", "Why traditional placements and black-box hiring platforms are failing today"))
    
    col1 = [
        Paragraph("<b>THE PROBLEM IN CAMPUS HIRING</b>", ParagraphStyle('HProb', fontName='Helvetica-Bold', fontSize=11, textColor=colors.HexColor("#BE123C"))),
        Spacer(1, 6),
        card("Resume Credibility Inflation", "Students write buzzwords and self-report 'expert' skills without verifiable evidence, forcing recruiters to doubt every resume.", colors.HexColor("#BE123C"), width=340),
        Spacer(1, 6),
        card("Opaque 'Black-Box' AI Matchers", "Existing recruitment platforms use unexplainable ML classifiers. Rejected candidates never know why they were cut or how to improve.", colors.HexColor("#BE123C"), width=340),
        Spacer(1, 6),
        card("Manual, Disconnected Placement Cells", "Colleges manage drives across WhatsApp groups, Google Sheets, and email blasts with zero verifiable audit trails.", colors.HexColor("#BE123C"), width=340),
    ]

    col2 = [
        Paragraph("<b>THE CAMPUSLINK TRANSFORMATION</b>", ParagraphStyle('HSol', fontName='Helvetica-Bold', fontSize=11, textColor=C_GREEN)),
        Spacer(1, 6),
        card("Provenance-Based Skill Passport", "Separates self-reported claims from rubric-assessed proofs. Unverified claims earn zero evidence points.", C_GREEN, width=340),
        Spacer(1, 6),
        card("100% Explainable Matching", "Deterministic mathematical formula breaks down exact met criteria, missing gaps, bonus points, and next actionable steps.", C_GREEN, width=340),
        Spacer(1, 6),
        card("Unified Placement Tower OS", "Real-time cohort readiness analytics, guarded application state machine, and frozen materialized announcement broadcasts.", C_GREEN, width=340),
    ]

    p_table = Table([[col1, col2]], colWidths=[355, 355])
    p_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(p_table)
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 3: HOW IT WORKS: CORE USER WORKFLOWS
    # =========================================================================
    story.extend(slide_header("2. How Things Work: The 5-Step Student Journey", "From initial onboarding to verified readiness and job placement"))

    steps_data = [
        [
            card("1. Career Twin", "Students record skills across 4 standardized tiers (Beginner to Expert). Unverified claims are flagged until proven by project evidence.", C_BRAND, width=135),
            card("2. Opportunity Mirror", "Algorithm computes match score (0-100%) against corporate job criteria with full transparency into met criteria and skill gaps.", C_ACCENT, width=135),
            card("3. Skill Sprint", "Students solve coding challenges. Submissions are scored via Rubric v1. Scoring 70+ auto-promotes skill and records project proof.", C_TEAL, width=135),
            card("4. Interview Arena", "Mock interview practice room scoring STAR structure, substance, and quantitative metrics with an anti-duplication points ledger.", colors.HexColor("#D97706"), width=135),
            card("5. Verified Passport", "Holistic Readiness Score (50% Proficiency + 30% Evidence + 20% Momentum) unlocks guarded corporate applications.", C_GREEN, width=135),
        ]
    ]
    st_tbl = Table(steps_data, colWidths=[142, 142, 142, 142, 142])
    st_tbl.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(st_tbl)
    story.append(Spacer(1, 10))

    bottom_box = card(
        "CORE PHILOSOPHY: ZERO BLACK-BOX AI",
        "Every assessment score and match calculation uses published, deterministic formulas. "
        "Candidates receive actionable feedback on exactly which engineering decisions earned or lost points, "
        "fostering true pedagogical improvement rather than arbitrary algorithmic rejection.",
        C_PRIMARY, width=710
    )
    story.append(bottom_box)
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 4: THE TECHNICAL ENGINES & FORMULAS
    # =========================================================================
    story.extend(slide_header("3. Transparent Mathematical Engines", "Pure deterministic logic: auditable, explainable, and tamper-resistant"))

    f_data = [
        [
            card(
                "Explainable Match Formula (lib/match.ts)",
                "• Weight = Rank(minLevel) x 2<br/>"
                "• Met: Full Weight + min(Projects, 2) x 0.5<br/>"
                "• Partial: 75% weight for 1 level below<br/>"
                "• Nice-to-Have: +1 point at Intermediate+<br/>"
                "• Score = min(100, round(100 x Pts / Max))",
                C_ACCENT, width=225
            ),
            card(
                "Sprint Rubric v1 (lib/rubric.ts)",
                "• 40 Base Points<br/>"
                "• +25 Full Checklist Completed<br/>"
                "• +15 Verifiable Repo / Live Deploy URL<br/>"
                "• +15 Write-up Depth (>=40 words)<br/>"
                "• +5 Quality Attributes (tests, perf, a11y)<br/>"
                "• Threshold: 70+ auto-promotes skill tier",
                C_TEAL, width=225
            ),
            card(
                "Holistic Student Readiness",
                "• 50% Proficiency: (Mean Skill Rank / 4) x 50<br/>"
                "• 30% Evidence: (Evidenced / Total) x 30<br/>"
                "• 20% Momentum: min(20, Apps x 4 + Sprints x 6)<br/>"
                "• Unverified claims receive zero evidence points<br/>"
                "• Direct pedagogical incentive for real code",
                C_GREEN, width=225
            )
        ]
    ]
    f_tbl = Table(f_data, colWidths=[238, 238, 238])
    f_tbl.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(f_tbl)
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 5: SYSTEM ARCHITECTURE & TECH STACK
    # =========================================================================
    story.extend(slide_header("4. System Architecture & Complete Technology Stack", "Local-first monorepo built for enterprise security and resilience"))

    arch_box_data = [
        [
            card("Frontend Layer", "• React 19 & Vite 8 (Strict port 5173)<br/>• React Router v7 & Session Gates<br/>• TanStack Query (15s cache, auto-sync)<br/>• Tailwind CSS v4 & Lucide Icons", C_BRAND, width=225),
            card("API & Backend Layer", "• Express 4.21 & TypeScript 5.6<br/>• Zod strict runtime schema parsing<br/>• Helmet, dynamic CORS & CSRF guard<br/>• Multi-tier Express-Rate-Limit budgets", C_ACCENT, width=225),
            card("Database & Security", "• PostgreSQL 16+ & Prisma ORM 5<br/>• scrypt password hashing (memory-hard)<br/>• CSPRNG HMAC-SHA256 Email OTP<br/>• Revocable HttpOnly session tokens", C_TEAL, width=225)
        ]
    ]
    a_tbl = Table(arch_box_data, colWidths=[238, 238, 238])
    a_tbl.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(a_tbl)
    story.append(Spacer(1, 8))

    sec_summary = card(
        "DEFENSE-IN-DEPTH POSTURE",
        "Bound strictly to loopback 127.0.0.1; no wildcard interface exposure. "
        "Server-side RBAC enforces permissions strictly: client-submitted studentProfileId or companyId parameters "
        "are ignored in favor of the authoritative server session. Zero database errors or stack traces leak to clients.",
        C_PRIMARY, width=710
    )
    story.append(sec_summary)
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 6: WHAT IS WORKING & FINALE COMMITMENTS
    # =========================================================================
    story.extend(slide_header("5. What Is Built & Grand Finale Deliverables", "From current working prototype to final competition launch"))

    fin_data = [
        [
            card(
                "ALREADY BUILT & VERIFIED TODAY (100% WORKING)",
                "• 3-Step Email-verified student registration with live SMTP OTP<br/>"
                "• Career Twin with 4 skill tiers and linked project evidence<br/>"
                "• Opportunity Mirror with explainable match breakdown<br/>"
                "• Skill Sprint with live Rubric v1 grading & auto-promotion<br/>"
                "• Interview Arena with STAR evaluation & point ledgers<br/>"
                "• Placement Tower with cohort readiness & What-If Lab<br/>"
                "• Guarded Application FSM (Applied -> Shortlisted -> Hired)",
                C_GREEN, width=340
            ),
            card(
                "COMMITMENTS FOR GRAND FINALE LAUNCH",
                "• Multi-College Placement Consortium: Cross-campus placement drives<br/>"
                "• Cryptographically Signed PDF Skill Passports (W3C Verifiable Credentials)<br/>"
                "• Recruiter Bulk Resume Screening Portal with deterministic scoring<br/>"
                "• Automated Calendar Integration for shortlisted interview slots<br/>"
                "• Dockerized 1-click self-hosted deployment for university IT cells",
                C_BRAND, width=340
            )
        ]
    ]
    fin_tbl = Table(fin_data, colWidths=[355, 355])
    fin_tbl.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(fin_tbl)
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 7: IMPACT & VISION
    # =========================================================================
    story.extend(slide_header("6. The Vision: Restoring Trust in Campus Placements", "Empowering millions of students with verifiable career trajectory"))

    imp_data = [
        [
            card("For Students", "Replaces resume anxiety with a transparent growth roadmap. Every sprint closed directly lifts job match scores and readiness percentages.", C_BRAND, width=225),
            card("For Placement Cells", "Replaces chaotic spreadsheets with executive cohort intelligence, verified audit trails, and targeted student interventions.", C_ACCENT, width=225),
            card("For Corporate Recruiters", "Cuts screening time by 80% by filtering candidates on verified code proofs rather than unprovable self-attested claims.", C_TEAL, width=225)
        ]
    ]
    imp_tbl = Table(imp_data, colWidths=[238, 238, 238])
    imp_tbl.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(imp_tbl)
    story.append(Spacer(1, 10))

    closing_card = card(
        "CONCLUSION",
        "CAMPUSLINK transforms campus placements from an opaque lottery into a merit-based, "
        "evidence-driven career intelligence ecosystem. Built with production-grade engineering, "
        "local-first reliability, and mathematically auditable integrity.",
        C_PRIMARY, width=710
    )
    story.append(closing_card)

    print(f"Building Pitch Deck PDF: {filename} ...")
    doc.build(story, canvasmaker=SlideCanvas)
    print("Pitch Deck build completed successfully.")

if __name__ == "__main__":
    build_pitch_deck("CAMPUSLINK_Pitch_Deck.pdf")
