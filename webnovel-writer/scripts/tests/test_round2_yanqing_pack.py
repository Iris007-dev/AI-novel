#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for Round 2: 言情专属文档 + 集成 + 写章硬指标.

This test pack verifies:
1. 4 份 yanqing_*.md 文档存在且 frontmatter 正确
2. yanqing-chapter-templates.md 含 10 种章节模板
3. yanqing-writer-rules.md 含 6 段硬指标
4. yanqing-playbook.md 含 6 种爽点 + 6 种反转 + 9 段协议
5. yanqing-characters.md 含 36 组合矩阵
6. webnovel-write/SKILL.md 在硬规则 + Step 1.5 集成触发
"""

import re
from pathlib import Path

import pytest

PLUGIN_ROOT = Path(__file__).resolve().parents[2]
REFERENCES_DIR = PLUGIN_ROOT / "references"
GENRES_DIR = REFERENCES_DIR / "genres"
SKILLS_DIR = PLUGIN_ROOT / "skills"


def _read(path: Path) -> str:
    assert path.exists(), f"Expected file not found: {path}"
    return path.read_text(encoding="utf-8")


def _parse_frontmatter(path: Path) -> dict:
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
# 1. 4 份 yanqing_*.md 文件存在 + frontmatter 正确
# ============================================================

class TestYanqingFiles:
    """Verify the 4 yanqing genre reference files exist with proper frontmatter."""

    FILES = {
        "yanqing-playbook.md": "yanqing-playbook",
        "yanqing-characters.md": "yanqing-characters",
        "yanqing-chapter-templates.md": "yanqing-chapter-templates",
        "yanqing-writer-rules.md": "yanqing-writer-rules",
    }

    def test_all_files_exist(self):
        for name in self.FILES:
            assert (GENRES_DIR / name).exists(), f"missing: {name}"

    def test_all_have_frontmatter(self):
        for name, expected_name in self.FILES.items():
            fm = _parse_frontmatter(GENRES_DIR / name)
            assert fm.get("name") == expected_name, \
                f"{name} frontmatter name mismatch: {fm.get('name')}"

    def test_all_list_genre_scope(self):
        """All 4 files should declare a genre_scope with at least 古言 and 现言."""
        for name in self.FILES:
            fm = _parse_frontmatter(GENRES_DIR / name)
            scope = fm.get("genre_scope", "")
            assert "古言" in scope, f"{name} genre_scope missing 古言"
            assert "现言" in scope, f"{name} genre_scope missing 现言"

    def test_combined_line_count_over_1000(self):
        """All 4 files combined should have substantive content (>1000 lines)."""
        total = 0
        for name in self.FILES:
            total += sum(1 for _ in (GENRES_DIR / name).open(encoding="utf-8"))
        assert total > 1000, f"combined lines {total} < 1000"


# ============================================================
# 2. yanqing-chapter-templates.md
# ============================================================

class TestYanqingChapterTemplates:
    """Verify the 10 chapter types are documented."""

    CHAPTER_PATH = GENRES_DIR / "yanqing-chapter-templates.md"

    def test_has_ten_chapter_types(self):
        text = _read(self.CHAPTER_PATH)
        for n in range(1, 11):
            marker = f"### {n}. "
            assert marker in text, f"missing chapter type #{n}"

    def test_each_chapter_has_structure_skeleton(self):
        text = _read(self.CHAPTER_PATH)
        # Structure skeleton is the [开场...主体...章末钩子] block
        # Each chapter has these keywords
        assert text.count("结构骨架") >= 10
        assert text.count("节奏比例") >= 10
        assert text.count("糖点位置") >= 10
        assert text.count("章末钩子") >= 10

    def test_defines_short_chapter_template(self):
        text = _read(self.CHAPTER_PATH)
        assert "## 十一" in text or "短章" in text, \
            "missing short-chapter template"

    def test_provides_hook_templates(self):
        text = _read(self.CHAPTER_PATH)
        # 章末钩子模板 should appear in at least 5 chapters
        assert text.count("模板") >= 10


# ============================================================
# 3. yanqing-writer-rules.md
# ============================================================

class TestYanqingWriterRules:
    """Verify the 6 hard-metric sections are present."""

    RULES_PATH = GENRES_DIR / "yanqing-writer-rules.md"

    def test_six_sections(self):
        text = _read(self.RULES_PATH)
        # Expect 一 through 六 numbered sections
        for n in range(1, 7):
            cn = "一二三四五六"[n - 1]
            assert f"## {cn}、" in text, f"missing section ## {cn}、"

    def test_dialogue_ratio_35_45(self):
        text = _read(self.RULES_PATH)
        assert "35-45%" in text or "35%" in text

    def test_emotional_hook_required(self):
        text = _read(self.RULES_PATH)
        assert "情感性" in text
        assert "事件性" in text

    def test_word_count_table(self):
        text = _read(self.RULES_PATH)
        for ch in ("相遇章", "心动章", "大婚章", "过渡章"):
            assert ch in text, f"word count table missing: {ch}"


# ============================================================
# 4. yanqing-playbook.md
# ============================================================

class TestYanqingPlaybook:
    """Verify the 6 cool points, 6 reversals, 9 anti-AI rules."""

    PLAYBOOK_PATH = GENRES_DIR / "yanqing-playbook.md"

    def test_six_yanqing_cool_points(self):
        text = _read(self.PLAYBOOK_PATH)
        for cp in ("暗涌式心动", "反差式沦陷", "误会式心疼",
                   "公费式撒糖", "身份式碾压", "深情式回响"):
            assert cp in text, f"missing cool point: {cp}"

    def test_six_yanqing_reversals(self):
        text = _read(self.PLAYBOOK_PATH)
        for marker in ("R1", "R2", "R3", "R4", "R5", "R6"):
            assert marker in text, f"missing reversal: {marker}"

    def test_four_sugar_types(self):
        text = _read(self.PLAYBOOK_PATH)
        for s in ("微触", "微甜", "微酸", "微烫"):
            assert s in text, f"missing sugar type: {s}"

    def test_nine_anti_ai_rules(self):
        text = _read(self.PLAYBOOK_PATH)
        # Anti-AI rules numbered 5.1 through 5.9
        for n in range(1, 10):
            assert f"5.{n}" in text, f"missing anti-AI rule 5.{n}"

    def test_yanqing_phase_names(self):
        text = _read(self.PLAYBOOK_PATH)
        for phase in ("建立期", "拉扯期", "确认期", "考验期", "爆发期"):
            assert phase in text, f"missing phase: {phase}"


# ============================================================
# 5. yanqing-characters.md
# ============================================================

class TestYanqingCharacters:
    """Verify the 36-combination matrix."""

    CHARS_PATH = GENRES_DIR / "yanqing-characters.md"

    def test_six_male_types(self):
        text = _read(self.CHARS_PATH)
        for m in ("M1 高冷", "M2 温柔", "M3 痞气",
                  "M4 病娇", "M5 权谋", "M6 暗涌"):
            assert m in text, f"missing male archetype: {m}"

    def test_six_female_types(self):
        text = _read(self.CHARS_PATH)
        for f in ("F1 坚韧", "F2 聪慧", "F3 白月光",
                  "F4 反差", "F5 救赎", "F6 双强"):
            assert f in text, f"missing female archetype: {f}"

    def test_36_combination_matrix(self):
        text = _read(self.CHARS_PATH)
        # Should mention both 推荐组合 (top 5) and 高风险组合
        assert "Top 5" in text or "推荐组合" in text
        assert "高风险" in text

    def test_sugar_focus_table(self):
        text = _read(self.CHARS_PATH)
        # The 糖点聚焦方向 table must list each male archetype's focus
        for marker in ("少言多行", "细节糖", "互怼糖", "张力糖", "信任糖", "知情糖"):
            assert marker in text, f"missing sugar focus: {marker}"


# ============================================================
# 6. webnovel-write/SKILL.md integration
# ============================================================

class TestWriteSkillIntegration:
    """Verify webnovel-write/SKILL.md pulls yanqing pack into Step 1.5."""

    SKILL_PATH = SKILLS_DIR / "webnovel-write" / "SKILL.md"

    def _step_1_5_section(self) -> str:
        """Return the text of the Step 1.5 subsection (under Step 1, before Step 2)."""
        text = _read(self.SKILL_PATH)
        # Use the #### Step 1.5： header (4 #) not the 硬规则 reference
        marker = "#### Step 1.5"
        idx = text.find(marker)
        assert idx > 0, f"#### Step 1.5 header not found"
        # Section ends at the next ### Step
        end_idx = text.find("\n### Step", idx + len(marker))
        if end_idx < 0:
            end_idx = len(text)
        return text[idx:end_idx]

    def test_hard_rules_mention_yanqing(self):
        text = _read(self.SKILL_PATH)
        m = re.search(r"## 硬规则\s*\n(.*?)(?=\n## )", text, re.DOTALL)
        assert m, "## 硬规则 section not found"
        rules = m.group(1)
        assert "言情" in rules, "hard rules don't reference yanqing"
        assert "yanqing" in rules, "hard rules don't reference yanqing files"

    def test_step_1_5_present(self):
        text = _read(self.SKILL_PATH)
        assert "#### Step 1.5" in text, "Step 1.5 #### header not found"
        section = self._step_1_5_section()
        assert "言情" in section

    def test_step_1_5_lists_all_four_files(self):
        section = self._step_1_5_section()
        for f in ("yanqing-playbook.md", "yanqing-characters.md",
                  "yanqing-chapter-templates.md", "yanqing-writer-rules.md"):
            assert f in section, f"Step 1.5 missing file: {f}"

    def test_step_1_5_loads_via_genre_check(self):
        """Step 1.5 must check state.json for genre match."""
        section = self._step_1_5_section()
        assert "state.json" in section
        assert "genre" in section

    def test_genre_set_includes_required(self):
        """Step 1.5 must list at least 古言 + 现言 in the genre set."""
        section = self._step_1_5_section()
        for g in ("古言", "现言", "豪门总裁", "替身文"):
            assert g in section, f"Step 1.5 genre set missing: {g}"

    def test_yanqing_phase_names_in_task(self):
        """Step 1.5 must inject phase names into task."""
        section = self._step_1_5_section()
        for phase in ("建立期", "拉扯期", "确认期", "考验期", "爆发期"):
            assert phase in section

    def test_minimal_mode_handling(self):
        """Step 1.5 must specify --minimal behaviour."""
        section = self._step_1_5_section()
        assert "--minimal" in section


# ============================================================
# 7. 跨切面烟雾测试
# ============================================================

class TestCrossCutting:
    """Smoke tests for Round 2 wiring."""

    def test_no_regression_step_1_intact(self):
        text = _read(SKILLS_DIR / "webnovel-write" / "SKILL.md")
        assert "### Step 1：context-agent" in text

    def test_no_regression_step_3_5_intact(self):
        """Round 1's Step 3.5 must still be intact."""
        text = _read(SKILLS_DIR / "webnovel-write" / "SKILL.md")
        assert "### Step 3.5：跨章一致性审查" in text

    def test_step_1_5_positioned_correctly(self):
        """Step 1.5 must appear after Step 1 and before Step 2."""
        text = _read(SKILLS_DIR / "webnovel-write" / "SKILL.md")
        step_1_pos = text.find("### Step 1：context-agent")
        step_1_5_pos = text.find("#### Step 1.5")
        step_2_pos = text.find("### Step 2：起草正文")
        assert step_1_pos > 0
        assert step_1_5_pos > step_1_pos
        assert step_1_5_pos < step_2_pos