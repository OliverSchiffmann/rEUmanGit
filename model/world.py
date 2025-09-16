from model._agent import AgentEnum, BaseAgent


class World:
    _now: int
    _agents: dict[int, BaseAgent]
    _agents_by_type: dict[AgentEnum, list[int]]

    def __init__(self) -> None:
        self._now = 0
        self._agents = {}
        self._agents_by_type = {AgentEnum.CUSTOMER: []}

    def tick(self) -> None:
        self._now += 1

    def now(self) -> int:
        return self._now

    def add_agent(self, agent: BaseAgent):
        if agent.id() in self._agents:
            exit(f"Agent with id already exists. Received: {agent.id}")
        self._agents[agent.id()] = agent
        self._agents_by_type[agent.type()].append(agent.id())

    def call_next(self, rng):
        for _, agent in self._agents.items():
            agent.next(rng)
