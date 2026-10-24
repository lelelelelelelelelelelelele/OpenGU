def figures(endpoints,contrasts,cs_summary):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import numpy as np
    plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False,'pdf.fonttype':42})
    def save(fig,name):
        fig.savefig(OUT/(name+'.png'),dpi=180,bbox_inches='tight');fig.savefig(OUT/(name+'.pdf'),bbox_inches='tight');plt.close(fig)
    fig,axes=plt.subplots(2,2,figsize=(10.5,7),sharex=True,sharey=True)
    styles=[('original','published','#1768ac','o',-.07),('retained','published','#dd6b20','s',-.02),('original','raw','#1768ac','^',.03),('retained','raw','#dd6b20','D',.08)]
    for i,method in enumerate(('GIF','MEGU')):
        for j,baseline in enumerate(('random','degree')):
            ax=axes[i,j]
            for graph,kind,color,marker,offset in styles:
                if method=='GIF' and kind=='raw':continue
                rr=sorted([r for r in contrasts if r['method']==method and r['right']==baseline and r['graph']==graph and r['triangle']==kind],key=lambda r:float(r['ratio']))
                assert len(rr)==2
                ax.errorbar(np.arange(2)+offset,[r['gu_retrain_disagreement_delta_pp_mean'] for r in rr],yerr=[r['gu_retrain_disagreement_delta_pp_sd'] for r in rr],label=graph+'/'+kind,color=color,marker=marker,linestyle='-' if kind=='published' else '--',capsize=3,lw=1.5)
            ax.axhline(0,color='#64748b',lw=.7);ax.set_xticks([0,1]);ax.set_xticklabels(['5%','33%']);ax.set_title(method+': R-point minus '+baseline.title());ax.grid(axis='y',alpha=.18)
            if j==0:ax.set_ylabel('Difference in GU-Ret D (pp)')
            if i==1:ax.set_xlabel('Deletion budget')
    handles,labels=axes[1,0].get_legend_handles_labels();fig.legend(handles,labels,loc='lower center',ncol=4,bbox_to_anchor=(.5,-.01));fig.suptitle('Fixed-weight graph and MEGU postprocessing controls | CiteSeer')
    fig.tight_layout(rect=(0,.05,1,.95));save(fig,'strategy_graph_controls')
    fig,axes=plt.subplots(2,2,figsize=(11,7.5),sharex=True)
    order=[(s,r) for r in ('0.05','0.33') for s in ('random','degree','r_point')]
    colors=['#238b45','#cb4545','#94a3b8'];labels=['Ret corrects O/G','Ret harms O/G','Both predictions wrong']
    for i,method in enumerate(('GIF','MEGU')):
        for j,graph in enumerate(('original','retained')):
            ax=axes[i,j];left=np.zeros(6)
            for metric,color,label in zip(('ret_only_corrects_pct','ret_only_harms_pct','ret_only_both_wrong_pct'),colors,labels):
                means=[stats.mean(number(x,metric) for x in endpoints if (x['method'],x['graph'],x['triangle'],x['selector'],x['ratio'])==(method,graph,'published',selector,ratio)) for selector,ratio in order]
                ax.barh(np.arange(6),means,left=left,color=color,label=label);left+=np.asarray(means)
            ax.set_yticks(np.arange(6));ax.set_yticklabels([s.replace('r_point','R-point').title()+' '+str(int(float(r)*100))+'%' for s,r in order]);ax.invert_yaxis();ax.set_title(method+' / '+graph+' graph');ax.grid(axis='x',alpha=.15)
            if i==1:ax.set_xlabel('Test nodes in O = GU != Ret (%)')
    handles,labels=axes[0,0].get_legend_handles_labels();fig.legend(handles,labels,loc='lower center',ncol=3,bbox_to_anchor=(.5,-.01));fig.suptitle('Truth decomposition of the Ret-only prediction change | published pipeline')
    fig.tight_layout(rect=(0,.05,1,.95));save(fig,'ret_only_truth')
    fig,axes=plt.subplots(1,2,figsize=(11,5.5),sharey=True)
    effects=[('cs_gu_ret_D_change_pp','Updated C&S: GU-Ret D','#7851a9'),('matched_minus_published_OG_D_pp','Matched Original C&S: O-GU D','#1768ac'),('matched_minus_published_OR_D_pp','Matched Original C&S: O-Ret D','#dd6b20')]
    for ax,graph in zip(axes,('original','retained')):
        for k,(metric,label,color) in enumerate(effects):
            rr=[next(r for r in cs_summary if (r['graph'],r['selector'],r['ratio'])==(graph,s,ratio)) for s,ratio in order]
            ax.errorbar([r[metric+'_mean'] for r in rr],np.arange(6)+(k-1)*.17,xerr=[r[metric+'_sd'] for r in rr],fmt='o',capsize=2,label=label,color=color)
        ax.axvline(0,color='#64748b',lw=.8);ax.set_yticks(np.arange(6));ax.set_yticklabels([s.replace('r_point','R-point').title()+' '+str(int(float(r)*100))+'%' for s,r in order]);ax.set_title(graph.title()+' graph');ax.set_xlabel('Change caused by specified C&S comparison (pp)');ax.grid(axis='x',alpha=.15)
    axes[0].invert_yaxis()
    handles,labels=axes[0].get_legend_handles_labels();fig.legend(handles,labels,loc='lower center',ncol=1,bbox_to_anchor=(.5,-.07));fig.suptitle('MEGU four-endpoint controls | mean and sample SD across 3 joint runs')
    fig.tight_layout(rect=(0,.12,1,.94));save(fig,'megu_cs_controls')
