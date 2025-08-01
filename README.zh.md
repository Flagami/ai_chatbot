# 轻量级 AI 聊天 Web UI 💬
🔥 这是一个纯 Python 实现的 AI 聊天服务 Web UI（基于 Streamlit），专为开发者和技术爱好者设计。  
✨它提供了一个简洁直观的界面，让用户可以与 AI 进行交互式对话。，整个服务设计得非常简单，易于部署和使用，不需要复杂的配置。  
🪧 项目默认接入的是部署在硅基流动（Silicon flow）平台上部署的大模型，没有注册过的大陆用户可以享受免费获取2000万 Tokens的福利  
💡 只需要注册时候填写邀请码【BKxj3kST】或者直接点击邀请链接注册即可 🔗https://cloud.siliconflow.cn/i/BKxj3kST  

## ✨ 主要功能
* **对话界面: 提供一个聊天气泡式的对话界面，清晰地展示用户和 AI 的对话内容。

* **个性化头像: 支持为用户和 AI 设置自定义头像，增加界面的趣味性。

* **会话管理: 允许用户清空当前对话，开启新的聊天会话。

* **轻量化: 基于 Streamlit 框架，整个服务以纯 Python 代码实现，不依赖于其他复杂的 Web 框架或前端技术。

* **易于部署: 只需运行一个 Python 脚本即可启动服务。

## 核心代码逻辑
主应用 app.py 的代码逻辑如下：  
    1.	设置页面配置: 调用 setup_page_config()，为 Streamlit 应用设置页面标题和布局。  
	2.	加载头像: 调用 load_avatars()，加载用于用户和 AI 的头像图片。  
	3.	初始化会话状态: 调用 initialize_session_state()，初始化 Streamlit 的 session_state，用于存储聊天历史。  
	4.	渲染侧边栏: 调用 render_sidebar()，渲染侧边栏，通常用于放置一些设置选项。  
	5.	渲染聊天界面: 调用 render_chat_interface()，根据会话状态渲染整个聊天界面，并处理用户的输入。  

# 🚀 如何运行
<u>前提条件:</u> 确保你的系统中已安装 Python 3.11+。

## 1. 克隆项目
```bash
git clone <repo-url>
cd <repo-folder>
```

## 2. 安装依赖
```bash
conda create -n chatbot python=3.11 -y

conda activate chatbot

pip install -r requirements.txt
```

## 3. 运行应用
```bash
streamlit run app.py
```
**应用将在本地启动，你可以在浏览器中访问 http://localhost:8501 来使用该服务。**

## 🌐 截图
上图展示了该 Web UI 的一个示例界面，左侧为侧边栏，右侧为 AI 聊天窗口。
![img.png](img.png)

# 📄 许可证
本项目采用 MIT 许可证 开源。