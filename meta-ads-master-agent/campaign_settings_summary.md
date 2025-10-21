# Meta Ads Campaign Settings - $300 Offer
## Extracted from export_20251020_1346.xlsx

---

## CAMPAIGN LEVEL SETTINGS

**Campaign Name:** `$300 Meta Ads Ai Agent`  
**Campaign Objective:** `Outcome Leads` (New Objective: Yes)  
**Campaign Status:** `ACTIVE`  
**Buying Type:** `AUCTION`  
**Campaign Bid Strategy:** Not specified (defaults to ad set level)  
**Campaign Start Time:** 10/20/2025 10:42:47 am  
**Campaign Stop Time:** None (runs indefinitely)  
**Campaign Daily Budget:** Not set (budget at ad set level)  
**Campaign Lifetime Budget:** Not set  

---

## AD SET LEVEL SETTINGS

**Ad Set Name:** `$300 Meta Ads Ai Agent - IG`  
**Ad Set Status:** `ACTIVE`  
**Ad Set Daily Budget:** `$20.00` (2000 cents)  
**Ad Set Lifetime Budget:** `$0` (using daily budget)  

### Destination & Optimization
- **Destination Type:** `LEAD_FROM_IG_DIRECT` (Instagram lead forms)
- **Optimization Goal:** `LEAD_GENERATION`
- **Billing Event:** `IMPRESSIONS`
- **Bid Strategy:** `Highest volume or value`
- **Attribution Spec:** `[{"event_type":"CLICK_THROUGH","window_days":1}]` (1-day click attribution)
- **Use Accelerated Delivery:** `No`

### Geographic Targeting
- **Countries:** `US` (United States only)
- **Location Types:** `home, recent`
- **Excluded Countries:** None
- **Excluded Cities/Regions:** None

### Demographic Targeting
- **Age Min:** `18`
- **Age Max:** `65`
- **Gender:** Not specified (all genders)
- **Education Status:** Not specified
- **Income:** Not specified
- **Relationship:** Not specified

### Interest & Behavior Targeting (Flexible Inclusions)

The campaign uses **Flexible Inclusions** with 4 OR groups:

**Group 1: AI Interests**
- Artificial intelligence (computing) - ID: 6002898176962
- A.I. Artificial Intelligence - ID: 6002968393168

**Group 2: Marketing Interests**
- Digital marketing (marketing) - ID: 6003127206524
- Marketing automation - ID: 6003295328342
- Social media marketing (marketing) - ID: 6003389760112
- Online advertising (marketing) - ID: 6003526234370
- Advertising (marketing) - ID: 6003584163107
- Social media (online media) - ID: 6004030160948

**Group 3: Software/Tools Interests**
- Asana (software) - ID: 6002908703310
- Salesforce.com - ID: 6003109235784
- HubSpot - ID: 6003126155749
- Wix.com - ID: 6003199702082
- Shopify (software) - ID: 6003230166788
- WordPress - ID: 6003241014410
- Trello - ID: 6003766257632
- MailChimp - ID: 6004588220333
- Marketo - ID: 6006140080953

**Group 4: Entrepreneurship**
- Small business owners (behavior) - ID: 6002714898572
- Entrepreneurship (business and finance) - ID: 6003371567474

### Audience Settings
- **Custom Audiences:** None specified in this campaign
- **Excluded Custom Audiences:** None
- **Advantage Audience:** `0` (disabled - manual targeting)
- **Targeting Optimization:** `none`
- **Targeting Relaxation:** None

### Placement Settings
- **Publisher Platforms:** Not specified (likely automatic placements)
- **Facebook Positions:** Not specified
- **Instagram Positions:** Not specified
- **Audience Network Positions:** Not specified
- **Device Platforms:** Not specified
- **User Device:** Not specified
- **User Operating System:** Not specified

---

## AD LEVEL SETTINGS

**Ad Name:** `$300 Ai Agent Runs Your Meta Ads Forever`  
**Ad Status:** `ACTIVE`  

### Ad Copy
**Body (Primary Text):**  
`$300 Ai Agent Runs Your Meta Ads Forever - Setup & Running In 24 Hours - 1 on 1 Setup Call Included - 30 Day Guarantee`

**Title/Headline:** Not specified  
**Link Description:** Not specified  
**Display Link:** Not specified  

### Creative
- **Link Object ID:** `o:122106081866003922`
- **Link:** `https://www.instagram.com/` (Instagram destination)
- **Dynamic Creative:** Not used

### Call to Action
- Not explicitly specified in export (likely using Instagram lead form CTA)

---

## KEY DIFFERENCES FROM CURRENT AGENT CONFIGURATION

1. **Objective:** Current agent uses `OUTCOME_TRAFFIC`, Excel shows `Outcome Leads` with `LEAD_FROM_IG_DIRECT`
2. **Budget:** Current agent uses $5/day (500 cents), Excel shows $20/day (2000 cents)
3. **Targeting:** 
   - Current agent uses 13 custom audiences (mikee.ai visitors, video viewers, etc.)
   - Excel campaign uses NO custom audiences, only interest-based targeting with 4 flexible inclusion groups
4. **Geographic:**
   - Current agent targets worldwide (excluding IN, SG, TW)
   - Excel campaign targets US only
5. **Optimization:**
   - Current agent optimizes for traffic/link clicks
   - Excel campaign optimizes for lead generation with Instagram lead forms
6. **Messaging:**
   - Current agent: "Free AI Agent Download"
   - Excel campaign: "$300 Ai Agent Runs Your Meta Ads Forever - Setup & Running In 24 Hours - 1 on 1 Setup Call Included - 30 Day Guarantee"

---

## RECOMMENDED IMPLEMENTATION STRATEGY

For the autonomous agent to test the $300 offer while maintaining hook testing:

1. **Keep the hook testing framework** (20 variations, 70/30 exploitation/exploration)
2. **Update all hooks** to promote the $300 offer instead of free download
3. **Change campaign objective** from OUTCOME_TRAFFIC to Outcome Leads
4. **Update destination type** to LEAD_FROM_IG_DIRECT or create landing page
5. **Update targeting** to use interest-based flexible inclusions (4 OR groups from Excel)
6. **Update budget** to $20/day per ad (or keep $5/day for testing)
7. **Update geographic targeting** to US only (or keep worldwide for broader reach)
8. **Update ad copy** to use the $300 offer messaging
9. **Update image prompts** to reflect "$300 AI Agent" instead of "Free Download"

---

## META ADS API IMPLEMENTATION NOTES

### Campaign Creation Parameters
```python
campaign_params = {
    'name': '$300 Meta Ads Ai Agent - Hook Test {hook_name}',
    'objective': 'OUTCOME_LEADS',  # Changed from OUTCOME_TRAFFIC
    'status': 'ACTIVE',
    'special_ad_categories': []
}
```

### Ad Set Creation Parameters
```python
adset_params = {
    'name': '$300 Meta Ads Ai Agent - {hook_name}',
    'optimization_goal': 'LEAD_GENERATION',  # Changed from LINK_CLICKS
    'billing_event': 'IMPRESSIONS',
    'bid_strategy': 'LOWEST_COST_WITHOUT_CAP',  # Highest volume
    'daily_budget': 2000,  # $20 in cents (or 500 for $5)
    'campaign_id': campaign_id,
    'targeting': {
        'age_min': 18,
        'age_max': 65,
        'geo_locations': {
            'countries': ['US'],  # Changed from worldwide
            'location_types': ['home', 'recent']
        },
        'flexible_spec': [
            # Group 1: AI Interests
            {'interests': [
                {'id': '6002898176962', 'name': 'Artificial intelligence (computing)'},
                {'id': '6002968393168', 'name': 'A.I. Artificial Intelligence'}
            ]},
            # Group 2: Marketing Interests
            {'interests': [
                {'id': '6003127206524', 'name': 'Digital marketing (marketing)'},
                {'id': '6003295328342', 'name': 'Marketing automation'},
                {'id': '6003389760112', 'name': 'Social media marketing (marketing)'},
                {'id': '6003526234370', 'name': 'Online advertising (marketing)'},
                {'id': '6003584163107', 'name': 'Advertising (marketing)'},
                {'id': '6004030160948', 'name': 'Social media (online media)'}
            ]},
            # Group 3: Software/Tools Interests
            {'interests': [
                {'id': '6002908703310', 'name': 'Asana (software)'},
                {'id': '6003109235784', 'name': 'Salesforce.com'},
                {'id': '6003126155749', 'name': 'HubSpot'},
                {'id': '6003199702082', 'name': 'Wix.com'},
                {'id': '6003230166788', 'name': 'Shopify (software)'},
                {'id': '6003241014410', 'name': 'WordPress'},
                {'id': '6003766257632', 'name': 'Trello'},
                {'id': '6004588220333', 'name': 'MailChimp'},
                {'id': '6006140080953', 'name': 'Marketo'}
            ]},
            # Group 4: Entrepreneurship
            {'behaviors': [{'id': '6002714898572', 'name': 'Small business owners'}],
             'interests': [{'id': '6003371567474', 'name': 'Entrepreneurship (business and finance)'}]}
        ],
        'targeting_automation': {
            'advantage_audience': 0  # Disabled
        }
    },
    'destination_type': 'LEAD_FROM_IG_DIRECT',  # Instagram lead forms
    'status': 'ACTIVE'
}
```

### Ad Creation Parameters
```python
ad_params = {
    'name': '$300 Ai Agent Runs Your Meta Ads Forever - {hook_name}',
    'adset_id': adset_id,
    'creative': {
        'object_story_spec': {
            'instagram_actor_id': instagram_account_id,
            'link_data': {
                'message': '$300 Ai Agent Runs Your Meta Ads Forever - Setup & Running In 24 Hours - 1 on 1 Setup Call Included - 30 Day Guarantee',
                'link': 'https://www.instagram.com/',  # Or landing page URL
                'image_hash': image_hash
            }
        }
    },
    'status': 'ACTIVE'
}
```

---

**Generated:** 2025-10-20  
**Source:** export_20251020_1346.xlsx

