import rclpy
from rclpy.node import Node
from pinky_llm.robot_tools import ToolSet, create_tools
from pinky_interfaces.srv import Agent
from pathlib import Path
from ament_index_python.packages import get_package_share_directory

import yaml
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langgraph.checkpoint.memory import MemorySaver


llm_dir = get_package_share_directory('pinky_llm')
nav2_dir = get_package_share_directory('pinky_navigation')
env_file_path = Path(llm_dir) / '.env'
load_dotenv(dotenv_path=env_file_path)

prompt_file = Path(llm_dir) / 'params/prompt.yaml'
with open(prompt_file, 'r', encoding='utf-8') as f:
    prompt_data = yaml.safe_load(f)    

class AgentLLM(Node):
    def __init__(self):
        super().__init__('agent_llm')

        self.srv = self.create_service(Agent, 'llm_agent', self.handle_question)
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    
        yaml_file = Path(nav2_dir) / 'params/points.yaml'
        with open(yaml_file, 'r') as f:
            config = yaml.safe_load(f)

        places = {name: (info["x"], info["y"], info["qz"], info["qw"]) for name, info in config["places"].items()}
        tool_set = ToolSet(places)
        tool_list = create_tools(tool_set)

        # langchain v1.2+ 의 create_agent API 사용
        # checkpointer 를 지정하면 session 별 대화 히스토리를 자동 관리합니다.
        self.checkpointer = MemorySaver()
        self.agent_graph = create_agent(
            model=self.llm,
            tools=tool_list,
            system_prompt=prompt_data["system"],
            checkpointer=self.checkpointer,
        )
        
        self.get_logger().info("agent service start")

    def process_query(self, query):
        # session_id 기반으로 대화 히스토리를 유지합니다.
        config = {"configurable": {"thread_id": "pinky"}}
        result = self.agent_graph.invoke(
            {"messages": [{"role": "user", "content": query}]},
            config=config,
        )
        # 최종 AI 메시지를 반환
        messages = result.get("messages", [])
        if messages:
            return messages[-1].content
        return str(result)

    def handle_question(self, request, response):
        self.get_logger().info(f"💬: {request.question}"+"\n")
        try:
            answer = self.process_query(request.question)
            response.answer = answer
        except Exception as e:
            self.get_logger().info(str(e))
            response.answer = "잘 이해하지 못했어요.. 자세하게 물어봐 주시겠어요?"
        return response
    
def main(args=None):
    rclpy.init(args=args)
    agent = AgentLLM()
    try:
        rclpy.spin(agent) 
    finally:
        agent.destroy_node()
        rclpy.shutdown()
