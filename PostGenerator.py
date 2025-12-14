from langgraph.graph import StateGraph,START,END
from typing import TypedDict, Literal, Annotated
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import os
import streamlit as st

load_dotenv()

# generator_llm = ChatGoogleGenerativeAI(
#     model = "gemini-2.5-flash",
#     google_api_key = os.getenv('GOOGLE_API_KEY')
#
# )
# evaluator_llm = ChatGoogleGenerativeAI(
#     model = "gemini-2.5-flash",
#     google_api_key = os.getenv('GOOGLE_API_KEY')
#
# )
# optimizer_llm = ChatGoogleGenerativeAI(
#     model = "gemini-2.5-flash",
#     google_api_key = os.getenv('GOOGLE_API_KEY')
#
# )

generator_llm = ChatGroq(
    model = "openai/gpt-oss-20b",
    api_key = os.getenv('GROQ_API_KEY')

)
evaluator_llm = ChatGroq(
    model = "openai/gpt-oss-20b",
    api_key = os.getenv('GROQ_API_KEY')

)
optimizer_llm = ChatGroq(
    model = "openai/gpt-oss-20b",
    api_key = os.getenv('GROQ_API_KEY')

)

class Linkedinstate(TypedDict):
    topic : str
    tweet : str
    evaluation : Literal["Approved", "Need_Improvement"]
    feedback : str
    iteration : int
    max_iteration : int

def generate_post(state : Linkedinstate):
    messages = [
        SystemMessage(content= "You are enthusiastic and very knowledgeable linkdin influencer"),
        HumanMessage(content=f"""
                Write a post for Linkdin in a intelligent tone on the topic {state['topic']}
                Rules : -
                1. Do not exceed 280 words.
                2. Do not use Question Answer format.
                3. Use smart humor , maybe slight sarcasm but also knowledgeable tone.
                4. Use Simple Day - to - Day english
                5. This is version {state['iteration'] + 1}
"""
                     )
    ]
    response = generator_llm.invoke(messages).content
    return {'tweet' : response}

class post_evaluation(BaseModel):
    evaluation : Literal["Approved","Need_Improvement"] = Field(..., description="Final evaluation result")
    feedback : str = Field(..., description="Constructive feedback for the post")

structured_evaluator_llm = evaluator_llm.with_structured_output(post_evaluation)


def evaluate_post(state: Linkedinstate):
    messages = [
        SystemMessage(
            content=(
                "You are a strict, no-nonsense LinkedIn content evaluator. "
                "You judge posts like a senior content editor. "
                "You do NOT rewrite the post. "
                "You only evaluate and give precise feedback."
            )
        ),
        HumanMessage(
            content=f"""
Evaluate the following LinkedIn post **very strictly**.

Post:
\"\"\"
{state['tweet']}
\"\"\"

Evaluation Rules:
1. Check if the tone is intelligent, professional, and suitable for LinkedIn.
2. Language must be simple, clear, and free of slang or cringe expressions.
3. Humor or sarcasm must be subtle and tasteful (not forced).
4. The post must feel insightful, not generic or AI-like.
5. No question–answer format.
6. Must stay within 280 words.
7. The post should provide value (insight, lesson, or perspective).

Decision Rules:
- If ALL rules are satisfied → return **Approved** 
- If ANY rule is violated → return **Need_Improvement**
- In both cases give 1 paragraph feedback explaining the strength and weakness

Output Format (STRICT – follow exactly):
Evaluation: Approved OR Need_Improvement
Feedback: Short, specific, actionable feedback explaining what is wrong (if any)

This is iteration {state['iteration'] + 1}.
"""
        )
    ]
    response = structured_evaluator_llm.invoke(messages)

    return {"evaluation": response.evaluation, "feedback" : response.feedback}


def optimize_post(state: Linkedinstate):
    messages = [
        SystemMessage(
            content=(
                "You are a senior LinkedIn content editor and copy optimizer. "
                "Your job is to IMPROVE posts based strictly on feedback. "
                "You rewrite intelligently, not creatively. "
                "You keep the original intent, topic, and structure. "
                "You do NOT add fluff, emojis, or hashtags."
            )
        ),
        HumanMessage(
            content=f"""
You are given:
1) An original LinkedIn post
2) Strict evaluator feedback

Your task:
- Rewrite the post to FIX all issues mentioned in the feedback
- Improve clarity, insight, tone, and professionalism
- Make it feel more human, less AI-like
- Preserve the original topic and message
- Follow all LinkedIn rules strictly

Rules to follow (MANDATORY):
1. Max 280 words
2. NO question–answer format
3. Tone must be intelligent, professional, and confident
4. Humor or sarcasm must be subtle and tasteful (optional, not forced)
5. Use simple, day-to-day English
6. No cringe phrases, no buzzwords, no motivational clichés
7. Do NOT explain what you changed
8. Output ONLY the optimized post text

Original Post:
{state['tweet']}

Evaluator Feedback:
{state['feedback']}

This is optimization iteration {state['iteration'] + 1}.
Return only the improved LinkedIn post.
"""
        )
    ]

    response = optimizer_llm.invoke(messages).content

    return {
        "tweet": response,
        "iteration": state["iteration"] + 1
    }

def route_Evaluation(state :Linkedinstate):
    if state['evaluation'] == 'Approved' or state['iteration'] >= state['max_iteration']:
        return "Approved"
    else:
        return "Need_Improvement"


graph = StateGraph(Linkedinstate)
graph.add_node("generate", generate_post)
graph.add_node("evaluate", evaluate_post)
graph.add_node("optimize", optimize_post)

graph.add_edge(START, "generate")
graph.add_edge("generate", "evaluate")

graph.add_conditional_edges("evaluate", route_Evaluation, {"Approved" : END,"Need_Improvement" : "optimize" })
graph.add_edge("optimize", "evaluate")

workflow = graph.compile()

st.title("Linkedin post Generator")

user_input = st.text_input("Enter The topic on which you want to generate post: ")


initial_state = {"topic": user_input, "iteration" : 0, "max_iteration" : 5}


if st.button("Submit"):
    st.subheader("Post : ")
    if user_input:
        output_state = workflow.invoke(initial_state)
        st.write(output_state['tweet'])
    else:
        st.write("Please Enter Something")



# print(output_state['tweet'])

