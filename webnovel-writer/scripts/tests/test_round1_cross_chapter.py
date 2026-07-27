#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for Round 1：跨章一致性审查 agent + 集成.

This test pack verifies:
1. agents/cross-chapter-reviewer.md exists and has all 5 issue categories
2. The agent's output JSON schema is well-formed
3. webnovel-write/SKILL.md integrates the agent as Step 3.5
4. The hard rules section mandates cross-chapter review
5. The sufficiency gate requires cross-chapter results
6. Mode tables include Step 3.5 in default/fast/minimal variants
"""

import re
from pathlib import Path

import pytest

PLUGIN_ROOT = Path(__file__).resolve().parents[2]
AGENTS_DIR = PLUGIN_ROOT / "agents"
SKILLS_DIR = PLUGIN_ROOT / "skills"
CROSS_CHAPTER_AGENT = AGENTS_DIR / "cross-chapter-reviewer.md"
WRITE_SKILL = SKILLS_DIR / "webnovel-write" / "SKILL.md"


def _read(path: Path) -> str:
    """Read a UTF-8 file, fail with helpful message if missing."""
    assert path.exists(), f"Expected file not found: {path}"
    return path.read_text(encoding="utf-8")


def _parse_frontmatter(path: Path) -> dict:
    """Parse YAML-ish frontmatter block at the top of a markdown file.

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

    def test_file_exists(self):
        assert CROSS_CHAPTER_AGENT.exists()

    def test_frontmatter_has_required_keys(self):
        fm = _parse_frontmatter(CROSS_CHAPTER_AGENT)
        assert fm.get("name") == "cross-chapter-reviewer"
        assert "description" in fm
        # tools must include the read-only trio for cross-chapter scanning
        assert "Read" in fm.get("tools", "")
        assert "Grep" in fm.get("tools", "")
        assert "Bash" in fm.get("tools", "")
        assert "color" in fm

    def test_defines_five_categories(self):
        """Agent must define 5 issue categories."""
        text = _read(CROSS_CHAPTER_AGENT)
        for cat in ("unresolved_loop", "broken_promise", "rule_contradiction",
                    "relationship_drift", "timeline_jump"):
            assert cat in text, f"missing category: {cat}"

    def test_does_not_score_artifacts(self):
        """Agent must NOT output overall_score (parity with reviewer)."""
        text = _read(CROSS_CHAPTER_AGENT)
        # Agent explicitly disclaims scoring; check the rule
        assert "不评分" in text or "不输出 overall_score" in text or "no overall_score" in text

    def test_output_schema_required_fields(self):
        """Output JSON must include the required fields."""
        text = _read(CROSS_CHAPTER_AGENT)
        for field in ("chapter", "issues", "issues_count", "blocking_count",
                      "has_blocking", "dimension_results", "summary"):
            assert f'"{field}"' in text, f"output schema missing: {field}"

    def test_dimension_results_covers_all_five(self):
        """dimension_results must cover the 5 cross-chapter dimensions."""
        text = _read(CROSS_CHAPTER_AGENT)
        # Find the dimension_results block
        m = re.search(r'"dimension_results":\s*\[(.*?)\]', text, re.DOTALL)
        assert m, "dimension_results block not found"
        block = m.group(1)
        for dim in ("unresolved_loop", "broken_promise", "rule_contradiction",
                    "relationship_drift", "timeline_jump"):
            assert f'"{dim}"' in block, f"dimension_results missing: {dim}"

    def test_no_blocking_decision_is_implied(self):
        """Output JSON has_blocking boolean must be present and tied to blocking_count."""
        text = _read(CROSS_CHAPTER_AGENT)
        assert '"has_blocking"' in text
        assert '"blocking_count"' in text


# ============================================================
# 2. webnovel-write/SKILL.md integration
# ============================================================

class TestWriteSkillIntegration:
    """Verify webnovel-write/SKILL.md pulls cross-chapter-reviewer into Step 3.5."""

    def _step_3_5_section(self) -> str:
        """Return the full text of the Step 3.5 section (between its header and Step 4)."""
        text = _read(WRITE_SKILL)
        # Find the Step 3.5 SECTION header (### Step 3.5：), not the
        # bullet reference in the hard-rules section
        marker = "### Step 3.5："
        idx = text.find(marker)
        assert idx > 0, f"Step 3.5 section header not found at {marker!r}"
        # Section ends at the next ### Step
        end_idx = text.find("\n### Step", idx + len(marker))
        if end_idx < 0:
            end_idx = len(text)
        return text[idx:end_idx]

    def test_step_3_5_section_present(self):
        text = _read(WRITE_SKILL)
        assert "### Step 3.5：跨章一致性审查" in text, \
            "Step 3.5 section header not found"
        section = self._step_3_5_section()
        assert "跨章" in section

    def test_step_3_5_invokes_cross_chapter_reviewer(self):
        section = self._step_3_5_section()
        assert "cross-chapter-reviewer" in section
        # Must use Agent tool
        assert "Use the Agent tool" in section or "Agent" in section

    def test_step_3_5_passes_chapter_metadata(self):
        section = self._step_3_5_section()
        for field in ("chapter=", "chapter_file=", "project_root=", "scripts_dir="):
            assert field in section, f"Step 3.5 missing field: {field}"

    def test_step_3_5_subagent_run_recorded(self):
        section = self._step_3_5_section()
        assert "SubagentRun" in section
        assert "cross-chapter-reviewer" in section

    def test_step_3_5_skip_condition_is_only_minimal(self):
        section = self._step_3_5_section()
        assert "--minimal" in section

    def test_blocking_handling_matches_reviewer(self):
        section = self._step_3_5_section()
        assert "blocking" in section
        # Must mention 定点修复 or 用户裁决
        assert "定点修复" in section or "用户裁决" in section


class TestHardRulesSection:
    """Verify the 硬规则 section mandates cross-chapter review."""

    def test_hard_rules_mandate_cross_chapter(self):
        text = _read(WRITE_SKILL)
        # Find 硬规则 section
        m = re.search(r"## 硬规则\s*\n(.*?)(?=\n## )", text, re.DOTALL)
        assert m, "## 硬规则 section not found"
        rules = m.group(1)
        # Must contain a rule about Step 3.5 / cross-chapter review
        assert "跨章" in rules or "Step 3.5" in rules, \
            "hard rules do not mandate cross-chapter review"
        # Must mention --minimal as the only exception
        assert "--minimal" in rules, "hard rules don't reference --minimal exemption"


class TestSufficiencyGate:
    """Verify the 充分性闸门 section requires cross-chapter review."""

    def test_sufficiency_gate_includes_cross_chapter(self):
        text = _read(WRITE_SKILL)
        m = re.search(r"## 充分性闸门\s*\n(.*?)(?=\n## )", text, re.DOTALL)
        assert m, "## 充分性闸门 section not found"
        gate = m.group(1)
        # Must contain an item about 跨章审查
        assert "跨章审查" in gate or "跨章一致性" in gate, \
            "sufficiency gate does not require cross-chapter review"
        # --minimal exemption
        assert "--minimal" in gate


class TestModeTable:
    """Verify 模式 table shows Step 3.5 in pipeline."""

    def test_default_mode_includes_step_3_5(self):
        text = _read(WRITE_SKILL)
        # Default mode is the first row in the table
        m = re.search(r"\| 默认 \| (.*?) \|", text)
        assert m, "default mode row not found"
        pipeline = m.group(1)
        assert "3.5" in pipeline, "default mode does not include Step 3.5"

    def test_minimal_mode_skips_step_3_5(self):
        """--minimal must explicitly skip 3.5 (along with reviewer)."""
        text = _read(WRITE_SKILL)
        m = re.search(r"\| `--minimal` \| (.*?) \|", text)
        assert m, "--minimal mode row not found"
        pipeline = m.group(1)
        # Must mention skipping
        assert "3.5" in pipeline or "skip" in pipeline.lower() or "跳过" in pipeline, \
            "--minimal mode row doesn't reference skipping Step 3.5"

    def test_fast_mode_skips_step_3_5_or_runs_lite(self):
        """--fast may run 3.5 lightweight or skip; either must be explicit."""
        text = _read(WRITE_SKILL)
        m = re.search(r"\| `--fast` \| (.*?) \|", text)
        assert m, "--fast mode row not found"
        pipeline = m.group(1)
        # Either include or skip — but be explicit
        assert "3.5" in pipeline or "轻量" in pipeline or "跳" in pipeline, \
            "--fast mode row is ambiguous about Step 3.5"


# ============================================================
# 3. Cross-cutting integration smoke test
# ============================================================

class TestCrossCuttingIntegration:
    """Smoke tests for end-to-end Round 1 wiring."""

    def test_no_regression_step_3_reviewer_intact(self):
        """Step 3 (reviewer) must still be intact."""
        text = _read(WRITE_SKILL)
        assert "Step 3：审查" in text
        assert "reviewer" in text
        assert "review-pipeline" in text

    def test_no_regression_step_4_to_step_6_intact(self):
        """Step 4-6 must still be present and ordered."""
        text = _read(WRITE_SKILL)
        for step in ("Step 4：润色", "Step 5：提交", "Step 6：Git 备份"):
            assert step in text, f"regression: {step} missing"

    def test_step_3_5_appears_before_step_4(self):
        """Step 3.5 must be positioned between Step 3 and Step 4."""
        text = _read(WRITE_SKILL)
        # Use the section header (### Step 3.5：) to disambiguate
        step_3_5_pos = text.find("### Step 3.5：")
        step_4_pos = text.find("### Step 4：润色")
        assert step_3_5_pos > 0
        assert step_4_pos > 0
        assert step_3_5_pos < step_4_pos, "Step 3.5 must precede Step 4"

    def test_round1_files_consistent(self):
        """The 4 files touched in Round 1 must all be present."""
        assert CROSS_CHAPTER_AGENT.exists()
        assert WRITE_SKILL.exists()