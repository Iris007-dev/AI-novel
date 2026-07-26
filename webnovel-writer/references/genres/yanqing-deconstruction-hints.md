---
name: yanqing-deconstruction-hints
purpose: 言情类参考书拆解时专用——识别伏笔密度、糖点频率、言情人设组合、反转套路
genre_scope: 古言 | 现言 | 宫斗宅斗 | 青春甜宠 | 豪门总裁 | 狗血言情 | 替身文 | 种田 | 现言脑洞 | 民国言情 | 幻想言情 | 职场婚恋
triggered_by: deconstruction-agent 在题材为言情类时自动加载；webnovel-init Step 1.5 用户选言情参考书时
companion_files: references/genres/yanqing-playbook.md | references/genres/yanqing-characters.md | references/genres/yanqing-chapter-templates.md
---

<context>
此文件用于言情类参考书拆解。deconstruction-agent 在题材为言情类时，加载本文件补充言情专属识别规则。
通用拆书流程见 `agents/deconstruction-agent.md`，本文件不重复，只补充言情特化。
</context>

<instructions>

## 一、言情拆书 6 项必须识别

### 1.1 伏笔密度识别

言情有 ≥3 类伏笔需特别识别：

- **情感伏笔**：埋下"她/他会爱上对方"的理由（前 1/3 卷必须有 ≥5 处）
- **误会伏笔**：埋下"误会的触发条件"
- **真相伏笔**：埋下"身份秘密 / 替身 / 血脉真相"
- **甜点伏笔**：埋下"日后回味的甜时刻"

识别方法：
- Grep 关键词："其实她/他早就..." / "那时的她/他还不知道..." / "多年以后才明白..."
- 找出前 1/3 卷已有伏笔数
- 判断伏笔回收是否对等（前 1/3 伏笔数 ≥后 1/3 回收数 × 2 视为铺设充分）

### 1.2 糖点频率识别

按 `references/genres/yanqing-writer-rules.md` §三·3.1 标准，逐章统计：

- 微触数 / 微甜数 / 微酸数 / 微烫数
- 每 3 章是否有 ≥1 微烫
- 每 30 章是否有 ≥1 组合糖点
- 章末钩子是否全是情感性（非事件性）

输出至 `cool_point_loops` 字段：
```json
{
  "cool_point_loops": [
    {"setup": "前 30 章微烫分布", "release": "中段微烫密度", "reaction_layers": "≥3 种糖点类型", "transition": "糖点类型轮换", "pacing_ratio": "每 3 章 ≥1", "transfer_rule": "复制糖点模式+换题材事件"}
  ]
}
```

### 1.3 言情人设组合识别

按 `references/genres/yanqing-characters.md` 矩阵识别：

- 男主属 M1-M6 哪个？
- 女主属 F1-F6 哪个？
- 两人是 Top 5 推荐组合之一吗？
- 有没有踩人设漂移的坑？

输出至 `protagonist_patterns` 字段。

### 1.4 言情反派识别

按 `references/genres/yanqing-playbook.md` §五·5.8 识别反派：

- 是否满足 4 项（可理解动机/可欣赏能力/可同情过去/可尊重退场）中的 ≥2 项？
- 反派有没有独立的人际圈 / 过去？
- 反派退场是否有尊严？

输出至 `antagonist_pressure_patterns` 字段。

### 1.5 言情反转套路识别

按 `references/genres/yanqing-playbook.md` §二 6 种反转识别：

- R1 真假千金 / R2 重生 / R3 失忆 / R4 复仇 / R5 错位告白 / R6 久别重逢
- 每种反转都被用了多少次？
- 反转的铺垫是否充分（前文 ≥5 章伏笔）？
- 是否有反套路变种？

### 1.6 言情节奏曲线识别

按 `references/genres/yanqing-playbook.md` §四·4.3 6 阶段节奏识别：

```
建立期（第 1-10 章）→ 拉扯期（11-30）→ 确认期（31-50）→ 考验期（51-70）→ 爆发期（71-85）→ 甜蜜期/新平衡（86-100）
```

按此阶段识别参考书所属阶段：
- 阶段 1-3 在前 1/2 卷？
- 阶段 4-6 在后 1/2 卷？
- 每阶段是否有标志事件（第一次心动 / 表白 / 大考验 / 真相 / 大婚）？

## 二、言情专属差异化要求

拆解言情书时，必须显式给出以下**差异化要求**（初始化时强制提示用户）：

### 2.1 反套路变种

每种借用的模式必须配 ≥1 条反套路变种：

```
例：
- ✅ 借用"破镜重圆"模式 + 反套路：让女主先放手，让男主追回来（不是双方同时回头）
- ✅ 借用"病娇男主"人设 + 反套路：让男主有"让步"时刻（不是完美情人）
- ✅ 借用"白月光"反派 + 反套路：让白月光反衬女主更好（不是单纯嫉妒）
```

### 2.2 不能复制的元素

言情书最容易"复制粘贴"的有毒元素：

- ❌ 男主深情但无独立人格 → ✅ 男主必须有 ≥2 个独立兴趣/事业/人际圈
- ❌ 女主圣母讨人喜欢 → ✅ 女主必须有 ≥1 次让读者"她其实很复杂"的瞬间
- ❌ 反派只是"嫉妒女主" → ✅ 反派必须有 4 项中的 ≥2 项（见 §1.4）
- ❌ 情感靠直白宣告 → ✅ 必须靠行为/生理/物体暗示
- ❌ 章末全是事件钩子 → ✅ 必须有 ≥70% 情感性钩子

### 2.3 题材适配

言情拆解必须给出**适配到目标题材**的映射：

```
例：拆《何以笙箫默》（现言甜宠）→ 用于《古言权谋》写作
映射：
- ❌ 不能复制：律所 / 现代都市 / 摄影专业
- ✅ 适配：朝堂律法 / 古风都市 / 鉴赏专业
- 反派：从"何以玫"映射为"太后党羽"
- 糖点映射：从"等候 7 年"映射为"被迫和亲后重逢"
```

## 三、言情拆书禁区清单

deconstruction-agent 在言情类拆解时，**显式禁止**以下行为：

1. ❌ 把参考书女主名 / 男主名 / 地名直接复制到新书
2. ❌ 把参考书的家族 / 势力 / 门派名复制
3. ❌ 把参考书的"具体情感事件"复制到新书设定（如"等了 7 年"）
4. ❌ 把参考书的"金手指"或"特殊能力"复制
5. ❌ 把参考书的"具体礼仪规范"复制

允许的是：
- ✅ 抽象模式（"先建立信任再表白"）
- ✅ 情绪曲线（"甜中带虐再甜"）
- ✅ 结构骨架（"卷二陌生人 / 卷三表白 / 卷四考验"）

## 四、与言情包联动

deconstruction-agent 加载本文件后，输出 JSON 必须额外包含：

```json
{
  "yanqing_metadata": {
    "sugar_density_observed": "每 3 章 N 个微烫 / 每章 M 个微触",
    "yanqing_male_archetype_detected": "M1-M6 之一",
    "yanqing_female_archetype_detected": "F1-F6 之一",
    "yanqing_combination_detected": "F_x × M_y",
    "yanqing_combination_score": 1-5,
    "yanqing_villain_quality": "4 项命中数",
    "yanqing_red_line_violations": ["已观察到的反 AI 协议违反"],
    "yanqing_phases_detected": ["建立期", "拉扯期", ...]
  }
}
```

此 metadata 供 init 主流程直接读取，避免二次分析。

## 五、AI 执行指令

1. **拆解前必读**：题材为言情类时，deconstruction-agent 必须 Read 本文件后再开始拆解。
2. **6 项识别必做**：§一 的 6 项必须全部识别并输出，禁止跳过。
3. **差异化必输出**：§二 的差异化要求必须出现在 `differentiation_requirements` 字段。
4. **禁区清单必输出**：§三 的禁区清单必须出现在 `do_not_copy` 字段。
5. **metadata 必填**：§四 的 `yanqing_metadata` 必须输出到 init_reference_research JSON 顶层。
6. **降级保护**：如果参考书无法识别任何言情人设/糖点/反派，必须在 `quality.passed=false` 的同时输出 `yanqing_metadata.gaps_detected` 提示用户。

</instructions>

<examples>

<example>
<input>用户想拆《何以笙箫默》（现言甜宠）用于新书</output>
<target_genre>古言甜宠</target_genre>

</input>
<output>

**yanqing_metadata 识别结果**：

```json
{
  "yanqing_metadata": {
    "sugar_density_observed": "前 30 章 8 个微烫 / 平均每章 1.2 个微触",
    "yanqing_male_archetype_detected": "M6 暗涌隐忍",
    "yanqing_female_archetype_detected": "F2 聪慧冷静",
    "yanqing_combination_detected": "F2 × M6",
    "yanqing_combination_score": 5,
    "yanqing_villain_quality": "命中 3/4（可理解动机 / 可同情过去 / 可尊重退场）",
    "yanqing_red_line_violations": [],
    "yanqing_phases_detected": ["建立期", "拉扯期", "确认期", "考验期", "爆发期"]
  }
}
```

**§二·2.2 不能复制的元素**：
- ❌ 不能复制：何以琛的"律师"职业 → ✅ 古言版可改为"朝堂律官"或"大理寺少卿"
- ❌ 不能复制：赵默笙的"摄影专业" → ✅ 古言版可改为"画师"或"医女"
- ❌ 不能复制：以琛默笙等待 7 年的具体时间 → ✅ 古言版可用"被迫和亲后重逢"

**§二·2.3 题材适配**：
- 反派：从"何以玫"映射为"郡主"
- 糖点模式：从"等候 7 年"映射为"被迫和亲后重逢"
- 误会伏笔：从"默笙父亲害何以琛父亲"映射为"女主父亲曾得罪男主家族"

**§三 禁区清单输出到 do_not_copy**：
1. "何以琛" / "赵默笙" / "何以玫" / "路远风" 等角色名
2. 律师事务所 / 摄影专业 / 美国留学等具体背景
3. "等了 7 年"这一具体情感事件

**推荐反套路变种**：从"默笙失忆"借鉴—但让她记得（反方向）。
