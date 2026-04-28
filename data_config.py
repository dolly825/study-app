import streamlit as st
import os
import pandas as pd

# 全局文件路径
main_file_path = "课程项目汇总.csv"
daily_file_path = "每日学习记录.csv"


# —— 主课程数据 ——
@st.cache_data
def load_main_data():
    if not os.path.exists(main_file_path):
        return pd.DataFrame(columns=["类型", "课程", "作者", "课程时长（小时）", "学习时长（小时）"])
    custom_dtypes = {
        "类型": str,
        "课程": str,
        "作者": str,
        "课程时长（小时）": float,
        "学习时长（小时）": str
    }
    return pd.read_csv(main_file_path, dtype=custom_dtypes)


def save_main_data(df):
    df.to_csv(main_file_path, index=False)


# —— 每日学习数据 ——
@st.cache_data
def load_daily_data():
    if not os.path.exists(daily_file_path):
        return pd.DataFrame(columns=["类型", "课程", "学习时长（小时）", "开始时间", "结束时间"])

    custom_dtypes = {
        "类型": str,
        "课程": str,
        "学习时长（小时）": str
    }
    custom_dates = ["开始时间", "结束时间"]

    df = pd.read_csv(daily_file_path, dtype=custom_dtypes, parse_dates=custom_dates)
    
    if "学习时长（小时）" in df.columns:
        df["学习时长（小时）"] = pd.to_timedelta(df["学习时长（小时）"], errors="coerce")
    return df  # 修复：必须永远返回df


def save_daily_data(df):
    df.to_csv(daily_file_path, index=False)


# —— 公共工具：timedelta 转 xx小时xx分钟 ——
def timedelta_to_hm(td):
    if pd.isna(td):
        return "0小时0分钟"
    total_sec = int(td.total_seconds())
    h = total_sec // 3600
    m = (total_sec % 3600) // 60
    return f"{h}小时{m}分钟"
