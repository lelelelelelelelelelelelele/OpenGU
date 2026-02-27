📊 各图质量对比分析
旧版图（report/paper/figures/）
fig1_gnndelete_ratio.png — GNNDelete F1 Drop vs Ratio（柱状图）

✅ 配色区分清晰，6种策略用不同颜色
✅ 有 Avg Random Drop 参考基准线（dashed）
❌ 致命问题：random 策略柱子几乎看不到（和 baseline dashed line 重叠，存在感近零），这实际揭示了数据本身的非单调性问题，但呈现上让读者困惑
❌ 柱组之间过于拥挤，4个ratio × 6个策略 = 24柱，视觉噪声大
❌ 标题过于描述性，不够论文化
fig2_grapheraser_shard.png — GraphEraser Shard Protection（箱线图）

✅ 箱线图很直观，展现 Before/After Unlearn 的对比
✅ 离群点标注清晰
❌ 核心问题：After Unlearn 普遍高于 Before，说明 GraphEraser 有 "protection/repair" 效果，但图表没有任何文字解释这个反常现象
❌ 颜色（绿/橙）对色盲用户不友好，且两色过于相近
fig3_relative_f1_drop.png — 多方法综合柱状图

❌ 最差的图：X轴标签 45° 旋转，13组方法密密麻麻排列，极难阅读
❌ 6种策略中 random/degree/pagerank 的柱子极小（几乎为0），浪费空间
❌ 误差棒有时比柱子本身高，说明数据方差很大
❌ 这张图承载了太多信息，一张图里有13个method×config组合
fig_supp_gif_ratio.png — GIF Ratio 折线图

✅ 折线图比柱状图更适合展示 ratio 变化趋势
⚠️ 所有线都汇聚到一起，差异模糊（GIF 本身对攻击不敏感，导致线条紧密）
❌ 没有 shaded area（置信区间）
❌ random 线几乎是最高的，与预期（random应该是低点）不符，说明数据或指标定义问题
新版图（results/paper_figures/）
FIG-1 Generalization — 分组柱状图（多子图）

✅ 用 facet 分面（GIF / GNNDelete / GraphEraser），叙事清晰
✅ 连续色阶（深蓝→绿），视觉上传达"策略升级"概念
❌ 问题：3个子图 x 轴宽度非常不均匀——GNNDelete 的 cora-GAT 有巨大柱子，GIF 的柱子几乎看不见，对比时视觉重心偏向 GNNDelete，可能误导读者
❌ random 和 degree 的柱子几乎为0，占用图例空间却贡献少
FIG-2 Scaling — 双子图折线图

✅ 最清晰的一张图！折线图 + 双方法对比，叙事流畅
✅ 排除了 random baseline 专注算法策略对比（符合 visualization_plan）
❌ 两个子图 y 轴范围完全不同（GIF 0-4%，GNNDelete 0-17.5%），没有统一，比较时容易误判
❌ X 轴刻度不对齐（GIF 子图从 0.01 开始，但 0 标签存在），轻微误导
FIG-3 Spectrum — 简洁分组柱状图

✅ 最好的一张图！只保留3种关键策略（TracIn/IM/Hybrid），数字标注清晰
✅ 方法排序直观（从低到高漏洞：GIF→GNNDelete）
❌ 缺少误差棒（没有不确定性信息），学术论文需要置信区间
❌ 只有 Cora-GCN 数据，如果这是 "Universal Vulnerability" 谱，应该更好地区分该是哪个数据集/模型配置
FIG-4 Significance — 热图

✅ 热图选择好，颜色编码清晰（深红=高显著）
✅ 数值直接标注（-log10 p-value）
❌ 颜色范围问题：colorbar 从 -1.0 到 4.0，但没有标 α=0.05 对应的显著性阈值线（-log10(0.05)≈1.3），读者不知道哪些格子满足统计显著
❌ MEGU 行两个格子（0.94, 0.99）低于 1.3（即p>0.05），但颜色上看起来仍然"正常"，没有视觉区分
FIG-5 Collateral — 散点图

✅ 概念设计非常好（攻击水深 vs 模仿质量）
✅ 右下角 target region 绿色阴影区设计有创意
❌ 核心问题（与上一会话分析一致）：几乎没有点落在 target region（bottom-right），说明当前攻击方法不够完美，这既是数据的实际情况，也是图的弱点
❌ 标注文字密集重叠（左下角 "IDEA/hybrid_v4" 等多点叠在一起）
❌ 图例太大（占据右侧 1/3 空间），压缩了散点的展示空间
🏆 综合排名（论文可用性）
排名	图	评分	理由
🥇 1	FIG-3 Spectrum	9/10	信息密度适中，叙事清晰，数字标注好
🥈 2	FIG-2 Scaling	8/10	折线图最适合 ratio 分析，排除 random 策略对
🥉 3	FIG-4 Significance	7.5/10	热图选择正确，需加显著性阈值线
4	FIG-1 Generalization	7/10	分面设计好，但柱子高度差异悬殊影响视觉平衡
5	FIG-5 Collateral	6/10	概念好但数据不支持，图例过大，标注拥挤
6	fig2_grapheraser_shard	5.5/10	箱线图选择好，但没解释反常现象
7	fig1_gnndelete_ratio	5/10	柱状图太密，random 消失
8	fig_supp_gif_ratio	4.5/10	线条太密集，差异不明显
9	fig3_relative_f1_drop	3/10	信息过载，X 轴不可读
🔧 具体改进建议
高优先级（直接影响 paper 质量）
FIG-3（最重要，但需改进）：

添加误差棒（跨 seed 的 std）
在图题或副标题注明数据来自 Cora-GCN
FIG-4（统计图必须修）：

# 在 colorbar 旁加一条显著性分界线
ax.axhline(y=-np.log10(0.05), color='black', linestyle='--', label='p=0.05')
# 或者用不同底色标注 p>0.05 的格子
用灰色或交叉线标注不显著的格子（MEGU行）
FIG-5（概念需重思）：

如果 target region 内几乎没有点，要么移除该 target region，要么换讨论逻辑：改为说"我们的攻击（bottom-left 的 GraphEraser 点)做到了低 collateral，同时高 drop"
考虑分两个子图：一个是有数据标注的（GNNDelete），一个是紧凑型（其他方法）
中优先级
FIG-1：

统一3个子图 y 轴范围（或至少对齐刻度比例）
考虑去掉 random/degree 策略柱子（它们几乎为零），减少视觉噪声，只保留 tracin / im_v4 / hybrid_v4
FIG-2：

两子图 y 轴统一到相同范围，让读者直观感受二者差异
添加 shaded area（如果有多 seed 数据）
低优先级（格式优化）
所有新版图：

字体大小统一（建议正文12pt，标题14pt）
colormap 使用论文友好色盲方案（如 viridis 或 RdYlBu）
导出 PDF 时确认字体嵌入（plt.rcParams['pdf.fonttype'] = 42）
总结
新版 FIG-1~5 整体远优于旧版图，应以 results/paper_figures/ 为论文正式图。旧版图可以作为分析草稿保留，但不应直接用于投稿。当前最需要修复的是 FIG-4（缺显著性阈值） 和 FIG-5（target region 内无点的逻辑矛盾）。

