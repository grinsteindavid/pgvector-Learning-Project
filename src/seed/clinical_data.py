"""
Sample clinical/healthcare data tailored for Wolters Kluwer Health context.
Focus: Clinical decision support, workflow optimization, AI for burnout reduction.
"""

CLINICAL_ORGANIZATIONS = [
    {
        "name": "Mayo Clinic",
        "org_type": "health_system",
        "specialty": "Multi-specialty",
        "description": "World-renowned academic medical center integrating clinical practice, education, and research. Pioneer in AI-assisted diagnosis and clinical decision support systems for complex cases.",
        "city": "Rochester",
        "state": "Minnesota",
        "services": {"emergency": True, "telehealth": True, "research": True},
        "ai_use_cases": ["diagnostic_support", "clinical_documentation", "research_analytics"]
    },
    {
        "name": "Cleveland Clinic",
        "org_type": "health_system",
        "specialty": "Cardiology",
        "description": "Leading heart and cardiovascular care center utilizing AI-powered ECG analysis and predictive models for heart failure risk stratification. Implements clinical workflows to reduce physician documentation burden.",
        "city": "Cleveland",
        "state": "Ohio",
        "services": {"emergency": True, "telehealth": True, "cardiac_surgery": True},
        "ai_use_cases": ["ecg_analysis", "risk_prediction", "workflow_automation"]
    },
    {
        "name": "Johns Hopkins Hospital",
        "org_type": "academic_medical_center",
        "specialty": "Oncology",
        "description": "Premier cancer treatment and research facility leveraging AI for tumor detection, treatment planning, and clinical trial matching. Focus on reducing clinician burnout through intelligent documentation assistants.",
        "city": "Baltimore",
        "state": "Maryland",
        "services": {"emergency": True, "research": True, "clinical_trials": True},
        "ai_use_cases": ["tumor_detection", "treatment_planning", "documentation_ai"]
    },
    {
        "name": "Kaiser Permanente",
        "org_type": "integrated_health_system",
        "specialty": "Primary Care",
        "description": "Largest integrated healthcare network in the US focusing on preventive care and population health. Uses AI for patient risk scoring, care gap identification, and automated appointment scheduling to address staffing shortages.",
        "city": "Oakland",
        "state": "California",
        "services": {"telehealth": True, "preventive_care": True, "pharmacy": True},
        "ai_use_cases": ["population_health", "care_gaps", "scheduling_optimization"]
    },
    {
        "name": "Mass General Brigham",
        "org_type": "health_system",
        "specialty": "Neurology",
        "description": "Leading neuroscience center implementing AI for stroke detection, EEG interpretation, and neurological disease progression modeling. Active research in ambient clinical intelligence for note generation.",
        "city": "Boston",
        "state": "Massachusetts",
        "services": {"emergency": True, "research": True, "stroke_center": True},
        "ai_use_cases": ["stroke_detection", "eeg_analysis", "ambient_documentation"]
    },
    {
        "name": "UPMC Health System",
        "org_type": "health_system",
        "specialty": "Transplant Surgery",
        "description": "Major organ transplant center using AI for donor-recipient matching, post-transplant monitoring, and clinical decision support. Implements intelligent alerting to reduce alarm fatigue among clinical staff.",
        "city": "Pittsburgh",
        "state": "Pennsylvania",
        "services": {"transplant": True, "emergency": True, "research": True},
        "ai_use_cases": ["organ_matching", "patient_monitoring", "alert_optimization"]
    },
    {
        "name": "Cedars-Sinai Medical Center",
        "org_type": "academic_medical_center",
        "specialty": "Gastroenterology",
        "description": "Leading GI and digestive disease center utilizing AI-enhanced endoscopy for polyp detection and GI cancer screening. Focus on clinical workflow efficiency and reducing documentation time.",
        "city": "Los Angeles",
        "state": "California",
        "services": {"emergency": True, "research": True, "telehealth": True},
        "ai_use_cases": ["endoscopy_ai", "cancer_screening", "workflow_efficiency"]
    },
    {
        "name": "Mount Sinai Health System",
        "org_type": "health_system",
        "specialty": "Geriatrics",
        "description": "Comprehensive geriatric care network implementing AI for fall risk prediction, medication interaction checking, and care coordination for elderly patients with multiple chronic conditions.",
        "city": "New York",
        "state": "New York",
        "services": {"emergency": True, "long_term_care": True, "home_health": True},
        "ai_use_cases": ["fall_prevention", "drug_interactions", "care_coordination"]
    },
    {
        "name": "Intermountain Healthcare",
        "org_type": "integrated_health_system",
        "specialty": "Value-Based Care",
        "description": "Pioneer in value-based care models using AI for cost prediction, quality metrics tracking, and clinical pathway optimization. Known for data-driven approaches to reducing unnecessary care variation.",
        "city": "Salt Lake City",
        "state": "Utah",
        "services": {"telehealth": True, "preventive_care": True, "analytics": True},
        "ai_use_cases": ["cost_prediction", "quality_analytics", "pathway_optimization"]
    },
    {
        "name": "Geisinger Health",
        "org_type": "integrated_health_system",
        "specialty": "Genomics",
        "description": "Leader in genomic medicine integrating AI for genetic risk prediction, pharmacogenomics, and personalized treatment recommendations. Implements clinical decision support for genetic counseling.",
        "city": "Danville",
        "state": "Pennsylvania",
        "services": {"genomics": True, "research": True, "primary_care": True},
        "ai_use_cases": ["genetic_risk", "pharmacogenomics", "personalized_medicine"]
    },
    {
        "name": "Northwell Health",
        "org_type": "health_system",
        "specialty": "Emergency Medicine",
        "description": "Largest health system in New York using AI for ED patient flow optimization, sepsis early detection, and triage assistance. Focus on reducing wait times and improving emergency clinician efficiency.",
        "city": "New Hyde Park",
        "state": "New York",
        "services": {"emergency": True, "trauma_center": True, "telehealth": True},
        "ai_use_cases": ["patient_flow", "sepsis_detection", "triage_optimization"]
    },
    {
        "name": "Advocate Aurora Health",
        "org_type": "health_system",
        "specialty": "Behavioral Health",
        "description": "Integrated behavioral health network using AI for depression screening, suicide risk assessment, and mental health resource matching. Implements virtual care solutions to address therapist shortages.",
        "city": "Milwaukee",
        "state": "Wisconsin",
        "services": {"behavioral_health": True, "telehealth": True, "crisis_services": True},
        "ai_use_cases": ["depression_screening", "risk_assessment", "resource_matching"]
    },
    {
        "name": "CommonSpirit Health",
        "org_type": "health_system",
        "specialty": "Rural Health",
        "description": "Largest Catholic health system serving rural and underserved communities. Uses AI-powered telehealth and remote monitoring to extend specialist access. Focus on addressing healthcare workforce shortages in rural areas.",
        "city": "Chicago",
        "state": "Illinois",
        "services": {"telehealth": True, "community_health": True, "remote_monitoring": True},
        "ai_use_cases": ["telehealth_ai", "remote_monitoring", "specialist_access"]
    },
    {
        "name": "Mercy Health",
        "org_type": "health_system",
        "specialty": "Women's Health",
        "description": "Comprehensive women's health network implementing AI for mammography screening, prenatal risk assessment, and maternal health monitoring. Uses clinical decision support for high-risk pregnancy management.",
        "city": "St. Louis",
        "state": "Missouri",
        "services": {"womens_health": True, "maternity": True, "telehealth": True},
        "ai_use_cases": ["mammography_ai", "prenatal_risk", "maternal_monitoring"]
    },
    {
        "name": "Atrium Health",
        "org_type": "health_system",
        "specialty": "Pediatrics",
        "description": "Leading pediatric care network using AI for childhood disease prediction, growth monitoring, and vaccine schedule optimization. Implements family-centered care coordination with intelligent scheduling.",
        "city": "Charlotte",
        "state": "North Carolina",
        "services": {"pediatrics": True, "emergency": True, "telehealth": True},
        "ai_use_cases": ["pediatric_prediction", "growth_monitoring", "care_coordination"]
    }
]


CLINICAL_TOOLS = [
    {
        "name": "UpToDate Clinical Decision Support",
        "category": "Clinical Decision Support",
        "description": "Evidence-based clinical decision support system providing point-of-care recommendations for diagnosis, treatment, and drug information. Reduces time clinicians spend searching for medical literature.",
        "target_users": ["physicians", "nurse_practitioners", "physician_assistants"],
        "problem_solved": "Reduces clinical uncertainty and time spent researching treatment options at point of care"
    },
    {
        "name": "Lexicomp Drug Information",
        "category": "Drug Reference",
        "description": "Comprehensive drug database with interaction checking, dosing calculators, and IV compatibility. Integrates with EHR systems to provide real-time medication safety alerts.",
        "target_users": ["pharmacists", "physicians", "nurses"],
        "problem_solved": "Prevents medication errors and adverse drug interactions through real-time clinical alerts"
    },
    {
        "name": "Emmi Patient Engagement",
        "category": "Patient Education",
        "description": "Interactive multimedia patient education platform for informed consent, procedure preparation, and chronic disease management. Reduces staff time spent on repetitive patient education.",
        "target_users": ["patients", "care_coordinators", "nurses"],
        "problem_solved": "Automates patient education delivery and improves health literacy and treatment adherence"
    },
    {
        "name": "Medi-Span Drug Interaction Database",
        "category": "Clinical Surveillance",
        "description": "Enterprise drug interaction and contraindication database powering medication safety checks across health systems. Provides severity-graded alerts to reduce alert fatigue.",
        "target_users": ["clinical_informaticists", "pharmacists", "ehr_developers"],
        "problem_solved": "Enables intelligent medication safety alerting with reduced false positives"
    },
    {
        "name": "ProVation Procedure Documentation",
        "category": "Clinical Documentation",
        "description": "Automated procedure documentation for endoscopy, surgery, and diagnostic procedures. Uses structured templates and voice input to reduce documentation time by up to 50%.",
        "target_users": ["gastroenterologists", "surgeons", "proceduralists"],
        "problem_solved": "Eliminates post-procedure documentation burden and improves coding accuracy"
    },
    {
        "name": "Sentri7 Clinical Surveillance",
        "category": "Clinical Surveillance",
        "description": "Real-time clinical surveillance platform monitoring patient data for sepsis, AKI, deterioration, and antimicrobial stewardship. Reduces time to intervention through intelligent alerting.",
        "target_users": ["hospitalists", "intensivists", "clinical_pharmacists"],
        "problem_solved": "Enables early detection of clinical deterioration and reduces adverse events"
    },
    {
        "name": "PEPID Emergency Medicine Reference",
        "category": "Point of Care",
        "description": "Mobile-first clinical reference for emergency medicine with offline access. Provides rapid access to protocols, drug dosing, and differential diagnosis support in high-pressure environments.",
        "target_users": ["emergency_physicians", "paramedics", "urgent_care"],
        "problem_solved": "Provides instant clinical decision support in time-critical emergency situations"
    },
    {
        "name": "Health Language Semantic Platform",
        "category": "Interoperability",
        "description": "Clinical terminology management and semantic normalization platform. Enables accurate data exchange and analytics by mapping disparate clinical vocabularies to standard terminologies.",
        "target_users": ["clinical_informaticists", "data_engineers", "analysts"],
        "problem_solved": "Solves clinical data interoperability and enables accurate population health analytics"
    },
    {
        "name": "POC Advisor Antimicrobial Stewardship",
        "category": "Clinical Decision Support",
        "description": "AI-powered antimicrobial stewardship tool recommending optimal antibiotic selection based on local resistance patterns, patient factors, and evidence-based guidelines.",
        "target_users": ["infectious_disease", "pharmacists", "hospitalists"],
        "problem_solved": "Reduces antibiotic resistance and improves infection treatment outcomes"
    },
    {
        "name": "Clinical Effectiveness Analytics",
        "category": "Analytics",
        "description": "Quality measurement and clinical variation analytics platform identifying care gaps, outcome variations, and improvement opportunities across health system populations.",
        "target_users": ["quality_officers", "medical_directors", "analysts"],
        "problem_solved": "Identifies clinical variation and drives evidence-based quality improvement"
    },
    {
        "name": "Ambient Clinical Documentation AI",
        "category": "Documentation",
        "description": "AI-powered ambient listening technology that automatically generates clinical documentation from patient-provider conversations. Allows clinicians to focus on patients instead of computers.",
        "target_users": ["physicians", "nurse_practitioners", "specialists"],
        "problem_solved": "Eliminates documentation burden and reduces clinician burnout from EHR time"
    },
    {
        "name": "Prior Authorization Automation",
        "category": "Revenue Cycle",
        "description": "AI-driven prior authorization platform automating payer requirement lookups, documentation gathering, and submission. Reduces staff time on administrative tasks by 70%.",
        "target_users": ["revenue_cycle", "clinical_staff", "care_coordinators"],
        "problem_solved": "Automates administrative burden of insurance prior authorizations"
    },
    {
        "name": "Clinical Pathway Optimizer",
        "category": "Care Management",
        "description": "Evidence-based care pathway platform with real-time variance tracking and AI-powered next-best-action recommendations. Standardizes care while adapting to individual patient needs.",
        "target_users": ["care_managers", "hospitalists", "quality_teams"],
        "problem_solved": "Reduces unwarranted clinical variation and improves care standardization"
    },
    {
        "name": "Nurse Staffing Intelligence",
        "category": "Workforce Management",
        "description": "Predictive staffing platform using AI to forecast patient census, acuity, and optimal nurse-to-patient ratios. Addresses nursing shortages through intelligent scheduling.",
        "target_users": ["nurse_managers", "staffing_coordinators", "cno"],
        "problem_solved": "Optimizes nurse staffing to address workforce shortages and reduce burnout"
    },
    {
        "name": "Clinical Trial Matching Engine",
        "category": "Research",
        "description": "AI-powered clinical trial matching platform that automatically screens patients against trial eligibility criteria. Accelerates recruitment and expands patient access to novel therapies.",
        "target_users": ["research_coordinators", "oncologists", "investigators"],
        "problem_solved": "Automates clinical trial screening and accelerates patient recruitment"
    }
]
