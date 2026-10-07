from app.schemas import ConnectorDefinition, Plan, TaskRequest


class PlannerProvider:
    """Replaceable provider boundary. Mock mode is deterministic and needs no credentials."""
    async def plan(self, task: TaskRequest) -> Plan:
        app = task.application_id or "mock-fund-portal"
        return Plan(objective=task.request, application_id=app, environment="browser",
                    actions=["Open the search page", "Search for the requested item"],
                    expected_result="The matching report is visible", risk_level="low")

    async def generate(self, task: TaskRequest, plan: Plan) -> ConnectorDefinition:
        from app.schemas import Action, Target
        return ConnectorDefinition(name="Fund portal search", application_id=plan.application_id,
            environment="browser", inputs=["query"], expected_result="Matching result is visible",
            steps=[Action(type="fill", target=Target(role="textbox", name="Search"), value="{{query}}"),
                   Action(type="click", target=Target(role="button", name="Search"))])


provider = PlannerProvider()
