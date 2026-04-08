import gradio as gr
import os
import json
from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from env.environment import RuralHealthEnv
from env.models import Action, ActionType, UrgencyLevel, Observation, ChatMessage
from env.tasks.task_easy import EasyTask
from env.tasks.task_medium import MediumTask
from env.tasks.task_hard import HardTask

# FastAPI App
app = FastAPI(title="RuralHealthEnv API")

# Initialize Environment
env = RuralHealthEnv(seed=42)
current_task = None

# Pydantic Models for API
class ResetRequest(BaseModel):
    task_id: Optional[str] = "hard"

class StepRequest(BaseModel):
    action_type: str
    content: Optional[str] = None
    details: Optional[Dict[str, Any]] = {}

class StepResponse(BaseModel):
    observation: Dict[str, Any]
    reward: float
    done: bool
    info: Dict[str, Any]

# API Endpoints
@app.post("/reset", response_model=Dict[str, Any])
async def reset_env(request: ResetRequest):
    global env, current_task
    task_map = {
        "easy": EasyTask(seed=42),
        "medium": MediumTask(seed=42),
        "hard": HardTask(seed=42)
    }
    task = task_map.get(request.task_id, HardTask(seed=42))
    current_task = task
    obs = task.reset()
    return obs.model_dump()

@app.post("/step", response_model=StepResponse)
async def step_env(request: StepRequest):
    global env, current_task
    if current_task is None:
        current_task = HardTask(seed=42)
        current_task.reset()
    
    action = Action(
        action_type=ActionType(request.action_type),
        content=request.content,
        details=request.details
    )
    obs, reward, done, info = current_task.step(action)
    return {
        "observation": obs.model_dump(),
        "reward": reward,
        "done": done,
        "info": info
    }

@app.get("/state")
async def get_state():
    return env.state().model_dump()

@app.get("/health")
async def health():
    return {"status": "healthy", "version": "0.2.0"}

# --- Gradio UI Logic ---
obs_ui = None

def start_session_ui():
    global obs_ui, current_task
    task = HardTask(seed=42)
    current_task = task
    obs_ui = task.reset()
    # Gradio 5 format: list of messages (dictionaries)
    history = [{"role": "assistant", "content": "New Patient Call Started. Patient: " + obs_ui.latest_utterance}]
    return history, f"Patient Info: {obs_ui.patient_info.age}yo {obs_ui.patient_info.gender}. Extracted: {obs_ui.symptoms}"

def chat_ui(message, history):
    global obs_ui, current_task
    if obs_ui is None:
        history.append({"role": "assistant", "content": "Please Reset/Start first."})
        return history, ""
    
    action = Action(action_type=ActionType.ASK_QUESTION, content=message)
    obs_ui, reward, done, info = current_task.step(action)
    
    # Update local history with message dictionaries
    history.append({"role": "user", "content": message})
    history.append({"role": "assistant", "content": obs_ui.latest_utterance})
    
    status = f"Step Reward: {reward} | Total Reward: {current_task.env.state().cumulative_reward:.2f} | Status: {'DONE' if done else 'In Progress'}"
    extracted = f"Extracted Symptoms: {obs_ui.symptoms}"
    return history, f"{status}\n{extracted}"

def classify_ui(urgency):
    global obs_ui, current_task
    if obs_ui is None: return "Reset first."
    action = Action(action_type=ActionType.CLASSIFY_URGENCY, details={"urgency": urgency})
    obs_ui, reward, done, info = current_task.step(action)
    return f"Classification: {urgency} | Reward: {reward} | Done: {done}"

with gr.Blocks(title="RuralHealthEnv v0.2.0") as demo:
    gr.Markdown("# 🏥 RuralHealthEnv (v0.2.0) - Conversational AI Assistant")
    gr.Markdown("This interface handles voice-call assistance simulation for rural India.")
    
    with gr.Row():
        reset_btn = gr.Button("Start New Case")
        task_info = gr.Textbox(label="Case Metadata", interactive=False)
    
    # In Gradio 5, 'type' is removed. It defaults to messages.
    chatbot = gr.Chatbot(label="Voice Call Log")
    msg = gr.Textbox(label="Your Question to Patient")
    
    with gr.Row():
        urgency_btn = gr.Radio(["low", "medium", "high"], label="Classify Urgency")
        submit_btn = gr.Button("Classify Urgency")
        refer_btn = gr.Button("Refer to Hospital")
    
    output_log = gr.Textbox(label="Agent Log / Result", interactive=False)
    
    reset_btn.click(start_session_ui, inputs=[], outputs=[chatbot, task_info])
    msg.submit(chat_ui, inputs=[msg, chatbot], outputs=[chatbot, output_log])
    submit_btn.click(classify_ui, inputs=[urgency_btn], outputs=[output_log])
    
    def refer_patient_ui():
        global obs_ui, current_task
        if obs_ui is None: return "Reset first."
        action = Action(action_type=ActionType.REFER)
        obs_ui, reward, done, info = current_task.step(action)
        return f"Referral Successful. Reward: {reward} | Final Score: {current_task.env.state().cumulative_reward:.2f}"
    
    refer_btn.click(refer_patient_ui, outputs=[output_log])

# Mount Gradio to FastAPI
app = gr.mount_gradio_app(app, demo, path="/")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)
