import gradio as gr
import os
import json
from env.environment import RuralHealthEnv
from env.models import Action, ActionType, UrgencyLevel

# Initialize Environment
env = RuralHealthEnv(seed=42)
obs = None

def start_session():
    global obs
    # For simplicity, we just reset the env.
    obs = env.reset()
    history = [{"role": "assistant", "content": "New Patient Call Started. Patient: " + obs.latest_utterance}]
    return history, f"Patient Info: {obs.patient_info.age}yo {obs.patient_info.gender}. Extracted: {obs.symptoms}"

def chat(message, history):
    global obs
    if obs is None:
        history.append({"role": "assistant", "content": "Please Reset/Start first."})
        return history, ""
    
    # Send user question as ASK_QUESTION action
    action = Action(action_type=ActionType.ASK_QUESTION, content=message)
    obs, reward, done, info = env.step(action)
    
    # Update local history
    history.append({"role": "user", "content": message})
    history.append({"role": "assistant", "content": obs.latest_utterance})
    
    status = f"Step Reward: {reward} | Total Reward: {env.state().cumulative_reward:.2f} | Status: {'DONE' if done else 'In Progress'}"
    extracted = f"Extracted Symptoms: {obs.symptoms}"
    
    return history, f"{status}\n{extracted}"

def classify(urgency):
    global obs
    if obs is None: return "Reset first."
    action = Action(action_type=ActionType.CLASSIFY_URGENCY, details={"urgency": urgency})
    obs, reward, done, info = env.step(action)
    return f"Classification: {urgency} | Reward: {reward} | Done: {done}"

with gr.Blocks(title="RuralHealthEnv v0.2.0") as demo:
    gr.Markdown("# 🏥 RuralHealthEnv (v0.2.0) - Conversational AI Assistant")
    gr.Markdown("Interact with a simulated rural patient to assess urgency and provide care recommendations.")
    
    with gr.Row():
        reset_btn = gr.Button("Start New Case")
        task_info = gr.Textbox(label="Case Metadata", interactive=False)
    
    chatbot = gr.Chatbot(label="Voice Call Log")
    msg = gr.Textbox(label="Your Question to Patient")
    
    with gr.Row():
        urgency_btn = gr.Radio(["low", "medium", "high"], label="Classify Urgency")
        submit_btn = gr.Button("Classify Urgency")
        treat_btn = gr.Button("Treat Locally")
        refer_btn = gr.Button("Refer to Hospital")
    
    output_log = gr.Textbox(label="Agent Log / Result", interactive=False)
    
    reset_btn.click(start_session, inputs=[], outputs=[chatbot, task_info])
    msg.submit(chat, inputs=[msg, chatbot], outputs=[chatbot, output_log])
    submit_btn.click(classify, inputs=[urgency_btn], outputs=[output_log])
    
    # Treat/Refer buttons (Simplified for demonstration)
    def refer_patient():
        global obs
        action = Action(action_type=ActionType.REFER)
        obs, reward, done, info = env.step(action)
        return f"Referral Successful. Reward: {reward} | Final Score: {env.state().cumulative_reward:.2f}"
    
    refer_btn.click(refer_patient, outputs=[output_log])

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
