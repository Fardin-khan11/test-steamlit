import streamlit as st
import database as db
import pandas as pd

if "user" not in st.session_state or st.session_state.user is None:
    st.warning("Please log in to access this page.")
    st.stop()

user = st.session_state.user

st.title("📅 Timetable Planner")
st.caption("Organize your weekly learning schedule.")

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

subjects = db.get_subjects(user["id"])
subject_names = [s["subject_name"] for s in subjects]

tab1, tab2 = st.tabs(["View Timetable", "Generate/Edit Schedule"])

timetable_entries = db.get_timetable(user["id"])

with tab1:
    if not timetable_entries:
        st.info("No timetable found. Switch to the Edit tab to create one.")
    else:
        df_tt = pd.DataFrame(timetable_entries, columns=["ID", "User ID", "Day", "Time Slot", "Subject", "Duration Hours", "Created"])
        
        # Pivot table to show Days as columns (optional) or just display sorted by day and time
        # Sort by day order
        df_tt["Day_Num"] = df_tt["Day"].apply(lambda x: DAYS.index(x))
        df_tt = df_tt.sort_values(by=["Day_Num", "Time Slot"])
        
        for day in DAYS:
            day_data = df_tt[df_tt["Day"] == day]
            if not day_data.empty:
                st.subheader(day)
                display_cols = ["Time Slot", "Subject", "Duration Hours"]
                st.dataframe(day_data[display_cols], hide_index=True, use_container_width=True)

with tab2:
    if not subject_names:
        st.warning("You need to add Subjects before creating a timetable.")
        st.stop()
        
    st.subheader("Edit Timetable Entries")
    st.write("Current entries:")
    
    # Simple editor using st.data_editor
    if timetable_entries:
        df_edit = pd.DataFrame(timetable_entries, columns=["ID", "User", "Day", "Time Slot", "Subject", "Duration Hours", "Created"])
        df_edit = df_edit[["Day", "Time Slot", "Subject", "Duration Hours"]]
    else:
        df_edit = pd.DataFrame(columns=["Day", "Time Slot", "Subject", "Duration Hours"])
    
    edited_df = st.data_editor(df_edit, num_rows="dynamic", use_container_width=True,
        column_config={
            "Day": st.column_config.SelectboxColumn("Day", options=DAYS, required=True),
            "Time Slot": st.column_config.TextColumn("Time Slot (e.g. 09:00-10:00)", required=True),
            "Subject": st.column_config.SelectboxColumn("Subject", options=subject_names, required=True),
            "Duration Hours": st.column_config.NumberColumn("Duration (Hrs)", min_value=0.5, max_value=8.0, step=0.5, required=True)
        }
    )
    
    if st.button("💾 Save Timetable", type="primary"):
        # Convert df to dicts
        entries = edited_df.to_dict('records')
        # Filter incomplete rows
        valid_entries = [e for e in entries if pd.notna(e["Day"]) and pd.notna(e["Time Slot"]) and pd.notna(e["Subject"])]
        db.save_timetable(user["id"], valid_entries)
        st.success("Timetable saved successfully!")
        st.rerun()

    st.divider()
    st.markdown("### Auto-generate (Beta)")
    st.markdown("Automatically assign study slots based on your subjects' study hours. This will replace the current timetable.")
    if st.button("✨ Auto-Generate Timetable"):
        if not subjects:
            st.error("Add subjects to auto-generate relative hours.")
        else:
            generated = []
            current_day_idx = 0
            time_slots = ["08:00-09:00", "09:15-10:15", "10:30-11:30", "14:00-15:00", "15:15-16:15", "16:30-17:30"]
            for sub in subjects:
                hours_needed = int(sub["study_hours"])
                for _ in range(hours_needed):
                    slot = time_slots[len(generated) % len(time_slots)]
                    day = DAYS[current_day_idx % 5] # Weekdays only
                    generated.append({
                        "day": day,
                        "time_slot": slot,
                        "subject": sub["subject_name"],
                        "duration_hours": 1.0
                    })
                    current_day_idx += 1
            
            db.save_timetable(user["id"], generated)
            st.success("Timetable auto-generated!")
            st.rerun()
