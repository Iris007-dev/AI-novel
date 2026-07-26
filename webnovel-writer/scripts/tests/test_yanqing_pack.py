#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for the yanqing ("言情")强化包.

This pack ships:
1. agents/cross-chapter-reviewer.md — 跨章一致性审查
2. references/genres/yanqing-playbook.md — 言情专属爽点/反转/糖点指南
3. references/shared/strand-weave-pattern.md — 言情变体小节
4. skills/webnovel-write/SKILL.md — 集成到写章流程

这些测试只做静态文件检查，不依赖 Claude Code 运行时，
确保 4 个新文件/改动确实存在且符合 schema。
"""

import json
import re
from pathlib import Path

import pytest

PLUGIN_ROOT = Path(__file__).resolve().parents[2]
AGENTS_DIR = PLUGIN_ROOT / "agents"
REFERENCES_DIR = PLUGIN_ROOT / "references"
SHARED_REFS = REFERENCES_DIR / "shared"
GENRES_REFS = REFERENCES_DIR / "genres"
SKILLS_DIR = PLUGIN_ROOT / "skills"


def _read(path: Path) -> str:
    """Read a UTF-8 file, fail with helpful message if missing."""
    assert path.exists(), f"Expected file not found: {path}"
    return path.read_text(encoding="utf-8")


def _parse_frontmatter(path: Path) -> dict:
    """Parse a YAML-ish frontmatter block at the top of a markdown file.

    Returns a flat dict with string values. Sufficient for our schema checks.
    """
    text = _read(path)
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    assert m, f"No frontmatter in {path}"
    fm = {}
    for line in m.group(1).splitlines():
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        fm[key.strip()] = value.strip()
    return fm


# ============================================================
# 1. cross-chapter-reviewer agent
# ============================================================

class TestCrossChapterReviewerAgent:
    """Verify agents/cross-chapter-reviewer.md exists and is well-formed."""

    AGENT_PATH = AGENTS_DIR / "cross-chapter-reviewer.md"

    def test_file_exists(self):
        assert self.AGENT_PATH.exists()

    def test_frontmatter_has_required_keys(self):
        fm = _parse_frontmatter(self.AGENT_PATH)
        assert fm.get("name") == "cross-chapter-reviewer"
        assert "description" in fm
        assert "tools" in fm
        assert "color" in fm

    def test_defines_five_categories(self):
        """agent must define 5 issue categories."""
        text = _read(self.AGENT_PATH)
        for cat in ("unresolved_loop", "broken_promise", "rule_contradiction",
                    "relationship_drift", "timeline_jump"):
            assert cat in text, f"missing category: {cat}"

    def test_defines_yanqing_red_lines(self):
        """言情专属红线 must be present."""
        text = _read(self.AGENT_PATH)
        for marker in ("情感专一性", "人设连续性", "糖点频率", "反派功能性"):
            assert marker in text, f"missing yanqing red line: {marker}"

    def test_output_schema_is_strict_json(self):
        text = _read(self.AGENT_PATH)
        # Requirement: output must include chapter, issues, blocking_count, has_blocking
        for field in ("chapter", "issues", "issues_count", "blocking_count",
                      "has_blocking", "dimension_results", "summary"):
            assert f'"{field}"' in text, f"output schema missing: {field}"

    def test_does_not_score_artifacts(self):
        """agent must not output overall_score (parity with reviewer)."""
        text = _read(self.AGENT_PATH)
        assert "不评分" in text
        assert "overall_score" not in text or "不输出 overall_score" in text


# ============================================================
# 2. yanqing-playbook
# ============================================================

class TestYanqingPlaybook:
    """Verify references/genres/yanqing-playbook.md is complete."""

    PLAYBOOK_PATH = GENRES_REFS / "yanqing-playbook.md"

    def test_file_exists(self):
        assert self.PLAYBOOK_PATH.exists()

    def test_has_frontmatter_with_genre_scope(self):
        fm = _parse_frontmatter(self.PLAYBOOK_PATH)
        assert "genre_scope" in fm
        # Must cover at least 古言 and 现言
        for required in ("古言", "现言", "言情"):
            assert required in fm["genre_scope"], f"genre_scope missing: {required}"

    def test_defines_six_yanqing_cool_points(self):
        text = _read(self.PLAYBOOK_PATH)
        expected = [
            "暗涌式心动", "反差式沦陷", "误会式心疼",
            "公费式撒糖", "身份式碾压", "深情式回响",
        ]
        for cp in expected:
            assert cp in text, f"missing yanqing cool point: {cp}"

    def test_defines_six_yanqing_reversals(self):
        text = _read(self.PLAYBOOK_PATH)
        # R1..R6 markers
        for marker in ("R1.", "R2.", "R3.", "R4.", "R5.", "R6."):
            assert marker in text, f"missing reversal: {marker}"

    def test_defines_four_sugar_types(self):
        """微触 / 微甜 / 微酸 / 微烫."""
        text = _read(self.PLAYBOOK_PATH)
        for s in ("微触", "微甜", "微酸", "微烫"):
            assert s in text, f"missing sugar type: {s}"

    def test_has_density_table(self):
        """Must include sugar density rules (per-chapter/per-3/per-10)."""
        text = _read(self.PLAYBOOK_PATH)
        for period in ("逐章", "每 3 章", "每 10"):
            assert period in text, f"density rule missing: {period}"

    def test_has_hundred_chapter_template(self):
        text = _read(self.PLAYBOOK_PATH)
        # 100 章情感节奏模板 must cover the 5 main phases
        for phase in ("建立期", "拉扯期", "确认期", "考验期", "爆发期"):
            assert phase in text, f"phase missing: {phase}"
        # Last band must include 甜蜜 or 新平衡
        last_band = text.split("第 71-85 章")[1] if "第 71-85 章" in text else ""
        assert "甜蜜" in last_band or "新平衡" in last_band, \
            "last band must include 甜蜜期 or 新平衡期"

    def test_has_anti_ai_protocol(self):
        """情感真实度协议 (5.1-5.5) must be present."""
        text = _read(self.PLAYBOOK_PATH)
        for marker in ("不直白", "不悬浮", "不工具人", "不完美主义", "不滥用巧合"):
            assert marker in text, f"anti-AI rule missing: {marker}"

    def test_has_ai_execution_directives(self):
        """Section 六 AI 执行指令 must have 5 directives."""
        text = _read(self.PLAYBOOK_PATH)
        for n in range(1, 6):
            assert f"{n}." in text, f"directive {n} missing"


# ============================================================
# 3. strand-weave-pattern.md 言情变体
# ============================================================

class TestStrandWeaveYanqingVariant:
    """Verify the 言情变体 section was added to strand-weave-pattern.md."""

    STRAND_PATH = SHARED_REFS / "strand-weave-pattern.md"

    def test_file_exists(self):
        assert self.STRAND_PATH.exists()

    def test_yanqing_section_header_present(self):
        text = _read(self.STRAND_PATH)
        assert "言情变体" in text

    def test_lists_yanqing_genre_scope(self):
        text = _read(self.STRAND_PATH)
        for g in ("古言", "现言", "宫斗宅斗", "青春甜宠",
                  "豪门总裁", "狗血言情", "替身文", "种田"):
            assert g in text, f"genre scope missing: {g}"

    def test_yanqing_strand_ratio(self):
        """Fire 45-55%, Quest 30-40%, Constellation 15-20%."""
        text = _read(self.STRAND_PATH)
        assert "45-55%" in text, "Fire 占比 45-55% missing"
        assert "30-40%" in text, "Quest 占比 30-40% missing"
        assert "15-20%" in text, "Constellation 占比 15-20% missing"

    def test_yanqing_warning_thresholds(self):
        """Quest 不连续 >3, Fire >2 章未出现, Constellation >8 章未出现."""
        text = _read(self.STRAND_PATH)
        assert "3 章" in text
        assert "2 章未出现" in text
        assert "8 章未出现" in text

    def test_has_thirty_chapter_yanqing_template(self):
        text = _read(self.STRAND_PATH)
        # The new template must redefine 前 30 章
        assert "言情前 30 章织网模板" in text

    def test_yanqing_phase_field(self):
        """strand_tracker extension must include yanqing_phase."""
        text = _read(self.STRAND_PATH)
        assert "yanqing_phase" in text
        assert "secondary" in text


# ============================================================
# 4. webnovel-write SKILL.md integration
# ============================================================

class TestSkillIntegration:
    """Verify webnovel-write/SKILL.md pulls everything together."""

    SKILL_PATH = SKILLS_DIR / "webnovel-write" / "SKILL.md"

    def test_step_1_5_yanqing_trigger(self):
        """Step 1.5 言情题材判定 must be present."""
        text = _read(self.SKILL_PATH)
        assert "言情题材判定" in text
        assert "yanqing-playbook.md" in text

    def test_step_3_5_cross_chapter_review(self):
        """Step 3.5 cross-chapter-reviewer integration must be present."""
        text = _read(self.SKILL_PATH)
        assert "Step 3.5" in text
        assert "cross-chapter-reviewer" in text

    def test_hard_rules_include_yanqing(self):
        text = _read(self.SKILL_PATH)
        # The hard rules section must explicitly mention yanqing
        assert "yanqing-playbook.md" in text
        # And the genre list
        for g in ("古言", "现言", "宫斗宅斗", "青春甜宠",
                  "豪门总裁", "狗血言情", "替身文", "种田"):
            assert g in text, f"hard rules missing genre: {g}"

    def test_cross_chapter_consumes_genre(self):
        """Step 3.5 must pass genre to the agent."""
        text = _read(self.SKILL_PATH)
        # The Skillmd must wire `genre` into the cross-chapter-reviewer task
        idx = text.find("cross-chapter-reviewer")
        assert idx > 0
        snippet = text[idx:idx + 1500]
        assert "genre" in snippet

    def test_no_regression_existing_steps(self):
        """Existing 6-step pipeline must still be intact."""
        text = _read(self.SKILL_PATH)
        for step in ("Step 1", "Step 2", "Step 3", "Step 4", "Step 5", "Step 6"):
            assert step in text, f"regression: {step} missing"


# ============================================================
# Round 2 additions:
# - 4 份言情流派模板的 §9 言情套件
# - yanqing-playbook §五 扩展到 8 段
# - yanqing-characters.md 人设 36 组合
# - webnovel-init Step 3.5 言情人设推荐
# ============================================================

GENRES_DIR_TPL = PLUGIN_ROOT / "templates" / "genres"
INIT_SKILL_PATH = SKILLS_DIR / "webnovel-init" / "SKILL.md"


class TestYanqingGenreTemplates:
    """Verify 4 份言情流派模板已加 §9 言情套件."""

    EXPECTED = ["现言脑洞.md", "豪门总裁.md", "替身文.md", "青春甜宠.md"]

    def test_all_files_exist(self):
        for name in self.EXPECTED:
            assert (GENRES_DIR_TPL / name).exists(), f"missing: {name}"

    def test_each_template_has_yanqing_section(self):
        for name in self.EXPECTED:
            text = _read(GENRES_DIR_TPL / name)
            assert "## 9. 言情套件" in text, f"{name} missing §9 言情套件"

    def test_each_template_references_playbook(self):
        for name in self.EXPECTED:
            text = _read(GENRES_DIR_TPL / name)
            assert "yanqing-playbook.md" in text, f"{name} must reference playbook"

    def test_present_path_is_correct_no_typo(self):
        """Regress against the 'yanr*ies' typo found in earlier draft."""
        text = _read(GENRES_DIR_TPL / "豪门总裁.md")
        assert "yanries" not in text, "typo 'yanries' leaked into template"
        assert "references/genres/yanqing-playbook.md" in text

    def test_strand_ratios_are_yanqing_aligned(self):
        """Templates must include a Strand 配比 table with Fire >= 45%."""
        for name in self.EXPECTED:
            text = _read(GENRES_DIR_TPL / name)
            # Look for a Fire ratio in the 45-55% range
            assert "45%" in text or "50%" in text or "55%" in text, \
                f"{name} Fire 占比 < 45% (不符合言情 strand 配比)"


class TestYanqingPlaybookRound2:
    """Verify §五 extended to 8 段."""

    PLAYBOOK_PATH = GENRES_REFS / "yanqing-playbook.md"

    def test_section_5_has_eight_subsections(self):
        text = _read(self.PLAYBOOK_PATH)
        for n in range(1, 10):
            marker = f"### 5.{n}"
            assert marker in text, f"§5.{n} missing"

    def test_new_subsections_present(self):
        text = _read(self.PLAYBOOK_PATH)
        for marker in ("5.6 不悬空台词", "5.7 不靠巧合恋爱",
                       "5.8 不忽视反派动机", "5.9 不滥用巧合反转"):
            assert marker in text, f"missing: {marker}"

    def test_5_7_has_two_examples_minimum(self):
        text = _read(self.PLAYBOOK_PATH)
        # §5.7 不靠巧合恋爱 must have at least 2 ❌ examples
        sec_start = text.find("### 5.7")
        sec_end = text.find("### 5.8")
        section = text[sec_start:sec_end]
        assert section.count("❌") >= 2, "§5.7 needs ≥2 反例"
        assert section.count("✅") >= 1, "§5.7 needs ≥1 正确示例"

    def test_5_8_lists_four_villain_traits(self):
        text = _read(self.PLAYBOOK_PATH)
        sec_start = text.find("### 5.8")
        sec_end = text.find("### 5.9")
        section = text[sec_start:sec_end]
        for marker in ("可被理解的动机", "可被欣赏的能力",
                       "可被同情的过去", "可被尊重的退场"):
            assert marker in section, f"§5.8 missing villain trait: {marker}"


class TestYanqingCharactersMatrix:
    """Verify yanqing-characters.md has the 6×6 matrix and supporting structure."""

    CHARS_PATH = GENRES_REFS / "yanqing-characters.md"

    def test_file_exists(self):
        assert self.CHARS_PATH.exists()

    def test_has_frontmatter(self):
        fm = _parse_frontmatter(self.CHARS_PATH)
        assert fm.get("name") == "yanqing-characters"

    def test_defines_six_male_types(self):
        text = _read(self.CHARS_PATH)
        for m in ("M1 高冷", "M2 温柔", "M3 痞气", "M4 病娇", "M5 权谋", "M6 暗涌"):
            assert m in text, f"missing male type: {m}"

    def test_defines_six_female_types(self):
        text = _read(self.CHARS_PATH)
        for f in ("F1 坚韧", "F2 聪慧", "F3 白月光", "F4 反差", "F5 救赎", "F6 双强"):
            assert f in text, f"missing female type: {f}"

    def test_has_36_combination_matrix(self):
        """Top-5 推荐 + 高风险组合 + 完整 6×6 表."""
        text = _read(self.CHARS_PATH)
        assert "Top 5" in text or "推荐组合 Top 5" in text
        assert "高风险组合" in text
        # Each combination should have a star rating; verify ★★★★★ shows up at least 5 times
        assert text.count("★★★★★") >= 5, "should have ≥5 五星组合"

    def test_has_sugar_focus_table(self):
        text = _read(self.CHARS_PATH)
        assert "糖点聚焦方向" in text or "糖点聚焦" in text
        # Must mention each sugar focus type
        for marker in ("少言多行", "细节糖", "互怼糖", "张力糖", "信任糖", "知情糖"):
            assert marker in text, f"missing sugar focus: {marker}"

    def test_has_villain_config_table(self):
        text = _read(self.CHARS_PATH)
        assert "反派配置" in text

    def test_has_relationship_stage_map(self):
        """§六 关系阶段与糖点映射 must have 6 stages."""
        text = _read(self.CHARS_PATH)
        for stage in ("陌生人", "暧昧", "心动", "考验", "真相", "新平衡"):
            assert stage in text, f"missing stage: {stage}"


class TestInitSkillIntegration:
    """Verify webnovel-init/SKILL.md auto-loads yanqing pack for 言情题材."""

    def test_step_3_5_yanqing_section(self):
        text = _read(INIT_SKILL_PATH)
        assert "Step 3.5" in text
        assert "言情人设组合推荐" in text

    def test_step_3_5_loads_characters_matrix(self):
        text = _read(INIT_SKILL_PATH)
        assert "yanqing-characters.md" in text

    def test_step_3_5_loads_genre_template(self):
        text = _read(INIT_SKILL_PATH)
        assert "templates/genres/" in text

    def test_step_3_5_persists_character_archetype(self):
        text = _read(INIT_SKILL_PATH)
        assert "character_archetype" in text
        assert "selected_idea" in text

    def test_step_3_5_has_high_risk_warning(self):
        text = _read(INIT_SKILL_PATH)
        assert "高风险" in text

    def test_writeskill_loads_characters_matrix(self):
        text = _read(SKILLS_DIR / "webnovel-write" / "SKILL.md")
        assert "yanqing-characters.md" in text


# ============================================================
# Round 3 additions:
# - 10 种言情章节模板
# - 言情写章硬指标
# - 6 流派模板 §9（5 个剩余）
# - 4 个言情专属 cross-chapter issue category
# ============================================================

CROSS_CHAPTER_AGENT = AGENTS_DIR / "cross-chapter-reviewer.md"


class TestYanqingChapterTemplates:
    """Verify references/genres/yanqing-chapter-templates.md exists with 10 types."""

    TPL_PATH = GENRES_REFS / "yanqing-chapter-templates.md"

    def test_file_exists(self):
        assert self.TPL_PATH.exists()

    def test_has_frontmatter(self):
        fm = _parse_frontmatter(self.TPL_PATH)
        assert fm.get("name") == "yanqing-chapter-templates"

    def test_defines_all_ten_chapter_types(self):
        """10 章型必须全部存在."""
        text = _read(self.TPL_PATH)
        chapter_markers = [
            "### 1. 相遇章",
            "### 2. 重逢章",
            "### 3. 误会章",
            "### 4. 心动章",
            "### 5. 表白章",
            "### 6. 信任危机章",
            "### 7. 复仇章",
            "### 8. 反派翻车章",
            "### 9. 真相大白章",
            "### 10. 大婚章",
        ]
        for marker in chapter_markers:
            assert marker in text, f"missing chapter type: {marker}"

    def test_each_chapter_has_structure(self):
        """每章必须有结构骨架 + 节奏比例 + 糖点位置 + 章末钩子模板 + 踩坑警示."""
        text = _read(self.TPL_PATH)
        for marker in ("结构骨架", "节奏比例", "糖点位置", "章末钩子", "踩坑警示"):
            count = text.count(marker)
            # Each of the 10 chapters has these 5 sections
            assert count >= 10, f"'{marker}' appears {count} times, expected ≥10"

    def test_short_chapter_template_present(self):
        text = _read(self.TPL_PATH)
        assert "## 十一" in text
        assert "短章" in text

    def test_uses_template_sentences(self):
        """每章必须有典型模板句和章末钩子模板（用反例 ❌ + 正例 ✅）."""
        text = _read(self.TPL_PATH)
        assert text.count("❌") >= 30, "should have ≥30 ❌ examples (10 ch × 3)"
        assert text.count("✅") >= 20, "should have ≥20 ✅ examples"

    def test_loads_into_writeskill(self):
        text = _read(SKILLS_DIR / "webnovel-write" / "SKILL.md")
        assert "yanqing-chapter-templates.md" in text


class TestYanqingWriterRules:
    """Verify references/genres/yanqing-writer-rules.md exists with hard metrics."""

    RULES_PATH = GENRES_REFS / "yanqing-writer-rules.md"

    def test_file_exists(self):
        assert self.RULES_PATH.exists()

    def test_has_frontmatter(self):
        fm = _parse_frontmatter(self.RULES_PATH)
        assert fm.get("name") == "yanqing-writer-rules"

    def test_defines_six_sections(self):
        """6 段行为约束必须存在."""
        text = _read(self.RULES_PATH)
        for n in range(1, 7):
            marker = f"## {n}."
            assert marker in text, f"missing section: {marker}"

    def test_word_count_table_present(self):
        """字数下限表必须按章型分级."""
        text = _read(self.RULES_PATH)
        for ch in ("相遇章", "心动章", "表白章", "过渡章"):
            assert ch in text, f"missing chapter in word table: {ch}"

    def test_dialogue_ratio_enforced(self):
        text = _read(self.RULES_PATH)
        assert "35-45%" in text
        assert "对话占比" in text

    def test_sugar_type_quota_table(self):
        """§3.1 糖点下限表必须覆盖所有 10 章型 + 过渡章."""
        text = _read(self.RULES_PATH)
        for ch in ("相遇章", "重逢章", "误会章", "心动章", "表白章",
                   "信任危机章", "复仇章", "反派翻车章", "真相大白章",
                   "大婚章", "过渡章"):
            assert ch in text, f"sugar table missing: {ch}"

    def test_emotional_hook_required(self):
        """§4 章末钩子强制要求必须是情感性."""
        text = _read(self.RULES_PATH)
        assert "情感性钩子" in text
        assert "事件性钩子" in text
        # Must show ❌ examples of forbidden event hooks
        for forbidden in ("第二天，她发现他不见了",
                          "三日后，真相大白",
                          "敌人终于来了"):
            assert forbidden in text, f"missing forbidden hook: {forbidden}"

    def test_loads_into_writeskill(self):
        text = _read(SKILLS_DIR / "webnovel-write" / "SKILL.md")
        assert "yanqing-writer-rules.md" in text


class TestAllYanqingGenreTemplatesExtended:
    """Verify ALL 8 言情 templates now have §9 (round 2 + round 3 combined)."""

    EXPECTED = [
        "古言.md", "现言脑洞.md", "豪门总裁.md", "替身文.md",
        "青春甜宠.md", "宫斗宅斗.md", "幻想言情.md", "民国言情.md",
        "狗血言情.md", "种田.md", "职场婚恋.md",
    ]

    def test_all_have_section_9(self):
        for name in self.EXPECTED:
            assert (GENRES_DIR_TPL / name).exists(), f"missing: {name}"
            text = _read(GENRES_DIR_TPL / name)
            assert "## 9. 言情套件" in text, f"{name} missing §9"

    def test_all_reference_playbook(self):
        for name in self.EXPECTED:
            text = _read(GENRES_DIR_TPL / name)
            assert "yanqing-playbook.md" in text, f"{name} not referencing playbook"

    def test_round3_templates_have_specific_sugar_templates(self):
        """Round 3 新增的 6 个模板必须有专属糖点模板."""
        for name in ["宫斗宅斗.md", "幻想言情.md", "民国言情.md",
                     "狗血言情.md", "种田.md", "职场婚恋.md"]:
            text = _read(GENRES_DIR_TPL / name)
            assert "专属糖点模板" in text, f"{name} missing sugar templates"

    def test_round3_templates_have_villain_config(self):
        for name in ["宫斗宅斗.md", "幻想言情.md", "民国言情.md",
                     "狗血言情.md", "种田.md", "职场婚恋.md"]:
            text = _read(GENRES_DIR_TPL / name)
            assert "反派配置" in text, f"{name} missing villain config"


class TestCrossChapterYanqingIssueCategories:
    """Verify 4 new yanqing_* issue categories in cross-chapter-reviewer."""

    NEW_CATEGORIES = [
        "yanqing_monogamy_drift",
        "yanqing_character_drift",
        "yanqing_sugar_density_low",
        "yanqing_villain_absence",
    ]

    def test_categories_in_text(self):
        text = _read(CROSS_CHAPTER_AGENT)
        for cat in self.NEW_CATEGORIES:
            assert cat in text, f"missing category: {cat}"

    def test_categories_in_output_schema(self):
        """Output JSON schema must include all 4 categories."""
        text = _read(CROSS_CHAPTER_AGENT)
        # Find the output schema section
        schema_start = text.find('"category": "unresolved_loop')
        schema_end = text.find('"yanqing_red_lines_triggered"')
        schema = text[schema_start:schema_end]
        for cat in self.NEW_CATEGORIES:
            assert cat in schema, f"output schema missing: {cat}"

    def test_categories_in_dimension_results(self):
        """dimension_results must list all 4 yanqing_* dimensions."""
        text = _read(CROSS_CHAPTER_AGENT)
        dim_start = text.find('"dimension_results":')
        dim_end = text.find("`yanqing_red_lines_triggered`")
        section = text[dim_start:dim_end]
        for cat in self.NEW_CATEGORIES:
            assert cat in section, f"dimension_results missing: {cat}"

    def test_section_6_5_through_6_8_present(self):
        text = _read(CROSS_CHAPTER_AGENT)
        for n in (5, 6, 7, 8):
            assert f"### 6.{n}" in text, f"§6.{n} missing"

    def test_monogamy_severity_is_critical(self):
        """§6.5 情感专一性必须 critical."""
        text = _read(CROSS_CHAPTER_AGENT)
        sec_start = text.find("### 6.5")
        sec_end = text.find("### 6.6")
        section = text[sec_start:sec_end]
        assert "critical" in section, "§6.5 must mark severity=critical"

    def test_villain_absence_escalation(self):
        """§6.8 反派缺席必须 5 章 medium → 10 章 high."""
        text = _read(CROSS_CHAPTER_AGENT)
        sec_start = text.find("### 6.8")
        sec_end = text.find("## 7.")
        section = text[sec_start:sec_end]
        assert "5 章" in section and "10 章" in section, "§6.8 must have escalation"
        assert "medium" in section and "high" in section, "§6.8 must mark severities"


class TestYanqingPackFinalRegression:
    """Final smoke test: all 5 round-3 documents must coexist."""

    def test_all_new_files_exist(self):
        for p in [
            GENRES_REFS / "yanqing-chapter-templates.md",
            GENRES_REFS / "yanqing-writer-rules.md",
            GENRES_REFS / "yanqing-characters.md",
            GENRES_REFS / "yanqing-playbook.md",
        ]:
            assert p.exists(), f"missing: {p}"

    def test_all_round3_genre_templates_have_yanqing_section(self):
        for name in ["宫斗宅斗.md", "幻想言情.md", "民国言情.md",
                     "狗血言情.md", "种田.md", "职场婚恋.md"]:
            text = _read(GENRES_DIR_TPL / name)
            assert "## 9. 言情套件" in text
            assert "Strand 配比" in text
            assert "糖点密度" in text


# ============================================================
# Round 4 additions:
# - 15 条言情专属 CSV 条目
# - yanqing-deconstruction-hints.md
# - init 细分流派推荐
# - quality_trend_report.py 加 5 个言情专属字段
# ============================================================

CSV_BRIDGE = PLUGIN_ROOT / "references" / "csv" / "桥段套路.csv"
CSV_COOLPOINT = PLUGIN_ROOT / "references" / "csv" / "爽点与节奏.csv"
CSV_CHARACTERS = PLUGIN_ROOT / "references" / "csv" / "人设与关系.csv"
DECONSTRUCTION_HINTS = GENRES_REFS / "yanqing-deconstruction-hints.md"


class TestYanqingCSVBridgePatterns:
    """Verify 5 言情专属桥段 added to 桥段套路.csv."""

    EXPECTED_IDS = ["TR-201", "TR-202", "TR-203", "TR-204", "TR-205"]

    def test_csv_grew_by_five_rows(self):
        """CSV should now have ≥113 lines (108 original data + 5 new)."""
        text = _read(CSV_BRIDGE)
        lines = [l for l in text.splitlines() if l.strip() and not l.startswith("﻿")]
        assert len(lines) >= 113, f"expected ≥113 lines, got {len(lines)}"

    def test_each_new_yanqing_id_present(self):
        text = _read(CSV_BRIDGE)
        for tid in self.EXPECTED_IDS:
            assert tid in text, f"missing TR id: {tid}"

    def test_each_new_row_has_16_columns(self):
        """All CSV rows must have 16 columns (header count)."""
        import csv
        with open(CSV_BRIDGE, 'r', encoding='utf-8-sig') as f:
            reader = csv.reader(f)
            for row in reader:
                assert len(row) == 16, f"row has {len(row)} cols: {row[:3]}"


class TestYanqingCSVCoolPoints:
    """Verify 5 言情专属爽点 added to 爽点与节奏.csv."""

    EXPECTED_IDS = ["PA-201", "PA-202", "PA-203", "PA-204", "PA-205"]

    def test_csv_grew_by_five_rows(self):
        text = _read(CSV_COOLPOINT)
        lines = [l for l in text.splitlines() if l.strip() and not l.startswith("﻿")]
        assert len(lines) >= 109, f"expected ≥109 lines, got {len(lines)}"

    def test_each_new_yanqing_id_present(self):
        text = _read(CSV_COOLPOINT)
        for pid in self.EXPECTED_IDS:
            assert pid in text, f"missing PA id: {pid}"

    def test_each_new_row_has_13_columns(self):
        import csv
        with open(CSV_COOLPOINT, 'r', encoding='utf-8-sig') as f:
            reader = csv.reader(f)
            for row in reader:
                assert len(row) == 13, f"row has {len(row)} cols"


class TestYanqingCSVCharacters:
    """Verify 5 言情专属人设 added to 人设与关系.csv."""

    EXPECTED_IDS = ["CH-201", "CH-202", "CH-203", "CH-204", "CH-205"]

    def test_csv_grew_by_five_rows(self):
        text = _read(CSV_CHARACTERS)
        lines = [l for l in text.splitlines() if l.strip() and not l.startswith("﻿")]
        assert len(lines) >= 106, f"expected ≥106 lines, got {len(lines)}"

    def test_each_new_yanqing_id_present(self):
        text = _read(CSV_CHARACTERS)
        for cid in self.EXPECTED_IDS:
            assert cid in text, f"missing CH id: {cid}"

    def test_each_new_row_has_15_columns(self):
        import csv
        with open(CSV_CHARACTERS, 'r', encoding='utf-8-sig') as f:
            reader = csv.reader(f)
            for row in reader:
                assert len(row) == 15, f"row has {len(row)} cols"


class TestYanqingDeconstructionHints:
    """Verify yanqing-deconstruction-hints.md is complete."""

    def test_file_exists(self):
        assert DECONSTRUCTION_HINTS.exists()

    def test_has_frontmatter(self):
        fm = _parse_frontmatter(DECONSTRUCTION_HINTS)
        assert fm.get("name") == "yanqing-deconstruction-hints"

    def test_defines_six_identifications(self):
        """§一 必须有 6 项必须识别."""
        text = _read(DECONSTRUCTION_HINTS)
        for n in range(1, 7):
            assert f"### 1.{n}" in text, f"missing §1.{n}"

    def test_defines_two_differentiation_blocks(self):
        text = _read(DECONSTRUCTION_HINTS)
        assert "## 二" in text
        assert "## 三" in text
        assert "## 四" in text

    def test_metadata_schema_present(self):
        text = _read(DECONSTRUCTION_HINTS)
        assert "yanqing_metadata" in text
        for field in ("sugar_density_observed", "yanqing_male_archetype_detected",
                      "yanqing_female_archetype_detected", "yanqing_combination_detected",
                      "yanqing_combination_score", "yanqing_villain_quality",
                      "yanqing_red_line_violations", "yanqing_phases_detected"):
            assert field in text, f"missing metadata field: {field}"

    def test_has_he_yishi_example(self):
        """Example must mention 何以笙箫默."""
        text = _read(DECONSTRUCTION_HINTS)
        assert "何以笙箫默" in text


class TestInitSubGenreRecommendation:
    """Verify webnovel-init/SKILL.md Step 3.6 with sub-genre matrix."""

    def test_step_3_6_present(self):
        text = _read(INIT_SKILL_PATH)
        assert "Step 3.6" in text

    def test_sub_genre_matrix_present(self):
        text = _read(INIT_SKILL_PATH)
        for sub_genre in ("古言甜宠", "古言权谋", "古言虐恋",
                          "现言甜宠", "现言虐恋",
                          "霸总甜宠", "白月光", "带球跑流"):
            assert sub_genre in text, f"missing sub-genre: {sub_genre}"

    def test_sub_genre_id_field(self):
        """sub_genre must be persisted to idea_bank.json."""
        text = _read(INIT_SKILL_PATH)
        assert "sub_genre" in text
        assert "idea_bank.json" in text

    def test_deconstruction_hints_loaded(self):
        text = _read(INIT_SKILL_PATH)
        assert "yanqing-deconstruction-hints.md" in text


class TestQualityTrendYanqingFields:
    """Verify quality_trend_report.py adds 5 言情专属 fields."""

    QUALITY_TREND = PLUGIN_ROOT / "scripts" / "quality_trend_report.py"

    def test_script_imports(self):
        """The script must still be importable after changes."""
        import subprocess
        result = subprocess.run(
            ["python", "-c",
             "import sys; sys.path.insert(0, '.'); "
             "from quality_trend_report import build_yanqing_quality_section; "
             "print('OK')"],
            capture_output=True, text=True,
            cwd=str(PLUGIN_ROOT / "scripts"),
        )
        assert result.returncode == 0, f"import failed: {result.stderr}"

    def test_function_signature(self):
        """Function must take review_records + review_trend."""
        text = _read(self.QUALITY_TREND)
        assert "def build_yanqing_quality_section" in text
        assert "review_records: List" in text
        assert "review_trend: Dict" in text

    def test_defines_five_field_titles(self):
        """5 个言情专属字段标题."""
        text = _read(self.QUALITY_TREND)
        for title in (
            "yanqing_sugar_density_trend",
            "yanqing_heartbeat_moment_frequency",
            "yanqing_villain_activity",
            "yanqing_hook_type_distribution",
            "yanqing_emotional_consistency",
        ):
            assert title in text, f"missing field: {title}"

    def test_called_from_build_quality_report(self):
        text = _read(self.QUALITY_TREND)
        assert "build_yanqing_quality_section" in text
        # Must be called and the result conditionally appended
        assert "yanqing_section" in text

    def test_empty_records_returns_empty_string(self):
        """Function returns '' if no records."""
        import subprocess
        test_code = (
            "import sys; sys.path.insert(0, '.'); "
            "from quality_trend_report import build_yanqing_quality_section; "
            "r = build_yanqing_quality_section([], {}); "
            "assert r == '', repr(r)"
        )
        result = subprocess.run(
            ["python", "-c", test_code],
            capture_output=True, text=True,
            cwd=str(PLUGIN_ROOT / "scripts"),
        )
        assert result.returncode == 0, f"test failed: {result.stderr}"

    def test_recognizes_all_four_yanqing_categories(self):
        """Function must aggregate all 4 yanqing_* categories."""
        text = _read(self.QUALITY_TREND)
        for cat in ("yanqing_monogamy_drift", "yanqing_character_drift",
                    "yanqing_sugar_density_low", "yanqing_villain_absence"):
            assert cat in text, f"missing category: {cat}"
