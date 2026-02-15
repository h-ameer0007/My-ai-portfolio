"""SQLite database operations for YouTube Semantic Optimizer."""

import sqlite3
import json
from datetime import datetime
from typing import Optional, List, Dict, Any
from pathlib import Path

from config.settings import DB_PATH


class DataService:
    """Handles all SQLite database operations."""

    def __init__(self, db_path: Optional[Path] = None):
        self.db_path = str(db_path or DB_PATH)
        self._init_db()

    def _get_conn(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL")
        return conn

    def _init_db(self):
        """Initialize database tables."""
        conn = self._get_conn()
        try:
            conn.executescript("""
                CREATE TABLE IF NOT EXISTS projects (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    channel TEXT DEFAULT '',
                    topic TEXT NOT NULL,
                    target_audience TEXT DEFAULT '',
                    status TEXT DEFAULT 'active',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );

                CREATE TABLE IF NOT EXISTS step_outputs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    project_id INTEGER NOT NULL,
                    step_number INTEGER NOT NULL,
                    step_name TEXT NOT NULL,
                    input_data TEXT DEFAULT '',
                    output_data TEXT DEFAULT '',
                    gemini_tokens INTEGER DEFAULT 0,
                    claude_tokens INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
                );

                CREATE TABLE IF NOT EXISTS video_analytics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    project_id INTEGER NOT NULL,
                    views INTEGER DEFAULT 0,
                    watch_time_hours REAL DEFAULT 0.0,
                    ctr REAL DEFAULT 0.0,
                    avg_view_duration REAL DEFAULT 0.0,
                    likes INTEGER DEFAULT 0,
                    comments INTEGER DEFAULT 0,
                    shares INTEGER DEFAULT 0,
                    revenue REAL DEFAULT 0.0,
                    date_recorded DATE DEFAULT CURRENT_DATE,
                    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
                );

                CREATE INDEX IF NOT EXISTS idx_step_outputs_project
                    ON step_outputs(project_id, step_number);
                CREATE INDEX IF NOT EXISTS idx_analytics_project
                    ON video_analytics(project_id, date_recorded);
            """)
            conn.commit()
        finally:
            conn.close()

    # --- Project Operations ---

    def create_project(self, name: str, topic: str, channel: str = "",
                       target_audience: str = "") -> int:
        conn = self._get_conn()
        try:
            cursor = conn.execute(
                """INSERT INTO projects (name, channel, topic, target_audience)
                   VALUES (?, ?, ?, ?)""",
                (name, channel, topic, target_audience)
            )
            conn.commit()
            return cursor.lastrowid
        finally:
            conn.close()

    def get_project(self, project_id: int) -> Optional[Dict[str, Any]]:
        conn = self._get_conn()
        try:
            row = conn.execute(
                "SELECT * FROM projects WHERE id = ?", (project_id,)
            ).fetchone()
            return dict(row) if row else None
        finally:
            conn.close()

    def get_all_projects(self) -> List[Dict[str, Any]]:
        conn = self._get_conn()
        try:
            rows = conn.execute(
                "SELECT * FROM projects ORDER BY updated_at DESC"
            ).fetchall()
            return [dict(r) for r in rows]
        finally:
            conn.close()

    def update_project(self, project_id: int, **kwargs):
        conn = self._get_conn()
        try:
            allowed = {"name", "channel", "topic", "target_audience", "status"}
            updates = {k: v for k, v in kwargs.items() if k in allowed}
            if not updates:
                return
            updates["updated_at"] = datetime.now().isoformat()
            set_clause = ", ".join(f"{k} = ?" for k in updates)
            values = list(updates.values()) + [project_id]
            conn.execute(
                f"UPDATE projects SET {set_clause} WHERE id = ?", values
            )
            conn.commit()
        finally:
            conn.close()

    def delete_project(self, project_id: int):
        conn = self._get_conn()
        try:
            conn.execute("DELETE FROM step_outputs WHERE project_id = ?", (project_id,))
            conn.execute("DELETE FROM video_analytics WHERE project_id = ?", (project_id,))
            conn.execute("DELETE FROM projects WHERE id = ?", (project_id,))
            conn.commit()
        finally:
            conn.close()

    # --- Step Output Operations ---

    def save_step_output(self, project_id: int, step_number: int, step_name: str,
                         input_data: str, output_data: str,
                         gemini_tokens: int = 0, claude_tokens: int = 0):
        """Save step output. CRITICAL: Deletes old entries before inserting to handle re-runs."""
        conn = self._get_conn()
        try:
            # CRITICAL FIX: Delete existing entries for this step before inserting
            conn.execute(
                "DELETE FROM step_outputs WHERE project_id = ? AND step_number = ?",
                (project_id, step_number)
            )
            conn.execute(
                """INSERT INTO step_outputs
                   (project_id, step_number, step_name, input_data, output_data,
                    gemini_tokens, claude_tokens)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (project_id, step_number, step_name, input_data, output_data,
                 gemini_tokens, claude_tokens)
            )
            # Update project timestamp
            conn.execute(
                "UPDATE projects SET updated_at = ? WHERE id = ?",
                (datetime.now().isoformat(), project_id)
            )
            conn.commit()
        finally:
            conn.close()

    def get_step_output(self, project_id: int, step_number: int) -> Optional[str]:
        """Get step output. No caching - always fetch fresh from database."""
        conn = self._get_conn()
        try:
            row = conn.execute(
                """SELECT output_data FROM step_outputs
                   WHERE project_id = ? AND step_number = ?
                   ORDER BY created_at DESC LIMIT 1""",
                (project_id, step_number)
            ).fetchone()
            return row["output_data"] if row else None
        finally:
            conn.close()

    def get_all_step_outputs(self, project_id: int) -> Dict[int, str]:
        """Get all step outputs for a project as {step_number: output_data}."""
        conn = self._get_conn()
        try:
            rows = conn.execute(
                """SELECT step_number, output_data FROM step_outputs
                   WHERE project_id = ? ORDER BY step_number""",
                (project_id,)
            ).fetchall()
            return {row["step_number"]: row["output_data"] for row in rows}
        finally:
            conn.close()

    def get_completed_steps(self, project_id: int) -> List[int]:
        """Get list of completed step numbers (unique)."""
        conn = self._get_conn()
        try:
            rows = conn.execute(
                """SELECT DISTINCT step_number FROM step_outputs
                   WHERE project_id = ? ORDER BY step_number""",
                (project_id,)
            ).fetchall()
            return [row["step_number"] for row in rows]
        finally:
            conn.close()

    def get_project_progress(self, project_id: int) -> float:
        """Get project progress as a fraction (0.0 to 1.0). Capped at 1.0."""
        completed = self.get_completed_steps(project_id)
        total_steps = 10
        return min(len(completed) / total_steps, 1.0)

    def get_token_usage(self, project_id: int) -> Dict[str, int]:
        """Get total token usage for a project."""
        conn = self._get_conn()
        try:
            row = conn.execute(
                """SELECT COALESCE(SUM(gemini_tokens), 0) as gemini_total,
                          COALESCE(SUM(claude_tokens), 0) as claude_total
                   FROM step_outputs WHERE project_id = ?""",
                (project_id,)
            ).fetchone()
            return {
                "gemini_tokens": row["gemini_total"],
                "claude_tokens": row["claude_total"],
                "total_tokens": row["gemini_total"] + row["claude_total"],
            }
        finally:
            conn.close()

    # --- Video Analytics Operations ---

    def save_analytics(self, project_id: int, **kwargs):
        conn = self._get_conn()
        try:
            fields = ["views", "watch_time_hours", "ctr", "avg_view_duration",
                       "likes", "comments", "shares", "revenue", "date_recorded"]
            data = {k: kwargs.get(k, 0) for k in fields}
            if "date_recorded" not in kwargs:
                data["date_recorded"] = datetime.now().strftime("%Y-%m-%d")
            cols = ", ".join(data.keys())
            placeholders = ", ".join("?" for _ in data)
            values = [project_id] + list(data.values())
            conn.execute(
                f"INSERT INTO video_analytics (project_id, {cols}) VALUES (?, {placeholders})",
                values
            )
            conn.commit()
        finally:
            conn.close()

    def get_analytics(self, project_id: int) -> List[Dict[str, Any]]:
        conn = self._get_conn()
        try:
            rows = conn.execute(
                """SELECT * FROM video_analytics
                   WHERE project_id = ? ORDER BY date_recorded DESC""",
                (project_id,)
            ).fetchall()
            return [dict(r) for r in rows]
        finally:
            conn.close()

    def get_all_analytics_summary(self) -> List[Dict[str, Any]]:
        """Get analytics summary across all projects."""
        conn = self._get_conn()
        try:
            rows = conn.execute("""
                SELECT p.id, p.name, p.topic,
                       COUNT(DISTINCT so.step_number) as steps_completed,
                       COALESCE(SUM(so.gemini_tokens), 0) as total_gemini_tokens,
                       COALESCE(SUM(so.claude_tokens), 0) as total_claude_tokens,
                       MAX(va.views) as max_views,
                       MAX(va.ctr) as max_ctr
                FROM projects p
                LEFT JOIN step_outputs so ON p.id = so.project_id
                LEFT JOIN video_analytics va ON p.id = va.project_id
                GROUP BY p.id
                ORDER BY p.updated_at DESC
            """).fetchall()
            return [dict(r) for r in rows]
        finally:
            conn.close()
