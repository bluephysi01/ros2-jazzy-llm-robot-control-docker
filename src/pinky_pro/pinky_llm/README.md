# pinky_llm (ROS 2) - Docker 실행 주의사항

## 증상

`ros2 run pinky_llm agent_service` 실행 시 아래와 유사한 에러가 발생할 수 있습니다.

- `ImportError: cannot import name 'create_tool_calling_agent' from 'langchain.agents'`

## 원인

컨테이너에 설치된 `langchain` 버전과 코드가 기대하는 API가 서로 달라서 발생합니다.
볼륨 마운트는 **소스 코드만** 공유하고, Python 패키지(`pip`로 설치되는 의존성)는 **컨테이너 이미지에 설치된 버전**을 그대로 사용합니다.

## 확인

컨테이너 안에서 버전을 확인하세요.

```bash
python3 -c "import langchain; print(langchain.__version__)"
python3 -c "import langchain_openai, langchain_core, langchain_community; print('ok')"
```

## 해결

1) 컨테이너에서 LangChain 관련 패키지 버전을 코드에 맞게 업그레이드/다운그레이드(핀)합니다.

2) 이 패키지의 `pinky_llm/agent_service.py` 는 LangChain 버전 차이를 흡수하기 위해
`create_tool_calling_agent` 가 없으면 `create_openai_tools_agent` / `create_openai_functions_agent` 로 자동 대체를 시도합니다.

3) Dockerfile을 사용 중이라면, 이미지 빌드 단계에 다음과 같이 의존성 설치를 포함시키는 방식을 권장합니다.

```bash
pip install -U langchain langchain-openai langchain-core langchain-community pyyaml python-dotenv
```

