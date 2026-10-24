# GU–Ret参考敏感性：pilot

全部预定GIF/MEGU条件与old-final/new-final/best比较；表中正值表示R-point分歧高于相应基线，单位为百分点。

change_in_request_contrast_vs_oldfinal_pp是相同seed/method的请求差相对旧参考的改变量。每一对D、CE及双方accuracy在上级gu_reference_pairs.csv中，全部类别和四格整数分别在gu_reference_classes.csv及gu_reference_correctness.csv。

科学状态：stop_unexplained_final_difference。如新旧final不可解释，所有数值仅用于定位差异，不得据此开始机制推断。

只读保存预测，没有训练或forward；MEGU为保存的updated+C&S。类别解释为post-hoc descriptive。33%参考敏感性不等于5%→33%在新参考下的完整预算交互。

| seed | method | baseline | checkpoint_role | rpoint_minus_baseline_disagreement_pp | change_in_request_contrast_vs_oldfinal_pp |
| --- | --- | --- | --- | --- | --- |
| 42 | GIF | random | old_final | 17.267267 | 0.000000 |
| 42 | GIF | random | final | 17.717718 | 0.450450 |
| 42 | GIF | random | best | 13.063063 | -4.204204 |
| 42 | GIF | degree | old_final | 20.870871 | 0.000000 |
| 42 | GIF | degree | final | 21.171171 | 0.300300 |
| 42 | GIF | degree | best | 15.465465 | -5.405405 |
| 42 | MEGU | random | old_final | 18.918919 | 0.000000 |
| 42 | MEGU | random | final | 19.969970 | 1.051051 |
| 42 | MEGU | random | best | 14.864865 | -4.054054 |
| 42 | MEGU | degree | old_final | 21.321321 | 0.000000 |
| 42 | MEGU | degree | final | 22.372372 | 1.051051 |
| 42 | MEGU | degree | best | 16.666667 | -4.654655 |
