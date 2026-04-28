import streamlit as st
from datetime import datetime, timedelta
from data_config import (
    load_main_data,
    load_daily_data,
    save_daily_data,
    timedelta_to_hm
)
import pandas as pd


# --- 课程学习主程序 ---
def show_study_page():
    st.header("📚 课程学习与计时")

    # 初始化状态
    if "start_time" not in st.session_state:
        st.session_state.start_time = None
        st.session_state.is_running = False
        st.session_state.warning_msg = None

    df_main_data = load_main_data()

    if df_main_data.empty:
        st.warning("暂无课程，请先去「添加记录」中添加课程！")
        return

    # 下拉列表
    selected_row = st.selectbox(
        "选择要学习的课程",
        options=df_main_data.to_dict('records'),  # 把每一行变成字典
        format_func=lambda row: f"{row['类型']} - {row['课程']} - {row['作者']}"  # 显示时用我们定义的格式
    )

    st.divider()

    # --- 计时按钮 ---
    col1, col2 = st.columns(2)

    with col1:
        # 开始按钮
        if st.button("▶️ 开始学习", use_container_width=True, type="primary", disabled=st.session_state.is_running):
            st.session_state.start_time = datetime.now()
            st.session_state.is_running = True
            st.rerun()

    with col2:
        # 结束按钮
        if st.button("🛑 结束学习", use_container_width=True, type="secondary",
                     disabled=not st.session_state.is_running):
            end_time = datetime.now()
            start_time = st.session_state.start_time

            # --- 新增的判断逻辑 ---
            study_duration = end_time - start_time
            one_minute = timedelta(minutes=1)

            if study_duration < one_minute:
                st.session_state.warning_msg = "⚠️ 学习时长不足1分钟，不算做有效学习！"
                # 重置状态
                st.session_state.is_running = False
                st.session_state.start_time = None
                st.rerun()

            # --- 更新每日学习记录 ---
            # 构建新记录
            new_daily_record = pd.DataFrame({
                "类型": [selected_row["类型"]],
                "课程": [selected_row["课程"]],
                "学习时长（小时）": [study_duration],
                '开始时间': [start_time],
                '结束时间': [end_time]
            })

            # 读取旧数据并追加
            df_current_daily_data = load_daily_data()
            df_updated_daily_data = pd.concat([df_current_daily_data, new_daily_record], ignore_index=True)
            save_daily_data(df_updated_daily_data)

            # 重置状态
            st.session_state.is_running = False
            st.session_state.start_time = None

            # 清除缓存并刷新
            load_daily_data.clear()
            st.rerun()

    # --- 学习状态显示 ---
    if 'warning_msg' not in st.session_state:
        st.session_state.warning_msg = None

    if st.session_state.warning_msg:
        st.warning(st.session_state.warning_msg)
        # 关键步骤：显示后立即销毁消息，保证下次刷新不显示
        st.session_state.warning_msg = None
    elif st.session_state.is_running:
        st.info(f"⏱️ 正在学习中... 开始时间: {st.session_state.start_time.strftime('%H:%M:%S')}")
    else:
        st.success("准备就绪，请选择课程并开始学习。")

    st.divider()

    # --- 显示每日课程记录表 ---
    st.subheader("📅 今日学习明细")
    df_daily_data = load_daily_data()

    if df_daily_data.empty:
        st.info("空空如也～快去开启你的第一次学习之旅吧✨")
    else:
        # 筛选当日学习明细
        today = datetime.today().date()
        df_daily_today = df_daily_data[df_daily_data["开始时间"].dt.date == today]

        if df_daily_today.empty:
            st.info("今日学习空白啦～抓紧充电学习吧✨")
        else:
            # 转换表格用于展示
            df_show = df_daily_today.copy()
            df_show["学习时长"] = df_daily_today["学习时长（小时）"].apply(timedelta_to_hm)
            df_show['日期'] = df_daily_today['开始时间'].dt.strftime('%Y年%m月%d日')
            df_show['时段'] = (
                    df_daily_today['开始时间'].dt.strftime('%H:%M:%S')
                    + '-'
                    + df_daily_today['结束时间'].dt.strftime('%H:%M:%S')
            )
            st.dataframe(df_show[['类型', '课程', '学习时长', '日期', '时段']], use_container_width=True)

        # --- 学习任务完成情况判断 ---
        # 总时长
        total_duration = df_daily_today['学习时长（小时）'].sum()
        # 目标时长
        target_duration = pd.Timedelta(hours=6)
        # 差值
        diff_duration = target_duration - total_duration

        if total_duration >= target_duration:
            # 已完成
            st.success(f"🎉 **恭喜！已完成今日学习任务**，累计学习 **{timedelta_to_hm(total_duration)}**。")
        else:
            # 未完成，显示还差多久
            st.warning(
                f"💪 今日已累计学习 **{timedelta_to_hm(total_duration)}**，距完成学习任务还差 **{timedelta_to_hm(diff_duration)}**。")

    st.caption("ℹ️ 每日学习时长需满足 6 小时。")
