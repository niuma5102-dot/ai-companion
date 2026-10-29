import streamlit as st
import os
from openai import OpenAI
from datetime import datetime
import json
from dotenv import load_dotenv

# 从 .env 文件加载环境变量（如 DEEPSEEK_API_KEY）
load_dotenv()

# 设置页面的配置项
st.set_page_config(
    page_title="AI智能伴侣",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={}
)

# 生成会话标识函数
def generate_session_name():
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# 保存会话信息函数
def save_session():
    if st.session_state.current_session:
        # 构建新的会话对象
        session_data = {
            "nick_name": st.session_state.nick_name,
            "nature": st.session_state.nature,
            "current_session": st.session_state.current_session,
            "messages": st.session_state.messages
        }

        # 如果 sessions 目录不存在，则创建
        if not os.path.exists("sessions"):
            os.makedirs("sessions")

        # 保存会话数据
        with open(f"sessions/{st.session_state.current_session}.json", "w", encoding="utf-8") as f:
            json.dump(session_data, f, ensure_ascii=False, indent=4)

# 加载所有的会话列表信息
def load_sessions():
    sessions_list = []
    # 加载 sessions 目录下的文件
    if os.path.exists("sessions"):
        file_list = os.listdir("sessions")
        for filename in file_list:
            if filename.endswith(".json"):
                sessions_list.append(filename[0:-5:])
    sessions_list.sort(reverse=True)  # 排序，降序排序
    return sessions_list

# 加载指定会话信息
def load_session(session_name):
    try:
        if os.path.exists(f"sessions/{session_name}.json"):
            # 读取会话数据
            with open(f"sessions/{session_name}.json", "r", encoding="utf-8") as f:
                session_data = json.load(f)
                st.session_state.nick_name = session_data["nick_name"]
                st.session_state.nature = session_data["nature"]
                st.session_state.messages = session_data["messages"]
                st.session_state.current_session = session_name
    except Exception as e:
        st.error(f"会话加载失败, 错误信息为：{e}")

# 删除会话信息
def delete_session(session_name):
    try:
        if os.path.exists(f"sessions/{session_name}.json"):
            os.remove(f"sessions/{session_name}.json")  # 删除文件
            # 如果删除的是当前会话，则需要更新消息列表
            if session_name == st.session_state.current_session:
                st.session_state.messages = []
                st.session_state.current_session = generate_session_name()
    except Exception as e:
        st.error(f"会话删除失败, 错误信息为：{e}")


# 大标题
st.title("AI智能伴侣")

# 添加 logo
st.logo("resources/img_1.png")

# 系统提示词
system_prompt = """
        你叫%s, 现在是用户的真实伴侣, 请完全代入伴侣角色。
        规则:
            1. 每次只回1条消息
            2. 禁止任何场景或状态描述性文字
            3. 匹配用户的语言
            4. 回复简短, 像微信聊天一样
            5. 有需要的话可以用♥*等 emoji 表情
            6. 用符合伴侣性格的方式对话
            7. 回复的内容, 要充分体现伴侣的性格特征
        伴侣性格:
            -%s
        你必须严格遵守上述规则来回复用户。
    """

# 初始化聊天信息
if 'messages' not in st.session_state:
    st.session_state.messages = []
# 昵称
if 'nick_name' not in st.session_state:
    st.session_state.nick_name = "柳如烟"
# 性格
if "nature" not in st.session_state:
    st.session_state.nature = "活泼开朗，温柔可爱的台湾姑娘"
# 会话标识
if "current_session" not in st.session_state:
    st.session_state.current_session = generate_session_name()


# 展示聊天信息
st.text(f"当前会话: {st.session_state.current_session}")
for message in st.session_state.messages:
    st.chat_message(message["role"]).write(message["content"])

# 创建与 AI 大模型交互的客户端对象
# 默认使用 DeepSeek 兼容接口，API Key 通过环境变量 DEEPSEEK_API_KEY 注入（见 .env.example）
client = OpenAI(
    api_key=os.environ.get("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)


# 左侧的侧边栏
with st.sidebar:
    # 会话信息
    st.subheader("AI控制面板")

    # 新建会话按钮
    if st.button("新建会话", width="stretch", icon="🩷", type="primary"):

        # 1. 保存当前会话信息
        save_session()

        # 2. 创建新的会话
        if st.session_state.messages:  # 如果聊天信息非空
            st.session_state.messages = []
            st.session_state.current_session = generate_session_name()
            save_session()
            st.rerun()  # 重新运行当前页面

    # 会话历史
    st.text("历史会话")
    session_list = load_sessions()
    for session in session_list:
        col1, col2 = st.columns([4, 1])
        with col1:
            if st.button(
                session,
                width="stretch",
                icon="💌",
                type="primary" if session == st.session_state.current_session else "secondary"
            ):
                load_session(session)
                st.rerun()
        with col2:
            # 删除会话信息
            if st.button("", width="stretch", icon="💔", key=session):
                delete_session(session)
                st.rerun()  # 重新运行当前页面

    # 分割线
    st.divider()

    st.subheader("伴侣信息")
    # 昵称
    nick_name = st.text_input("昵称", placeholder="请输入伴侣的昵称", value=st.session_state.nick_name)
    if nick_name:
        st.session_state.nick_name = nick_name
    # 性格输入框
    nature = st.text_area("性格", placeholder="请输入伴侣的性格描述", value=st.session_state.nature)
    if nature:
        st.session_state.nature = nature


# 输入框
prompt = st.chat_input("请输入您要问的问题：")
if prompt:  # 字符串非空即为 True
    st.chat_message("user").write(prompt)
    # 保存用户输入的提示词
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 调用 AI 大模型（流式输出）
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": system_prompt % (st.session_state.nick_name, st.session_state.nature)},
            *st.session_state.messages
        ],
        stream=True,
    )

    # 流式输出
    response_message = st.empty()  # 创建一个空的组件，用于展示大模型返回的结果

    full_response = ""
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            content = chunk.choices[0].delta.content
            full_response += content
            response_message.chat_message("assistant").write(full_response)

    # 保存大模型的返回结果与会话信息
    st.session_state.messages.append({"role": "assistant", "content": full_response})
    save_session()
