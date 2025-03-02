import os
import google.generativeai as genai

import openai
from tqdm import tqdm
import networkx as nx
import numpy as np
import argparse
import time
from datetime import datetime, timedelta, timezone
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)  # for exponential backoff


model_list = ["text-davinci-003","code-davinci-002","gpt-3.5-turbo","gpt-4"]
parser = argparse.ArgumentParser(description="reach_without_x")
parser.add_argument('--model', type=str, default="text-davinci-003", help='name of LM (default: text-davinci-003)')
parser.add_argument('--mode', type=str, default="easy", help='mode (default: easy)')
parser.add_argument('--prompt', type=str, default="none", help='prompting techniques (default: none)')
parser.add_argument('--T', type=int, default=0, help='temprature (default: 0)')
parser.add_argument('--token', type=int, default=400, help='max token (default: 400)')
parser.add_argument('--SC', type=int, default=0, help='self-consistency (default: 0)')
parser.add_argument('--SC_num', type=int, default=5, help='number of cases for self-consistency (default: 5)')
args = parser.parse_args()
assert args.prompt in ["CoT", "none", "0-CoT", "LTM", "PROGRAM","k-shot","Instruct","Algorithm", "Recitation","hard-CoT","medium-CoT"]



def translate(m, edges, queries, args):
    Q = ''
    Q = Q +"Note that (i,j) means that node i and node j are connected with an undirected edge.\nGraph:"
    for i in range(m):
        Q = Q + ' ('+str(edges[i][0])+','+str(edges[i][1])+')'
    Q = Q + "\n"

    Q = Q + "Q: Is there a path between "
    Q_list = []
    for i in range(10):
        Q_i = Q + "node "+str(queries[i][0])+" and node "+str(queries[i][1])+" without going through node "+str(queries[i][2])+"? If there is a path then return answer as '\nA:Yes, there is a path.' and if not then return '\nA:No, there is no path.' "
        Q_list.append(Q_i)
    return Q_list

@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(1000))
def predict(Q, args):
    input = Q
    # Create the model
    generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
    }
    model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    )
    try:
        Answer_list = []
        for text in input:
            chat_session = model.start_chat(history=[])
            response = chat_session.send_message(text)
            Answer_list.append(response.text)  # Adjust based on Groq response structure
        return Answer_list
    except Exception as e:  # Catch generic exceptions
        print(f"Unexpected error: {e}")
        raise e

def log(Q_list, res, answer, args):
    utc_dt = datetime.utcnow().replace(tzinfo=timezone.utc)
    bj_dt = utc_dt.astimezone(timezone(timedelta(hours=8)))
    time = bj_dt.now().strftime("%Y%m%d---%H-%M")
    newpath = 'log/reach_dense/'+args.model+'-'+args.mode+'-'+time+'-'+args.prompt
    if args.SC == 1:
        newpath = newpath + "+SC"
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    newpath = newpath + "/"
    np.save(newpath+"res.npy", res)
    np.save(newpath+"answer.npy", answer)
    with open(newpath+"prompt.txt","w") as f:
        f.write(Q_list[0])
        f.write("\n")
        f.write("Acc: " + str(res.sum())+'/'+str(len(res)) + '\n')
        print(args, file=f)
    
def main():
    if 'GEMINI_API_KEY' in os.environ:
        api_key = os.environ["GEMINI_API_KEY"]
        genai.configure(api_key=api_key)
    else:
        raise Exception("Missing openai key!")
    res, answer = [], []
    match args.mode:
        case "easy":
            g_num = 10
        case "medium":
            g_num = 120
        case "hard":
            g_num = 68
    for i in tqdm(range(20,40)):
        with open("generation/dense_graphs/"+args.mode+"/dense_graph_"+str(i)+".txt","r") as f, open("answers/output2_dense_hard.txt","a", encoding="utf-8") as f5:
            n, m = [int(x) for x in next(f).split()]
            edges = []
            queries = []
            num_nodes = 0
            for line in f: # read rest of lines
                if num_nodes < m:
                    edges.append([int(x) for x in line.split()])
                else:
                    queries.append([int(x) for x in line.split()])
                num_nodes += 1
            # print(f"Edges list: {edges}")
            # print(f"Queries list: {queries}")


            Q_list = translate(m, edges, queries, args)
            # print(f"Q list: {Q_list}")
            sc = 1
            if args.SC == 1:
                sc = args.SC_num
            sc_list = []
            for k in range(sc):
                answer_list = predict(Q_list, args)
                # print(f"Answer list for value k: {answer_list}")
                sc_list.append(answer_list)
                time.sleep(62)
            for j in range(10):
                vote = 0
                for k in range(sc):
                    
                    ans = sc_list[k][j].lower()
                    f5.write("i value: " + str(i)+" j value: "+str(j)+ans+"\n")
                    answer.append(ans)
                    #ans = os.linesep.join([s for s in ans.splitlines() if s]).replace(' ', '')
                    # if "yes" in ans:
                    if (queries[j][3]==1) and ("yes, there is a path" in ans or "yes. there is a path" in ans or "yes there is a path" in ans):
                        vote += 1
                    elif (queries[j][3]==0) and ("no, there is no path" in ans or "no. there is no path" in ans or "no there is no path" in ans):
                        vote += 1
                if vote * 2 >= sc:
                    res.append(1)
                else:
                    res.append(0)
                
            # for j in range(5):
            #     vote = 0
            #     for k in range(sc):
            #         ans = sc_list[k][j+5].lower()
            #         f5.write(ans+"\n")
            #         answer.append(ans)
            #         #ans = os.linesep.join([s for s in ans.splitlines() if s]).replace(' ', '')
            #         if "no" in ans:
            #             vote += 1
            #     if vote * 2 >= sc:
            #         res.append(1)
            #     else:
            #         res.append(0)

    res = np.array(res)
    answer = np.array(answer)
    print((res==1).sum())
    log(Q_list, res, answer, args)

if __name__ == "__main__":
    main()
