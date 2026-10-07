# 1. remember the student’s name, goal, and preferred explanation style, ✅
# 2. answer study questions in that style, ✅
# 3. keep only the last few chat turns in active memory ✅
# 4. compress older turns into a short running summary, ✅
# 5. save that summary to a local file so it can be loaded again after restarting the script. ✅
import sys
import markdown
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from utils import RED, GREEN, BLUE, RESET
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, trim_messages
from langchain_core.messages.utils import count_tokens_approximately
from langchain_core.output_parsers import StrOutputParser
import os


main_model = ChatOllama(
    model="llama3.2:3b",
)
summarizer_model = ChatOllama(
    model="llama3.2:3b",
)

MAX_TOKENS = 500
parser = StrOutputParser()
history = []
summary = ""
sum_count = 0
iteration = 1
system_prompt = "You are a teacher that mentors the user as a student. Begin by asking for the student's name, topic of interest, and preferred explanation style. Always mention their name in every conversation."

while True:

    # restart
    removed_history=[]
    reprint_history = False

    # trim kept history
    kept_history = trim_messages(
        history,
        max_tokens = MAX_TOKENS,
        token_counter = count_tokens_approximately,
        strategy = "last",
        start_on="human",
        allow_partial = False
    )

    # get the removed history
    removed_history = history[:len(history) - len(kept_history)]
    
    print(f"[debug]: removed history: {removed_history}")

    if (len(removed_history) != 0):

        reprint_history = True
        history = kept_history

        transcript = "\n".join([f"{h.type}: {h.content}" for h in removed_history]) # for summary to consume
        

        # 2. summarize
        summary_prompt = ChatPromptTemplate([
            ("system", "You are a note-taker, you never talk to the student. Summarize this conversation in bullet points. Do not answer or address the student or question. Return only these four lines: Name, Goal/topic, Preferred style, Conversation summary. Use Unknown for missing profile details."),
            HumanMessage(content=f"previous summary: {summary}\n Previous chat transcript: {transcript}\n Write the updated summary: "),
        ])

        summary = (summary_prompt | summarizer_model | parser).invoke({
            "summary": summary or "none yet",
            "transcript": transcript or "none yet",
        })

        # 3. save summary to file
        with open("day-01/exercise-02-summary.md", "w", encoding="utf-8") as file:
            file.write(summary)

        os.system('cls' if os.name == 'nt' else 'clear') 

        print(f"{GREEN}\n[debug] SUMMARY: \n{summary} {RESET}\n")

        # print chat history
    # else:
    #     # print 

    # invoke
    prompt = ChatPromptTemplate([
        ("system", system_prompt),
        SystemMessage(content=summary),
        MessagesPlaceholder("history"),
    ])

    chain = prompt | main_model | parser

    result = chain.invoke({"history" : history })
    history.append(AIMessage(result))

    # debug tokens
    print(f"[debug] kept ~{count_tokens_approximately(kept_history)} / {MAX_TOKENS} tokens, "
      f"removed {len(removed_history)} msgs")

    # print history
    if (reprint_history):
        for (h) in history:
            print(f"{BLUE if h.type == 'ai' else ''} \n{h.type}: {h.content} \n{RESET}")

    else:
        print(f"{BLUE if history[-1].type == 'ai' else ''} \n{history[-1].type}: {history[-1].content} \n{RESET}")

    # human input always follows after AI response
    human_input = input("You :")
    # a or b or c is eq. to a || b || c in JS.
    if (human_input in ("quit","exit","X")) : 
        break

    history.append(HumanMessage(human_input))

    
    print(f"[debug] iteration : {iteration}")
    # [debug] to check history contents passed into prompt
    # print(f"{RED}\n[debug]HISTORY: \n")
    # for (index, h) in enumerate(history, start=1):
    #     print(f"{RED}\n{index}. {h.type}: {h.content} {RESET}\n")

    iteration+=1


