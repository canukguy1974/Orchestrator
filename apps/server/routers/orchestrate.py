from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List
from server.models import OrchestrateReq, OrchestrateRes, Reply, ToolEvent, Offer
from server import persona_repo
from server.offer_engine import evaluate as offers_eval
from server.tools import rag, budget, avatar, crm, kyc, case, payments
router = APIRouter()

def last_user_text(messages: List[Dict[str, Any]]) -> str:
    for m in reversed(messages):
        if m['role'] == 'user': return m['content']
    return ''

@router.post('/orchestrate', response_model=OrchestrateRes)
def orchestrate(req: OrchestrateReq):
    try:
        persona = persona_repo.load_persona(req.persona)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f'Unknown persona: {req.persona} ({e})')
    
    allowed = set(persona.get('tools', []))
    text = last_user_text([m.model_dump() for m in req.messages])
    tool_events: List[ToolEvent] = []
    context_data = {}
    
    # RAG Search
    rag_chunks = []
    if 'rag.search' in allowed:
        out = rag.search(query=text, namespaces=persona.get('ragNamespaces', []), user_id=req.user_id, k=3)
        tool_events.append(ToolEvent(name='rag.search', input={'query': text}, output={'count': len(out)}))
        rag_chunks = out
        context_data['rag_results'] = out
    
    # Budget Analysis
    budget_insights = {}
    if 'budget.analyze' in allowed:
        out = budget.analyze(user_id=req.user_id, horizon_days=30)
        tool_events.append(ToolEvent(name='budget.analyze', input={'user_id': req.user_id}, output={'summary': out.get('summary')}))
        budget_insights = out
        context_data['budget'] = out
    
    # CRM Lookup (if user_id looks like customer identifier)
    customer_data = {}
    if 'crm.lookup' in allowed and req.user_id:
        out = crm.lookup(req.user_id)
        tool_events.append(ToolEvent(name='crm.lookup', input={'identifier': req.user_id}, output={'found': out.get('found')}))
        if out.get('found'):
            customer_data = out.get('customer', {})
            context_data['customer'] = customer_data
    
    # KYC Check (mock trigger for new customers)
    if 'kyc.verify' in allowed and customer_data.get('segment') == 'new':
        out = kyc.verify(req.user_id, ['passport', 'utility_bill'])
        tool_events.append(ToolEvent(name='kyc.verify', input={'user_id': req.user_id}, output={'status': out.get('overall_status')}))
        context_data['kyc_status'] = out
    
    # Generate persona-appropriate response
    display_name = persona.get('displayName', 'Assistant')
    reply_parts = [f"[{display_name}]"]
    
    if rag_chunks:
        reply_parts.append(f"I found {len(rag_chunks)} relevant documents.")
        if persona.get('id') == 'teller-v1':
            reply_parts.append("I can help you with account services and transactions.")
        elif persona.get('id') == 'exec-v1':
            reply_parts.append("Here are the key insights from our knowledge base.")
    
    if budget_insights:
        reply_parts.append(f"Budget outlook: {budget_insights.get('summary', 'Analysis complete.')}")
    
    if customer_data:
        reply_parts.append(f"Hello {customer_data.get('name', 'valued customer')}!")
        if customer_data.get('segment') == 'premium':
            reply_parts.append("As a premium member, I'm here to provide personalized assistance.")
    
    if not rag_chunks and not budget_insights and not customer_data:
        reply_parts.append("How can I help you today?")
    
    reply_text = " ".join(reply_parts)
    
    # Avatar/TTS
    media = None
    if 'avatar.speak' in allowed:
        voice_config = persona.get('voice', {})
        media = avatar.speak(text=reply_text, persona_voice=voice_config.get('tone', 'neutral'))
    
    # Offer Engine
    user_profile = {
        'segments': [customer_data.get('segment', 'newcomer')],
        'balance': customer_data.get('balance', 250),
        'products': customer_data.get('products', [])
    }
    offers = offers_eval(user_profile, {'persona': req.persona, 'context': context_data})
    
    return OrchestrateRes(
        reply=Reply(text=reply_text, media=media), 
        offers=[Offer(**o) for o in offers], 
        tool_events=tool_events
    )
