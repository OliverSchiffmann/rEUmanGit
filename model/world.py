from model._agent import AgentEnum, BaseAgent

inital_retailer_stock_A: int = 100
inital_factory_stock_A: int = 0
production_rate_A: float = 15  # units produced per day


class World:
    _now: int
    _agents: dict[int, BaseAgent]
    _agents_by_type: dict[AgentEnum, list[int]]
    _retailer_stock_A: int
    _factory_stock_A: int
    _production_rate_A: float
    _work_in_process_A: float  # for handling non-integer production rates

    def __init__(self) -> None:
        self._now = 0
        self._agents = {}
        self._agents_by_type = {AgentEnum.CUSTOMER: []}
        self._retailer_stock_A = inital_retailer_stock_A
        self._factory_stock_A = inital_factory_stock_A
        self._production_rate_A = production_rate_A
        self._work_in_process_A = 0.0

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
        self._work_in_process_A += self._production_rate_A
        new_whole_As = int(self._work_in_process_A)
        if new_whole_As >= 1:
            self._factory_stock_A += new_whole_As
            self._work_in_process_A -= new_whole_As
        print(
            f"Factory Stock of A: {self._factory_stock_A}, Retailer Stock of A: {self._retailer_stock_A}"
        )
        # some logic needed here to get factory stock to update retailer stock
        for _, agent in self._agents.items():
            agent.next(rng, self._now, self._retailer_stock_A)

    def confirm_order(self):
        self._retailer_stock_A = self._retailer_stock_A - 1
