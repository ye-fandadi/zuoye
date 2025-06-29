import os
from langchain.agents import initialize_agent, Tool
from langchain.llms import OpenAI
from tools.knowledge_tool import DeepSeekKnowledgeTool
from tools.api_tool import WeatherAPI
from tools.local_function_tool import LocalFunctionTool

deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY")

if not deepseek_api_key or not openai_api_key:
    raise EnvironmentError("请设置环境变量 DEEPSEEK_API_KEY 和 OPENAI_API_KEY")

llm = OpenAI(temperature=0, openai_api_key=openai_api_key)

knowledge_tool = DeepSeekKnowledgeTool(api_key=deepseek_api_key)
weather_api = WeatherAPI()
local_function_tool = LocalFunctionTool()

tools = [
    Tool(
        name="知识库问答",
        func=knowledge_tool.query,
        description="回答基于知识库的问题"
    ),
    Tool(
        name="天气查询",
        func=weather_api.get_weather,
        description="根据城市名查询实时天气"
    ),
    Tool(
        name="本地排序",
        func=lambda input_str: local_function_tool.sort_list(eval(input_str)),
        description="对数字列表进行排序，输入格式示例：[5,3,1]"
    )
]

agent = initialize_agent(tools, llm, agent="conversational-react-description", verbose=True)

def main():
    print("智能协作Agent已启动，输入 exit 退出")
    while True:
        user_input = input("你：")
        if user_input.lower() == "exit":
            break
        response = agent.run(user_input)
        print("Agent：", response)

if __name__ == "__main__":
    main()
