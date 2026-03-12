"""
Video Annotation System
A Streamlit application for annotating videos with multiple-choice questions
"""

import streamlit as st
import json
import time
import re
import hashlib
from datetime import datetime
from pathlib import Path

# Import utility modules
from utils.data_parser import load_questions, parse_questions_data
from utils.video_loader_gdrive import VideoLoaderGDrive
from utils.video_loader_onedrive_folder import VideoLoaderOneDriveFolder
from utils.session_manager import initialize_session, save_progress, load_progress
from utils.response_recorder import save_response, export_responses, load_responses
import config

# Page configuration
st.set_page_config(
    page_title="Video Annotation System",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
    :root {
        --anno-bg: var(--secondary-background-color);
        --anno-text: var(--text-color);
        --anno-border: rgba(127, 127, 127, 0.35);
        --anno-accent: var(--primary-color);
    }
    .main-header {
        font-size: 2rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    .question-box {
        background-color: var(--anno-bg);
        color: var(--anno-text);
        border: 1px solid var(--anno-border);
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .choice-box {
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 0.3rem;
        border: 2px solid #e0e0e0;
    }
    .correct-answer {
        background-color: #d4edda;
        border-color: #28a745;
    }
    .video-container {
        margin: 1rem 0;
    }
    .stProgress > div > div > div > div {
        background-color: #4CAF50;
    }
    .annotation-guide {
        background-color: var(--anno-bg);
        color: var(--anno-text);
        border: 1px solid var(--anno-border);
        border-left: 4px solid var(--anno-accent);
        padding: 0.75rem 1rem;
        border-radius: 0.25rem;
        margin-bottom: 0.5rem;
    }
    .compact-video [data-testid="stVideo"] {
        max-width: 460px;
    }
    .compact-video video {
        max-height: 260px;
    }
    .right-panel p, .right-panel li, .right-panel label, .right-panel .stMarkdown {
        font-size: 1.15rem;
    }
    .right-panel h3 {
        font-size: 1.45rem;
    }
    .option-item {
        background: var(--anno-bg);
        color: var(--anno-text);
        border: 1px solid var(--anno-border);
        border-radius: 8px;
        padding: 0.6rem 0.75rem;
        margin: 0.35rem 0;
    }
    .evidence-title {
        font-size: 1.25rem;
        font-weight: 700;
    }
    .evidence-note {
        font-size: 1.05rem;
        color: var(--anno-text);
    }
    .evidence-meta {
        font-size: 1.02rem;
        line-height: 1.45;
        background: var(--anno-bg);
        color: var(--anno-text);
        border: 1px solid var(--anno-border);
        border-radius: 8px;
        padding: 0.55rem 0.75rem;
        margin-top: 0.35rem;
    }
</style>
""", unsafe_allow_html=True)

def render_small_video(video_url, clip_id=None, video_loader=None):
    """Render videos in a smaller box to keep evidence compact."""
    left_spacer, video_col, right_spacer = st.columns([1.2, 3.6, 1.2])
    with video_col:
        st.markdown("<div class='compact-video'>", unsafe_allow_html=True)
        if video_loader and hasattr(video_loader, 'render_video'):
            # Use Google Drive loader's render method
            video_loader.render_video(clip_id if clip_id else video_url)
        else:
            # Fallback to st.video
            st.video(video_url)
        st.markdown("</div>", unsafe_allow_html=True)

def resolve_clip_video_url(clip_id, query_video_loader, evidence_video_loader):
    """Try evidence roots first, then query roots."""
    if not clip_id:
        return None
    for loader in [evidence_video_loader, query_video_loader]:
        video_url = loader.get_video_url(clip_id)
        if video_url:
            return video_url
    return None

def resolve_prefer_30s_clip(clip_id, query_video_loader, evidence_video_loader):
    """
    Resolve to clip ID (Google Drive version - simplified).
    Returns clip_id directly for Google Drive loaders.
    """
    if not clip_id:
        return None
    return str(clip_id).strip()

def unique_keep_order(items):
    seen = set()
    out = []
    for x in items:
        if x and x not in seen:
            seen.add(x)
            out.append(x)
    return out

def _parse_hms8(hms8):
    """
    Parse HHMMSSff string to (display, seconds_float).
    """
    s = str(hms8)
    if len(s) != 8 or not s.isdigit():
        return None, None
    hh = int(s[0:2])
    mm = int(s[2:4])
    ss = int(s[4:6])
    ff = int(s[6:8])
    sec = hh * 3600 + mm * 60 + ss + ff / 100.0
    return f"{hh:02d}:{mm:02d}:{ss:02d}.{ff:02d}", sec

def _extract_time_info_from_clip_id(clip_id):
    """
    Return dict with timestamp details from clip id/segment id if parsable.
    """
    cid = str(clip_id).strip()
    m_clip = CLIP_ID_PATTERN.match(cid)
    if m_clip:
        day, t = m_clip.groups()
        display, sec = _parse_hms8(t)
        return {
            'day': int(day),
            'timestamp_display': display,
            'second_of_day': sec,
            'segment_start_display': None,
            'segment_end_display': None
        }

    m_seg = SEGMENT_ID_PATTERN.match(cid)
    if m_seg:
        day, start_t, end_t = m_seg.groups()
        start_display, start_sec = _parse_hms8(start_t)
        end_display, end_sec = _parse_hms8(end_t)
        return {
            'day': int(day),
            'timestamp_display': None,
            'second_of_day': None,
            'segment_start_display': start_display,
            'segment_end_display': end_display,
            'segment_start_second': start_sec,
            'segment_end_second': end_sec
        }
    return {}

def _format_seconds(val):
    try:
        return f"{float(val):.2f}s"
    except Exception:
        return str(val)

def _format_day_time_from_second(val, day=None):
    """Format second-of-day values as 'Day X Time HH:MM:SS'."""
    try:
        sec = float(val)
    except Exception:
        return str(val)

    # Keep within a 24h clock for display.
    if sec >= 0:
        sec = sec % 86400

    hh = int(sec // 3600)
    mm = int((sec % 3600) // 60)
    ss = sec - (hh * 3600 + mm * 60)

    if abs(ss - round(ss)) < 1e-6:
        time_str = f"{hh:02d}:{mm:02d}:{int(round(ss)):02d}"
    else:
        time_str = f"{hh:02d}:{mm:02d}:{ss:05.2f}"

    if day is not None:
        return f"Day {day} Time {time_str}"
    return f"Time {time_str}"

def _normalize_evidence_items(evidence_items):
    """
    Normalize evidence items to dict form with at least `clip_id`.
    Accepts list[str] or list[dict].
    """
    out = []
    for it in evidence_items:
        if isinstance(it, str):
            cid = it.strip()
            if cid:
                out.append({'clip_id': cid})
        elif isinstance(it, dict):
            cid = (
                it.get('clip_id')
                or it.get('support_clip_id')
                or it.get('query_time')
            )
            if cid:
                x = dict(it)
                x['clip_id'] = str(cid).strip()
                out.append(x)
    return out

def _dedup_evidence_items(items):
    """
    De-duplicate evidence by clip_id so the same clip is not shown repeatedly.
    Merge complementary metadata when duplicates exist.
    """
    def _is_present(v):
        return v not in [None, "", [], {}]

    def _merge_field(existing, incoming, field):
        old = existing.get(field)
        new = incoming.get(field)
        if not _is_present(old) and _is_present(new):
            existing[field] = new
            return
        if _is_present(old) and _is_present(new) and old != new and field in {"source_role", "option_label", "event_id"}:
            old_vals = [x.strip() for x in str(old).split(" | ") if x.strip()]
            new_vals = [x.strip() for x in str(new).split(" | ") if x.strip()]
            merged = []
            seen = set()
            for v in old_vals + new_vals:
                if v not in seen:
                    seen.add(v)
                    merged.append(v)
            existing[field] = " | ".join(merged)

    by_clip = {}
    order = []
    for it in items:
        cid = it.get('clip_id')
        if not cid:
            continue
        if cid not in by_clip:
            by_clip[cid] = dict(it)
            order.append(cid)
            continue

        existing = by_clip[cid]
        # Merge incoming metadata without creating duplicate UI cards.
        for k in set(existing.keys()) | set(it.keys()):
            _merge_field(existing, it, k)

    return [by_clip[cid] for cid in order]

def _build_evidence_meta_lines(item):
    """
    Build readable metadata lines for evidence clip card.
    """
    lines = []
    clip_id = item.get('clip_id')
    lines.append(f"clip_id: {clip_id}")

    source_role = item.get('source_role')
    if source_role:
        lines.append(f"role: {source_role}")

    if item.get('option_label'):
        lines.append(f"option_label: {item.get('option_label')}")
    if item.get('event_id'):
        lines.append(f"event_id: {item.get('event_id')}")
    if item.get('query_time_text'):
        lines.append(f"query_time_text: {item.get('query_time_text')}")

    # Parse day/time from clip id when possible.
    ti = _extract_time_info_from_clip_id(clip_id)
    clip_day = ti.get('day')

    # Preferred explicit seconds from input JSON if available.
    for k in ['clip_second', 'relative_second', 'second_in_clip', 'offset_sec']:
        if k in item and item.get(k) not in [None, ""]:
            lines.append(f"second_in_clip: {_format_seconds(item.get(k))}")
            break

    # Absolute seconds or range if provided.
    for k in ['timestamp_sec', 'start_sec', 'end_sec', 'evidence_second', 'query_second', 'time_sec']:
        if k in item and item.get(k) not in [None, ""]:
            lines.append(f"{k}: {_format_day_time_from_second(item.get(k), day=clip_day)}")

    # Derive second_in_clip from absolute fields when possible.
    try:
        if ('second_in_clip' not in ''.join(lines)) and item.get('timestamp_sec') is not None and item.get('start_sec') is not None:
            sec_clip = float(item.get('timestamp_sec')) - float(item.get('start_sec'))
            if sec_clip >= 0:
                lines.append(f"second_in_clip: {_format_seconds(sec_clip)}")
    except Exception:
        pass

    # Derive second_in_clip from frame index if available (assume 1 FPS unless fps is provided).
    frame_path = item.get('frame_path')
    if frame_path:
        m = re.search(r'frame_(\d+)\.', str(frame_path))
        if m:
            try:
                frame_idx = int(m.group(1))
                fps = float(item.get('fps', 1.0) or 1.0)
                if fps > 0:
                    sec_clip = frame_idx / fps
                    lines.append(f"second_in_clip_estimated: {_format_seconds(sec_clip)} (from frame index, fps={fps:g})")
            except Exception:
                pass

    if ti.get('day') is not None:
        lines.append(f"day: {ti.get('day')}")
    if ti.get('timestamp_display'):
        lines.append(f"time_of_day: {ti.get('timestamp_display')}")
    # Do not show second_of_day fallback; only show clip-relative seconds when available.
    if ti.get('segment_start_display'):
        lines.append(f"segment_start: {ti.get('segment_start_display')}")
    if ti.get('segment_end_display'):
        lines.append(f"segment_end: {ti.get('segment_end_display')}")

    if item.get('frame_path'):
        lines.append(f"frame_path: {item.get('frame_path')}")

    if isinstance(item.get('object_snapshot'), dict):
        snap = item.get('object_snapshot')
        obj = snap.get('object_name')
        loc = snap.get('location')
        status = snap.get('status')
        if obj:
            lines.append(f"object: {obj}")
        if loc:
            lines.append(f"location: {loc}")
        if status:
            if isinstance(status, list):
                lines.append(f"status: {', '.join(map(str, status))}")
            else:
                lines.append(f"status: {status}")

    if item.get('dense_caption_context'):
        ctx = item.get('dense_caption_context')
        if isinstance(ctx, list) and ctx:
            lines.append(f"context: {ctx[0]}")
        elif isinstance(ctx, str):
            lines.append(f"context: {ctx}")

    return lines

def render_evidence_group(title, look_for_note, evidence_items, query_video_loader, evidence_video_loader, expanded=False):
    """
    Render a section of evidence clips with explicit annotation guidance.
    """
    items = _normalize_evidence_items(evidence_items)
    items = _dedup_evidence_items(items)

    st.markdown(f"<div class='evidence-title'>{title}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='evidence-note'>What to look for: {look_for_note}</div>", unsafe_allow_html=True)

    if not items:
        st.caption("No clips available in this group.")
        return

    for i, item in enumerate(items):
        cid = item.get('clip_id')
        with st.expander(f"{title} {i + 1}: {cid}", expanded=expanded and i == 0):
            clip_resolved = resolve_prefer_30s_clip(cid, query_video_loader, evidence_video_loader)
            if clip_resolved:
                render_small_video(clip_resolved, clip_id=cid, video_loader=evidence_video_loader)
            else:
                st.info(f"Video not configured: {cid}")

            meta_lines = _build_evidence_meta_lines(item)
            meta_text = "<br/>".join([f"<b>{line.split(':', 1)[0]}:</b> {line.split(':', 1)[1].strip()}" if ':' in line else line for line in meta_lines])
            st.markdown(f"<div class='evidence-meta'>{meta_text}</div>", unsafe_allow_html=True)

def _extract_identity_token(clip_id):
    """Extract identity token like A3_TASHA from DAYx_A3_TASHA_xxxxxxxx."""
    if not clip_id:
        return None
    parts = str(clip_id).split('_')
    if len(parts) < 3:
        return None
    return f"{parts[1]}_{parts[2]}".upper()

def _sort_clip_id(clip_id):
    """
    Sort key for clip IDs: day then time.
    Falls back to lexicographic for unexpected patterns.
    """
    parts = str(clip_id).split('_')
    if len(parts) < 4:
        return (999, str(clip_id))
    day_str = parts[0].upper().replace('DAY', '')
    time_str = parts[-1]
    try:
        day_num = int(day_str)
    except ValueError:
        day_num = 999
    return (day_num, time_str, str(clip_id))

CLIP_ID_PATTERN = re.compile(r'^DAY(\d+)_A\d+_[A-Za-z0-9]+_(\d{8})$')
SEGMENT_ID_PATTERN = re.compile(r'^DAY(\d+)_A\d+_[A-Za-z0-9]+_(\d{8})_(\d{8})$')
IDENTITY_FROM_VIDEO_ID_PATTERN = re.compile(
    r'^DAY\d+_(A\d+_[A-Za-z0-9]+)_(\d{8})(?:_(\d{8}))?$',
    re.IGNORECASE
)

def _get_day_time_bounds(clip_id):
    """
    Returns (day, start_time, end_time) for clip/segment IDs, else None.
    """
    cid = str(clip_id).strip()
    m_seg = SEGMENT_ID_PATTERN.match(cid)
    if m_seg:
        day, start_t, end_t = m_seg.groups()
        return int(day), int(start_t), int(end_t)

    m_clip = CLIP_ID_PATTERN.match(cid)
    if m_clip:
        day, t = m_clip.groups()
        t = int(t)
        return int(day), t, t

    return None

def _extract_identity_from_video_id(video_id):
    """Extract identity token like A1_JAKE from clip/segment ID."""
    if not video_id:
        return None
    m = IDENTITY_FROM_VIDEO_ID_PATTERN.match(str(video_id).strip())
    if not m:
        return None
    return m.group(1).upper()

def _collect_identity_tokens(questions, scan_limit=400):
    """
    Collect identity tokens from loaded questions.
    Keeps order of first appearance.
    """
    identities = []
    seen = set()

    for q in questions[:scan_limit]:
        candidate_ids = []
        candidate_ids.append(q.get('query_time'))
        candidate_ids.append(q.get('answer_support_clip_id'))

        for e in q.get('evidence_times', []) or []:
            if isinstance(e, dict):
                candidate_ids.append(e.get('clip_id'))

        for ch in q.get('choices', []) or []:
            if isinstance(ch, dict):
                candidate_ids.append(ch.get('support_clip_id'))

        for cid in candidate_ids:
            identity = _extract_identity_from_video_id(cid)
            if identity and identity not in seen:
                seen.add(identity)
                identities.append(identity)

    return identities

def build_evidence_video_roots(questions):
    """
    Build compact evidence roots to avoid scanning the entire EgoLife tree.
    Prefer per-identity directories (e.g., /EgoLife/A1_JAKE).
    """
    roots = []
    seen = set()

    def add_root(path_obj):
        p = Path(path_obj).expanduser()
        key = str(p)
        if key in seen:
            return
        seen.add(key)
        roots.append(p)

    evidence_bases = [Path(config.EVIDENCE_VIDEO_ROOT).expanduser()]
    for fallback in getattr(config, 'EVIDENCE_VIDEO_ROOT_FALLBACKS', []):
        fp = Path(fallback).expanduser()
        if str(fp) not in [str(x) for x in evidence_bases]:
            evidence_bases.append(fp)
    identities = _collect_identity_tokens(questions)

    for base in evidence_bases:
        for identity in identities:
            identity_root = base / identity
            if identity_root.exists():
                add_root(identity_root)

    # Fallback if no identity-specific directory was found.
    if not roots:
        for base in evidence_bases:
            if base.exists():
                add_root(base)

    add_root(config.LOCAL_VIDEO_ROOT)
    add_root(config.CACHE_DIR)
    return roots

def is_before_or_equal_query_time(video_id, query_time):
    """
    Keep videos that occur before or at the query timestamp.
    For segment IDs, use segment start time for ordering.
    """
    if not query_time:
        return True
    vid_bounds = _get_day_time_bounds(video_id)
    query_bounds = _get_day_time_bounds(query_time)
    if not vid_bounds or not query_bounds:
        return True

    vid_day, vid_start, _ = vid_bounds
    query_day, query_start, _ = query_bounds

    if vid_day < query_day:
        return True
    if vid_day > query_day:
        return False
    return vid_start <= query_start

def get_all_video_ids_for_identity(
    query_video_loader,
    evidence_video_loader,
    identity_token=None,
    query_time=None,
    only_before_query_time=False
):
    """
    Build a full list of available video IDs from local index + mapping keys.
    If identity_token is given (e.g. A3_TASHA), filter to that identity.
    """
    clip_ids = set()

    for loader in [query_video_loader, evidence_video_loader]:
        try:
            clip_ids.update(loader.local_index.get('direct', {}).keys())
            clip_ids.update(loader.url_map.keys())
        except Exception:
            continue

    cleaned = []
    for cid in clip_ids:
        cid = str(cid).strip()
        if not cid:
            continue
        if identity_token and identity_token.upper() not in cid.upper():
            continue
        if only_before_query_time and query_time and not is_before_or_equal_query_time(cid, query_time):
            continue
        cleaned.append(cid)

    return sorted(set(cleaned), key=_sort_clip_id)

def get_full_2h_segment_ids(query_video_loader, identity_token=None, query_time=None):
    """
    Return full 2-hour segment IDs available for this identity.
    """
    seg_ids = []
    try:
        for cid in query_video_loader.local_index.get('direct', {}).keys():
            if not SEGMENT_ID_PATTERN.match(str(cid)):
                continue
            if identity_token and identity_token.upper() not in str(cid).upper():
                continue
            if query_time and not is_before_or_equal_query_time(cid, query_time):
                continue
            seg_ids.append(str(cid))
    except Exception:
        return []
    return sorted(set(seg_ids), key=_sort_clip_id)

def _stable_question_uid(question, idx):
    """Build a stable UID for each question to support exact resume."""
    for key in ['sample_id', 'query_id', 'qa_id', 'id']:
        val = question.get(key)
        if val not in [None, '']:
            return str(val)
    base = f"{question.get('query', '')}|{question.get('correct_choice', '')}"
    digest = hashlib.sha1(base.encode('utf-8')).hexdigest()[:12]
    return f"auto_{idx}_{digest}"

def _build_question_uid_list(questions):
    """Ensure question UIDs are unique even if sample IDs repeat."""
    used = {}
    uids = []
    for idx, q in enumerate(questions):
        base_uid = _stable_question_uid(q, idx)
        if base_uid in used:
            used[base_uid] += 1
            uid = f"{base_uid}__dup{used[base_uid]}"
        else:
            used[base_uid] = 0
            uid = base_uid
        uids.append(uid)
    return uids

def _hash_file_identity(path_str):
    """Dataset identity from absolute path + mtime + size."""
    p = Path(path_str).expanduser()
    if not p.exists():
        return hashlib.sha1(str(path_str).encode('utf-8')).hexdigest()[:16]
    stat = p.stat()
    raw = f"{p.resolve()}::{stat.st_size}::{stat.st_mtime_ns}"
    return hashlib.sha1(raw.encode('utf-8')).hexdigest()[:16]

def _dataset_name_to_output_id(name):
    """
    Build a stable output ID from dataset file name.
    Example: A1_JAKE_entity_mem_annotation_input.json -> A1_JAKE_entity_mem_annotation_input
    """
    stem = Path(str(name)).stem
    clean = re.sub(r'[^a-zA-Z0-9._-]+', '_', stem).strip('._-')
    return clean or "dataset"

def _persist_uploaded_json(uploaded_json):
    """Persist uploaded JSON bytes to data/uploaded_sources and return path + dataset_id + parsed data."""
    raw_bytes = uploaded_json.getvalue()
    dataset_id = hashlib.sha1(raw_bytes).hexdigest()[:16]
    upload_dir = Path(config.DATA_DIR) / "uploaded_sources"
    upload_dir.mkdir(parents=True, exist_ok=True)
    safe_name = re.sub(r'[^a-zA-Z0-9._-]+', '_', uploaded_json.name)
    local_path = upload_dir / f"{dataset_id}_{safe_name}"
    if not local_path.exists():
        local_path.write_bytes(raw_bytes)
    parsed = json.loads(raw_bytes.decode('utf-8'))
    return str(local_path), dataset_id, parsed

def _progress_output_path(progress_key):
    safe = re.sub(r'[^a-zA-Z0-9._-]+', '_', str(progress_key))
    if len(safe) > 180:
        safe = safe[:180]
    return str(Path(config.DATA_DIR) / f"progress_{safe}.json")

def _responses_output_path(output_id):
    safe = re.sub(r'[^a-zA-Z0-9._-]+', '_', str(output_id))
    if len(safe) > 180:
        safe = safe[:180]
    return str(Path(config.DATA_DIR) / f"responses_{safe}.jsonl")

def main():
    # Initialize session state
    initialize_session()

    # Sidebar
    with st.sidebar:
        st.title("Video Annotation")

        # Video source selector
        st.subheader("📹 Video Source")
        if 'video_source' not in st.session_state:
            st.session_state.video_source = getattr(config, 'DEFAULT_VIDEO_SOURCE', 'gdrive')

        video_source = st.radio(
            "Select video source:",
            options=['gdrive', 'onedrive'],
            format_func=lambda x: "Google Drive (30s clips)" if x == 'gdrive' else "OneDrive (Full videos)",
            key='video_source_selector',
            index=0 if st.session_state.video_source == 'gdrive' else 1
        )
        st.session_state.video_source = video_source

        if video_source == 'gdrive':
            st.caption("✓ Google Drive folder configured")
        else:
            st.caption("✓ OneDrive folder configured (Long videos)")

        st.markdown("---")

        # Data source selector
        default_data_path = st.session_state.get('data_file_path', str(config.DATA_FILE))
        data_file_path = st.text_input(
            "Annotation JSON path",
            value=default_data_path,
            help="Path to a local annotation JSON file."
        ).strip()
        st.session_state.data_file_path = data_file_path

        uploaded_json = st.file_uploader(
            "Or upload updated annotation JSON",
            type=['json'],
            accept_multiple_files=False
        )

        if uploaded_json is not None:
            try:
                persisted_upload_path, dataset_id, uploaded_data = _persist_uploaded_json(uploaded_json)
                questions = parse_questions_data(uploaded_data)
                current_source_key = f"path::{persisted_upload_path}"
                dataset_name = _dataset_name_to_output_id(uploaded_json.name)
                source_caption = f"Loaded from upload: {uploaded_json.name} (saved as {persisted_upload_path})"
            except json.JSONDecodeError as e:
                st.error(f"Failed to parse uploaded JSON: {e}")
                questions = []
                current_source_key = "upload::invalid"
                dataset_id = "invalid_upload"
                dataset_name = "invalid_upload"
                source_caption = "Upload parse failed"
        else:
            questions = load_questions(data_file_path)
            current_source_key = f"path::{data_file_path}"
            dataset_id = _hash_file_identity(data_file_path)
            dataset_name = _dataset_name_to_output_id(data_file_path)
            source_caption = f"Loaded from path: {data_file_path}"

        st.caption(source_caption)

        total_questions = len(questions)
        if total_questions <= 0:
            st.error("No questions loaded. Check the JSON path or uploaded file.")
            st.stop()

        # Google Drive - no need for local evidence roots
        st.caption("Videos loaded from Google Drive")
        st.caption(f"Dataset: {dataset_name}")

        # Initialize user_id if not exists
        if 'user_id' not in st.session_state or not st.session_state.user_id:
            st.session_state.user_id = "annotator_001"

        # Build dataset+output context and auto-resume to exact sample UID.
        question_uids = _build_question_uid_list(questions)
        uid_to_idx = {uid: idx for idx, uid in enumerate(question_uids)}
        progress_key = f"{dataset_id}::{st.session_state.user_id}"
        responses_output_path = _responses_output_path(st.session_state.user_id)

        if st.session_state.get('active_progress_key') != progress_key:
            context_responses = load_responses(
                filter_user_id=st.session_state.user_id,
                filter_dataset_id=dataset_id,
                response_file=responses_output_path
            )
            answered_uids = {
                r.get('question_uid') for r in context_responses if r.get('question_uid')
            }

            progress_data = load_progress(progress_key)
            resume_idx = 0
            if progress_data:
                resume_uid = progress_data.get('current_question_uid')
                if resume_uid in uid_to_idx:
                    resume_idx = uid_to_idx[resume_uid]
                else:
                    idx = progress_data.get('current_index', 0)
                    if isinstance(idx, int):
                        resume_idx = max(0, min(idx, total_questions))
            else:
                # If no checkpoint file, resume from first unanswered UID.
                for i, uid in enumerate(question_uids):
                    if uid not in answered_uids:
                        resume_idx = i
                        break
                else:
                    resume_idx = total_questions

            st.session_state.current_index = resume_idx
            st.session_state.responses = context_responses
            st.session_state.question_start_time = time.time()
            st.session_state.active_progress_key = progress_key
            st.session_state.active_dataset_id = dataset_id
            st.session_state.questions_source_key = current_source_key
            st.session_state.resume_checkpoint = progress_data if progress_data else {}

        # Keep current context metadata refreshed.
        st.session_state.active_dataset_id = dataset_id
        st.session_state.active_progress_key = progress_key

        # User ID input
        if 'user_id' not in st.session_state or not st.session_state.user_id:
            st.session_state.user_id = st.text_input(
                "Enter your Annotator ID:",
                value="annotator_001",
                key="user_id_input"
            )
        else:
            st.info(f"Annotator: {st.session_state.user_id}")

        st.markdown("---")

        completed_uids = {
            r.get('question_uid') for r in st.session_state.responses if r.get('question_uid')
        }
        completed_count = len(completed_uids)
        remaining_count = max(total_questions - completed_count, 0)

        # Progress info
        st.metric("Total Questions", total_questions)
        st.metric("Current Question", min(st.session_state.current_index + 1, total_questions if total_questions > 0 else 1))
        st.metric("Completed", completed_count)
        st.metric("Remaining", remaining_count)

        # Progress bar
        progress = completed_count / total_questions if total_questions > 0 else 0
        st.progress(progress)
        st.caption(f"Progress: {progress*100:.1f}%")

        st.markdown("---")
        st.caption(f"Dataset: {dataset_name}")
        st.caption(f"Resume key: {progress_key}")
        checkpoint = st.session_state.get('resume_checkpoint', {})
        with st.expander("Resume Status", expanded=True):
            if checkpoint:
                st.caption(f"Last saved: {checkpoint.get('last_saved', 'N/A')}")
                st.caption(f"Saved question UID: {checkpoint.get('current_question_uid', 'N/A')}")
                st.caption(f"Saved index: {checkpoint.get('current_index', 'N/A')}")
            else:
                st.caption("No previous checkpoint for this dataset + annotator.")
            current_uid = question_uids[st.session_state.current_index] if st.session_state.current_index < len(question_uids) else "N/A"
            st.caption(f"Current question UID: {current_uid}")
            st.caption("Auto-save is enabled on submit/skip/navigation.")

        with st.expander("Output Files", expanded=True):
            responses_path = responses_output_path
            progress_path = _progress_output_path(progress_key)
            st.caption(f"Responses JSONL: {responses_path}")
            st.caption(f"Progress checkpoint: {progress_path}")

        st.markdown("---")

        # Navigation
        st.subheader("Navigation")

        def _uid_for_index(idx):
            if 0 <= idx < len(question_uids):
                return question_uids[idx]
            return None

        def _save_checkpoint(idx):
            uid = _uid_for_index(idx)
            save_progress(
                idx,
                st.session_state.responses,
                progress_key=progress_key,
                extra_state={
                    'dataset_id': dataset_id,
                    'current_question_uid': uid
                }
            )
            st.session_state.resume_checkpoint = {
                'last_saved': datetime.now().isoformat(),
                'current_index': idx,
                'current_question_uid': uid
            }

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Previous", disabled=st.session_state.current_index == 0):
                st.session_state.current_index -= 1
                st.session_state.question_start_time = time.time()
                _save_checkpoint(st.session_state.current_index)
                st.rerun()
        with col2:
            if st.button("Skip", disabled=st.session_state.current_index >= total_questions - 1):
                st.session_state.current_index += 1
                st.session_state.question_start_time = time.time()
                _save_checkpoint(st.session_state.current_index)
                st.rerun()

        # Jump to question
        jump_to = st.number_input(
            "Jump to question:",
            min_value=1,
            max_value=total_questions,
            value=st.session_state.current_index + 1,
            key="jump_input"
        )
        if st.button("Go"):
            st.session_state.current_index = jump_to - 1
            st.session_state.question_start_time = time.time()
            _save_checkpoint(st.session_state.current_index)
            st.rerun()

        st.markdown("---")

        # Save and export
        if st.button("💾 Save Progress"):
            _save_checkpoint(st.session_state.current_index)
            st.success("Progress saved!")

        if st.button("📥 Export Responses"):
            export_file = export_responses(st.session_state.responses)
            st.success(f"Exported to {export_file}")

            # Add download button
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            jsonl_content = ""
            for response in st.session_state.responses:
                jsonl_content += json.dumps(response, ensure_ascii=False) + '\n'

            st.download_button(
                label="⬇️ Download Responses",
                data=jsonl_content,
                file_name=f'responses_{timestamp}.jsonl',
                mime='application/jsonl',
                key=f'download_responses_{timestamp}'
            )

    # Main content
    if st.session_state.current_index >= total_questions:
        st.balloons()
        st.success("🎉 You have completed all questions!")
        st.metric("Total Time Spent", f"{sum([r.get('time_spent_seconds', 0) for r in st.session_state.responses]):.0f} seconds")
        st.metric("Accuracy", f"{sum([1 for r in st.session_state.responses if r.get('is_correct', False)]) / len(st.session_state.responses) * 100:.1f}%" if st.session_state.responses else "N/A")

        if st.button("🔄 Start Over"):
            st.session_state.current_index = 0
            st.session_state.responses = []
            st.session_state.question_start_time = time.time()
            st.rerun()
        return

    # Get current question
    current_question = questions[st.session_state.current_index]
    current_question_uid = question_uids[st.session_state.current_index] if st.session_state.current_index < len(question_uids) else f"idx_{st.session_state.current_index}"
    choices = current_question.get('choices', [])
    correct_answer = current_question.get('correct_choice', '')

    # Header
    st.markdown(f"<div class='main-header'>Question {st.session_state.current_index + 1} of {total_questions}</div>", unsafe_allow_html=True)

    # Video loaders - create based on selected source
    video_source = st.session_state.get('video_source', 'gdrive')

    if video_source == 'gdrive':
        # Google Drive loaders
        query_video_loader = VideoLoaderGDrive(
            base_folder_url=config.GDRIVE_BASE_FOLDER,
            mapping_file=config.VIDEO_MAPPING_FILE
        )
        evidence_video_loader = VideoLoaderGDrive(
            base_folder_url=config.GDRIVE_BASE_FOLDER,
            mapping_file=config.VIDEO_MAPPING_FILE
        )
    else:
        # OneDrive loaders
        query_video_loader = VideoLoaderOneDriveFolder(
            folder_url=config.ONEDRIVE_VIDEO_FOLDER
        )
        evidence_video_loader = VideoLoaderOneDriveFolder(
            folder_url=config.ONEDRIVE_VIDEO_FOLDER
        )

    # Layout: Video on left, Question and choices on right
    col_left, col_right = st.columns([2.2, 2.8])

    with col_left:
        st.subheader("🎬 Evidence Review (30s Clips)")
        query_time = current_question.get('query_time', '')
        identity_token = _extract_identity_token(query_time)

        query_items = []
        if query_time:
            query_items.append({
                'clip_id': query_time,
                'source_role': 'query_time',
                'query_time_text': current_question.get('raw_query_time', ''),
                'frame_path': current_question.get('query_frame_path', '')
            })

        answer_support_clip = current_question.get('answer_support_clip_id', '')
        explicit_correct_items = []
        explicit_distractor_items = []
        for e in current_question.get('evidence_times', []):
            if not isinstance(e, dict):
                continue
            x = dict(e)
            x['source_role'] = x.get('source_role', 'supporting_evidence')
            cid = x.get('clip_id', '')
            role = str(x.get('source_role', '')).strip().lower()

            # Keep evidence grouping explicit and avoid showing all evidence as "correct".
            if role in {'correct_option', 'correct', 'answer_support', 'answer_support_clip'}:
                explicit_correct_items.append(x)
            elif role in {'distractor', 'distractor_evidence', 'negative'}:
                explicit_distractor_items.append(x)
            elif cid and query_time and str(cid) == str(query_time):
                query_items.append(x)
            elif cid and answer_support_clip and str(cid) == str(answer_support_clip):
                explicit_correct_items.append(x)
            else:
                explicit_distractor_items.append(x)

        correct_option_items = []
        distractor_items = []
        for ch in choices:
            cid = ch.get('support_clip_id', '')
            if not cid:
                continue
            option_item = {
                'clip_id': cid,
                'source_role': 'choice_support',
                'option_label': ch.get('label', ''),
                'event_id': ch.get('event_id', ''),
                'frame_path': ch.get('support_frame_path', ''),
            }
            if ch.get('label', '') == correct_answer:
                correct_option_items.append(option_item)
            else:
                distractor_items.append(option_item)

        # Fallback: include answer support clip in correct-evidence group.
        if answer_support_clip:
            correct_option_items.append({
                'clip_id': answer_support_clip,
                'source_role': 'answer_support_clip'
            })

        render_evidence_group(
            title="Query Evidence",
            look_for_note="Find the anchor moment and scene context at query time.",
            evidence_items=query_items,
            query_video_loader=query_video_loader,
            evidence_video_loader=evidence_video_loader,
            expanded=True
        )
        render_evidence_group(
            title="Correct Option Evidence",
            look_for_note="Check evidence that supports why the ground-truth option is correct.",
            evidence_items=explicit_correct_items + correct_option_items,
            query_video_loader=query_video_loader,
            evidence_video_loader=evidence_video_loader
        )
        render_evidence_group(
            title="Distractor Evidence",
            look_for_note="Check why distractors are plausible but still incorrect.",
            evidence_items=explicit_distractor_items + distractor_items,
            query_video_loader=query_video_loader,
            evidence_video_loader=evidence_video_loader
        )

        # Optional browser - Google Drive folder
        with st.expander("📂 Browse All Videos (Google Drive)", expanded=False):
            st.markdown(f"""
            <a href="{config.GDRIVE_BASE_FOLDER}" target="_blank" style="
                display: inline-block;
                padding: 12px 24px;
                background-color: #4285f4;
                color: white;
                text-decoration: none;
                border-radius: 6px;
                font-size: 14px;
                font-weight: 600;
            ">
                📂 Open Google Drive Folder
            </a>
            """, unsafe_allow_html=True)
            if identity_token:
                st.caption(f"Look for folder: {identity_token}")

    with col_right:
        st.markdown("<div class='right-panel'>", unsafe_allow_html=True)

        # Question
        st.markdown("<div class='question-box'>", unsafe_allow_html=True)
        st.markdown("### Question")
        st.markdown(f"**{current_question.get('query', 'No question text')}**")
        st.markdown("</div>", unsafe_allow_html=True)

        with st.expander("📘 Annotation Guidelines", expanded=True):
            st.markdown("<div class='annotation-guide'>", unsafe_allow_html=True)
            st.markdown(
                "1. Review Query Evidence first to locate the anchor moment.\n"
                "2. Review Correct Option Evidence and confirm why ground truth is valid.\n"
                "3. Review Distractor Evidence and check whether distractors are truly incorrect.\n"
                "4. If query wording is unclear, revise it in 'Updated query text'.\n"
                "5. Use Overall decision: Accept / Revise / Reject."
            )
            st.markdown("</div>", unsafe_allow_html=True)

        # Additional info
        with st.expander("Additional Information"):
            st.caption(f"**Sample ID:** {current_question.get('sample_id', 'N/A')}")
            st.caption(f"**Object:** {current_question.get('object_name', 'N/A')}")
            st.caption(f"**Query Type:** {current_question.get('query_type', 'N/A')}")
            st.caption(f"**Difficulty:** {current_question.get('difficulty_tier', 'N/A')} ({current_question.get('difficulty_score', 0):.2f})")

        # Choices
        st.markdown("### 📝 Options and Ground Truth")
        choices = current_question.get('choices', [])
        correct_answer = current_question.get('correct_choice', '')
        gt_text = ""
        for choice in choices:
            label = choice.get('label', '')
            text = choice.get('text', '')
            is_gt = (label == correct_answer)
            if is_gt:
                gt_text = text
            suffix = " ✅ Ground Truth" if is_gt else ""
            st.markdown(
                f"<div class='option-item'><b>{label}.</b> {text}{suffix}</div>",
                unsafe_allow_html=True
            )

        if correct_answer:
            st.info(f"Ground-truth label: {correct_answer}")
        if gt_text:
            st.caption(f"Ground-truth text: {gt_text}")

        with st.expander("🎥 Choice Support Videos", expanded=False):
            for choice in choices:
                label = choice.get('label', '')
                support_clip = choice.get('support_clip_id', '')
                if support_clip:
                    with st.expander(f"Choice {label}: {support_clip}", expanded=False):
                        support_clip_resolved = resolve_clip_video_url(support_clip, query_video_loader, evidence_video_loader)
                        if support_clip_resolved:
                            render_small_video(support_clip_resolved, clip_id=support_clip, video_loader=evidence_video_loader)
                        else:
                            st.info(f"Support video not configured: {support_clip}")

        st.markdown("### ✅ Human Verification")

        query_quality = st.radio(
            "Query quality",
            [
                "Good query (clear and answerable)",
                "Needs minor revision (wording/style)",
                "Needs major revision (logic/temporal ambiguity)",
                "Bad query (not answerable or invalid)",
            ],
            key=f"query_quality_{st.session_state.current_index}"
        )

        query_action = st.radio(
            "Query action",
            [
                "Keep original query",
                "Revise query text",
                "Reject this sample",
            ],
            key=f"query_action_{st.session_state.current_index}"
        )

        revised_query = st.text_area(
            "Updated query text (edit when needed)",
            value=current_question.get('query', ''),
            height=120,
            key=f"revised_query_{st.session_state.current_index}"
        )

        generated_answer_check = st.radio(
            "Generated correct choice quality",
            [
                "Correct",
                "Incorrect",
                "Unsure",
            ],
            horizontal=True,
            key=f"answer_quality_{st.session_state.current_index}"
        )

        options_quality = st.radio(
            "Options quality",
            [
                "Good options",
                "Usable but needs edits",
                "Bad options (regenerate)",
            ],
            horizontal=True,
            key=f"options_quality_{st.session_state.current_index}"
        )

        observed_issues = st.multiselect(
            "Observed issues",
            [
                "Ambiguous query",
                "Temporal inconsistency",
                "Multiple plausible correct options",
                "No correct option",
                "Distractors too easy",
                "Distractors unrealistic",
                "Option wording unclear",
                "Other",
            ],
            key=f"issues_{st.session_state.current_index}"
        )

        overall_decision = st.radio(
            "Overall decision",
            [
                "Accept",
                "Revise",
                "Reject",
            ],
            horizontal=True,
            key=f"overall_{st.session_state.current_index}"
        )

        verification_notes = st.text_area(
            "Verification notes",
            value="",
            height=90,
            key=f"notes_{st.session_state.current_index}"
        )

        st.markdown("---")

        # Submit button
        col_submit, col_skip = st.columns(2)
        with col_submit:
            if st.button("Submit Verification", type="primary", use_container_width=True):
                if query_action == "Revise query text" and not revised_query.strip():
                    st.warning("Please provide revised query text or choose another query action.")
                    st.stop()

                # Calculate time spent
                time_spent = time.time() - st.session_state.question_start_time

                # Save response
                response = {
                    'sample_id': current_question.get('sample_id', ''),
                    'question_uid': current_question_uid,
                    'question_index': st.session_state.current_index,
                    'dataset_id': dataset_id,
                    'source_key': current_source_key,
                    'user_answer': None,
                    'correct_answer': correct_answer,
                    'is_correct': None,
                    'time_spent_seconds': round(time_spent, 2),
                    'timestamp': datetime.now().isoformat(),
                    'user_id': st.session_state.user_id,
                    'human_verification': {
                        'query_quality': query_quality,
                        'query_action': query_action,
                        'original_query': current_question.get('query', ''),
                        'revised_query': revised_query.strip(),
                        'generated_answer_check': generated_answer_check,
                        'options_quality': options_quality,
                        'observed_issues': observed_issues,
                        'overall_decision': overall_decision,
                        'notes': verification_notes.strip(),
                        'ground_truth_label': correct_answer,
                        'ground_truth_text': gt_text
                    }
                }

                response['annotation_output_id'] = st.session_state.user_id
                save_response(response, response_file=responses_output_path)
                st.session_state.responses.append(response)
                st.success("Verification saved.")
                st.info(f"Time spent: {time_spent:.1f} seconds")

                # Auto-advance after 2 seconds
                time.sleep(2)
                st.session_state.current_index += 1
                st.session_state.question_start_time = time.time()
                _save_checkpoint(st.session_state.current_index)
                st.rerun()

        with col_skip:
            if st.button("Skip Question", use_container_width=True):
                st.session_state.current_index += 1
                st.session_state.question_start_time = time.time()
                _save_checkpoint(st.session_state.current_index)
                st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
