from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List
from server.models import OrchestrateReq, OrchestrateRes, Reply, ToolEvent, Offer
from server import persona_repo
from server.offer_engine import evaluate as offers_eval
from server.tools import rag, budget, avatar
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
    allowed=set(persona.get('tools', []))
    text=last_user_text([m.model_dump() for m in req.messages])
    tool_events: List[ToolEvent] = []
    rag_chunks=[]
    if 'rag.search' in allowed:
        out=rag.search(query=text, namespaces=persona.get('ragNamespaces', []), user_id=req.user_id, k=3)
        tool_events.append(ToolEvent(name='rag.search', input={'query': text}, output={'count': len(out)}))
        rag_chunks=out
    budget_insights={}
    if 'budget.analyze' in allowed:
        out=budget.analyze(user_id=req.user_id, horizon_days=30)
        tool_events.append(ToolEvent(name='budget.analyze', input={'user_id': req.user_id}, output={'summary': out.get('summary')}))
        budget_insights=out
    reply_text=f"[{persona.get('displayName')}] I found {len(rag_chunks)} relevant docs. "
    if budget_insights: reply_text += f"Budget outlook: {budget_insights.get('summary')}."
    else: reply_text += 'Ask me another question or choose an action.'
    media=None
    if 'avatar.speak' in allowed:
        media=avatar.speak(text=reply_text, persona_voice=persona.get('voice',{}).get('tone','neutral'))
    user_mock={'segments':['newcomer'], 'balance':250}
    offers=offers_eval(user_mock, {'persona': req.persona})
    return OrchestrateRes(reply=Reply(text=reply_text, media=media), offers=[Offer(**o) for o in offers], tool_events=tool_events)
