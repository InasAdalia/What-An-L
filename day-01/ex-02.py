# 1. remember the student’s name, goal, and preferred explanation style, ✅
# 2. answer study questions in that style, ✅
# 3. keep only the last few chat turns in active memory ✅
# 4. compress older turns into a short running summary, ✅
# 5. save that summary to a local file so it can be loaded again after restarting the script. ✅
import sys
import markdown
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from utils import RED, GREEN, RESET
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser
import os


llm = ChatOllama(
    model="llama3.2:3b",
)

MAX_HISTORY = 8
KEEP_RECENT = 4
parser = StrOutputParser()
history = []
summary = ""
sum_count = 0
iteration = 1
system_prompt = "You are a teacher that mentors the user as a student. Begin by asking for the student's name, topic of interest, and preferred explanation style. Always mention their name in every conversation."

while True:
    prompt = ChatPromptTemplate([
        ("system", system_prompt),
        SystemMessage(content=summary),
        *history,
    ])
    chain = prompt | llm | parser

    # result = chain.invoke({
    #     "name": "",
    # })
    
    # history.append(AIMessage(result))

    history.append("AI Response")

    if (len(history) > MAX_HISTORY): # summarize the first 4 messages and trim off history
        
        # 1. clear terminal
        os.system('cls' if os.name == 'nt' else 'clear') 

        trimmed_history = history[:KEEP_RECENT+1]
        # transcript = "\n".join([f"{h.type}: {h.content}" for h in trimmed_history])

        # # 2. summarize
        # summary_prompt = ChatPromptTemplate([
        #     ("system", "You are a note-taker, you never talk to the student. Summarize this conversation in bullet points. Do not answer or address the student or question. Return only these four lines: Name, Goal/topic, Preferred style, Conversation summary. Use Unknown for missing profile details."),
        #     HumanMessage(content=f"previous summary: {summary}\n Previous chat transcript: {transcript}\n Write the updated summary: "),
        # ])

        # summary = (summary_prompt | llm | parser).invoke({
        #     "summary": summary or "none yet",
        #     "transcript": transcript or "none yet",
        # })
        sum_count += 1
        summary = f"summary invoked: {sum_count} history: {trimmed_history}\n\n"
        # 3. save summary to file
        with open("day-01/exercise-02-summary.md", "w", encoding="utf-8") as file:
            file.write(summary)

        print(f"{GREEN}\n[debug] SUMMARY: \n{summary} {RESET}\n")

        # 3. KEEP LAST 4 MESSAGES. lenh(history) will be reduced
        history = history[-KEEP_RECENT:]
        print(f"{GREEN}\n[debug] KEEP RECENT: \n{history} {RESET}\n")

        for (h) in history:
            # print(f"{h.type}: {h.content}")
            print(h)


    else: # print last element
        # print(f"{history[-1].type}: {history[-1].content}")
        print(history[-1])

    # print only the last 4 message index
    print(f"[debug] iteration : {iteration}")

    human_input = input("You :")

    # a or b or c is eq. to a || b || c in JS.
    if (human_input in ("quit","exit","X")) : 
        break
    history.append(f"human input {human_input}")
    # history.append(HumanMessage(human_input))

    # [debug] to check history contents passed into prompt
    # print(f"{RED}\n[debug]HISTORY: \n")
    # for (index, h) in enumerate(history, start=1):
    #     print(f"{RED}\n{index}. {h.type}: {h.content} {RESET}\n")

    iteration+=1


