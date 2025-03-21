from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider

from .config import settings


def test_func():
    model = OpenAIModel("gpt-4o-mini", provider=OpenAIProvider(api_key=settings.open_api_key))
    roulette_agent = Agent(
        model,
        deps_type=int,
        result_type=bool,
        system_prompt=(
            "Use the `roulette_wheel` function to see if the "
            "customer has won based on the number they provide."
        ),
    )

    @roulette_agent.tool
    async def roulette_wheel(ctx: RunContext[int], square: int) -> str:
        """check if the square is a winner"""
        return "winner" if square == ctx.deps else "loser"

    # Run the agent
    success_number = 18
    result = roulette_agent.run_sync("Put my money on square eighteen", deps=success_number)
    print(result.data)
    # > True

    result = roulette_agent.run_sync("I bet five is the winner", deps=success_number)
    print(result.data)
    # > False
