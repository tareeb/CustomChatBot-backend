# CustomChatBots

**Customized Informative Conversations for Your Customers**

To View Front-End Repository, Please visit here : - **Frontend:** [CustomChatBot Frontend](https://github.com/tareeb/CustomChatBot-frontend)


---

## Table of Contents

- [Project Overview](#project-overview)
- [Motivation](#motivation)
- [Vision](#vision)
- [Our Journey](#our-journey)
- [Our Approach](#our-approach)
- [Features](#features)
- [How It Works](#how-it-works)
  - [Frontend](#frontend)
  - [Backend](#backend)

---

## Project Overview

With **CustomChatBots**, you can effortlessly create chatbots that follow custom instructions and utilize your own data as a knowledgebase. Updating the data and instructions is simple and can be done anytime with just a few clicks. After creating a chatbot, you receive a public URL that you can integrate into your own user interfaces. Alternatively, you can use our ready-made React components in your projects.

---

## Motivation

With the advent of the google, what used to be a research became as simple as a search. Before gogole finding information required visiting libraries, meeting people, and a lot of effort but then after google, just sit at your home, browse through web, do some clicks on some pages and you got your information.But then again with the advent of the chatgpt, what used to be a search became a conversation. Now No one had to search through webpages for information just ask it and you will get a  direct answer. Moreover, you get a customized information tailored to your needs rather than general content.
We live in an information age where everyone wants information but the way people request information and their expectations and anticipation of the quality and format of the retrieved information has changed. People Want quick and easy access to information.
Our project aims to provide a tool that allows people to create chatbots for conversations and deliver the information they want to communicate in a conversational way where topic of discussion, conversational tone and information is of the choice of the creator of chatbot. So that people can get information in a seamless way.

---

## Vision

We envision a new web era where complex interactions are simplified through chat. Users won’t need to follow complicated tutorials, navigate through multiple pages, difficulty in adjusting settings, manage web pages, or fill out difficult forms. Everything will be accessible with simple natural language commands.

---

## Our Journey

With the development of Large Language Model (LLM) Agents, our vision is becoming a reality. We have started small, similar to how the web began with simple HTML for information sharing. Our goal is to provide easy access to information and ensure our bots deliver customized information in a personalized manner.

---

## Our Approach

We believe in open source and have built our project on top of open-source technologies. This allows others to build on our work easily. Our system is versatile and uses modern LLM libraries like Langchain. Doing so allowed our code to be reuseable and updateable like changing LLM in the backend is as simple as changing a line - Thanks to Langchain Wrappers.

---

## Features

- **Create Chatbots Easily:** Users can create chatbots with custom instructions and data through a simple frontend.
- **Update Vector Database:** Users can update their chatbot’s data anytime with just a few clicks.
- **Set Custom Prompts:** Allows for more customization of chatbot responses.
- **Public URL for a Chatbot:** After creation, users receive a public URL specific for their chatbot using which they can chat with the chatbot.
- **API Integration:** Use the API to create their own interfaces and integrate anywhere.
- **Custom React Components:** We have also built custom react components which can be used as an interface to integrate chatbots into your projects.
  - **SideChatBot:** Easy to install by passing a unique chatbot ID to add a side chatbot to a website.
  - **ASKFAQ:** A  component that works like a list of FAQs where users can ask questions. It can be added to FAQ pages by installing and passing the chatbot ID.
- **LLM Guard:** Added LLM Guards to Protects the system from prompt injections.
- **Session Cookies:** Automatically set to manage chat sessions and reference chat history.
- **Authentication/Authorization:** Ensures only authorized users can modify their chatbots.
- **Open Source Code:** Both frontend and backend are open source, built with modern libraries for easy customization and updates.
- **Versatile Pipelines:** Code is reusable, making it easy to change components.

---

## How It Works

### Frontend

Here we will share the Screenshots of Front End UI and working of the CustomChatBot: 

#### Landing Page and Auth Screens: 

![image](https://github.com/user-attachments/assets/33bb3d2c-9b63-411a-9f7d-2812b2255395)

![image](https://github.com/user-attachments/assets/77e29d64-6df3-486b-93ea-461009b0296b)

![image](https://github.com/user-attachments/assets/aea21388-771d-49c3-a39b-762a8c3bdac4)

![image](https://github.com/user-attachments/assets/36b0c881-da84-4c64-b426-779fea3fd6f1)

**Fun Fact:** *All the Images are generated using Genearative AI. Like This Image on login screen is showing a chatbot is saving customer from all those extensive documentations and unstructured data  and is providing easy and quick access of information.*


#### Creating and Configuring Chatbot :

- Sign up and Login and will land on Admin Page
  
  ![image](https://github.com/user-attachments/assets/c3b470f4-f826-492e-ba88-6f03c98dc0ff)

- Click the Create Button to fill the form to create Chatbot
  
  ![image](https://github.com/user-attachments/assets/61666023-c5bc-4e85-b2b5-24b9260aec72)

- Chatbot created, in the chatbot configuration page update settings like keeping it public or not and the prompt insturctions.
  
  ![image](https://github.com/user-attachments/assets/a0a04a9a-2dfd-4a51-8c24-264da741c68d)

- Update the knowledge base by uploading PDFs , or remove them and add new one to keep the chatbot knowledge uptodate.
  
  ![image](https://github.com/user-attachments/assets/486b7032-a7dc-482a-b357-ac9e13fd32a8)
  ![image](https://github.com/user-attachments/assets/7625a177-e251-4335-aff2-3728c5d64747)

- Testing the Chatbot:
- By clicking the Chat icon you can start the chat direclty to test the capability of your chatbot.
  
  ![image](https://github.com/user-attachments/assets/ffd1c51c-b8ad-4e99-bb9c-8e81405884d8)

- That's it Chatbot is set, if you feel like it is doing what it's need to do , make it public. Using the public URL given below the chatbot you can integrate it with in your own projects and create custom interfaces. ( *Right now it says localhost as backend is only running localy*)

- Or You can Use Our React Components and Pass them your Chatbot IDs.

### React Components and Use Cases : 

For now we have come up with two usecase.

- **Side Bot Component:** Have a Side bot to answer your customer's query right away.
- Which will appear by clicking that smiley Icon:
  
  ![image](https://github.com/user-attachments/assets/f5aefc1c-b076-4b6b-a9c5-84ca93a9b68b)
  ![image](https://github.com/user-attachments/assets/dc5f9473-c65d-4ad9-b433-7b9347bc5322)


- **A FAQ Component:** A chat interface to query if got confused or unclear about FAQ.
  
  ![image](https://github.com/user-attachments/assets/bdbf37ec-a86d-4624-bdf5-d3c8de942d67)
  ![image](https://github.com/user-attachments/assets/064b849a-7c39-48eb-8fc5-c1989d9de23d)
  ![image](https://github.com/user-attachments/assets/3797dcf0-92b6-4ba6-8ea5-ca2a02f68b6d)

---

## Backend

The backend of **CustomChatBots** is built using **Django**, providing robust functionality for chatbot creation, database management, and user authentication. While most features are same just as any other project, the core discussion should be about  pipeline architecture. Below are the key components and details of our backend system:

### Components
- We have utilized and try different components
- **Langchain Library:** We utilize the Langchain library to ensure that different components can be easily swapped or updated. This flexibility allows for seamless integration and modification of various parts of the system.

- **Vector Database:**
  - **Chroma:** Used for efficient vector storage and retrieval.
  
- **Embedding Models:**
  - **Hugging Face Models:** We employ open-source embedding models such as `all-MiniLM-L6-v2` to generate embeddings for our data.
  
- **Large Language Models (LLM):**
  - **Llama-3 using Grok:** Our primary LLM for generating responses.
  - **Azure OpenAI:** An alternative LLM option that we have experimented with.
  
- **Graph Database:**
  - **Neo4j:** Utilized for parent-child chunking to manage and organize data relationships effectively.

### Pipeline Architecture

Our backend features two distinct pipelines that users can select from the frontend:

#### 1. Simple Pipeline

- **Description:** 
  - Implements a straightforward Retrieval Augmented Generation (RAG) approach.
  - Ideal for structured and well-formatted data, such as FAQs format.
    
- **Advantages:**
  - **Performance:** Reduces the number of LLM calls, resulting in a faster system.
  - **Technologies Used:** Combines Grok, Llama-3, and ChromaDB for optimal performance.

#### 2. Advanced Pipeline

- **Description:**
  - Incorporates advanced RAG techniques, including multi-query retrievers and parent-child chunking.
  - Designed to handle raw and unstructured data effectively.
  
- **Functionality:**
  - **Multi-Query Retriever:** Enhances the retrieval process by handling multiple queries simultaneously.
  - **Parent-Child Chunking:** Organizes data into hierarchical structures for better information retrieval.
  
- **Advantages:**
  - **Flexibility:** Capable of fetching and processing information from raw data sources.
  
- **Drawbacks:**
  - **Performance:** May be slower compared to the simple pipeline due to the more LLM calls.

### Versatility and Customization

- **Component Flexibility:** Thanks to Langchain, components like the LLM and embedding models can be changed with minimal effort. For example:
  - **Changing LLM:** Can be achieved with a single line of code.
  - **Switching Embedding Models:** Simply update the model name to use a different Hugging Face embedding model.

- **Codebase Design:** Our code is structured to support easy modifications and updates, ensuring that developers can customize and extend the functionality as needed.

## Next Steps

Our Immediate next steps are to : 

1. **Publish React Components to NPM:**
   - **Objective:** Make our React components easily installable and fully customizable for developers.
   - **Action:** Upload the existing React components to the NPM registry.
   
2. **Create Generalized Components:**
   - **Objective:** Increase the flexibility of our components by decoupling them from our internal API.
   - **Action:** Refactor react components so that they do not internally call our API. Instead, allow users to integrate any API of their choice, enabling broader usage scenarios and easier integration with various projects.

These steps will make **CustomChatBots** more accessible and adaptable, allowing developers to integrate our chatbots seamlessly into their own applications and workflows.

---


### Installation and Wokring for Front End: 

After cloning to start the porject
Run Command : npm run dev


### Installation and Working for Backend :

Set the Following Environment Variables:

for these both environment varaibles Visit https://neo4j.com/sandbox/:

NEO4J_URL: url of neo4j cluster

NEO4J_PASSWORD: password for neo4j cluster

Visit https://dashboard.cohere.com/welcome/login?source=readme&redirect=%2Fdocs%2Foverview and get the api key for cohere and set the given env variable:

COHERE_KEY

Set the environments variables for chat model and embeddings models:

OPENAI_AZURE_API_KEY

OPENAI_AZURE_API_KEY_3

Set the Groq api key. you can get the key by visiting https://console.groq.com/:

GROQ_API_KEY

Set the lekura api key for LLM GUARD. You can get the api key by visiting https://platform.lakera.ai/:

LAKERA_API_KEY


Installation Steps:

-Create python virtual environment: "Python -m venv myenv"

-Activate the virtual environment

-Install dependencies 

-Run the following command to start the chroma server: chroma run  --path "path to directory" --port 8001

-Run django server: "python manage.py runserver"

