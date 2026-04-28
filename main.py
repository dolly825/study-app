from data_config import *
import pandas as pd

# 导入页面
from daily_study import show_study_page

# 页面全局配置（必须放在最顶部）
st.set_page_config(
    page_title="AI 学习记录管理系统",
    page_icon="📚",
    layout="centered"
)

# 侧边栏菜单
st.sidebar.title("🛠️ 系统导航")
st.sidebar.subheader("🎓 学习记录")

menu_options = [
    "📚 课程学习",
    "📊 查看记录",
    "➕ 添加记录",
    "✏️ 修改记录",
    "🗑️ 删除记录"
]

menu = st.sidebar.radio(
    "选择功能",
    menu_options,
    label_visibility="collapsed",
    index=None
)

# --- 主界面逻辑 ---

# 0. 欢迎页面 (当没有选中任何菜单时显示)
if menu is None:
    st.header("👋 欢迎使用 AI 学习记录管理系统")
    st.markdown("请在左侧选择功能开始使用。")

# 1. 📚 课程学习 (核心修改部分)
elif menu == "📚 课程学习":
    show_study_page()

# 2. 📊 查看记录
elif menu == "📊 查看记录":
    st.header("📊 当前学习记录")
    df = load_main_data()
    if df.empty:
        st.info("📭 暂无记录，快去添加吧！")
    else:
        st.dataframe(df, use_container_width=True)

# 3. ➕ 添加记录
elif menu == "➕ 添加记录":
    st.info("🛠️ 该功能正在努力开发中，敬请期待～")
    # st.header("➕ 添加新记录")
    #
    # with st.form("add_form"):
    #     col1, col2 = st.columns(2)
    #     with col1:
    #         author = st.text_input("作者")
    #         course = st.text_input("课程名称")
    #     with col2:
    #         duration_input = st.text_input("课程时长 (小时，如: 4.5 或 4)")
    #         date = st.text_input("学习时长 (如: 2026-04-24)")
    #
    #     submitted = st.form_submit_button("💾 保存记录")
    #
    #     if submitted:
    #         if not author or not course:
    #             st.error("作者和课程是必填项！")
    #         else:
    #             try:
    #                 duration = float(duration_input)
    #             except ValueError:
    #                 duration = 0.0
    #
    #             new_data = pd.DataFrame({
    #                 "作者": [author],
    #                 "课程": [course],
    #                 "课程时长": [duration],
    #                 "学习时长": [date]
    #             })
    #
    #             df = load_main_data()
    #             df = pd.concat([df, new_data], ignore_index=True)
    #             save_main_data(df)
    #             load_main_data.clear()
    #             st.success("✅ 记录添加成功！")

# 4. ✏️ 修改记录
elif menu == "✏️ 修改记录":
    st.info("🛠️ 该功能正在努力开发中，敬请期待～")
# st.header("✏️ 修改记录")
#
# if "success_msg" in st.session_state:
#     st.success(st.session_state.success_msg)
#     del st.session_state.success_msg
#
# df = load_main_data()
#
# if df.empty:
#     st.warning("暂无数据可修改。")
# else:
#     row_to_update = st.selectbox(
#         "选择要修改的记录行号",
#         df.index,
#         format_func=lambda x: f"{x}: {df.iloc[x]['课程']} - {df.iloc[x]['作者']}"
#     )
#
#     st.divider()
#     st.subheader("输入新数据 (留空则保持原值)")
#
#     current_row = df.iloc[row_to_update]
#
#     with st.form("update_form"):
#         col1, col2 = st.columns(2)
#         with col1:
#             new_author = st.text_input("作者", value=str(current_row['作者']))
#             new_course = st.text_input("课程名称", value=str(current_row['课程']))
#         with col2:
#             new_duration_raw = st.text_input("课程时长", value=str(current_row['课程时长']))
#             new_date = st.text_input("学习时长", value=str(current_row['学习时长']))
#
#         submitted = st.form_submit_button("🔄 更新记录")
#
#         if submitted:
#             df.at[row_to_update, '作者'] = new_author
#             df.at[row_to_update, '课程'] = new_course
#             df.at[row_to_update, '课程时长'] = new_duration_raw
#             df.at[row_to_update, '学习日期'] = new_date
#
#             save_main_data(df)
#
#             try:
#                 load_main_data.clear()
#             except AttributeError:
#                 pass
#
#             st.session_state.success_msg = "✅ 记录已更新！"
#             st.rerun()

# 5. 🗑️ 删除记录
elif menu == "🗑️ 删除记录":
    st.header("🗑️ 删除记录")
    df = load_main_data()

    if df.empty:
        st.warning("暂无数据可删除。")
    else:
        st.dataframe(df, use_container_width=True)

        row_to_delete = st.number_input("输入要删除的行号", min_value=0, max_value=len(df) - 1, step=1)

        if st.button("🔥 确认删除"):
            df = df.drop(index=row_to_delete).reset_index(drop=True)
            save_main_data(df)
            load_main_data.clear()
            st.success("✅ 删除成功！")
            st.rerun()

# 后续你其他页面（查看/添加/修改/删除）
# 只需要：
# 1. 新建 view.py / add.py 等
# 2. 写 def show_xxx_page():
# 3. 在这里加 elif 分发即可
