"""
Shared data models and utilities for Meta Ads Master Agent
UPDATED FOR: "AI Runs Your Ads Forever" - $300 One-Time + Money-Back Guarantee
"""

from dataclasses import dataclass, asdict
from typing import List, Dict, Optional
from datetime import datetime
from enum import Enum


class HookType(Enum):
    AUTOMATION = "automation"
    GUARANTEE = "guarantee"
    VALUE = "value"
    FOREVER = "forever"
    RESULTS = "results"


class CreativeType(Enum):
    IMAGE = "image"
    VIDEO = "video"


class CreativeStyle(Enum):
    MRBEAST = "mrbeast"
    MEME = "meme"
    MINIMALIST = "minimalist"
    SCREENSHOT = "screenshot"
    BEFORE_AFTER = "before_after"
    TESTIMONIAL = "testimonial"
    URGENCY = "urgency"
    QUESTION = "question"


class AdStatus(Enum):
    ACTIVE = "active"
    PAUSED = "paused"
    ARCHIVED = "archived"


@dataclass
class HookData:
    """Hook variation data"""
    name: str
    hook: str
    primary_text: str
    hook_type: str
    creative_style: str
    performance_score: float = 0.0
    
    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class CreativeAsset:
    """Generated creative asset"""
    asset_type: CreativeType
    url: str
    local_path: Optional[str] = None
    hook_name: str = ""
    cost: float = 0.0
    metadata: Dict = None
    
    def to_dict(self) -> Dict:
        data = asdict(self)
        data['asset_type'] = self.asset_type.value
        return data


@dataclass
class PerformanceMetrics:
    """Ad performance metrics"""
    creative_id: int
    impressions: int = 0
    clicks: int = 0
    spend: float = 0.0
    conversions: int = 0
    ctr: float = 0.0
    cpc: float = 0.0
    cpa: float = 0.0
    performance_score: float = 0.0
    updated_at: datetime = None
    
    def __post_init__(self):
        if self.updated_at is None:
            self.updated_at = datetime.now()
    
    def calculate_derived_metrics(self):
        """Calculate CTR, CPC, CPA"""
        if self.impressions > 0:
            self.ctr = (self.clicks / self.impressions) * 100
        
        if self.clicks > 0:
            self.cpc = self.spend / self.clicks
        
        if self.conversions > 0:
            self.cpa = self.spend / self.conversions
        
        # Performance score: weighted combination
        self.performance_score = (
            (self.ctr * 0.3) +
            (100 - min(self.cpc, 10) * 10) * 0.3 +
            (self.conversions * 0.4)
        )
    
    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class CampaignConfig:
    """Campaign configuration"""
    campaign_id: Optional[str] = None
    adset_id: Optional[str] = None
    ad_id: Optional[str] = None
    hook_data: Optional[HookData] = None
    creative_asset: Optional[CreativeAsset] = None
    daily_budget: int = 2000  # $20 in cents
    status: AdStatus = AdStatus.ACTIVE
    
    def to_dict(self) -> Dict:
        data = {
            'campaign_id': self.campaign_id,
            'adset_id': self.adset_id,
            'ad_id': self.ad_id,
            'daily_budget': self.daily_budget,
            'status': self.status.value
        }
        if self.hook_data:
            data['hook_data'] = self.hook_data.to_dict()
        if self.creative_asset:
            data['creative_asset'] = self.creative_asset.to_dict()
        return data


# UPDATED HOOK VARIATIONS - "AI Runs Your Ads Forever" Focus
HOOK_VARIATIONS = [
    # CORE "FOREVER" HOOKS
    HookData(
        name="AI_Runs_Ads_Forever",
        hook="AI Runs Your Ads Forever - $300 One-Time Payment",
        primary_text="AI RUNS\nYOUR ADS\nFOREVER\n$300 ONE-TIME",
        hook_type="forever",
        creative_style="mrbeast"
    ),
    HookData(
        name="Forever_300_OneTime",
        hook="$300 One-Time - AI Runs Your Meta Ads Forever",
        primary_text="$300\nONE-TIME\nAI RUNS ADS\nFOREVER",
        hook_type="forever",
        creative_style="minimalist"
    ),
    HookData(
        name="Runs_Forever_Guaranteed",
        hook="AI Runs Your Ads Forever - Guaranteed to Work or Money Back",
        primary_text="AI RUNS ADS\nFOREVER\nGUARANTEED\nOR REFUND",
        hook_type="forever",
        creative_style="mrbeast"
    ),
    HookData(
        name="Pay_Once_Forever",
        hook="Pay $300 Once - AI Runs Your Ads Forever",
        primary_text="PAY $300\nONCE\nAI RUNS ADS\nFOREVER",
        hook_type="forever",
        creative_style="screenshot"
    ),
    
    # GUARANTEE HOOKS
    HookData(
        name="Money_Back_Guarantee",
        hook="AI Runs Your Ads Forever - 30-Day Money-Back Guarantee",
        primary_text="AI RUNS ADS\nFOREVER\n30-DAY\nMONEY BACK",
        hook_type="guarantee",
        creative_style="testimonial"
    ),
    HookData(
        name="Guaranteed_To_Work",
        hook="$300 AI Agent - Guaranteed to Work or Full Refund",
        primary_text="$300 AI\nGUARANTEED\nTO WORK\nOR REFUND",
        hook_type="guarantee",
        creative_style="mrbeast"
    ),
    HookData(
        name="Zero_Risk_Forever",
        hook="Zero Risk - AI Runs Your Ads Forever or Money Back",
        primary_text="ZERO RISK\nAI RUNS ADS\nFOREVER\nOR REFUND",
        hook_type="guarantee",
        creative_style="minimalist"
    ),
    HookData(
        name="Works_Or_Refund",
        hook="AI Runs Your Ads Forever - Works or Immediate Refund",
        primary_text="WORKS OR\nIMMEDIATE\nREFUND\n$300 ONE-TIME",
        hook_type="guarantee",
        creative_style="urgency"
    ),
    
    # VALUE HOOKS
    HookData(
        name="No_Monthly_Fees_Forever",
        hook="No Monthly Fees Ever - AI Runs Your Ads Forever for $300",
        primary_text="NO MONTHLY\nFEES EVER\nAI RUNS ADS\nFOREVER $300",
        hook_type="value",
        creative_style="before_after"
    ),
    HookData(
        name="OneTime_Runs_Forever",
        hook="$300 One-Time Payment - Runs Your Ads Forever",
        primary_text="$300\nONE-TIME\nRUNS YOUR ADS\nFOREVER",
        hook_type="value",
        creative_style="mrbeast"
    ),
    HookData(
        name="Forever_No_Subscription",
        hook="AI Runs Your Ads Forever - No Subscription Required",
        primary_text="AI RUNS ADS\nFOREVER\nNO SUBSCRIPTION\n$300 ONCE",
        hook_type="value",
        creative_style="minimalist"
    ),
    HookData(
        name="Own_It_Forever",
        hook="Own It Forever - $300 AI Runs Your Meta Ads 24/7",
        primary_text="OWN IT\nFOREVER\n$300 AI\nRUNS ADS 24/7",
        hook_type="value",
        creative_style="screenshot"
    ),
    
    # AUTOMATION + FOREVER HOOKS
    HookData(
        name="Automated_Forever",
        hook="Fully Automated Forever - AI Runs Your Ads for $300",
        primary_text="FULLY\nAUTOMATED\nFOREVER\n$300 ONE-TIME",
        hook_type="automation",
        creative_style="mrbeast"
    ),
    HookData(
        name="Set_Once_Runs_Forever",
        hook="Set Up Once - AI Runs Your Ads Forever",
        primary_text="SET UP\nONCE\nRUNS YOUR ADS\nFOREVER",
        hook_type="automation",
        creative_style="minimalist"
    ),
    HookData(
        name="Never_Touch_Again",
        hook="Never Touch Ads Again - AI Runs Them Forever for $300",
        primary_text="NEVER TOUCH\nADS AGAIN\nAI RUNS THEM\nFOREVER $300",
        hook_type="automation",
        creative_style="meme"
    ),
    HookData(
        name="247_Forever",
        hook="AI Runs Your Ads 24/7 Forever - $300 One-Time",
        primary_text="AI RUNS ADS\n24/7 FOREVER\n$300\nONE-TIME",
        hook_type="automation",
        creative_style="screenshot"
    ),
    
    # RESULTS + GUARANTEE HOOKS
    HookData(
        name="Results_Or_Refund",
        hook="Get Results or Full Refund - AI Runs Your Ads Forever",
        primary_text="RESULTS OR\nFULL REFUND\nAI RUNS ADS\nFOREVER",
        hook_type="results",
        creative_style="testimonial"
    ),
    HookData(
        name="Works_Forever_Guaranteed",
        hook="Works Forever or Money Back - $300 AI Agent",
        primary_text="WORKS\nFOREVER\nOR MONEY BACK\n$300 AI",
        hook_type="results",
        creative_style="mrbeast"
    ),
    HookData(
        name="Winning_Ads_Forever",
        hook="AI Finds Winning Ads Forever - Guaranteed or Refund",
        primary_text="AI FINDS\nWINNING ADS\nFOREVER\nOR REFUND",
        hook_type="results",
        creative_style="before_after"
    ),
    HookData(
        name="Forever_Optimization",
        hook="Forever Optimization - AI Tests Your Ads 24/7 for $300",
        primary_text="FOREVER\nOPTIMIZATION\nAI TESTS 24/7\n$300 ONCE",
        hook_type="results",
        creative_style="screenshot"
    ),
]


# Ad copy template
AD_COPY_TEMPLATE = "AI Runs Your Ads Forever - $300 One-Time Payment - Guaranteed to Work or Money Back - Setup in 24 Hours"

# Landing page URL
LANDING_PAGE_URL = "https://mikee.ai/agent"

# Meta Ads API Configuration
META_ADS_CONFIG = {
    "account_id": "act_283244530805042",
    "page_id": "122106081866003922",
    "objective": "OUTCOME_LEADS",
    "optimization_goal": "LEAD_GENERATION",
    "billing_event": "IMPRESSIONS",
    "bid_strategy": "LOWEST_COST_WITHOUT_CAP",
    "attribution_spec": [
        {
            "event_type": "CLICK_THROUGH",
            "window_days": 1
        }
    ]
}

# Interest-Based Targeting (US Only)
TARGETING_SPEC = {
    "geo_locations": {
        "countries": ["US"]
    },
    "age_min": 25,
    "age_max": 65,
    "flexible_spec": [
        {
            "interests": [
                {"id": "6002898176962", "name": "Artificial intelligence (computing)"},
                {"id": "6002968393168", "name": "A.I. Artificial Intelligence"}
            ]
        },
        {
            "interests": [
                {"id": "6003127206524", "name": "Digital marketing (marketing)"},
                {"id": "6003295328342", "name": "Marketing automation"},
                {"id": "6003389760112", "name": "Social media marketing (marketing)"},
                {"id": "6003526234370", "name": "Online advertising (marketing)"},
                {"id": "6003584163107", "name": "Advertising (marketing)"},
                {"id": "6004030160948", "name": "Social media (online media)"}
            ]
        },
        {
            "interests": [
                {"id": "6002908703310", "name": "Asana (software)"},
                {"id": "6003109235784", "name": "Salesforce.com"},
                {"id": "6003126155749", "name": "HubSpot"},
                {"id": "6003199702082", "name": "Wix.com"},
                {"id": "6003230166788", "name": "Shopify (software)"},
                {"id": "6003241014410", "name": "WordPress"},
                {"id": "6003766257632", "name": "Trello"},
                {"id": "6004588220333", "name": "MailChimp"},
                {"id": "6006140080953", "name": "Marketo"}
            ]
        },
        {
            "interests": [
                {"id": "6003371567474", "name": "Entrepreneurship (business and finance)"}
            ]
        }
    ],
    "publisher_platforms": ["facebook", "instagram"],
    "facebook_positions": ["feed", "right_hand_column"],
    "instagram_positions": ["stream"],
    "device_platforms": ["mobile", "desktop"]
}


# CREATIVE STYLE CONFIGURATIONS
CREATIVE_STYLE_CONFIGS = {
    "mrbeast": {
        "gradients": [
            ['deep royal blue (#1565c0)', 'electric purple (#9c27b0)', 'vibrant magenta (#e91e63)'],
            ['deep navy (#0a1929)', 'rich ocean blue (#1565c0)', 'bright cyan (#00b8d4)'],
            ['deep crimson (#b71c1c)', 'vibrant red (#d32f2f)', 'bright orange (#ff6f00)'],
            ['deep emerald (#004d40)', 'rich teal (#00897b)', 'bright gold (#ffd700)'],
            ['midnight blue (#1a237e)', 'royal purple (#6a1b9a)', 'electric violet (#7c4dff)']
        ],
        "font": "Bold, thick sans-serif (Impact or Bebas Neue style)",
        "text_color": "white with 4px black stroke outline",
        "effects": "Subtle radial glow behind text",
        "style_notes": "High energy, scroll-stopping, MrBeast-style"
    },
    "meme": {
        "background": "White or light gray",
        "font": "Impact or Arial Black",
        "text_color": "Black text, white stroke",
        "layout": "Top text / Image / Bottom text (classic meme format)",
        "style_notes": "Relatable, humorous, meme-style"
    },
    "minimalist": {
        "background": "Solid color (white, black, or brand color)",
        "font": "Clean sans-serif (Helvetica, Arial)",
        "text_color": "High contrast (black on white or white on black)",
        "layout": "Centered, lots of whitespace",
        "style_notes": "Clean, professional, Apple-style minimalism"
    },
    "screenshot": {
        "background": "Fake dashboard or app screenshot",
        "elements": "Graphs, metrics, UI elements",
        "font": "System font (SF Pro, Roboto)",
        "style_notes": "Looks like a real app/dashboard screenshot"
    },
    "before_after": {
        "background": "Split screen - red/dull left side, green/bright right side",
        "layout": "Split screen - before on left, after on right",
        "labels": "BEFORE / AFTER labels",
        "colors": "Red/dull for before, green/bright for after",
        "style_notes": "Visual transformation, clear contrast"
    },
    "testimonial": {
        "background": "Gradient or solid color",
        "elements": "Quote marks, attribution",
        "font": "Serif for quote, sans-serif for attribution",
        "style_notes": "Social proof, quote card style"
    },
    "urgency": {
        "background": "Red to orange gradient, alert colors",
        "colors": "Red, orange, yellow (alert colors)",
        "elements": "Arrows, exclamation marks, countdown vibes",
        "font": "Bold, attention-grabbing",
        "style_notes": "Creates FOMO, urgency, scarcity"
    },
    "question": {
        "background": "Clean, simple",
        "font": "Large, readable",
        "punctuation": "Large question mark",
        "style_notes": "Provocative question, makes user think"
    }
}

# Image generation API config
IMAGE_API_CONFIG = {
    "provider": "kie_ai_nano_banana",
    "api_key_env": "KIE_AI_API_KEY",
    "model": "nano",
    "aspect_ratio": "9:16",
    "output_format": "png"
}


# Database configuration
DATABASE_CONFIG = {
    "path": "/root/meta-ads-master-agent/data/meta_ads_performance.db",
    "tables": {
        "creatives": """
            CREATE TABLE IF NOT EXISTS creatives (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                hook_name TEXT NOT NULL,
                hook_text TEXT NOT NULL,
                primary_text TEXT NOT NULL,
                hook_type TEXT NOT NULL,
                creative_style TEXT NOT NULL,
                image_path TEXT,
                image_url TEXT,
                campaign_id TEXT,
                adset_id TEXT,
                ad_id TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """,
        "performance": """
            CREATE TABLE IF NOT EXISTS performance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                creative_id INTEGER NOT NULL,
                impressions INTEGER DEFAULT 0,
                clicks INTEGER DEFAULT 0,
                spend REAL DEFAULT 0.0,
                conversions INTEGER DEFAULT 0,
                ctr REAL DEFAULT 0.0,
                cpc REAL DEFAULT 0.0,
                cpa REAL DEFAULT 0.0,
                performance_score REAL DEFAULT 0.0,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (creative_id) REFERENCES creatives (id)
            )
        """
    }
}

