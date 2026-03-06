import json
import os
import time
import re
import streamlit as st
from typing import List, Dict, Any

# --- CONFIGURATION ---
PAGE_TITLE = "Multimodal-Attribution Annotation v5.7 (Empty Fix)"
LAYOUT = "wide"

# --- HELPER: TIME PARSING ---

def parse_timestamp_str(time_str: str) -> float:
    try:
        parts = time_str.strip().split(':')
        if len(parts) == 2:
            minutes, seconds = map(float, parts)
            return minutes * 60 + seconds
        elif len(parts) == 3:
            hours, minutes, seconds = map(float, parts)
            return hours * 3600 + minutes * 60 + seconds
        return -1.0
    except ValueError:
        return -1.0

def extract_citations_from_sentence(sentence: str) -> List[Dict[str, Any]]:
    citations = []
    parenthetical_matches = re.finditer(r'\((.*?)\)', sentence)
    
    for match in parenthetical_matches:
        full_content = match.group(1)
        segments = full_content.split(';')
        
        for segment in segments:
            segment = segment.strip()
            citation_pattern = r'^\s*([a-zA-Z]+)\s*,\s*(\d+:\d+(?:-\d+:\d+)?)\s*$'
            seg_match = re.match(citation_pattern, segment)
            
            if seg_match:
                modality = seg_match.group(1).lower()
                time_part = seg_match.group(2)
                
                if '-' in time_part:
                    start_str, end_str = time_part.split('-', 1)
                    start_time = parse_timestamp_str(start_str)
                    end_time = parse_timestamp_str(end_str)
                else:
                    start_time = parse_timestamp_str(time_part)
                    end_time = start_time
                
                citations.append({
                    'text': f"({segment})",
                    'modality': modality, # 'audio' or 'visual'
                    'start': start_time,
                    'end': end_time
                })
    return citations

# --- HELPER: FILE MATCHING ---

def get_file_timestamps(filename: str) -> tuple:
    root, ext = os.path.splitext(filename)

    is_image = ext.lower() in ['.jpg', '.jpeg', '.png', '.webp']
    
    pattern_range = re.compile(r'_(\d+)_(\d+)$') 
    pattern_point = re.compile(r'_(\d+)$')        

    # Only look for a range if it's NOT an image
    if not is_image:
        match_range = pattern_range.search(root)
        if match_range:
            return float(match_range.group(1)), float(match_range.group(2))
    
    # Fallback to point match
    match_point = pattern_point.search(root)
    if match_point:
        val = float(match_point.group(1))
        return val, val
        
    return None, None

def get_file_modality(filename: str) -> str:
    """Returns 'audio', 'visual', or 'unknown' based on extension."""
    ext = os.path.splitext(filename)[1].lower()
    if ext in ['.mp4', '.mov', '.webm', '.mkv', '.avi', '.jpg', '.png', '.jpeg']:
        return 'visual'
    if ext in ['.mp3', '.wav', '.ogg', '.flac', '.m4a']:
        return 'audio'
    return 'unknown'

def find_matching_files(target_citations: List[Dict], all_filenames: List[str]) -> List[Dict]:
    results = []
    file_inventory = []
    
    # Pre-process inventory
    for fname in all_filenames:
        s, e = get_file_timestamps(fname)
        modality = get_file_modality(fname)
        if s is not None:
            file_inventory.append({'name': fname, 'start': s, 'end': e, 'modality': modality})
            
    for cit in target_citations:
        target_start = cit['start']
        target_modality = cit['modality'] # e.g., 'audio' or 'visual'
        
        found_match = None
        
        # Filter 1: Time Match (tolerance 1.5s)
        time_candidates = [f for f in file_inventory if abs(f['start'] - target_start) < 1.5]
        
        # Filter 2: Modality Match
        for cand in time_candidates:
            if cand['modality'] == target_modality:
                found_match = cand['name']
                break
        
        if found_match:
            results.append({
                "citation_text": cit['text'], 
                "status": "found", 
                "filename": found_match, 
                "ui_label": f"{cit['text']}"
            })
        else:
            results.append({
                "citation_text": cit['text'], 
                "status": "missing", 
                "filename": None, 
                "ui_label": f"{cit['text']} (⚠️ File Missing)"
            })
    return results

# --- APP FUNCTIONS ---

@st.cache_data(show_spinner=False)
def load_data(input_path):
    if not os.path.exists(input_path): return []
    data = []
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip(): data.append(json.loads(line))
    except Exception as e:
        st.error(f"Error reading file: {e}")
    return data

def get_processed_count(output_path):
    if not os.path.exists(output_path): return 0
    with open(output_path, 'r', encoding='utf-8') as f:
        return sum(1 for _ in f)

def save_annotation(output_path, entry, atomic_facts, phase_1_indices, phase_2_data, duration_seconds):
    result = entry.copy()
    
    # --- Phase 1 Data ---
    coverage_dict = {}
    for idx, status in phase_1_indices.items():
        if 0 <= idx < len(atomic_facts):
            coverage_dict[atomic_facts[idx]] = status
    result['interpretability_judgment'] = coverage_dict 

    # --- Phase 2 Data ---
    attribution_dict = {}
    for idx, data in phase_2_data.items():
        if 0 <= idx < len(atomic_facts):
            
            # CASE A: Explicitly Skipped (No Citations)
            if 'citation_recall' in data and data['citation_recall'] is None:
                 attribution_dict[atomic_facts[idx]] = {
                    "citation_recall": None,
                    "evidences": []
                }
            
            # CASE B: Normal Attribution
            elif 'support_judgment' in data:
                is_recall = (data['support_judgment'] == "Supported")
                attribution_dict[atomic_facts[idx]] = {
                    "citation_recall": is_recall,
                    "evidences": data['necessary_evidences']
                }
        
    result['attribution_judgment'] = attribution_dict
    result['annotation_time_seconds'] = round(duration_seconds, 2)
    result['annotated_at'] = time.time()
    
    try:
        with open(output_path, 'a', encoding='utf-8') as f:
            f.write(json.dumps(result) + "\n")
    except Exception as e:
        st.error(f"Failed to save: {e}")

def render_media(file_path):
    if not os.path.exists(file_path):
        st.error(f"File not found: {os.path.basename(file_path)}")
        return
    ext = os.path.splitext(file_path)[1].lower()
    if ext in ['.mp4', '.mov', '.webm', '.mkv']: st.video(file_path)
    elif ext in ['.mp3', '.wav', '.ogg', '.flac']: 
        st.audio(file_path)
        st.caption(f"Audio: {os.path.basename(file_path)}")
    elif ext in ['.jpg', '.jpeg', '.png', '.webp']: st.image(file_path)
    else: st.warning(f"Unsupported format: {ext}")

# --- MAIN ---

def main():
    st.set_page_config(page_title=PAGE_TITLE, layout=LAYOUT)

    # --- SIDEBAR ---
    st.sidebar.title("⚙️ Config")
    input_file = st.sidebar.text_input("Input Path", value="./data.jsonl").strip()
    media_dir = st.sidebar.text_input("Media Dir", value="./snippets").strip()
    output_file = st.sidebar.text_input("Output Path", value="./annotations.jsonl").strip()

    if not os.path.exists(input_file):
        st.warning(f"Input file not found: {input_file}")
        st.stop()

    if "all_tasks" not in st.session_state:
        st.session_state.all_tasks = load_data(input_file)
    
    tasks = st.session_state.all_tasks
    processed_count = get_processed_count(output_file)
    current_idx = processed_count
    
    if current_idx >= len(tasks):
        st.success("🎉 All tasks completed!")
        st.stop()

    current_task = tasks[current_idx]
    
    # Data Mapping
    atomic_facts = current_task.get('atomic_facts_final', current_task.get('atomic_facts', []))
    extracted_files = current_task.get('extracted_files', [])
    target_sentence = current_task.get('sentence_text', '')
    full_context_text = current_task.get('full_generation_text', current_task.get('context_text', ''))
    original_meta = current_task.get('original_metadata', {})
    user_question = original_meta.get('question', '(No question found)')
    
    # Path to full video
    original_video_name = original_meta.get('video_path', current_task.get('video', ''))
    if "/" in original_video_name: 
        original_video_name = os.path.basename(original_video_name)
    full_video_path = os.path.join(media_dir, original_video_name)

    # State Management
    task_key = f"task_{current_idx}"
    if "current_task_key" not in st.session_state or st.session_state.current_task_key != task_key:
        st.session_state.current_task_key = task_key
        st.session_state.task_start_time = time.time()
        st.session_state.wizard_mode = "step1" 
        st.session_state.step1_ptr = 0
        st.session_state.step1_results = {} 
        st.session_state.step2_queue = [] 
        st.session_state.step2_ptr = 0
        st.session_state.step2_results = {} 

    st.sidebar.progress((current_idx) / len(tasks))
    st.sidebar.markdown(f"**Task:** {current_idx + 1} / {len(tasks)}")
    
    col_left, col_right = st.columns([1, 1.2])

    # === LEFT COLUMN: CONTEXT & MEDIA ===
    with col_left:
        st.subheader("Context Board")
        
        tab_text, tab_video = st.tabs(["📄 Context Info", "🎬 Full Video"])
        
        with tab_text:
            st.markdown("**Original Question:**")
            st.info(user_question)
            st.text_area("Full Generation", full_context_text, height=200, disabled=True)
            st.markdown("**Target Sentence:**")
            st.warning(target_sentence)
            
        with tab_video:
            if os.path.exists(full_video_path):
                st.video(full_video_path)
            else:
                fallback_path = os.path.join(media_dir, original_video_name)
                if os.path.exists(fallback_path):
                    st.video(fallback_path)
                else:
                    st.warning(f"Full video not found at: {full_video_path}")
        
        # Phase 2 Specific: Evidence Snippets
        if st.session_state.wizard_mode == "step2":
            st.divider()
            st.subheader("Attribution Evidence (Snippets)")
            if st.session_state.step2_queue:
                curr_fact_idx = st.session_state.step2_queue[st.session_state.step2_ptr]
                curr_fact_text = atomic_facts[curr_fact_idx]
                citations_needed = extract_citations_from_sentence(curr_fact_text)
                matched_items = find_matching_files(citations_needed, extracted_files)

                if not matched_items:
                    st.info("ℹ️ No specific timestamped citations detected for this fact.")
                else:
                    for idx, item in enumerate(matched_items):
                        st.markdown(f"**Snippet {idx+1}: {item['citation_text']}**")
                        if item['status'] == 'found':
                            render_media(os.path.join(media_dir, item['filename']))
                        else:
                            st.error(f"File missing: {item['filename']}")
                        st.divider()

    # === RIGHT COLUMN: ANNOTATION ===
    with col_right:
        
        # --- NEW: EMPTY LIST CHECK ---
        if not atomic_facts:
            st.warning("⚠️ This task contains no atomic facts.")
            if st.button("Submit Empty & Next", type="primary"):
                save_annotation(output_file, current_task, [], {}, {}, time.time() - st.session_state.task_start_time)
                st.rerun()
        
        else:
            # --- PHASE 1: CLAIM DETECTION ---
            if st.session_state.wizard_mode == "step1":
                curr_ptr = st.session_state.step1_ptr
                fact_text = atomic_facts[curr_ptr]
                
                st.header(f"Phase 1: Claim Detection ({curr_ptr + 1}/{len(atomic_facts)})")
                st.markdown("##### Atomic Fact:")
                st.success(fact_text)
                st.markdown("**(Q1) Is this fact CHECK-WORTHY?**")
                
                options_map = {
                    "A": "Option A: CHECK-WORTHY (Visual/Audio, Specific Claims)",
                    "B1": "Option B: NOT CHECK-WORTHY (Reason 1: Meta-data)",
                    "B2": "Option B: NOT CHECK-WORTHY (Reason 2: General Knowledge)",
                    "B3": "Option B: NOT CHECK-WORTHY (Reason 3: Subjective)"
                }
                options = list(options_map.values())
                prev_sel = st.session_state.step1_results.get(curr_ptr)
                choice = st.radio("Select Category:", options, index=options.index(prev_sel) if prev_sel in options else None)
                
                c_back, c_next = st.columns([1, 1])
                with c_back:
                    if curr_ptr > 0 and st.button("⬅️ Back"):
                        st.session_state.step1_ptr -= 1
                        st.rerun()
                with c_next:
                    is_last_step1 = (curr_ptr == len(atomic_facts) - 1)
                    temp_results = st.session_state.step1_results.copy()
                    if choice: temp_results[curr_ptr] = choice
                    to_check = [i for i, r in temp_results.items() if r and "Option A" in r]
                    will_skip_stage2 = (len(to_check) == 0) and is_last_step1
                    
                    btn_label = "Submit Task 🚀" if (is_last_step1 and will_skip_stage2) else ("Proceed to Phase 2 ➡️" if is_last_step1 else "Next Fact")
                    btn_type = "primary" if is_last_step1 else "secondary"
                    
                    if st.button(btn_label, type=btn_type, disabled=(choice is None)):
                        st.session_state.step1_results[curr_ptr] = choice
                        if not is_last_step1:
                            st.session_state.step1_ptr += 1
                            st.rerun()
                        else:
                            st.session_state.step2_queue = to_check
                            if not to_check:
                                save_annotation(output_file, current_task, atomic_facts, st.session_state.step1_results, {}, time.time() - st.session_state.task_start_time)
                                st.rerun()
                            else:
                                st.session_state.wizard_mode = "step2"
                                st.session_state.step2_ptr = 0
                                st.session_state.step2_results = {}
                                st.rerun()

            # --- PHASE 2: ATTRIBUTION ---
            elif st.session_state.wizard_mode == "step2":
                q_idx = st.session_state.step2_ptr
                real_idx = st.session_state.step2_queue[q_idx]
                fact_text = atomic_facts[real_idx]
                
                citations_needed = extract_citations_from_sentence(fact_text)
                matched_items = find_matching_files(citations_needed, extracted_files)
                
                st.header(f"Phase 2: Attribution ({q_idx + 1}/{len(st.session_state.step2_queue)})")
                st.markdown("##### Atomic Fact:")
                st.success(fact_text)
                
                prev_res = st.session_state.step2_results.get(real_idx, {})
                prev_support = prev_res.get("support_judgment", None)
                selected_evidences_text = []
                
                # 1. NO CITATION FOUND -> SKIP
                if not matched_items:
                    st.warning("⚠️ No citations found in this sentence. Skipping attribution step.")
                    support_choice = "SKIPPED_NO_CITATIONS" # Internal flag
                else:
                    # 2. CITATIONS FOUND
                    st.markdown("#### Step A: Verify Support (Recall)")
                    st.markdown("*Do the cited segments, when **combined**, provide enough evidence?*")
                    
                    support_choice = st.radio("Judgment:", ["Supported", "Not Supported"], 
                                              index=["Supported", "Not Supported"].index(prev_support) if prev_support else None, 
                                              horizontal=True, key=f"rad_{real_idx}")

                    if support_choice == "Supported":
                        st.divider()
                        
                        # 3. SINGLE CITATION -> AUTO-SELECT
                        if len(matched_items) == 1:
                            item = matched_items[0]
                            st.info(f"✅ **Single citation detected.** Automatically marked as relevant: **{item['citation_text']}**")
                            selected_evidences_text.append(item['citation_text'])
                        else:
                            # 4. MULTIPLE CITATIONS -> SHOW CHECKBOXES
                            st.markdown("#### Step B: Verify Relevance (Precision)")
                            st.markdown("*Select **ONLY** the timestamps actually necessary.*")
                            
                            prev_evs_text = set(prev_res.get("necessary_evidences", []))
                            
                            for idx, item in enumerate(matched_items):
                                if item['status'] == 'found':
                                    citation_txt = item['citation_text']
                                    filename = item['filename']
                                    
                                    is_checked = True if (citation_txt in prev_evs_text or not prev_evs_text) else False
                                    unique_key = f"chk_{real_idx}_{idx}_{filename}"
                                    
                                    if st.checkbox(f"Necessary: {citation_txt}", value=is_checked, key=unique_key):
                                        selected_evidences_text.append(citation_txt)

                st.divider()
                c_back, c_next = st.columns([1, 1])
                with c_back:
                    if st.button("⬅️ Back"):
                        if q_idx > 0:
                            st.session_state.step2_ptr -= 1
                            st.rerun()
                        else:
                            st.session_state.wizard_mode = "step1"
                            st.session_state.step1_ptr = len(atomic_facts) - 1
                            st.rerun()

                with c_next:
                    is_last_step2 = (q_idx == len(st.session_state.step2_queue) - 1)
                    btn_label = "Submit Task 🚀" if is_last_step2 else "Next Fact"
                    btn_type = "primary" if is_last_step2 else "secondary"
                    
                    validation_error = False
                    if support_choice != "SKIPPED_NO_CITATIONS" and support_choice == "Supported" and not selected_evidences_text:
                        validation_error = True
                    
                    if st.button(btn_label, type=btn_type, disabled=(support_choice is None)):
                        if validation_error:
                            st.error("Constraint: You must select at least one timestamp for 'Supported' facts.")
                        else:
                            # SAVE LOGIC
                            if support_choice == "SKIPPED_NO_CITATIONS":
                                st.session_state.step2_results[real_idx] = {
                                    "citation_recall": None,
                                    "evidences": []
                                }
                            else:
                                st.session_state.step2_results[real_idx] = {
                                    "support_judgment": support_choice,
                                    "necessary_evidences": selected_evidences_text 
                                }
                            
                            if not is_last_step2:
                                st.session_state.step2_ptr += 1
                                st.rerun()
                            else:
                                save_annotation(output_file, current_task, atomic_facts, st.session_state.step1_results, st.session_state.step2_results, time.time() - st.session_state.task_start_time)
                                st.rerun()

if __name__ == "__main__":
    main()