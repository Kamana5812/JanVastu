from collections import defaultdict
from datetime import timedelta
from sqlalchemy import func
from app.db.models.needs import Need,NeedStatus
from app.db.models.projects import PlanningContext,Project
from app.db.models.users import now
from app.core.rbac import scoped

INDICATOR_LABEL="JanVastu Analytical Indicator — not an official government metric."

def filtered(query,model,filters):
    for key in ("state","district","locality","ward_village","category"):
        if filters.get(key):query=query.filter(getattr(model,key)==filters[key])
    return query

def dashboard(db,user,filters,days=90):
    cutoff=now()-timedelta(days=days)
    needs=filtered(scoped(db.query(Need),Need,user),Need,filters).filter(Need.created_at>=cutoff).all()
    contexts=filtered(scoped(db.query(PlanningContext),PlanningContext,user),PlanningContext,filters).all()
    pq=filtered(scoped(db.query(Project),Project,user),Project,filters)
    if filters.get("project_status"):pq=pq.filter(Project.status==filters["project_status"])
    projects=pq.all()
    grouped=defaultdict(list)
    def key(row):return (row.state,row.district,row.locality or "",row.ward_village or "",row.category.value if hasattr(row.category,"value") else row.category)
    for n in needs:grouped[key(n)].append(n)
    lookup={key(c):c for c in contexts}
    hotspots=[]
    for area in sorted(set(grouped)|set(lookup)):
        records=grouped[area];context=lookup.get(area)
        demand=sum(1/(max(0,(now()-n.created_at).days)+1) for n in records if n.status!=NeedStatus.rejected)
        stock=context.infrastructure_stock if context else None
        investment=context.planned_investment if context else None
        vulnerability=context.vulnerability if context else None
        denominator=(stock+investment) if context else None
        gap=demand*vulnerability/denominator if denominator and denominator>0 else None
        if context:lat,lon=context.latitude,context.longitude
        elif records:
            lon,lat=db.query(func.ST_X(Need.location),func.ST_Y(Need.location)).filter(Need.id==records[0].id).one()
            lat,lon=round(lat,2),round(lon,2)
        else:continue
        recent=sum(n.created_at>=now()-timedelta(days=7) for n in records)
        previous=sum(now()-timedelta(days=14)<=n.created_at<now()-timedelta(days=7) for n in records)
        hotspots.append(dict(zip(("state","district","locality","ward_village","category"),area))|{
            "latitude":lat,"longitude":lon,"requests":len(records),"demand_intensity":round(demand,4),
            "infrastructure_stock":stock,"planned_investment":investment,"vulnerability":vulnerability,
            "gap_ratio":round(gap,4) if gap is not None else None,"supply_missing":context is None,
            "unbounded":denominator==0 and demand>0,"recent_reports":recent,"previous_reports":previous,
            "is_sample_context":context.is_sample if context else False,
            "independent_signals":len({n.reported_by_id for n in records if n.reported_by_id}),
            "source":context.source if context else "unavailable"})
    hotspots.sort(key=lambda h:(h["unbounded"],h["gap_ratio"] or 0,h["demand_intensity"]),reverse=True)
    counts={s.value:sum(n.status==s for n in needs) for s in NeedStatus}
    locations=[{"id":p.id,"name":p.name,"status":p.status,"latitude":lat,"longitude":lon,"is_sample":p.is_sample}
        for p in projects if p.location is not None for lon,lat in [db.query(func.ST_X(Project.location),func.ST_Y(Project.location)).filter(Project.id==p.id).one()]]
    hierarchy=[{"state":c.state,"district":c.district,"locality":c.locality,"ward_village":c.ward_village} for c in scoped(db.query(PlanningContext),PlanningContext,user).all()]
    return {"label":INDICATOR_LABEL,"days":days,"kpis":{"total":len(needs),"verified":counts["verified"],
        "high_gap":sum(h["unbounded"] or (h["gap_ratio"] or 0)>1 for h in hotspots),
        "active_projects":sum(p.status in ("planned","sanctioned","tendered","awarded","started","in_progress") for p in projects),"resolved":counts["resolved"],
        "pending_review":sum(bool(n.moderation_reason) for n in needs)},
        "sample_requests":sum(n.is_sample for n in needs),"by_status":counts,"hotspots":hotspots,"projects":locations,"hierarchy":hierarchy,
        "data_note":"Operational requests; infrastructure and investment context may be synthetic and is labeled per area."}
