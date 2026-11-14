from __future__ import annotations
import asyncio, json
import streamlit as st
from core.orchestrator import run_review
st.set_page_config(page_title='Automated Code Review Board',layout='wide')
st.title('Automated Code Review Board')
st.caption('CSE476 • Semantic Kernel plugins • deterministic offline static analysis')
left,right=st.columns(2)
with left: diff=st.text_area('Paste Git diff',height=280,placeholder='diff --git a/example.py b/example.py ...')
with right: repo=st.text_input('Optional local repository path'); base=st.text_input('Base branch',value='main'); block=st.checkbox('Block medium findings')
st.info('Fan-out: Style + Security + Test-Coverage agents run concurrently after Diff Agent. Fan-in: Reviewer Manager consolidates them.')
if st.button('Run review',type='primary'):
    try:
        with st.status('Executing Diff → [Style | Security | Coverage] → Manager',expanded=True) as status:
            report=asyncio.run(run_review(diff,repo or None,base,block)); status.update(label='Review complete',state='complete')
        st.subheader(f'{report.recommendation}'); st.write(report.reason)
        cols=st.columns(6); cols[0].metric('Files',report.files_changed); cols[1].metric('Findings',len(report.findings))
        for col,key in zip(cols[2:],['CRITICAL','HIGH','MEDIUM','LOW']): col.metric(key,report.counts[key])
        for finding in report.findings:
            st.markdown(f"**{finding.severity.value}** · `{finding.file_path}:{finding.line_number or '?'}` · {finding.agent_name} — {finding.title}")
            st.caption(f'{finding.description} Fix: {finding.suggested_fix}')
        st.download_button('Download JSON report',json.dumps(report.model_dump(mode='json'),indent=2),file_name='review-report.json',mime='application/json')
    except Exception as exc: st.error(str(exc))
