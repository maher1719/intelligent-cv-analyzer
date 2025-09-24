a="""
AdaBoost
AI Art Creation
AI Audio-to-audio
AI Chatbot
AI Chatbot Development
AI Content Creation
AI Content Editing
AI Content Writing
AI Design
AI Development
AI Graphic Design
AI Image Editing
AI Image-to-text
AI Mobile App Development
AI Model Development
AI Model Integration
AI Research
AI Text-to-speech
AI Text-to-text
AI Text-to-video
AI Translation
AI Writing
AI-Enhanced Classification
AI-Generated Art
AI-Generated Code
AI-Generated Music
AI-Generated Text
AI-Generated Video
AlexNet
AlphaCode
Apple Vision Pro
Artificial Neural Network
Autoencoder
Automatic Speech Recognition
Azure OpenAI
BARD AI
Batch Normalization
Bing AI
Bland AI
BLOOM
Bot Development
Chatbot Integration
ChatGPT AI Integration
ChatGPT Prompt
ChatGPT-3
ChatGPT-3.5
ChatGPT-4
Classification
Cluster Computing
ComfyUI
Conversational AI
Convolutional Neural Network
Copy.AI
Customer Service Chatbot
CycleGAN
DALL-E 2
DALL-E 3
Data Augmentation
Deep Belief Network
Deep Neural Network
Diffusion models
Dolly
Facial Recognition
Feedforward Neural Network
Figma AI
Gated Recurrent Unit
Generative Adversarial Network
Generative Model
GitHub CoPilot
GPT-J
GPT-Neo
Hugging Face
Image Analysis
Image Recognition
Image Upscaling
Jasper AI
Jurrasic-2
LaMDA
LangChain
Large Language Models (LLMs)
Linear Discriminant Analysis
LLaMA 2
LLM Prompt Engineering
Long Short-Term Memory Network
Machine Learning Algorithms
Machine Translation
Microsoft 365 CoPilot
Microsoft CNTK
MLflow
MLOps
Model Deployment
Model Monitoring
Model Testing & Optimization
Model Tuning
Multilayer Perceptron
Multimodal
Multimodal Large Language Model
Naive Bayes Classifier
Natural Language Generation
Natural Language Understanding
NLP Tokenization
Object Detection
Object Localization
Ontology
OpenAI Codex
Pre-Training
Radial Basis Function Network
Recommendation System
Recurrent Neural Network
Regression Analysis
Reinforcement Learning
Restricted Boltzmann Machine
Retell AI
RLHF
Self-Organizing Map
Sentiment Analysis
Speech Synthesis
Streamlit
StyleGAN
Text Recognition
Time Series Analysis
Time Series Forecasting
Transformer Model
Variational Autoencoder
Voice Synthesis
Whisper AI
Word2vec
YOLO""".lower().split("\n")
import pandas as pd
df=pd.DataFrame(a).to_csv("ai.csv",header=False,index=False)