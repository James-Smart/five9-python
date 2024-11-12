from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel, Field, validator, AliasChoices
from .five9_prompts import VCCPrompt
from .vcc_general import *

class Five9VCCDomain(BaseModel):
    name: str
    id: str

    prompts: Optional[Dict[str, VCCPrompt]] = {}
    ivr_scripts: Optional[Dict[str, IVRScriptBasic]] = {}
    inbound_campaigns: Optional[Dict[str, InboundCampaign]] = {}
    users: Optional[Dict[str, User]] = {}
    contact_fields: Optional[Dict[str, ContactField]] = {}
    dispositions: Optional[Dict[str, Disposition]] = {}
    connectors: Optional[Dict[str, Connector]] = {}

    skills: Optional[Dict[str, Skill]] = {}
    scripts: Optional[Dict[str, IVRScriptBasic]] = {}
    campaign_profiles: Optional[Dict[str, CampaignProfile]] = {}
    cavs: Optional[Dict[str, CallAttachedVariable]] = {}

